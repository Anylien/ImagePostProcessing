import json
import boto3
import imareg
import dynamoParser
from imageTools import *
from configparser import ConfigParser, NoSectionError, NoOptionError

configParser = ConfigParser()
configParser.read('setup.ini')

parserCropView = ConfigParser()
parserCropView.read('croppedview.ini')

# Bucket parameters :
bucket = str(configParser.get('BucketS3','name'))

# DynamoDB parameters :
dyanmodbName = str(configParser.get('DynamoDB','name'))
dynamodbRegion = str(configParser.get('DynamoDB','region'))
db = dynamoParser.DynamoDB(dyanmodbName,dynamodbRegion)

# Registration parameters :
registrationEstimationTrials = int(configParser.get('Estimation','trials'))
registrationEstimationMaxSteps = int(configParser.get('Estimation','maxSteps'))

# Final normal display parameters :
targetH = int(configParser.get('MainView','targetHeight'))
targetW = int(targetH*float(configParser.get('MainView','aspectRatio')))
bottom_margin_percent = int(configParser.get('MainView','marginBottomPercent'))
top_margin_percent = int(configParser.get('MainView','marginTopPercent'))

# Final crop display parameters :
targetH_crop = int(configParser.get('CroppedView','targetHeight'))
targetW_crop = int(configParser.get('CroppedView','targetWidth'))

# Thumbnail display parameters :
targetH_thumb = int(configParser.get('ThumbnailView','targetHeight'))
targetW_thumb = int(targetH_thumb*float(configParser.get('ThumbnailView','aspectRatio')))
bottom_margin_percent_thumb = int(configParser.get('ThumbnailView','marginBottomPercent'))
top_margin_percent_thumb = int(configParser.get('ThumbnailView','marginTopPercent'))

def save_image(image,s3Key) : # Save a numpy image to a temporary file on the Amazon instance and copy it to the bucket
    cv2.imwrite('/tmp/' + s3Key.split('/')[-1], image)
    s3.put_object(Body=open('/tmp/' + s3Key.split('/')[-1], 'rb'), Bucket=bucket, Key = s3Key)
    print(s3Key + " saved")

def get_image(key) : # Copy file from the bucket to the Amazon instance and load it as a numpy image
    download_path = '/tmp/{}'.format(key.split('/')[-1])
    s3.download_file(bucket, key, download_path)
    return cv2.imread(download_path, 0)

def load_scene(key,idj,dynamodb) : # Load a scene from Amazon S3 Bucket and DynamodDB
    image = get_image(key)
    boundingBox,typvie,typexe = dynamodb.read_meta(key,idj)
    typtes = key.split('/')[1]
    regionLeft = imareg.Region(imareg.Scene.get_region_left(db,key,idj,typtes+"$"+typvie+"$tpg-bfo-lft-spf-shp"))
    regionRight = imareg.Region(imareg.Scene.get_region_right(db,key,idj,typtes+"$"+typvie+"$tpg-bfo-rgh-spf-shp"))
    # To choose between the right or left 
    use_left = False
    use_right = False
    if typvie == 'sin' :
        use_left = True
        use_right = False
    if typvie == 'dex' : 
        use_left = False
        use_right = True
    if typvie == 'ant' :
        if typexe == 'ups' : 
            use_left = True
            use_right = True
        elif typexe == 'rls' :
            use_left = False
            use_right = True
        elif typexe == 'lls' :
            use_left = True
            use_right = False
        else :
            use_left = True
            use_right = True
    if typvie == 'pos' :
        if typexe == 'ups' : 
            use_left = True
            use_right = True
        elif typexe == 'rls' :
            use_left = False
            use_right = True
        elif typexe == 'lls' :
            use_left = True
            use_right = False
        else :
            use_left = True
            use_right = True
    scene = imareg.Scene(key,idj,typexe,typvie,image,regionLeft,regionRight,boundingBox,use_left,use_right)
    
    bll_left_x,bll_left_y,blr_left_x,blr_left_y = regionLeft.xMin,regionLeft.yMin,regionLeft.xMax,regionLeft.yMax
    bll_right_x,bll_right_y,blr_right_x,blr_right_y = regionRight.xMin,regionRight.yMin,regionRight.xMax,regionRight.yMax
    
    dynamodb.write_image_size(key,idj,np.shape(image)[0],np.shape(image)[1],"norori")
    dynamodb.write_technical_points(key,idj,bll_left_x,bll_left_y,blr_left_x,blr_left_y,bll_right_x,bll_right_y,blr_right_x,blr_right_y,use_left,use_right,"norori")
    
    print(scene)
    return scene
    
