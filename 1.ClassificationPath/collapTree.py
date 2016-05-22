
import json

ctakesJsonFile=open("Measurement.json","r")
locOrgFile=open("output.json","w")
jsonStr=ctakesJsonFile.read()
jsonLoad=json.loads(jsonStr)


locGraph={}

for file,doc in jsonLoad.items():
    list1={}
    aa=[]
    if "requesthostname" in doc and "responsehostname" and "url" in doc:
        if doc["requesthostname"] in locGraph:
            listofreponseforrequest = [' '.join(x.keys()) for x in locGraph[doc["requesthostname"]]]
            if doc["responsehostname"] not in listofreponseforrequest:
                list1= locGraph[doc["requesthostname"]]
                list1.append({ doc["responsehostname"]: doc["url"]})
                locGraph[doc["requesthostname"]]= list1
            else:

                aa = locGraph[doc["requesthostname"]]
                list2=[]
                for valuedict in aa:
                    index = aa.index(valuedict)
                    for key,value in valuedict.items():
                        if key == doc["responsehostname"]:
                            if type(value) is list :
                                list2.extend(value)
                                list2.append(doc["url"])
                            else:
                                list2.append(value)
                                list2.append(doc["url"])

                            locGraph[doc["requesthostname"]][index] = {key:list2}

        else:
            list1[doc["responsehostname"]]= doc["url"]
            locGraph[doc["requesthostname"]]= [list1]

#the NER contents derieved
datalistNER={}
for file,doc in jsonLoad.items():
    listofNERperfile =[]
    if "url" in doc and "NER" in doc :
        for eachNERfield,value in doc["NER"].items():
            if eachNERfield.startswith("NER_"):
                listofNERperfile.append( eachNERfield)
    datalistNER[doc["url"]]=  listofNERperfile



def formatRec(link,size):
    return {"name":link,"size":size}

itemList=[]

for k,v in locGraph.items():
    itemDetail={}
    itemDetail["name"]=k;
    lista=[]
    for response in v:
        itema={}
        urllist=[]
        for k1,v1 in response.items():
            itema["name"]=k1
            if type(v1) is list:
                urllist = [x for x in v1]
            else:
                urllist  =  v1.split()
            NERperurl = []
            itemurlNER={}
            itemurlNER1 =[]
            for eachurl in urllist:
                if (datalistNER.has_key(eachurl)):
                    NERperurl = datalistNER[eachurl]
                    itemurlNER["name"] = eachurl
                    itemurlNER["children"] = [formatRec(x,7) for x in NERperurl]
                itemurlNER1.append(itemurlNER)
            itema["children"] = itemurlNER1
            lista.append(itema)

    itemDetail["children"]=lista
    itemList.append(itemDetail)

finalLocOrgJson={"name":"Requests","children":itemList}
json.dump(finalLocOrgJson,locOrgFile,indent=4)
print "success"