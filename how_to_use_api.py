import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
#print(response)
#print(response.json())
#print(response.json()['items'])

#priting specific items from the json items
#for data in response.json()['items']:
	#print(data['title'])
	#print(data['link'])
	#print()

# let's say we just want to get the items where the answer_count is not 0
for data in response.json()['items']:
	if data['answer_count'] ==0:
		print('Skipped')
		print() 
	
	print(data['title'])
	print(data['link'])
	print()
