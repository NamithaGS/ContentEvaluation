
from tika import parser
import json, os
import solr
from orderedset import OrderedSet
from collections import OrderedDict
import random

#Path of the Solr folder
solr_path = "C:/Users/Manisha Kampasi/Downloads/solr-5.5.0/solr-5.5.0/server/solr/"
#Path of the folder where all files are stored
path = "C:/USC Course material/CS - 599/Assignment 3/CSCI-599-Assignment-3/testFiles4"
solr_corename = "commoncrawl"
solrfilePath=solr_path+solr_corename+'/data/index/'

size_of_solr_index_file = sum(os.path.getsize(solrfilePath+f) for f in os.listdir(solrfilePath))
#size_of_solr_index_file = 118910372
print size_of_solr_index_file

outputFile=open("size_diversity.json","w")
templateFile=open("pieChartTemplate.json","r")

#Load the d3js template file
pieChartTemplate=json.load(templateFile)
#extract all the individual components. We need to update only the "content" part
header = pieChartTemplate['header']
footer = pieChartTemplate['footer']
size = pieChartTemplate['size']
data = pieChartTemplate['data']
labels = pieChartTemplate['labels']
tooltips = pieChartTemplate['tooltips']
effects = pieChartTemplate['effects']
misc = pieChartTemplate['misc']

ContentTypes={}
#A function which strips the charset attached to the "Content-Type" field of a file parsed by Apache Tika
def validateContent(contentType):
    def filterType(x):
        if ';' in x:
            x = x.split(";")[0]
        return x
    if type(contentType) is list:
        contentTypeList=[filterType(x) for x in contentType if type(x) is not list]
        #return list(OrderedSet(contentTypeList))
        return contentTypeList[0]
    else:
        return filterType(contentType)

#Loop through the data and calculate total file size per mime type
for path,dirs,files in os.walk(path):
    for file in files:
        if file not in ".DS_Store":
            path_to_file = path+"/"+str(file)
            print path_to_file
            parsedData={}
            parsedData=parser.from_file(path_to_file)
            if len(parsedData) == 0:
                continue
            metadata = parsedData["metadata"]
            if "Content-Type" not in metadata:
                continue
            content_type=validateContent(metadata["Content-Type"])
            if content_type not in ContentTypes:
                ContentTypes[content_type]=int(os.path.getsize(path + '/' + file))
            else:
                ContentTypes[content_type]=int(ContentTypes[content_type] + os.path.getsize(path + '/' + file))

#Generate random colors for each mime type to represent it in D3js 
mimeList=[]
for k,v in ContentTypes.items():
    content=OrderedDict()
    content["label"] = k #langDictionary[k]["name"]
    content["value"] = round(float(v)/size_of_solr_index_file,2)
    content["color"] = "#%06x" % random.randint(0, 0xFFFFFF)
    mimeList.append(OrderedDict(content))

#Re-generate the template file, this time with the correct content
data['content'] = mimeList
completeDict={}
completeDict['header'] = header
completeDict['footer'] = footer
completeDict['size'] = size
completeDict['data'] = data
completeDict['labels'] = labels
completeDict['tooltips'] = tooltips
completeDict['effects'] = effects
completeDict['misc'] = misc
#Write to the output file
json.dump(completeDict,outputFile, indent=4)