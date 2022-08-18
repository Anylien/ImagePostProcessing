import json
import boto3
import numpy as np
import cv2
import imareg
import dynamoParser
from imageTools import *
from configparser import ConfigParser,NoSectionError,NoOptionError

boto3.setup_default_session(profile_name='default') ### PROFILE NAME IS 'default' HERE! ###

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


#####################################################################################################################

def display(image, name, scale = 1.0) : # Display an image to debug results
    
    #print("THE IMAGE IS :\n{}".format(image))
    
    width,height = np.shape(image)[:2]
    cv2.imshow(name,cv2.resize(image, (int(scale*height), int(scale*width))))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#####################################################################################################################



from drawings import drawer, image_calculator

draw = drawer(color_values = 'inverted_mean_proportion', main_contrast_exponent = 1.2, color_contrast_proportion = 0.6, pixel_color_study_proportion = 0.0, transparency = 0.3, message = False)

def add_grid(image, number_squares = 15, pixels_write = 1, pixels_space = 1, line_length = 1, min_mode = False, writing_size = 'compute_writing_size', writing_proportion = 1.0, adapt_writing_proportion = False, grid_stape_messsage = True):
    if(grid_stape_messsage):
        print("Adding adapted chosen grid to current image...")
    ###
    draw.draw_grid(image, number_squares, pixels_write, pixels_space, line_length, min_mode, writing_size, writing_proportion, adapt_writing_proportion)
    ###



#####################################################################################################################

"""
keypoints = ['bjo-ank-lft-spf-coo','bjo-ank-rgh-spf-coo','bjo-elb-lft-spf-coo',
             'bjo-elb-rgh-spf-coo','bjo-hip-lft-spf-coo','bjo-hip-rgh-spf-coo',
             'bjo-kne-lft-spf-coo','bjo-kne-rgh-spf-coo','bjo-shl-lft-spf-coo',
             'bjo-shl-rgh-spf-coo','bjo-wrs-lft-spf-coo','bjo-wrs-rgh-spf-coo',
             'bpo-ear-lft-spf-coo','bpo-ear-rgh-spf-coo','bpo-eye-lft-spf-coo',
             'bpo-eye-rgh-spf-coo','bpo-nos-unp-spf-coo','bsp-fra-lft-dst-coo',
             'bsp-fra-lft-prx-coo','bsp-fra-rgh-dst-coo','bsp-fra-rgh-prx-coo',
             'bsp-loi-unp-lde-coo','bsp-loi-unp-lsi-coo','bsp-shn-lft-dst-coo',
             'bsp-shn-lft-prx-coo','bsp-shn-rgh-dst-coo','bsp-shn-rgh-prx-coo',
             'bsp-tgh-lft-dst-coo','bsp-tgh-lft-prx-coo','bsp-tgh-rgh-dst-coo',
             'bsp-tgh-rgh-prx-coo','bsp-uar-lft-dst-coo','bsp-uar-lft-prx-coo',
             'bsp-uar-rgh-dst-coo','bsp-uar-rgh-prx-coo']
"""

#####################################################################################################################



def add_keypoints(image, scene, keypoints_list, disk_radius = 'compute_disk_radius', writing_size = 'compute_writing_size', writing_proportion = 1.0, adapt_writing_proportion = False, keypoints_stape_messsage = True):
    if(keypoints_stape_messsage):
        print("Adding keypoints to current image...")
    ###
    #draw.set_color_values([0.2, 1.0, 0.2])
    draw.set_pixel_color_study_proportion(1.0)
    draw.set_transparency(0.8)
    ###
    keypoints_data = read_dynamo_keypoints(scene, keypoints_list)
    for keypoint in keypoints_data:
        word, pos_x, pos_y = keypoint
        draw.draw_keypoint(image, pos_y, pos_x, disk_radius, word, writing_size, writing_proportion, adapt_writing_proportion)
    ###


def read_dynamo_keypoints(scene, keypoints_list, warnings = False): # Returns a LIST of coordinates!
    keypoints_data = []
    for keypoint in keypoints_list:
        try:
            word = keypoint[0]
            coordinates = db.read_keypoint_pos(scene.key, scene.idj, keypoint[2]) # class 'tuple'
            keypoints_data.append((word,coordinates[0],coordinates[1]))
        except:
            if(warnings):
                print("WARNING : No data found in AWS DynamoDB for SCENE KEY = {}, SCENE IDJ = {}, KEYPOINT = {}.".format(scene.key, scene.idj, keypoint))
    return keypoints_data



