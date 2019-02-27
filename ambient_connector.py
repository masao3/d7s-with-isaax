# coding: utf-8
import os
from datetime import datetime
import time
import ambient
import requests
class AmbientConnector():
    def __init__(self):
        '''
        Ambientに接続するためのキーが環境変数にセットされているかの確認
        該当する環境変数がない場合は強制終了
        '''
        try:
            CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
            WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
        except KeyError:
            print(KeyError)
            exit(1)
        # Ambientインスタンスの作成
        self.am = ambient.Ambient(CHANNEL_ID, WRITE_KEY)
        # バッファー用のデータを初期化
        self.datas = []
        # 最終送信時刻
        self.last_posted_at = datetime.now()
    # データをバッファーする
    def buffer(self, payload):
        self.datas.append(payload)
        # 前回の送信から10秒間隔が空いていればバッファーした直後に自動的に送信する
        if (datetime.now() - self.last_posted_at).seconds > 10:
            self.__send()
        return payload
    
    # バッファーデータを送信する(private method)
    def __send(self):
        r = self.am.send(self.datas)
        if (r.status_code == 200):
            self.datas = []
            self.last_posted_at = datetime.now()
            print('Ambient send successful')
        else:
            print('Ambient send error')
