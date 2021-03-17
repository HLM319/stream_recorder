import requests
import time
import sys
import argparse
import json

def acfunRecoder(authorId:int, path:str):
    authorId = str(authorId)

    headers = {'accept':'application/json, text/plain, */*',
               'accept-encoding':'gzip, deflate, br',
               'accept-language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
               'origin':'https://live.acfun.cn',
               'referer':'https://live.acfun.cn/',
               'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    headerResponse = requests.get('https://live.acfun.cn/api/header', headers=headers)
    headers.update({'cookie': ';'.join(f'{key}={item}' for key, item in headerResponse.cookies.items())})
    postHeader = dict({'content-type':'application/x-www-form-urlencoded'}, **headers)
    while True:
        loginResponse = requests.post('https://id.app.acfun.cn/rest/app/visitor/login', data={'sid':'acfun.api.visitor'}, headers=postHeader)
        startPlayapi = requests.post(f'https://api.kuaishouzt.com/rest/zt/live/web/startPlay?subBiz=mainApp&kpn=ACFUN_APP&kpf=PC_WEB\
                                    &userId={loginResponse.json()["userId"]}&did={headerResponse.cookies.get("_did")}\
                                    &acfun.api.visitor_st={loginResponse.json()["acfun.api.visitor_st"]}',
                                    data={'authorId':authorId, 'pullStreamType':'FLV'}, headers=postHeader)
        if (startPlayapi.json()['result'] == 1):
            link = max(json.loads(startPlayapi.json()['data']['videoPlayRes'])['liveAdaptiveManifest'][0]['adaptationSet']['representation'],
                    key=lambda i:i['bitrate'])['url']
            print('Start recode.')
            with requests.get(link, headers=headers, stream=True) as source:
                source.raise_for_status()
                with open(path + '/' + authorId + '-' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + '.flv', 'wb') as file:
                    for chuck in source.iter_content(1024):
                        file.write(chuck)
        else:
            time.wait(30)
            print('Not Streaming, trying again.')

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description='A simple stream recoder.')
    argParser.add_argument('authorId', action='store', type=int)
    argParser.add_argument('-p' ,'--path', action='store', default='.')
    args = vars(argParser.parse_args())
    acfunRecoder(args['authorId'], args['path'])