#!/usr/bin/python3
import sys
import json

f = open(sys.argv[1], 'r')
content = f.readlines()
f.close()
miles=[]
for index, line in enumerate(content):
    if index < 3:
        continue
    star_name=line[0:18].strip()
    miles_number=line[23:29].strip()
    sp_type=line[36:49].strip()
    miles.append({'star-name': star_name, 'miles-number': miles_number, 'spectral-type': sp_type})
    #print("index: {:4d}, star: {}, num: {}".format(index, star_name, miles_number))
    
json_f = open(sys.argv[2], 'w')
json.dump(miles, json_f)
json_f.close()
#print(miles)