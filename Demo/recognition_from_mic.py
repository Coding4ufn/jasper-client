#coding:utf-8
import requests
import json  

API_KEY = 'k0iEF21CdmUtjbsGZW9ZyeOl'
SECRET_KEY = '787674a9b0b22f845442f78287b1da8d'
   
def getToken(apiKey=API_KEY, secretKey=SECRET_KEY):  
	authUrl = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + \
				apiKey + "&client_secret=" + secretKey;    
	response = requests.get(authUrl)
	json = response.json()
	return json['access_token']

def baiduRecognition(audioData):  
	token = getToken()
	cuid = "xxxxxxxxxx"  
	srvUrl = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token   
	httpHeader = {  
        'Content-Type': 'audio/wav; rate = 8000', 
	}
	response = requests.post(srvUrl,headers=httpHeader,data=audioData)
	return response

def recognition(audioData):
	response = baiduRecognition(audioData)
	if response.ok:
		json = response.json()
		res = json.get('result', [])
		return [s[:-1] for s in res]
	return []

if __name__ == '__main__':
	from record import Record
	record = Record(channels=1)
	audioData = record.record(2)
	print recognition(audioData)[0]