#####################################################################################################################



def add_boxes(image, scene, keypoints_list, disk_radius = 'compute_disk_radius', writing_size = 'compute_writing_size', writing_proportion = 1.0, adapt_writing_proportion = False, boxes_stape_messsage = True):
    if(boxes_stape_messsage):
        print("Adding keypoints to current image...")
    o=0


def read_dynamo_boxes(scene, boxes_list, warnings = False): # Returns a LIST of coordinates!
    boxes_data = []
    for box in boxes_list:
        try:
            coordinates = db.read_bounding_box(scene.key, scene.idj) # NO! NOT BOUNDING BOX!!!
            print("COORDINATES : ",coordinates)
        except:
            if(warnings):
                print("oki")
    return boxes_data



#####################################################################################################################



import csv


def read_csv(name, message = False):
    data = []
    try:
        with open(name, mode ='r') as file:
            csvFile = csv.reader(file)
            if(message):
                print("READING CSV FILE '",name,"'...")
            row = 0
            for line in csvFile:
                if(row!=0):
                    data.append(line)
                row+=1
    except:
        if(message):
            print("ERROR : File '",name,"' can not be read as a CSV!")
    return data



#####################################################################################################################

def save_image(image, s3Key, image_name='') : # Save an image to a temporary file on the Amazon instance and upload it to the bucket

    print("\nSAVING IMAGE...")

    img_name = s3Key.split('/')[-1][:-4] + '_IMG' + image_name + '.png'

    print('IMAGE NAME : ' + img_name)

    cv2.imwrite('./created_images/{}' + img_name, image)
    
    s3_key = ''
    for nam in s3Key.split('/')[:-1]:
        s3_key += nam+'/'
    print("Saving at {} / {}".format(bucket,s3_key))
    s3_key += img_name
    
    s3.put_object(Body=open('./created_images/{}' + img_name, 'rb'), Bucket=bucket, Key = s3_key)
    
    print(s3_key + " saved")

#####################################################################################################################


#####################################################################################################################

def get_image(key) : # Copy file from the bucket to the Amazon instance and download it as a numpy image
    download_path = './downloaded_images/{}'.format(key.split('/')[-1])
    s3.download_file(Bucket=bucket, Key=key, Filename=download_path)
    return cv2.imread(download_path,0)

#####################################################################################################################


def load_scene(key,idj,dynamodb) : # Load a scene from Amazon S3 Bucket and DynamoDB
    image = get_image(key)
    boundingBox,typvie,typexe = dynamodb.read_meta(key,idj)
    typtes = key.split('/')[1] # 
    regionLeft = imareg.Region(imareg.Scene.get_region_left(db,key,idj,typtes+"$"+typvie+"$tpg-bfo-lft-spf-shp"))
    regionRight = imareg.Region(imareg.Scene.get_region_right(db,key,idj,typtes+"$"+typvie+"$tpg-bfo-rgh-spf-shp"))
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
        
    print(use_left,use_right)
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

def export_scene(scene,ratio,dx,dy,ratio_thumb,dx_thumb,dy_thumb, scene_id=0) :
    norsta = imareg.EdgeRegister.normalise_scale(scene.image,targetH_thumb,targetW_thumb,ratio_thumb,dx_thumb,dy_thumb)
    replace_color(norsta,0,scene.background_color)
    
    add_grid(norsta)
    ########################################################################################################################################################
    save_image(norsta, scene.key.replace('norori','northu'), 'A'+str(scene_id))
    ########################################################################################################################################################
    
    display(norsta,scene.key.replace('norori','northu'))
    db.write_translations(s.key,s.idj,int(dx+scene.tx),int(dy+scene.ty),ratio,"norsta")

    # NORMAL STANDARD -> norsta
    norsta = imareg.EdgeRegister.normalise_scale(scene.image,targetH,targetW,ratio,dx,dy)
    replace_color(norsta,0,scene.background_color)
    
    add_grid(norsta)
    ########################################################################################################################################################
    save_image(norsta, scene.key.replace('norori','norsta'), 'B'+str(scene_id))
    ########################################################################################################################################################
    
    display(norsta,scene.key.replace('norori','norsta')) #display(norsta,scene.key.replace('norori','norsta'),0.5)

    # CONTOUR WHITE BACKGROUND -> invsta
    invsta = cv2.Canny(imareg.EdgeRegister.normalise_scale(scene.image,targetH,targetW,ratio,dx,dy),80,150)
    
    add_grid(invsta)
    ########################################################################################################################################################
    save_image(invsta, scene.key.replace('norori','invsta'), 'C'+str(scene_id))
    ########################################################################################################################################################
    
    display(invsta,scene.key.replace('norori','invsta')) #display(invsta,scene.key.replace('norori','invsta'),0.5)


