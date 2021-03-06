import json
import requests
import secrets
import time
import csv

startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

endpoint = '/repositories/3/resources?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()

records = []
f=csv.writer(open('duplicateBeginEndDates.csv', 'wb'))
f2=csv.writer(open('asDates.csv', 'wb'))
f.writerow(['uri']+['begin']+['end']+['expression']+['type'])
f2.writerow(['uri']+['begin']+['end']+['expression']+['type'])
counter = 0
for id in ids:
    endpoint = '/repositories/3/resources/'+str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    for date in output['dates']:
        counter = counter + 1
        print counter
        try:
            begin = date['begin']
        except:
            begin = ''
        try:
            end = date['end']
        except:
            end = ''
        try:
            expression = date['expression']
        except:
            expression = ''
        if begin == end and begin != '' and begin != '':
            f.writerow([output['uri']]+[begin]+[end]+[expression]+[date['date_type']])
        else:
            f2.writerow([output['uri']]+[begin]+[end]+[expression]+[date['date_type']])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
