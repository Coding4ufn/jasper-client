#encoding=utf-8  
   
import wave  
import urllib, urllib2, pycurl  
import base64  
import json  
## get access token by api key & secret key  


PROCESSING = 0
EXIT = 0
EXTSTR = u'退出，'


def process_voice_cmd(vocmd):
    words = jieba.posseg.cut(vocmd)
    for word, flag in words:
        print('%s %s' % (word, flag))
        

def dump_res(buf):
    global PROCESSING, EXIT, EXTSTR
    print buf
    err = json.loads(buf)['err_no']
    #print 'err_no: %d' % err
    if err != 0:
        PROCESSING = 2
    else:
        result = json.loads(buf)['result']
        print 'result : %s' % (result[0])
        if result[0] == EXTSTR:
            EXIT = 1
        PROCESSING = 0
        process_voice_cmd(result[0])
   
def get_token():  
    apiKey = "P6yNkb53IwvBwvAEjVF9pQUz" 
    secretKey = "b0e5e316cece2a0ef1684315461fc457" 
   
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;  
   
    res = urllib2.urlopen(auth_url)  
    json_data = res.read()  
    return json.loads(json_data)['access_token']  

## post audio to server  
def use_cloud(token):  
    fp = wave.open('test.wav', 'rb')
    nf = fp.getnframes()  
    f_len = nf * 2 
    audio_data = fp.readframes(nf)  
    #with open('../static/audio/time.wav', 'rb') as f:
    #    speech_data = f.read();
   # audio_data = base64.b64encode(speech_data)
    #audio_data = speech_data
    f_len = len(audio_data)
    print 'file lenght %s' % f_len
   
    cuid = "6c:0b:84:91:5c:b0" #my xiaomi phone MAC  
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token  
    http_header = [  
        'Content-Type: audio/wav; rate=16000',  
        'Content-Length: %d' % f_len  
    ]  
   
    c = pycurl.Curl()  
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
    #c.setopt(c.RETURNTRANSFER, 1)  
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict  
    c.setopt(c.POST, 1)  
    c.setopt(c.CONNECTTIMEOUT, 30)  
    c.setopt(c.TIMEOUT, 30)  
    c.setopt(c.WRITEFUNCTION, dump_res)  
    c.setopt(c.POSTFIELDS, audio_data)  
    c.setopt(c.POSTFIELDSIZE, f_len)  
    c.perform() #pycurl.perform() has no return val 

if __name__ == "__main__":  
    token = get_token()
    print token
    use_cloud(token)