s3 = boto3.client('s3')

IDJ = 20190702095433
image_key = "staana.alfa1@gmail.com/masB01/20190702095433/norori/bdecb466-9c9e-11e9-a885-005056840793.png"

scene1 = load_scene(image_key, IDJ, db)
scene2 = load_scene(image_key, IDJ, db)
scene3 = load_scene(image_key, IDJ, db)
# staana.alfa1@gmail.com/masB01/20190804171200/norori/acd0170e-b6ca-11e9-ad58-005056840793.png

"""
# bucket
s3://neu-rc2-alf001-s3m-thw/
# key
staana.alfa1@gmail.com/masB01/20190702095433/norori/bdecb466-9c9e-11e9-a885-005056840793.png

"""

scenes = [scene1, scene2, scene3]

master_index = 0

'''for i in range(len(scenes)) :      
    display(scenes[i].get_crop(),scenes[i].key.replace('norori','norcro'))
    display(cv2.bitwise_not(scenes[i].get_crop()),scenes[i].key.replace('norori','invcro'))
   '''

'''REGISTERING'''
reg = imareg.EdgeRegister(registrationEstimationTrials, registrationEstimationMaxSteps)
if len(scenes) > 1:
    reg.roi_register([scenes[0], scenes[1]], master_index, scenes[1].use_left, scenes[1].use_right)
if len(scenes) > 2:
    reg.roi_register([scenes[0], scenes[2]], master_index, scenes[2].use_left, scenes[2].use_right)

'''SCALE, DX AND DY TO DISPLAY'''
use_all_images = scenes[0].view in ['sin', 'dex']
ratio, dx, dy = imareg.EdgeRegister.get_transformation_view(scenes, targetH, targetW, bottom_margin_percent,
                                                            top_margin_percent, use_all_images)
ratio_thumb, dx_thumb, dy_thumb = imareg.EdgeRegister.get_transformation_view(scenes, targetH_thumb, targetW_thumb,
                                                                              bottom_margin_percent_thumb,
                                                                              top_margin_percent_thumb, use_all_images)

typtes = scenes[master_index].key.split('/')[1]

try:
    parrelupp = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-rgh-spf-shp", "parrelupp$tpo-bll-rgh-spf-coo$viwcau"))
    parrelrig = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-rgh-spf-shp", "parrelrig$tpo-bll-rgh-spf-coo$viwcau"))
    parreldow = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-rgh-spf-shp", "parreldow$tpo-blr-rgh-spf-coo$viwcau"))
    parrellef = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-rgh-spf-shp", "parrellef$tpo-blr-rgh-spf-coo$viwcau"))
except NoSectionError as e:
    print(e)
except NoOptionError as e:
    print(e)
try:
    parrelupp = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-lft-spf-shp", "parrelupp$tpo-bll-lft-spf-coo$viwcau"))
    parrelrig = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-lft-spf-shp", "parrelrig$tpo-bll-lft-spf-coo$viwcau"))
    parreldow = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-lft-spf-shp", "parreldow$tpo-blr-lft-spf-coo$viwcau"))
    parrellef = float(parserCropView.get(typtes + "$" + scenes[master_index].view + "$tpg-bfo-lft-spf-shp", "parrellef$tpo-blr-lft-spf-coo$viwcau"))
except NoSectionError as e:
    print(e)
except NoOptionError as e:
    print(e)

viewportMaster = scenes[master_index].get_region().copy()
viewportMaster_extended = viewportMaster[:].copy()
viewportMaster_extended[0] -= int((viewportMaster[1] - viewportMaster[0]) * parrelupp)
viewportMaster_extended[1] += int((viewportMaster[1] - viewportMaster[0]) * parreldow)
viewportMaster_extended[2] -= int((viewportMaster[3] - viewportMaster[2]) * parrellef)
viewportMaster_extended[3] += int((viewportMaster[3] - viewportMaster[2]) * parrelrig)

