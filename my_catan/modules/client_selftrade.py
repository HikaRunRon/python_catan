from __future__ import print_function        ########クライアントのセルフトレードを担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
from modules import longest_road
from modules import client_draw as cld
from modules import client_start_setting
from modules import client_map_display
from modules import client_first_phase
import random
def client_selftrade(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,sock,self_trade,readfds,bufsize,volume):
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
  cld.draw_image(screen,"./picture/Action.png",540,60)
  cld.draw_image(screen,"./picture/client_trade.png",60,60)
  discard_resource_list = cld.draw_candidate_choose2(screen)
  if self_trade[0]:
    self_trade_discard = [True]
    while self_trade_discard[0]:
      pygame.display.update()
      pygame.time.wait(50) #20fps
              
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1: #蛮族の場所を選択
          x, y = event.pos
          if 1<=x and x<=120 and 1<=y and y<=60:
            self_trade[0] = False
            self_trade_discard[0] = False
          for i in range(5):
            if (discard_resource_list[i][0]-x)*(discard_resource_list[i][0]-x)+(discard_resource_list[i][1]-y)*(discard_resource_list[i][1]-y)<=400:
              trade_rate = 4
              if Player_Data[yourturn][12][0]==1:
                trade_rate = 3
              if Player_Data[yourturn][12][i+1]==1:
                trade_rate = 2
              if Player_Data[yourturn][2][i]>=trade_rate:
                Player_Data[yourturn][1] -= trade_rate
                Player_Data[yourturn][2][i] -= trade_rate
                self_trade_discard[0]=False
              break
      if self_trade_discard[0]==False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
      
    if self_trade[0]:
      cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
      cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
      cld.draw_image(screen,"./picture/frame.png",540,540)
      cld.draw_Dice(screen,Dice1[0],Dice2[0])
      cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
      cld.draw_image(screen,"./picture/Action.png",540,60)
      cld.draw_image(screen,"./picture/client_trade.png",60,60)
      discard_resource_list = cld.draw_candidate_choose(screen)
      pygame.display.update()
      self_trade_discard[0] = True
    while self_trade_discard[0]:
      pygame.display.update()
      pygame.time.wait(50) #20fps
              
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1: #蛮族の場所を選択
          x, y = event.pos
          for i in range(5):
            if (discard_resource_list[i][0]-x)*(discard_resource_list[i][0]-x)+(discard_resource_list[i][1]-y)*(discard_resource_list[i][1]-y)<=400:
              Player_Data[yourturn][1] += 1
              Player_Data[yourturn][2][i] += 1
              self_trade_discard[0]=False
              break
      if self_trade_discard[0]==False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
    msg1 = str(Player_Data[yourturn][2][0]) + "/" + str(Player_Data[yourturn][2][1]) + "/" + str(Player_Data[yourturn][2][2]) + "/" + str(Player_Data[yourturn][2][3]) + "/" + str(Player_Data[yourturn][2][4])
    sock.send("selftrade".encode('utf-8'))
    sock.recv(bufsize)
    sock.send(str(yourturn).encode('utf-8'))
    sock.recv(bufsize)
    sock.send(msg1.encode('utf-8'))
    sock.recv(bufsize)
    sock.send(str(Player_Data[yourturn][1]).encode('utf-8'))
    sock.recv(bufsize)
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])
    cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
    cld.draw_image(screen,"./picture/Action.png",540,60)
    cld.draw_image(screen,"./picture/client_trade.png",60,60)
    pygame.display.update()