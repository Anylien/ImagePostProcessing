#  07/15/2019
#
#  imageTools.py
#
#  Bastien HARMAND <bastien.harmand@mines-ales.org>

import random
from imageTools import *
from configparser import SafeConfigParser,NoSectionError,NoOptionError

parserKeypoints = SafeConfigParser()
parserKeypoints.read('keypoints.ini')

configParser = SafeConfigParser()
configParser.read('setup.ini')

# Final cropping display parameters :
targetH = int(configParser.get('MainView','targetHeight'))
targetW = int(targetH*float(configParser.get('MainView','aspectRatio')))
bottom_margin_percent = float(configParser.get('MainView','marginBottomPercent'))
top_margin_percent = float(configParser.get('MainView','marginTopPercent'))

# Thumbnail display parameters :
targetH_thumb = int(configParser.get('ThumbnailView','targetHeight'))
targetW_thumb = int(targetH_thumb*float(configParser.get('ThumbnailView','aspectRatio')))
bottom_margin_percent_thumb = float(configParser.get('ThumbnailView','marginBottomPercent'))
top_margin_percent_thumb = float(configParser.get('ThumbnailView','marginTopPercent'))


class Region :
    """
    Region class to define area of interest
    """
    def __init__(self,rect) :
        if len(rect)==4 : self.xMin,self.yMin,self.xMax,self.yMax = rect
        else : self.xMin,self.yMin,self.xMax,self.yMax = 0,0,1,1

    def __str__(self) : # Print the region
        if self.xMin==0 and self.yMin==0 and self.xMax==1 and self.yMax==1 : return "[]"
        else : return "pos = (" + str(self.xMin) + "," + str(self.yMin) + ") size = (" + str(self.xMax-self.xMin) + "," + str(self.yMax-self.yMin) + ")"

