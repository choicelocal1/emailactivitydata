import json
import requests
from datetime import datetime, timedelta
import asyncio

dateTimeObj = (datetime.now() - timedelta(days=1))
print(dateTimeObj)
sid = '44bd0e21-367d-4181-ae69-5004dc79b7fc'
sclient = 'ads4h6YHEBfZZjzoQocFBwFJNVdKrUxj'

authr = requests.get('https://669-GJU-501.mktorest.com/identity/oauth/token?grant_type=client_credentials&client_id=' + sid + '&client_secret=' + sclient)

res = authr.text
obj = json.loads(res)

print(res)
print(obj["access_token"])

r1 = requests.get('https://669-GJU-501.mktorest.com/rest/v1/activities/pagingtoken.json?sinceDatetime=' + str(dateTimeObj) + '&access_token=' + obj["access_token"])

print(r1.text)

res1 = r1.text
obj1 = json.loads(res1)

r2 = requests.get('https://669-GJU-501.mktorest.com/rest/v1/activities.json?access_token=' + obj["access_token"] + '&nextPageToken=' + obj1['nextPageToken'] + '&activityTypeIds=6,7,8,9,10,11')


res_json = json.loads(r2.text)

async def push_response(response):
	i = 0
	for val in response['result']:
		i += 1
		print(str(i) + ' Result')
		print(response['result'][i]['id'])
		if i == 299:
			i=0	

async def get_next_page(response):
	if response['moreResult'] == True:
		await push_response(response)
		r3 = requests.get('https://669-GJU-501.mktorest.com/rest/v1/activities.json?access_token=' + obj["access_token"] + '&nextPageToken=' + response['nextPageToken'] + '&activityTypeIds=6,7,8,9,10,11')
		await main(json.loads(r3.text))

	else:
		print('done')

async def main(response_json):
	task1 = asyncio.create_task(get_next_page(response_json))
	await task1
	print('Finished')
	
	
asyncio.run(main(res_json))
