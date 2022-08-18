# -*- coding: utf-8 -*-
"""
Created on Wed May 25 2022
@author: Antoine BOTTENMULLER
"""

import boto3
from configparser import SafeConfigParser
import cv2


boto3.setup_default_session(profile_name='default')

configParser = SafeConfigParser()
configParser.read('setup.ini')

s3 = boto3.client('s3')
bucket = str(configParser.get('BucketS3','name'))


def get_image(key) : # Copy file from the bucket to the Amazon instance and load it as a numpy image
    download_path = './downloaded_images/{}'.format(key.split('/')[-1])
    s3.download_file(bucket, key, download_path)
    return cv2.imread(download_path, 0)

print("BUCKET : ",bucket)

key_string = "staana.alfa1@gmail.com/masB01/20190804171200/norori/acd0170e-b6ca-11e9-ad58-005056840793.png"

o = get_image(key_string)




# NEW WORK TO DO :

# try to replicate the lambda function
# to deploy the lambda function!

# check how it is implemented in the old account, and deploy them to the new one as a lambda

# (it will not be the same lambda function!)




# KEYPOINTS NAMES

keypoints = ["bjo-ank-lft-spf-coo","bjo-ank-rgh-spf-coo","bjo-elb-lft-spf-coo",
             "bjo-elb-rgh-spf-coo","bjo-hip-lft-spf-coo","bjo-hip-rgh-spf-coo",
             "bjo-kne-lft-spf-coo","bjo-kne-rgh-spf-coo","bjo-shl-lft-spf-coo",
             "bjo-shl-rgh-spf-coo","bjo-wrs-lft-spf-coo","bjo-wrs-rgh-spf-coo",
             "bpo-ear-lft-spf-coo","bpo-ear-rgh-spf-coo","bpo-eye-lft-spf-coo",
             "bpo-eye-rgh-spf-coo","bpo-nos-unp-spf-coo","bsp-fra-lft-dst-coo",
             "bsp-fra-lft-prx-coo","bsp-fra-rgh-dst-coo","bsp-fra-rgh-prx-coo",
             "bsp-loi-unp-lde-coo","bsp-loi-unp-lsi-coo","bsp-shn-lft-dst-coo",
             "bsp-shn-lft-prx-coo","bsp-shn-rgh-dst-coo","bsp-shn-rgh-prx-coo",
             "bsp-tgh-lft-dst-coo","bsp-tgh-lft-prx-coo","bsp-tgh-rgh-dst-coo",
             "bsp-tgh-rgh-prx-coo","bsp-uar-lft-dst-coo","bsp-uar-lft-prx-coo",
             "bsp-uar-rgh-dst-coo","bsp-uar-rgh-prx-coo"]

"""
def read_dynamo_keypoints(scene):
    
    print("DYNAMO_DB NAME :", dyanmodbName)
    print("DYNAMO_DB REGION :", dynamodbRegion)
    
    #db.read_keypoint_pos(uid, job_id, keypoint_name)
    
    keypoint = keypoints[0]
    
    print("CURRENT SCENE :", scene.key, ";", scene.idj, ";", keypoint)
    
    try:
        coordinates = db.read_keypoint_pos(scene.key, scene.idj, keypoint) # class 'tuple'
    except:
        coordinates = (0,0)
        print("ERROR : No data found in AWS DynamoDB for SCENE KEY = {}, SCENE IDJ = {}, KEYPOINT = {}. Coordinates adapted to (0,0) tuple.".format(scene.key, scene.idj, keypoint))
    
    return coordinates
"""



# be able to select the wanted type of image processing WITH THE SETTINGS FILE 'setup.ini' in which we write the outputs we want!
# create a new folder among the other folders 'noriri', etc... in which all images will be stored, whatever if it's 'noriri', 'inviri' or whatever. distinguish their roles only with the ID

# in lambda, to stream a file call : wget



## WORK TO DO

# Make a Workflow diagram
# Ask Mathieu!
# To put in the README
# Write how to upload/export lambda function

# 1/ A text to explain how everything works
# 2/ A diagram to visualise the Workflow