def get_scenes(jsonContent) :
    print("Opening scenes from JSON...")
    scenes = []
    scene1 = load_scene(jsonContent['images']['1']['key'],jsonContent['images']['1']['idj'],db)
    scenes.append(scene1)
    if '2' in jsonContent['images'] :
        scene2 = load_scene(jsonContent['images']['2']['key'],jsonContent['images']['2']['idj'],db)
        scenes.append(scene2)
    if '3' in jsonContent['images'] :
        scene3 = load_scene(jsonContent['images']['3']['key'],jsonContent['images']['3']['idj'],db)
        scenes.append(scene3)
    return scenes

def export_scene(scene,ratio,dx,dy,ratio_thumb,dx_thumb,dy_thumb) :
    norsta = imareg.EdgeRegister.normalise_scale(scene.image,targetH_thumb,targetW_thumb,ratio_thumb,dx_thumb,dy_thumb)
    save_image(norsta,scene.key.replace('norori','northu'))
    db.write_translations(scene.key,scene.idj,int(dx+ratio*scene.tx),int(dy+ratio*scene.ty),ratio,"norsta")
    
    # NORMAL STANDARD -> norsta
    norsta = imareg.EdgeRegister.normalise_scale(scene.image,targetH,targetW,ratio,dx,dy)
    save_image(norsta,scene.key.replace('norori','norsta'))

    # CONTOUR WHITE BACKGROUND -> invsta
    invsta = cv2.Canny(imareg.EdgeRegister.normalise_scale(scene.image,targetH,targetW,ratio,dx,dy),80,150)
    save_image(invsta,scene.key.replace('norori','invsta'))

