# coding: utf-8
'''
このサンプルプログラムはD7Sセンサで取得したデータをAmbientに送信して可視化します。
Ambientにデータを送信する場合は5秒以上間隔を開ける必要があります。
https://ambidata.io/refs/spec/
Sleepを入れて10秒に1回送信します。
'''
from __future__ import print_function

import os
import time
import datetime

import grove_d7s
import ambient

# sensor instance
sensor = grove_d7s.GroveD7s()

# ambient instance
try:
    AMBIENT_CHANNEL_ID = int(os.environ['5894'])
    AMBIENT_WRITE_KEY = os.environ['ce74641e94346985']
    am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)
except KeyError:
    print("isaaxの環境変数サービスを使って AMBIENT_CHANNEL_ID と AMBIENT_WRITE_KEY を設定してください")
    exit(1)


def main():
    while sensor.isReady() == False:
        print('.')
        time.sleep(1.0)

    print("start")

    while True:
        # 10秒のインターバルを設定
        time.sleep(10)
        # センサーデータの取得
        si = sensor.getInstantaneusSI()
        pga = sensor.getInstantaneusPGA()
        now = datetime.datetime.today()
        eq = sensor.isEarthquakeOccuring()

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
        try:
            am.send(payload)
        except Exception as e:
            print(e)

        # デバッグ用に送信したデータを標準出力（本当は不要）
        print(now.strftime("[%Y/%m/%d %H:%M:%S]"),
            "SI={}[Kine]".format(si), 
            "PGA={}[gal]".format(pga),
            "EQ=%s" % eq)


if __name__ == '__main__':
    main()
