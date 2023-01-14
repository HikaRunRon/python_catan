from __future__ import print_function       ########クライアントの人数待ち画面を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
from modules import longest_road
from modules import client_draw as cld
def client_start_setting(running,sock,readfds,bufsize,backlog,screen,volume):
  while running:
    pygame.display.update() #ディスプレイ更新
    pygame.time.wait(50)
    for event in pygame.event.get():
      if event.type == QUIT:
        sock.send("QUIT".encode('utf-8'))
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          sock.send("QUIT".encode('utf-8'))
          pygame.quit()
          sys.exit()
        if event.key == 1073741906:
          if volume[0] < 1.0:
            pygame.mixer.music.pause()
            volume[0] += 0.1
            pygame.mixer.music.set_volume(volume[0])
            pygame.mixer.music.unpause()
        if event.key == 1073741905:
          if volume[0] > 0.0:
            pygame.mixer.music.pause()
            volume[0] -= 0.1
            pygame.mixer.music.set_volume(volume[0])
            pygame.mixer.music.unpause()
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg1 = sock.recv(bufsize).decode('utf-8')
      print("msg1,",msg1)
      sock.send("ok".encode('utf-8'))
      if msg1 == "plwt":
        msg2 = sock.recv(bufsize).decode('utf-8')
        print("msg2,",msg2)
        connections = int(msg2)
        print("connections,",connections)
        if backlog == 3:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-3.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-3.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-3.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/3-3.jpg").convert_alpha() #背景画像設定
            running = False
        else:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-4.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-4.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-4.jpg").convert_alpha() #背景画像設定
          elif connections == 3:
            bg = pygame.image.load("./picture/Setting_Screen/3-4.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/4-4.jpg").convert_alpha() #背景画像設定
            running = False
        rect_bg = bg.get_rect() #背景画像の大きさを取得
        screen.blit(bg,rect_bg) #背景描画
      elif msg1 == "serverdown":
        pygame.quit()
        sys.exit()