def lambda_handler(event, context):

    global BUCKET
    global KEY
    global s3
    s3 = boto3.client('s3')

    # We get the bucket name and key from the trigger
    BUCKET = event['Records'][0]['s3']['bucket']['name']
    KEY = str(event['Records'][0]['s3']['object']['key'])

    file_obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    file_content = json.loads(file_obj['Body'].read())
    
    scenes = get_scenes(file_content)
    
    master_index = 0

    '''REGISTERING'''
    reg = imareg.EdgeRegister(registrationEstimationTrials,registrationEstimationMaxSteps)
    if len(scenes)>1 :
        reg.roi_register([scenes[0],scenes[1]],master_index,scenes[1].use_left,scenes[1].use_right)
    if len(scenes)>2 :
        reg.roi_register([scenes[0],scenes[2]],master_index,scenes[2].use_left,scenes[2].use_right)
    
    '''SCALE, DX AND DY TO DISPLAY'''
    use_all_images = scenes[0].view in ['sin','dex'] 
    ratio,dx,dy = imareg.EdgeRegister.get_transformation_view(scenes,targetH,targetW,bottom_margin_percent,top_margin_percent,use_all_images)
    ratio_thumb,dx_thumb,dy_thumb = imareg.EdgeRegister.get_transformation_view(scenes,targetH_thumb,targetW_thumb,bottom_margin_percent_thumb,top_margin_percent_thumb,use_all_images)
    
    
    typtes = scenes[master_index].key.split('/')[1]
    
    try :
        parrelupp = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-rgh-spf-shp","parrelupp$tpo-bll-rgh-spf-coo$viwcau"))
        parrelrig = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-rgh-spf-shp","parrelrig$tpo-bll-rgh-spf-coo$viwcau"))
        parreldow = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-rgh-spf-shp","parreldow$tpo-blr-rgh-spf-coo$viwcau"))
        parrellef = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-rgh-spf-shp","parrellef$tpo-blr-rgh-spf-coo$viwcau"))
    except NoSectionError as e:
        print(e)
    except NoOptionError as e:
        print(e)
    try :
        parrelupp = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-lft-spf-shp","parrelupp$tpo-bll-lft-spf-coo$viwcau"))
        parrelrig = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-lft-spf-shp","parrelrig$tpo-bll-lft-spf-coo$viwcau"))
        parreldow = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-lft-spf-shp","parreldow$tpo-blr-lft-spf-coo$viwcau"))
        parrellef = float(parserCropView.get(typtes+"$"+scenes[master_index].view+"$tpg-bfo-lft-spf-shp","parrellef$tpo-blr-lft-spf-coo$viwcau"))
    except NoSectionError as e:
        print(e)
    except NoOptionError as e:
        print(e)
    
    viewportMaster = scenes[master_index].get_region().copy()
    viewportMaster_extended = viewportMaster[:].copy()
    viewportMaster_extended[0] -= int((viewportMaster[1]-viewportMaster[0])*parrelupp)
    viewportMaster_extended[1] += int((viewportMaster[1]-viewportMaster[0])*parreldow)
    viewportMaster_extended[2] -= int((viewportMaster[3]-viewportMaster[2])*parrellef)
    viewportMaster_extended[3] += int((viewportMaster[3]-viewportMaster[2])*parrelrig)
    

    for s in scenes :
        
        export_scene(s,ratio,dx,dy,ratio_thumb,dx_thumb,dy_thumb)
        image = s.image[:].copy()
        
        cropped_view_standard = image[viewportMaster_extended[0]:viewportMaster_extended[1],viewportMaster_extended[2]:viewportMaster_extended[3]].copy()
        
        height, width = np.shape(cropped_view_standard)[:2]
        ratio_scale = float(targetW_crop)/float(width)

        cropped_view_standard = cv2.resize(cropped_view_standard,(int(ratio_scale*width),int(ratio_scale*height)),interpolation = cv2.INTER_CUBIC)
        dx_db = -(-s.tx + viewportMaster_extended[2])*ratio_scale
        dy_db = -(-s.ty + (viewportMaster_extended[0]))*ratio_scale
     
        '''if int(ratio_scale*height) > targetH_crop :
            cropped_view_standard = cropped_view_standard[int(ratio_scale*height)-targetH_crop:,:]
            dy_db -= (int(ratio_scale*height)-targetH_crop)/ratio_scale'''
        
        save_image(cropped_view_standard,s.key.replace('norori','norcro'))
        save_image(cv2.bitwise_not(cropped_view_standard),s.key.replace('norori','invcro'))
        
        db.write_translations(s.key,s.idj,int(dx_db*ratio_scale),int(dy_db*ratio_scale),ratio_scale,"norcro")
        
    if len(scenes)>1 :
    
        if len(scenes)>2 :
            # OVERVIEW FOR THREE IMAGES -> oveviesta
            overview = compare_img(scenes[master_index].image,scenes[1].image,scenes[2].image)
            oveviesta = imareg.EdgeRegister.normalise_scale(overview,targetH,targetW,ratio,dx,dy)
            overview_white = compare_img(scenes[master_index].image,scenes[1].image,scenes[2].image,background = [255,255,255])
            ovevieinv = imareg.EdgeRegister.normalise_scale(overview_white,targetH,targetW,ratio,dx,dy)
    
        else :
            # OVERVIEW FOR TWO IMAGES -> oveviesta
            overview = compare_img(scenes[master_index].image,scenes[1].image,np.uint8(np.zeros(np.shape(scenes[1].image))))
            oveviesta = imareg.EdgeRegister.normalise_scale(overview,targetH,targetW,ratio,dx,dy)
            overview_white = compare_img(scenes[master_index].image,scenes[1].image,np.uint8(np.zeros(np.shape(scenes[1].image))),background = [255,255,255])
            ovevieinv = imareg.EdgeRegister.normalise_scale(overview_white,targetH,targetW,ratio,dx,dy)
    
        save_image(oveviesta,scenes[master_index].key.replace('norori','oveviesta'))
        save_image(ovevieinv,scenes[master_index].key.replace('norori','ovevieinv'))
        
    return ''
