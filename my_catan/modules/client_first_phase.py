from __future__ import print_function        ########クライアントの初期フェーズ（開拓地建設と街道建設）を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
from modules import longest_road
from modules import client_draw as cld

def client_first_phase(running,myturn,sock,readfds,bufsize,Mapdata_Edge,once,Mapdata_Mass,Player_Data,screen,Mapdata_Side,land,landnumber,backlog,yourturn,rightside,leftside,front,volume):

  settlement_sound = pygame.mixer.Sound("./music/settlement_sound01.mp3")
  road_sound = pygame.mixer.Sound("./music/road_sound.mp3")
  turn_start = pygame.mixer.Sound("./music/turn_start.mp3")

  while running[0]: #初動、開拓地&街道建設フェーズ
    pygame.display.update()
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
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
      elif msg == "Yourturn": #ターン通知を受け取った時、自分のターンを開始する。
        print("ok")
        myturn[0] = True
      elif msg == "Mapdata":
        msg1 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        if msg1 == "settlement":
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          pos = int(msg2)
          player = int(msg3)
          Mapdata_Edge[pos][0]=player*2 #クライアント側のデータ更新完了
          if once[player]!=0:
            for i in range(19):
              if pos in Mapdata_Mass[i][3]:
                x = Mapdata_Mass[i][0]
                if x != 0:
                  Player_Data[player][2][x-1] += 1
                  Player_Data[player][1] += 1
          once[player]=1
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
          settlement_sound.play()
        elif msg1 == "road":
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          pos = int(msg2)
          player = int(msg3)
          Mapdata_Side[pos][0]=player #クライアント側のデータ更新完了
          Player_Data[player][8] = longest_road.longestroad(Mapdata_Side,player)
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
          road_sound.play()
      elif msg == "firstphaseend":
        running[0] = False  
    if myturn[0] == False:
      continue  
    player_str = str(yourturn)

    print(yourturn)
    settlement = -1
    settlement_candidates = cld.draw_candidate_settlement(screen,yourturn,Mapdata_Edge,Mapdata_Side,0)
    turn_start.play()
    while myturn: #開拓地を置く
      pygame.display.update()
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          x, y = event.pos
          for i in settlement_candidates:
            if (Mapdata_Edge[i][4][0]-x)*(Mapdata_Edge[i][4][0]-x)+(Mapdata_Edge[i][4][1]-y)*(Mapdata_Edge[i][4][1]-y)<=500:
              settlement = i
              i_str = str(i)
              sock.send("Mapdata".encode('utf-8'))
              sock.recv(bufsize)
              sock.send("settlement".encode('utf-8'))
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(player_str.encode('utf-8'))
              sock.recv(bufsize)
              myturn[0] = False
              break
      if myturn[0] == False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
    msg = sock.recv(bufsize).decode('utf-8')
    sock.send("ok".encode('utf-8'))
    if msg == "Mapdata":
      msg1 = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      if msg1 == "settlement":
        msg2 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        msg3 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        pos = int(msg2)
        print(pos)
        player = int(msg3)
        Mapdata_Edge[pos][0]=player*2 #クライアント側のデータ更新完了
        trade_judge = Mapdata_Edge[pos][1]
        if trade_judge!=-1:
          Player_Data[player][12][trade_judge]=1
        if once[player]!=0:
          for i in range(19):
            if pos in Mapdata_Mass[i][3]:
              x = Mapdata_Mass[i][0]
              if x != 0:
                Player_Data[player][2][x-1] += 1
                Player_Data[player][1] += 1
        once[player]=1
        cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
        settlement_sound.play()
    road_candidates = cld.draw_candidate_road_0(screen,Mapdata_Edge,Mapdata_Side,settlement)
    myturn[0] = True
    while myturn[0]: #街道を置く
      pygame.display.update()
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          x, y = event.pos
          for i in road_candidates:
            if (Mapdata_Side[i][3][0]-x)*(Mapdata_Side[i][3][0]-x)+(Mapdata_Side[i][3][1]-y)*(Mapdata_Side[i][3][1]-y)<=500:
              i_str = str(i)
              sock.send("Mapdata".encode('utf-8'))
              sock.recv(bufsize)
              sock.send("road".encode('utf-8'))
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(player_str.encode('utf-8'))
              sock.recv(bufsize)
              myturn[0] = False
              break
      if myturn[0] == False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
    msg = sock.recv(bufsize).decode('utf-8')
    sock.send("ok".encode('utf-8'))
    if msg == "Mapdata":
      msg1 = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      if msg1 == "road":
        msg2 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        msg3 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        pos = int(msg2)
        print(pos)
        player = int(msg3)
        Mapdata_Side[pos][0]=player #クライアント側のデータ更新完了
        Player_Data[player][8] = longest_road.longestroad(Mapdata_Side,player)
        cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
        road_sound.play()