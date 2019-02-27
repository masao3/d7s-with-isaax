# coding: utf-8
# Sample that outputs the value acquired by D7S.
from __future__ import print_function
import os
import time
import datetime
import grove_d7s
from ambient_connector import AmbientConnector
# sensor instance
sensor = grove_d7s.GroveD7s()
# ambientをラップしたAmbientConnectorを使います
am = AmbientConnector()
def main():
    while sensor.isReady() == False:
        print('.')
        time.sleep(1.0)
    print("start")
    while True:
        # 1秒間隔でデータを取得する
        time.sleep(1.0)
        
        # センサーデータの取得
        si = sensor.getInstantaneusSI()
        pga = sensor.getInstantaneusPGA()
        now = datetime.datetime.today()
        eq = sensor.isEarthquakeOccuring()
        # デバッグ用にデータを標準出力（本当は不要）
        print(now.strftime("[%Y/%m/%d %H:%M:%S]"),
            "SI={}[Kine]".format(si), 
            "PGA={}[gal]".format(pga),
            "EQ=%s" % eq)
        # センサーの初期化中は値がNoneになるので処理をスキップ
        if si == None and pga == None:
            continue
        # Ambientに送信するペイロードを作成
        payload = {
            "d5": int(eq),
            "d1": si,
            "d2": pga,
            "created": now.strftime("%Y/%m/%d %H:%M:%S")
            }
        # データをバッファーする
        am.buffer(payload)
if __name__ == '__main__':
    main()
