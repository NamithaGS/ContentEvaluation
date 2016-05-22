from orderedset._orderedset import OrderedSet

import json
import string
import re
from stopwords import get_stopwords
from tika import language
stopwords=get_stopwords("en")
stopwords=[x.upper() for x in stopwords]


#freqListFile = open("/Users/charanshampur/solr/lucene_solr_4_10/solr/example/solr-webapp/webapp/MyHtml/freqList.json","w")
freqListFile = open("freqList.json","w")
sweetJsonFile=open("/Users/charanshampur/PycharmProjects/CSCI599/MetaScoreNew.json","r")
jsonLoad=json.load(sweetJsonFile)
langFile = open("Language.json","r")
langDictionary=json.load(langFile)
removeWords=["FOR","LOGIN","SALE","NEW","FREE","``","BUY","SYSTEM","WANT","REPORT","WITHIN","S","...","TO","SAN","P","W/","ALL","'S","W","M","PAGE","ITEMS"]
#print "NLTK succesfully loaded<br>"
#print "Json succesfully loaded"
wordCloud={}
skipList=["NER_DATE","id","Geographic_LATITUDE","content","title","Measurements","Meta_Score","NER_PERCENT","NER_MONEY",""]

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

for item in jsonLoad:
    print item["id"]
    text=""
    #Adding all the metadata fields
    for k,v in item.items():
        if k not in skipList and not re.match("Geographic|Optional|ctakes",k):
            if type(v) is list:
                v=" ".join(reduceList(v))
            text+=k+" "+str(v)+" "

    #Identifying language from content
    if "content" in item:
        lang=language.from_buffer(item["content"])
        text+=langDictionary[lang]["name"]+" "

    if "title" in item:
        if type(item["title"]) is list:
            text+=item["title"][0]
        else:
            text+=item["title"]

    text = re.sub(r"[(}{)|\\/><\[\],.;:@#?!&$-]+", ' ', text)
    try:
        tokens=(str(text).split())
    except:
        continue
    tokens=[w for w in tokens if w not in string.punctuation]
    for token in tokens:
        if token.upper() not in removeWords and not token.isdigit() and token.upper() not in stopwords:
            if token.upper() not in wordCloud:
                wordCloud[token.upper()]=1
            else:
                wordCloud[token.upper()]+=1

wordCloud=sorted(wordCloud.items(), key=lambda x: x[1],reverse=True)
wordJson=[]
wordDict={}
for i in range(0,120):
    wordDict["text"]=wordCloud[i][0]
    if int(wordCloud[i][1])>5000:
        normalizedSize=80
    else:
        normalizedSize=wordCloud[i][1]
    wordDict["size"]=normalizedSize
    wordJson.append(dict(wordDict))

jsonarray = json.dumps(wordJson,indent=4)
freqListFile.write(jsonarray)
freqListFile.close()