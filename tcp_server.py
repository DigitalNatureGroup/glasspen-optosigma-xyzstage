import pyOptoSigma
from pyOptoSigma import *
import time
import socket

import argparse

parser = argparse.ArgumentParser(description='ステージのポート番号を指定')
parser.add_argument('arg1', help='デバイスマネージャーを参照し、ステージコントローラーのポート番号を引数に入れてください.')
args = parser.parse_args()


stages = Session(Controllers.SHOT_304GS)
stages.append_stage(Stages.OSMS26_100)
stages.append_stage(Stages.OSMS26_100)
stages.append_stage(Stages.OSMS26_100)
stages.connect(portname=args.arg1)

server_ip = "localhost"
server_port = 2430
listen_num = 5
buffer_size = 1024

stage_num = 0
val = 0

# 1.ソケットオブジェクトの作成
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2.作成したソケットオブジェクトにIPアドレスとポートを紐づける
tcp_server.bind((server_ip, server_port))

# 3.作成したオブジェクトを接続可能状態にする
tcp_server.listen(listen_num)

# 4.ループして接続を待ち続ける
while True:
    # 5.クライアントと接続する
    client,address = tcp_server.accept()
    print("[*] Connected!! [ Source : {}]".format(address))
    while True:
        # 6.データを受信する
        data = client.recv(buffer_size).decode().split(',')
        if data == "" or (len(data)!=2):
            print("data error")
            print(data)
            break
        else:
            stage_num = int(data[0])
            val = int(data[1])
            print("stage:{}, val:{}".format(stage_num, val))
            # 7.クライアントへデータを返す
            print("move stage {}".format(stage_num))
            stages.move(stage=stage_num, amount=val, wait_for_finish=True)

            client.send(b"1")
    # 8.接続を終了させる
    client.close()