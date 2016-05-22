import os, json
import itertools


#This program creates a Master List (Union) of all the named entity keys identified by the 3 tools.
#For each of the named entities identified, find a resultant set containing the total number of entities 
#identified in the file under each of these categories (Ex, LOCATION, PERSON etc) by each of the tools 
#(OpenNLP, CoreNLP, NLTK).

path = os.getcwd() + "/ner"
UnionList=[]
MergedList=[]
CoreNLP={}
OpenNLP={}
NLTK={}
ResultDict={}
MaxFrequencyDict={}

def formatOutput():
    labels=[]
    series=[]
    listofv=[]
    for k,v in ResultDict.iteritems():
        seriesitems={}
        labels.append(k)
        x = v.split('|')
        listofv.append(x[0])
    seriesitems['values']=listofv
    seriesitems['label']='OpenNLP'
    series.append(seriesitems)
    listofv=[]
    for k,v in ResultDict.iteritems():
        seriesitems={}
        x =  v.split('|')
        listofv.append(x[1])
    seriesitems['values']=listofv
    seriesitems['label']='CoreNLP'
    series.append(seriesitems)
    listofv=[]
    for k,v in ResultDict.iteritems():
        seriesitems={}
        x =  v.split('|')
        listofv.append(x[2])
    seriesitems['values']=listofv
    seriesitems['label']='NLTK'
    series.append(seriesitems)
    print "{" + 'labels:' + str(labels) + ',series: ' + str(series) + "}"    

def deduplicate(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def processFiles():
    for item in UnionList:
        val=""
        if item in OpenNLP:
            val=str(OpenNLP.get(item))
        else:
            val='0'
        if item in CoreNLP:
            val=val + '|' + str(CoreNLP.get(item))
        else:
            val=val + '|' + '0'
        if item in NLTK:
            val=val + '|' + str(NLTK.get(item))
        else:
            val=val + '|' + "0"
        ResultDict[item]=val
    print ResultDict        

        
for path,dirs,files in os.walk(path):
    for file in files:
        fileList={}
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            json_data=open(path_to_file).read()
            jsonDict = json.loads(json_data)
            for value in jsonDict.itervalues():
                ner_data=value
            
            #print file                
            for key,value in ner_data.iteritems():
                if key!='Content-Length' and key!='Content-Type':
                    UnionList.append(key)
                    if key in fileList:
                        fileList[key] += len(value)
                    else:
                        fileList[key] = len(value)
                    if file=='corenlp.json':
                        CoreNLP=fileList
                    elif file=='opennlp.json':
                        OpenNLP=fileList
                    else:
                        NLTK=fileList
    UnionList=deduplicate(UnionList)
    processFiles()
    formatOutput()