for i in range(len(scenes)):
    
    s = scenes[i]
    
    ########################################################################################################################################################
    # Modifications à l'interieur de cette fonction!!!
    export_scene(s, ratio, dx, dy, ratio_thumb, dx_thumb, dy_thumb, i)
    
    ########################################################################################################################################################
    
    image = s.image[:].copy()
    
    ###
    image1 = image_calculator.from_2D_to_3D_image(image)
    ###
    #####
    # ADDING GRID
    #add_grid(image)
    #####
    ###
    # ADDING KEYPOINTS
    wanted_keypoints = read_csv('./neu-valter-ngc - coo.csv')
    add_keypoints(image, s, wanted_keypoints)
    ###
    #read_dynamo_boxes(s, [0])
    ###

    cropped_view_standard = image[viewportMaster_extended[0] - 200:viewportMaster_extended[1], viewportMaster_extended[2]:viewportMaster_extended[3]].copy()
    
    height, width = np.shape(cropped_view_standard)[:2]
    ratio_scale = float(targetW_crop) / float(width)
    
    cropped_view_standard = cv2.resize(cropped_view_standard, (int(ratio_scale * width), int(ratio_scale * height)), interpolation=cv2.INTER_CUBIC)
    dx_db = s.tx - viewportMaster_extended[2]
    dy_db = s.ty - (viewportMaster_extended[0] - 200)
    
    if int(ratio_scale * height) > targetH_crop:
        cropped_view_standard = cropped_view_standard[int(ratio_scale * height) - targetH_crop:, :]
        dy_db -= (int(ratio_scale * height) - targetH_crop) / ratio_scale
    
    
    ########################################################################################################################################################
    
    add_grid(cropped_view_standard)
    
    ########################################################################################################################################################
    save_image(image, s.key.replace('norori','norcro'), 'i'+str(i))
    save_image(cv2.bitwise_not(cropped_view_standard), s.key.replace('norori','invcro'), 'j'+str(i))
    ########################################################################################################################################################
    
    
    display(image, s.key.replace('norori', 'norcro'))
    display(cv2.bitwise_not(cropped_view_standard), s.key.replace('norori', 'invcro'))

    db.write_translations(s.key, s.idj, int(dx_db), int(dy_db), ratio_scale, "norcro")
    

if len(scenes) > 1:

    if len(scenes) > 2:
        # OVERVIEW FOR TWO IMAGES -> oveviesta
        overview = compare_img(scenes[master_index].image, scenes[1].image, scenes[2].image)
        oveviesta = imareg.EdgeRegister.normalise_scale(overview, targetH, targetW, ratio, dx, dy)
        overview_white = compare_img(scenes[master_index].image, scenes[1].image, scenes[2].image, background=[255, 255, 255])
        ovevieinv = imareg.EdgeRegister.normalise_scale(overview_white, targetH, targetW, ratio, dx, dy)

    else:
        # OVERVIEW FOR THREE IMAGES -> oveviesta
        overview = compare_img(scenes[master_index].image, scenes[1].image, np.uint8(np.zeros(np.shape(scenes[1].image))))
        oveviesta = imareg.EdgeRegister.normalise_scale(overview, targetH, targetW, ratio, dx, dy)
        overview_white = compare_img(scenes[master_index].image, scenes[1].image, np.uint8(np.zeros(np.shape(scenes[1].image))), background=[255, 255, 255])
        ovevieinv = imareg.EdgeRegister.normalise_scale(overview_white, targetH, targetW, ratio, dx, dy)
    
    
    add_grid(oveviesta)
    add_grid(ovevieinv)
    
    
    ########################################################################################################################################################
    save_image(oveviesta, scenes[master_index].key.replace('norori','oveviesta'), 'f0')
    save_image(ovevieinv, scenes[master_index].key.replace('norori','ovevieinv'), 'f1')
    ########################################################################################################################################################
    
    display(oveviesta, scenes[master_index].key.replace('norori', 'oveviesta')) #display(oveviesta, scenes[master_index].key.replace('norori', 'oveviesta'), 0.5)
    display(ovevieinv, scenes[master_index].key.replace('norori', 'ovevieinv')) #display(ovevieinv, scenes[master_index].key.replace('norori', 'ovevieinv'), 0.5)
