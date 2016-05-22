import os, json
import itertools

#This program creates a Master List (Union) of all the named entities (values) identified by the 3 tools.
#For each of the named entities identified, find a resultant set containing Boolean values 1 or 0 for 
#(OpenNLP,  CoreNLP,  NLTK) based on whether it is identified by that tool or not.
path = os.getcwd() + "/ner"
UnionList=[]
MergedList=[]
ResultDict={}

MaxFrequencyDict={}
def processFiles():
    for item in MergedList:
        templist=[]
        val=""
        if item in OpenNLP:
            val='1'
        else:
            val='0'
        if item in CoreNLP:
            val=val+'1'
        else:
            val=val + '0'
        if item in NLTK:
            val=val+'1'
        else:
            val=val+'0'
        ResultDict[item]=val
    
def selectmax():
    for key,value in ResultDict.iteritems():
        if value=='111':
            MaxFrequencyDict[key]=value
    if len(MaxFrequencyDict)<10:
        for k,v in ResultDict.iteritems():
            if(v=='101' or v=='011' or v=='110'):
                MaxFrequencyDict[key]=v

    
def formatOutput():
    labels=[]
    series=[]
    listofv=[]
    for k,v in MaxFrequencyDict.iteritems():
        seriesitems={}
        labels.append(k)
        listofv.append(v[0])
    seriesitems['values']=listofv
    seriesitems['label']='OpenNLP'
    series.append(seriesitems)
    listofv=[]
    for k,v in MaxFrequencyDict.iteritems():
        seriesitems={}
        listofv.append(v[1])
    seriesitems['values']=listofv
    seriesitems['label']='CoreNLP'
    series.append(seriesitems)
    listofv=[]
    for k,v in MaxFrequencyDict.iteritems():
        seriesitems={}
        listofv.append(v[2])
    seriesitems['values']=listofv
    seriesitems['label']='NLTK'
    series.append(seriesitems)
    print "{" + 'labels:' + str(labels) + ',series: ' + str(series) + "}"    
   
CoreNLP={}
OpenNLP={}
NLTK={}         
for path,dirs,files in os.walk(path):
    for file in files:
        fileList=[]
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            json_data=open(path_to_file).read()
            jsonDict = json.loads(json_data)
            for value in jsonDict.itervalues():
                ner_data=value
            
            #print file                
            for key,value in ner_data.iteritems():
                UnionList.append(value)
                fileList.append(value)
            x = list(itertools.chain(*fileList))
            if file=='corenlp.json':
                CoreNLP=x
            elif file=='opennlp.json':
                OpenNLP=x
            else:
                NLTK=x

    MergedList = list(itertools.chain(*UnionList))
    processFiles()
    selectmax()
    formatOutput()