class Scene :
    """
    Scene class for handling the main image and the region of interest
    """
    # A Scene is composed of a image, region of interest in pixels coordinates
    def __init__(self,key,idj,typexe,view,image,regionLeft,regionRight,boundingBox,use_left,use_right) :
        self.key,self.idj = key,idj
        self.image,self.orima = image,image
        self.regionLeft,self.regionRight = regionLeft,regionRight
        self.typexe,self.view,self.boundingBox = typexe,view,boundingBox
        self.tx,self.ty = 0,0 # Transformations coordinates to store the results
        self.use_left,self.use_right = use_left,use_right
        height,width = self.image.shape[:2]
        self.background_color = EdgeRegister.get_background_color(self.image[int(boundingBox[3]*height):int((boundingBox[3]+boundingBox[1])*height),int(boundingBox[2]*width):int((boundingBox[2]+boundingBox[0])*width)])
        
        
    def get_region_right(dynamodb,key,idj,typtes) : # Get the right region of interest from keypoints.ini file config
        try :
            cenX_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-bll-rgh-spf-coo$usecen'))[0]
            cenY_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-bll-rgh-spf-coo$usecen'))[1]
            edgX_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-bll-rgh-spf-coo$useedg'))[0]
            edgY_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-bll-rgh-spf-coo$useedg'))[1]
            cenX_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-blr-rgh-spf-coo$usecen'))[0]
            cenY_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-blr-rgh-spf-coo$usecen'))[1]
            edgX_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-blr-rgh-spf-coo$useedg'))[0]
            edgY_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-blr-rgh-spf-coo$useedg'))[1]
            parrelupp = float(parserKeypoints.get(typtes,'parrelupp$tpo-bll-rgh-spf-coo$usecen'))
            parrelrig = float(parserKeypoints.get(typtes,'parrelrig$tpo-bll-rgh-spf-coo$usecen'))
            parreldow = float(parserKeypoints.get(typtes,'parreldow$tpo-blr-rgh-spf-coo$usecen'))
            parrellef = float(parserKeypoints.get(typtes,'parrellef$tpo-blr-rgh-spf-coo$usecen'))
            bll_length = ((cenX_bll-edgX_bll)**2+(cenY_bll-edgY_bll)**2)**(1/2)
            blr_length = ((cenX_blr-edgX_blr)**2+(cenY_blr-edgY_blr)**2)**(1/2)
            bllX = int(cenX_bll-bll_length*parrelrig)
            bllY = int(cenY_bll-bll_length*parrelupp)
            blrX = int(cenX_blr+blr_length*parrellef)
            blrY = int(cenY_blr+blr_length*parreldow)
            return [bllX,bllY,blrX,blrY]
        except NoSectionError as e:
            print(e)
            return []
        except NoOptionError as e:
            print(e)
            return []
        except KeyError as e:
            print(e)
            return []

    def get_region_left(dynamodb,key,idj,typtes) : # Get the left region of interest from keypoints.ini file config
        try :
            cenX_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-bll-lft-spf-coo$usecen'))[0]
            cenY_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-bll-lft-spf-coo$usecen'))[1]
            edgX_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-bll-lft-spf-coo$useedg'))[0]
            edgY_bll = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-bll-lft-spf-coo$useedg'))[1]
            cenX_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-blr-lft-spf-coo$usecen'))[0]
            cenY_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-blr-lft-spf-coo$usecen'))[1]
            edgX_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'cox$tpo-blr-lft-spf-coo$useedg'))[0]
            edgY_blr = dynamodb.read_keypoint_pos(key,idj,parserKeypoints.get(typtes,'coy$tpo-blr-lft-spf-coo$useedg'))[1]
            parrelupp = float(parserKeypoints.get(typtes,'parrelupp$tpo-bll-lft-spf-coo$usecen'))
            parrelrig = float(parserKeypoints.get(typtes,'parrelrig$tpo-bll-lft-spf-coo$usecen'))
            parreldow = float(parserKeypoints.get(typtes,'parreldow$tpo-blr-lft-spf-coo$usecen'))
            parrellef = float(parserKeypoints.get(typtes,'parrellef$tpo-blr-lft-spf-coo$usecen'))
            bll_length = ((cenX_bll-edgX_bll)**2+(cenY_bll-edgY_bll)**2)**(1/2)
            blr_length = ((cenX_blr-edgX_blr)**2+(cenY_blr-edgY_blr)**2)**(1/2)
            bllX = int(cenX_bll-bll_length*parrelrig)
            bllY = int(cenY_bll-bll_length*parrelupp)
            blrX = int(cenX_blr+blr_length*parrellef)
            blrY = int(cenY_blr+blr_length*parreldow)
            return [bllX,bllY,blrX,blrY]
        except NoSectionError as e :
            print(e)
            return []
        except NoOptionError as e :
            print(e)
            return []
        except KeyError as e:
            print(e)
            return []

    def get_region(self) :
        if self.use_left and self.use_right : # In this case we provide a region containning the two areas
            yMin = min(self.regionLeft.yMin,self.regionRight.yMin)
            yMax = max(self.regionLeft.yMax,self.regionRight.yMax)
            xMin = min(self.regionLeft.xMin,self.regionRight.xMin)
            xMax = max(self.regionLeft.xMax,self.regionRight.xMax)
            return [yMin,yMax,xMin,xMax]
        elif self.use_left :
            return [self.regionLeft.yMin,self.regionLeft.yMax,self.regionLeft.xMin,self.regionLeft.xMax]
        else :
            return [self.regionRight.yMin,self.regionRight.yMax,self.regionRight.xMin,self.regionRight.xMax]

    def get_crop(self) :
        if self.use_left and self.use_right : # In this case we provide a crop containning the two areas
            yMin = min(self.regionLeft.yMin,self.regionRight.yMin)
            yMax = max(self.regionLeft.yMax,self.regionRight.yMax)
            xMin = min(self.regionLeft.xMin,self.regionRight.xMin)
            xMax = max(self.regionLeft.xMax,self.regionRight.xMax)
            print("Cropping both",xMin,xMax,yMin,yMax)
            return self.orima[yMin:yMax,xMin:xMax]
        elif self.use_left :
            print("Cropping left",self.regionLeft.xMin,self.regionLeft.xMax,self.regionLeft.yMin,self.regionLeft.yMax)
            return self.get_crop_left()
        else :
            print("Cropping right",self.regionRight.xMin,self.regionRight.xMax,self.regionRight.yMin,self.regionRight.yMax)
            return self.get_crop_right()

    def get_crop_both(self) : # Return the image of the region of interest
        yMin = min(self.regionLeft.yMin,self.regionRight.yMin)
        yMax = max(self.regionLeft.yMax,self.regionRight.yMax)
        xMin = min(self.regionLeft.xMin,self.regionRight.xMin)
        xMax = max(self.regionLeft.xMax,self.regionRight.xMax)
        return self.orima[yMin:yMax,xMin:xMax]

    def get_crop_left(self) : # Return the image of the region of interest
        return self.orima[self.regionLeft.yMin:self.regionLeft.yMax,self.regionLeft.xMin:self.regionLeft.xMax]

    def get_crop_right(self) : # Return the image of the region of interest
        return self.orima[self.regionRight.yMin:self.regionRight.yMax,self.regionRight.xMin:self.regionRight.xMax]

    def apply_transform(self,tx,ty,sceneMaster) : # Apply the tranformation to the main image
        width,height = np.shape(sceneMaster.image)
        
        if self.use_left and self.use_right and (self.regionRight.yMin*self.regionRight.xMin*self.regionLeft.yMin*self.regionLeft.xMin!=0) :
            yMin = min(self.regionLeft.yMin,self.regionRight.yMin)
            xMin = min(self.regionLeft.xMin,self.regionRight.xMin)
            yMinMaster = min(sceneMaster.regionLeft.yMin,sceneMaster.regionRight.yMin)
            xMinMaster = min(sceneMaster.regionLeft.xMin,sceneMaster.regionRight.xMin)
            tx -= (xMin-xMinMaster)
            ty -= (yMin-yMinMaster)
        elif self.use_left and (self.regionLeft.yMin*self.regionLeft.xMin!=0) :
            tx -= (self.regionLeft.xMin-sceneMaster.regionLeft.xMin)
            ty -= (self.regionLeft.yMin-sceneMaster.regionLeft.yMin)
        elif self.use_right and (self.regionRight.yMin*self.regionRight.xMin!=0) :
            tx -= (self.regionRight.xMin-sceneMaster.regionRight.xMin)
            ty -= (self.regionRight.yMin-sceneMaster.regionRight.yMin)
        self.tx,self.ty = tx,ty
        self.image = apply_transform(self.image,tx,ty,height,width)

    def get_output_images(self) : # Return the scene's output (normal thumbnail, normal standard, normal inversed)
        ratio,dx,dy = imareg.EdgeRegister.get_transformation_view(self,targetH,targetW,bottom_margin_percent,top_margin_percent)
        ratio_thumb,dx_thumb,dy_thumb = imareg.EdgeRegister.get_transformation_view(self,targetH_thumb,targetW_thumb,bottom_margin_percent_thumb,top_margin_percent_thumb)
        northu = imareg.EdgeRegister.normalise_scale(self.image,targetH_thumb,targetW_thumb,ratio_thumb,dx_thumb,dy_thumb)
        norsta = imareg.EdgeRegister.normalise_scale(self.image,targetH,targetW,ratio,dx,dy)
        invsta = cv2.Canny(imareg.EdgeRegister.normalise_scale(self.image,targetH,targetW,ratio,dx,dy),80,150)
        return northu,norsta,invsta

    def __str__(self) : # Print the scene
        txt = "-> " + self.key + "\n"
        txt += ("   typexe : " + self.typexe + ", typview : " + str(self.view) + "\n   left region : " +  str(self.regionLeft) + "\n   right region : " +  str(self.regionRight))
        txt += ("\n   bounding box : " + str(self.boundingBox))
        txt += ("\n   use left : " +str(self.use_left) + ", use right : " + str(self.use_right))
        return txt

