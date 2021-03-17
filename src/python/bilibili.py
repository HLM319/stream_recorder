import requests
import time
import sys
import argparse

def bilibiliRecoder(roomId:int, path:str):
    roomId = str(roomId)
    roomInfoBaseUrl = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='
    headers = {'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
                'dnt':'1',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    while True:
        roomInfo = requests.get(roomInfoBaseUrl + roomId, headers=headers)
        if roomInfo.json()['data']['live_status'] == 1:
            streamInfoBaseUrl = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid='
            streaminfo = requests.get(streamInfoBaseUrl + roomId, headers=headers)
            qn = max(streaminfo.json()['data']['accept_quality'])
            streaminfo = requests.get(streamInfoBaseUrl + roomId + '&quality=' + qn + '&platform=web')
            link = streaminfo.json()['data']['durl'][0]['url']
            downloadHeaders = {'Connection':'keep-alive',
                                'Host':link.split('/')[2],
                                'Origin':'https://live.bilibili.com',
                                'Referer':'https://live.bilibili.com/',
                                **headers}
            print('Start recode.')
            with requests.get(link, headers=headers, stream=True) as source:
                source.raise_for_status()
                with open(path + '/' + roomId + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + '.flv', 'wb') as file:
                    for chuck in source.iter_content(1024):
                        file.write(chuck)
        else:
            time.sleep(5)
            print('Not Streaming, trying again.')

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description='A simple stream recoder.')
    argParser.add_argument('roomid', action='store', type=int)
    argParser.add_argument('-p' ,'--path', action='store', default='.')
    args = vars(argParser.parse_args())
    bilibiliRecoder(args['roomid'], args['path'])