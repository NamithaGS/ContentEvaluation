
import json
import tika
import os
from collections import OrderedDict
from tika import parser
from tika import language
import random
path = "/Users/charanshampur/newAwsDump/testFiles4"
d3LanguageDist=open("D3Language.json","w")
langFile = open("Language.json","r")
langDictionary=json.load(langFile)
Language={}
for path,dirs,files in os.walk(path):
    for file in files:
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            print path_to_file
            lang = language.from_file(path_to_file)
            if lang not in Language:
                Language[lang]=1
            else:
                Language[lang]+=1

contentList=[]
for k,v in Language.items():
    content=OrderedDict()
    content["label"] = langDictionary[k]["name"]
    content["value"] = int(v)
    content["color"] = "#%06x" % random.randint(0, 0xFFFFFF)
    contentList.append(OrderedDict(content))


json.dump(contentList,d3LanguageDist,indent=4)

