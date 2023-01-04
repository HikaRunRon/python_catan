from __future__ import print_function
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import longest_road
import client_draw as cld

def client_first_phase(running,myturn,sock,readfds,bufsize,Mapdata_Edge,once,Mapdata_Mass,Player_Data,screen,Mapdata_Side,land,landnumber,backlog,yourturn,rightside,leftside,front):
  while running: #初動、開拓地&街道建設フェーズ
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
        myturn = True
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
        elif msg1 == "road":
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          pos = int(msg2)
          player = int(msg3)
          Mapdata_Side[pos][0]=player #クライアント側のデータ更新完了
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
      elif msg == "firstphaseend":
        running = False  
    if myturn == False:
      continue  
    player_str = str(yourturn)

    print(yourturn)
    settlement = -1
    settlement_candidates = cld.draw_candidate_settlement(screen,yourturn,Mapdata_Edge,Mapdata_Side,0)
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
              myturn = False
              break
      if myturn == False:
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
        if once[player]!=0:
          for i in range(19):
            if pos in Mapdata_Mass[i][3]:
              x = Mapdata_Mass[i][0]
              if x != 0:
                Player_Data[player][2][x-1] += 1
                Player_Data[player][1] += 1
        once[player]=1
        cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
    road_candidates = cld.draw_candidate_road_0(screen,Mapdata_Edge,Mapdata_Side,settlement)
    myturn = True
    while myturn: #街道を置く
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
              myturn = False
              break
      if myturn == False:
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
        cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新