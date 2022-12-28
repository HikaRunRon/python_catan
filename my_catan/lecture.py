from __future__ import print_function
import pygame
from pygame.locals import *
import socket
import select
import sys
import mapgene
import random
print("hello world!!")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPアドレスと通信プロトコルはIPv4,TCPを採択                                    #処理候補にサーバーソケットを追加
clients_socks = []                   #人数分のクライアントを格納するためのリスト
readfds = set([server_sock])         #処理候補(socket)を格納したset、後々select関数にぶち込む為だけに作成
sock.bind((host, port))       #ソケットをアドレスに結び付ける(IPアドレス = host , ポート番号 = port)
sock.listen(backlog)          #入力された接続可能クライアント数を設定(今回は3or4)


list = [0,1,2,3,4,5]
msg = ""
for i in list:
    i_str = str(i)
    msg += i_str
    msg += "/"
sock.send(msg.encode('utf-8'))  # "Message" →　01010010101001 #メッセージ送信側
sock.send("tomoya"encode('utf-8'))
sock.recv(4096)



msg = sock.recv(4096).decode('utf-8') # 01010010101001 →　"Message"　受信側

list = msg.split("/")
for i_str in list:
    

sock.send("ok".encode('utf-8'))
.