class EdgeRegister :
    """
    EdgeRegister class for estimating the transormation to register scenes based on region of interest
    """
    def __init__(self,population,maxSteps) :
        self.population = population
        self.maxSteps = maxSteps

    def random_try(master,features_number,sigma) : # Try random transformation for inital state
        width,height = np.shape(master)
        random_try = [int(np.random.normal(0, sigma, 1)[0]) for i in range(features_number)]
        random_try.append(0)
        return random_try

    def cross_try(try1,try2,mut,sigma) : # Give one try created randomly out of two tries
        cross_try = []
        for i in range(len(try1)) :
            if(random.random()<0.5) : cross_try.append(try1[i])
            else : cross_try.append(try2[i])
            if(random.random()<mut) : cross_try[i] += int(np.random.normal(0, sigma, 1)[0])
        return cross_try

    def get_transformation_view(scenes,resY,resX,bottom_margin_percent,top_margin_percent,use_all_bounding_box) : # Compute the scale and the translation transformation for standard displaying master image
        height,width = scenes[0].image.shape[:2]
        top_margin_pixels = int(resY*top_margin_percent/100.0)
        bottom_margin_pixels = int(resY*bottom_margin_percent/100.0)
        
        box_width = scenes[0].boundingBox[0]
        box_height = scenes[0].boundingBox[1]
        x = scenes[0].boundingBox[2]
        y = scenes[0].boundingBox[3]
        if use_all_bounding_box :
            bounding_boxes = [s.boundingBox for s in scenes]
            for b in bounding_boxes :
                if box_width<b[0] : box_width = b[0]
                if box_height<b[1] : box_height = b[1]
                if x>b[2] : x = b[2]
                if y>b[3] : y = b[3]
        box_height = int(box_height*height)
        ratioH = (resY-top_margin_pixels-bottom_margin_pixels)/box_height
        dx = -(x*ratioH*width)+((resX-box_width*ratioH*width)/2)
        dy = -(y*ratioH*height)+top_margin_pixels
        return(ratioH,dx,dy)

    def normalise_scale(image,resY,resX,ratio,dx,dy) : # Compute the transformation for standard displaying images
        height, width = image.shape[:2]
        res = cv2.resize(image,(int(ratio*width),int(ratio*height)),interpolation = cv2.INTER_CUBIC)
        M = np.float32([[1,0,dx],[0,1,dy]])
        imgOut = cv2.warpAffine(res,M,(resX,resY),borderMode=cv2.BORDER_REPLICATE)
        return imgOut

    def get_background_color(image) :
        hist_left = np.histogram(image[0,:],range(256))[0]
        hist_right = np.histogram(image[-1,:],range(256))[0]
        hist_top = np.histogram(image[:,0],range(256))[0]
        hist_down = np.histogram(image[:,-1],range(256))[0]
        colorValue,maxCount = 0,0
        for i in range(255) :
            count = hist_left[i] + hist_right[i] + hist_top[i] + hist_down[i]
            if count>maxCount :
                maxCount = count
                colorValue = i
        return colorValue

    def estimate_transformations(self,master, slave, horizontal, vertical) :
        width,height = np.shape(master)
        master_structure,slave_structure = structural_error(master,slave,horizontal, vertical)
        news_cut = int(95*self.population/100)
        keep_cut = int(5*self.population/100)
        transformations = [EdgeRegister.random_try(master,2,max(width,height)/64) for k in range(self.population)]
        step=1

        while step<self.maxSteps :
            for d in transformations :
                slave_shifted = apply_transform(slave_structure,d[0],d[1],height,width)
                d[2] = (np.sum((master_structure-slave_shifted)**2))
            transformations = sorted(transformations, key = lambda d:d[2])
            tx,ty,score =  transformations[0]
            step+=1
            for i in range(self.population) :
                if i>=keep_cut and i<news_cut :
                    transformations[i] = EdgeRegister.cross_try(transformations[random.randint(0,keep_cut)],transformations[random.randint(keep_cut,news_cut)],0.8,max(width,height)/64)
                elif i>=keep_cut :
                    transformations[i] = EdgeRegister.random_try(master,2,max(width,height)/64)
            slave_shifted = apply_transform(slave,tx,ty,height,width)
        return tx,ty,score

    def roi_register(self,scenes,master_index,use_left,use_right) :
         for i in range(len(scenes)) :
             if i!=master_index :
                 if use_left and use_right :
                     master = scenes[master_index].get_crop_both()
                     slave = scenes[i].get_crop_both()
                 elif use_right :
                     master = scenes[master_index].get_crop_right()
                     slave = scenes[i].get_crop_right()
                 else :
                     master = scenes[master_index].get_crop_left()
                     slave = scenes[i].get_crop_left()
                 tx,ty,score = self.estimate_transformations(master,slave,1,1)
                 scenes[i].apply_transform(tx,ty,scenes[master_index])
                 print("Translation correction estimation : (x : " + str(tx) + ", y : " + str(ty) + ")")
