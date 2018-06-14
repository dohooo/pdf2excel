import urllib.request,urllib.error,urllib.parse,sys,ssl,json
import base64

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=DQ7XPA80smAQxYozIrXpS1ng&client_secret=qN8M7PvGRTy2MwfQDnyKbjhdQa3UtWQg'
request1=urllib.request.Request(host)
request1.add_header('Content-Type', 'application/json;charset=UTF-8')
response = urllib.request.urlopen(request1)
content = response.read()
if (content):
    print(json.loads(str(content, encoding = "utf-8"))['access_token'])
Access_token=json.loads(str(content, encoding = "utf-8"))['access_token']

    



api_url = "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise?access_token="+Access_token 
_img = open(r'a2.jpg','rb')
base64_img=base64.b64encode(_img.read()) #读取文件内容，转换为base64编码

print(_img)
postdata = urllib.parse.urlencode({  
    "image":base64_img,  
    "templateSign":"25c21a77d7daa2446856871c49f253c4"  
}).encode("utf-8") #将数据使用urlencode编码后，使用encode（）设置utf-8编码  

req = urllib.request.Request(api_url,postdata)  
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

data = urllib.request.urlopen(req).read().decode("utf-8")  
print(data)  