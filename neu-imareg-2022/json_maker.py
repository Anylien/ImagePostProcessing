import boto3
import dynamoParser
import os
import json

s3_client = boto3.client('s3')
db = dynamoParser.DynamoDB('neu-worflow-test','eu-west-1')
outPutFolder = 'json'
         
def list_bucket(bucket_name, prefix) :
    print("LISTING OBJECTS IN : '" + bucket_name + "' WITH PREFIX : '" + prefix + "'")
    jobs = {}
    objNumber = 0
    for rep in s3_client.list_objects(Bucket = bucket_name)['Contents'] :
        key = rep['Key']
        if key.endswith(".png") and key.startswith(prefix) :
            if key.split('/')[3] == 'norori' :
                print(key)
                objNumber += 1
                idj = key.split('/')[2]
                exercice = db.read_exercice(key,int(idj))
                if idj in jobs :
                    jobs[idj].append([key,exercice])
                else :
                    jobs[idj] = [[key,exercice]]
    print(str(len(jobs)) + " JOBS FOUND, " + str(objNumber) + " OBJECTS")
    return jobs

def sortJobs(jobs) : # This function put the master scene at the first place
    for j in jobs :
        masterFound = False
        index = 2
        for i in range(len(jobs[j])) :
            key,ex = jobs[j][i]
            if ex=='ups' and not masterFound :
                jobs[j][i] = [key,ex,1]
                masterFound = True
            else :
                jobs[j][i] = [key,ex,index]
                index += 1
        if not masterFound :
            for i in range(len(jobs[j])) :
                jobs[j][i][2] -= 1

def writeJobs(jobs,idu) :
    for j in jobs :
        idj = jobs[j][0][0].split('/')[2]
        jsonContent = {"idu": idu,"idj" : idj,
        "idm" : jobs[j][0][0].split('/')[1], "imaregstatim": "","imaregstacou": "",
        "imaregsta": [jobs[j][k][0] for k in range(len(jobs[j]))]}
        os.mkdir(os.path.join(outPutFolder,idj))
        os.mkdir(os.path.join(outPutFolder,os.path.join(idj,"parbas")))
        os.mkdir(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","facana"))))
        with open(os.path.join(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","facana"))),j + '.json'), 'w') as f:
            json.dump(jsonContent, f, indent = 4)
        os.mkdir(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","imareg"))))
        with open(os.path.join(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","imareg"))),j + '.json'), 'w') as f:
            json.dump(jsonContent, f, indent = 4)
        os.mkdir(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","keypo1"))))
        with open(os.path.join(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","keypo1"))),j + '.json'), 'w') as f:
            json.dump(jsonContent, f, indent = 4)
        os.mkdir(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","objsce"))))
        with open(os.path.join(os.path.join(outPutFolder,os.path.join(idj,os.path.join("parbas","objsce"))),j + '.json'), 'w') as f:
            json.dump(jsonContent, f, indent = 4)

                
jobs = list_bucket('neuroapp-workflow-test','user.name@gmail.com')
sortJobs(jobs)
writeJobs(jobs,'user.name@gmail.com')
