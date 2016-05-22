import os,string,json,math,sys
import codecs
import pickle
filename = "C:/Users/Namithaa/Desktop/599/Project3/prog/task10/Measurements.json"

inputfile = codecs.open(filename, "r")
outputfile = open("data.csv","w")
outputfile.write("State,Min,Avg,Max\n")
def find_Stats(lst):
	result=[]
	max1=(1-sys.maxint)
	min1=sys.maxint
	avg=0
	for key in lst:
		key1=float(key)
		if key1>max1:
			max1=key1
		if key1<min1:
			min1=key1
		avg+=key1
	avg=1.0*avg/len(lst)
	result.append(min1)
	result.append(avg)
	result.append(max1)
	return result

bb=[]
unitlist = {}
bb = json.load(inputfile)
for eachfile in bb:
    for eachfiles1 in  eachfile[0].keys():
        bb = eachfile[0][eachfiles1]
        for eachline in bb:
            eachunit = eachline["unit"]
            eachmeas = eachline["number"]
            eachunit = eachunit.lower()
            if eachunit in unitlist.keys():
                unitlist[eachunit] = unitlist[eachunit] + " , " + eachmeas
            else:
                unitlist[eachunit] = eachmeas

print unitlist
min = 0.0
max = 0.0
avg = 0.0
for eachunit1, eachmeas1 in unitlist.items():
    lst1 = eachmeas1.split(" , ")
    result = find_Stats(lst1)
    min = int(result[0])
    avg = int(result[1])
    max = int(result[2])


    aa = eachunit1 +","+str(min)+","+str(avg)+","+str(max)
    outputfile.write(aa+"\n")







