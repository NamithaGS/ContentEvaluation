
import json
import tika
import re
import os
import math
from orderedset import OrderedSet
from tika import parser
path = "/Users/charanshampur/newAwsDump/testFiles4"
outputFile=open("ParserChain.json","w")
d3ParseChain=open("D3ParseChain.json","w")

parseChainPlot={}

def validateContent(contentType):
    def filterType(x):
        if ';' in x:
            x = x.split(";")[0]
        return x
    if type(contentType) is list:
        contentTypeList=[filterType(x) for x in contentType if type(x) is not list]
        return list(OrderedSet(contentTypeList))
    else:
        return filterType(contentType)

def formatChain(listParser):
    if type(listParser) is list:
        formatList = [x.split(".").pop() for x in listParser]
        return formatList
    else:
        formatList=listParser.split(".").pop()
    return formatList


def reduceList(nestedList):
    MainList=[]
    def subList(x):
        if type(x) is list:
            for item in x:
                subList(item)
        else:
            MainList.append(x)
    subList(nestedList)
    return list(OrderedSet(MainList))

def updateContentType(existingChain,contentLength,metaDataLength,contentType):

    def calculateNewAvg(x):
        storedFileCount = existingChain[x][0]
        storedContLen = existingChain[x][1]
        storedMetaLen = existingChain[x][2]
        newFileCount = storedFileCount + 1
        newContLen = ((storedContLen * storedFileCount) + contentLength)/newFileCount
        newMetaLen = ((storedMetaLen * storedFileCount) + metaDataLength)/newFileCount
        return [newFileCount,newContLen,newMetaLen]

    if len(existingChain)==0:
        if type(contentType) is list:
            for item in contentType:
                existingChain[item]=[1,contentLength,metaDataLength]
        else:
            existingChain[contentType]=[1,contentLength,metaDataLength]
    else:
        if type(contentType) is list :
            for item in contentType:
                if item in existingChain:
                    existingChain[item]=calculateNewAvg(item)
                else:
                    existingChain[item]=[1,contentLength,metaDataLength]
        else:
            if contentType in existChain:
                existingChain[contentType]=calculateNewAvg(contentType)
            else:
                existingChain[contentType]=[1,contentLength,metaDataLength]
    return existingChain

TotalFileSize=0
TotalMetaSize=0
for path,dirs,files in os.walk(path):
    for file in files:
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            print path_to_file
            parsedData={}
            parsedData=parser.from_file(path_to_file)
            if len(parsedData) == 0:
                continue
            if "metadata" not in parsedData:
                continue
            metadata = parsedData["metadata"]
            if "X-Parsed-By" not in metadata:
                continue
            if "Content-Type" not in metadata:
                continue
            parserChain = metadata["X-Parsed-By"]
            content = parsedData["content"]
            if content is None:
                contentLength=0
            else:
                contentLength=len(content)
            TotalFileSize+=contentLength
            metaDataLength = len(metadata)
            TotalMetaSize+=metaDataLength
            if type(parserChain) is list:
                parserChain=",".join(formatChain(reduceList(parserChain)))
            else:
                parserChain=formatChain(parserChain)
            contentType=validateContent(metadata["Content-Type"])
            if parserChain not in parseChainPlot:
                parseChainPlot[parserChain]=updateContentType({},contentLength,metaDataLength,contentType)
            else:
                existChain = parseChainPlot[parserChain]
                parseChainPlot[parserChain]=updateContentType(existChain,contentLength,metaDataLength,contentType)

json.dump(parseChainPlot,outputFile,indent=4)

for k,v in parseChainPlot.items():
    ContentTypes = v
    for type,listVal in ContentTypes.items():
        if (listVal[1]<500):
            listVal[1]=500
        if (listVal[2]<5):
            listVal[2]=5
        #listVal[1]=float(listVal[1])/float(TotalFileSize)
        #listVal[2]=float(listVal[2])/float(TotalMetaSize)
        parseChainPlot[k][type]=listVal


conceptList=[]
for key,value in parseChainPlot.items():
    conceptDetail={}
    conceptDetail["name"]=key
    conceptDetail["description"]=key
    itemList=[]
    for k,v in value.items():
        itemDetail={}
        itemDetail["name"]=k;
        itemDetail["description"]=k;
        itemDetail["size"]=v[1]
        itemList.append(itemDetail)
    conceptDetail["children"]=itemList
    conceptList.append(conceptDetail)

finalFlareJson={"name":"FileSize","children":conceptList}

json.dump(finalFlareJson,d3ParseChain,indent=4)