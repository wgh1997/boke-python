import base64
from datetime import datetime
import hashlib
import random
from wsgiref import headers
# from itsdangerous import json
import requests

import json

class YunTongXin():
        base_url = 'https://app.cloopen.com:8883'
        def __init__(self,accountSif,accountToken,appId,templateId):
                self.accountSif = accountSif # 账户ID
                self.accountToken = accountToken # 授权令牌
                self.appId = appId 
                self.templateId = templateId 


        def get_reust_url(self,sig):
                # POST  /2013-12-26/Accounts/{accountSid}/SMS/TemplateSMS?sig={SigParameter}
                self.url = self.base_url+'/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSif,sig)
                return self.url
        def get_timestamp(self):
                    
            return datetime.now().strftime('%Y%m%d%H%M%S')

        def get_sig(self,datetime):
                s = self.accountSif+self.accountToken+datetime
                m =hashlib.md5()
                m.update(s.encode())
                return m.hexdigest().upper()
        def get_request_header(self,timestamp):
                s = self.accountSif+':'+timestamp
                anth = base64.b64encode(s.encode()).decode()
                return {
                        'Accept':'application/json',
                        'Content-Type':'application/json;charset=utf-8',
                        'Authorization':anth
                }
        def get_request_body(self,phone,code):
                return {
                        "to":phone,
                        "appId":self.appId,
                        # "reqId":"abc123",
                        # "subAppend":"8888",
                        "templateId":self.templateId,
                        "datas":[code,"3"]
                }
        def get_request(self,url,header,body):

                res = requests.post(url,headers=header,data=body)
                return res.text
        def get_create_captcha(self):
                captcha = ''
                for i in range(6):
                        now_number = str(random.randint(0, 9))
                        captcha += now_number
                return captcha
        def run(self,phone,code):
                timestamp = self.get_timestamp()
                sig = self.get_sig(timestamp)
                url = self.get_reust_url(sig)
                header = self.get_request_header(timestamp)
                body = self.get_request_body(phone,code)
                data = self.get_request(url,header,json.dumps(body))
                return data


# if __name__ == '__main__':
#        yun = YunTongXin('8aaf0708806f236e01808e3319e00532','89f2b6b1438c4994bec72d05f195a174','8aaf0708806f236e01808e331ada0539',1)
      
#        res = yun.run('17635053817')
#        print(res)