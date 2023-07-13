import sys,requests,json,os,time
from time import sleep
import os
from dotenv import load_dotenv
import json
load_dotenv()


def return_data():

    indexArray=[]
    with open(os.getenv('INDEX_FILE_TXT'),mode='r') as f:
        for line in f:
            indexArray.append(line.strip())
    url="http://sis.rutgers.edu/soc/api/openSections.gzip"
    info={('year',str(2023)),('term',str(9)),('campus','NB')} #year=year, term= fall'9',spring'1'
    while True:
        #print('-----')
        subjects = requests.get(url,params=info)
        subjects.raise_for_status()
        subjects=subjects.json()
        openClasses=[]
        for index in indexArray:
            for item in subjects:
                if item==index:
                    openClasses.append(index)
                    break

        
        ret = []
        for index in openClasses:
            ret.append(index+' is open!')

        print(f"ssu is running... length of arr:{len(ret)}")
        '''
        registerCommand='./webregBot.py'
        for index in openClasses:
            registerCommand+=' '+index
        if len(openClasses)>0:
            os.system(registerCommand)
            for index in openClasses:
                for i in indexArray:
                    if index==i:
                        indexArray.remove(i)
        '''
        #print ('Sleeping...\nPress ctrl-c to stop.\n')
        #sleep(2)
        return ret
