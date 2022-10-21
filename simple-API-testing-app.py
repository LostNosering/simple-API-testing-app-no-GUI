#IMPORTS

import time
import multiprocessing
import requests
from random import randrange

#DATA

apis = [
    [
      '/api/admin/export',
      ['post', '{"indexPatternChecked":true,"taskName":"test","index":"audit*","query":"*","fields":["indices","method"],"initiatedUser":"IntelligenceTest","fromDate":"2022-10-10T07:27:59.261Z","toDate":"2022-10-17T07:27:59.261Z","timeCriteriaField":"@timestamp","metafields":false,"export_type":"csv","export_format":"csv","role":"admin","scheduled":false,"fastMode":true}', 'payload.taskName', 'data export name'],
    ],
    [
      '/api/admin/export',
      ['put', '{"id":"ghskzIMBIa-FH8WR_9Nh","taskName":"test2tg2","indexPatternChecked":true,"index":"audit*","query":"*","fields":"_all","fromDate":"now-1w","toDate":"now","timeCriteriaField":"@timestamp","export_format":"csv","fastMode":true,"emailText":"topic","emailAddresses":"pawethanski@gmail.com","cronFormat":"0 0 23 * * *","role":"admin","metafields":false}', 'payload.taskName', 'data export edited'],
    ],
    [
      '/api/admin/csvtask/enable',
      ['post', '{"id":"ghskzIMBIa-FH8WR_9Nh","initiatedUser":"IntelligenceTest"}', 'payload.id', 'data export enabled'],
    ],
    [
      '/api/admin/csvtask/disable',
      ['post', '{"id":"ghskzIMBIa-FH8WR_9Nh","initiatedUser":"IntelligenceTest"}', 'payload.id', 'data export disabled'],
    ],
  ]
  
#APIS EXAMPLE
#[
#    'API PATH',
#    ['METHOD', 'JSON DATA'],
#],

#USERS

apiUsers = [
  ['USER1', 'PASSWORD'],
  ['USER2', 'PASSWORD'],
  ['USER3', 'PASSWORD'],
  ['USER4', 'PASSWORD'],
  ['USER5', 'PASSWORD'],
  ['USER6', 'PASSWORD'],
  ['USER7', 'PASSWORD'],
  ]


#VARIABLES

requestCount = 50 #HOW MANY REQUESTS
onOff = True #ON/OFF
stopmode = True #STOP AFTER requestCount
userNum = 10 #HOW MANY USERS
serverURL = 'https://192.168.3.191:5601'
stoper = 0.5 #Stop between every psNum process 
cert = '/home/pawethanski/.local/lib/python3.10/site-packages/certifi/cacert.pem'

#DEFAULT VARIABLES 

sendedRequests = 0
operationlist = []

#CURL FUNC

def curl(url, payload, userPass, method):
    url = serverURL+url
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    if(method == 'post'):
        r = requests.post(url, data=payload, headers=headers, auth=(userPass[0], userPass[1]), verify=cert)
    elif (method == 'delete'):
        r = requests.delete(url, data=payload, headers=headers, auth=(userPass[0], userPass[1]), verify=cert)
    elif (method == 'put'):
        r = requests.put(url, data=payload, headers=headers, auth=(userPass[0], userPass[1]), verify=cert)
    elif (method == 'get'):
        r = requests.get(url, data=payload, headers=headers, auth=(userPass[0], userPass[1]), verify=cert)

#COUNTING FINAL DATA

def printCountData(operationlist):
    res = {}

    for i in operationlist:
        res[i] = operationlist.count(i)
    print(res)

#INIT

if __name__ == "__main__":
    i = 0
    while onOff:
        if(stopmode):
            if (sendedRequests >= requestCount):
                onOff = False
                print('Done!')
                break
        numList = []
        processList = []
        for x in range(userNum):
            numList.append(randrange(20))
            processList.append(multiprocessing.Process(target=curl(apis[numList[x]][0], apis[numList[x]][1][1], apiUsers[x], apis[numList[x]][1][0])))

        for x in range(userNum):
            processList[x].start()
         
        i += 1
        sendedRequests += 10

        operationlist.extend(numList)

        print('SENDED REQUESTS COUNTER:'+ str(sendedRequests))
        time.sleep(stoper)
    printCountData(operationlist)
        