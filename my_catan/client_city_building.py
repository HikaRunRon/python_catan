from __future__ import print_function    ########クライアントの都市建設を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import longest_road
import random
import client_draw as cld
import point_calculation as pc
def client_city_building(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,city_running,sock,bufsize,Winner,running,running1,readfds):
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
  cld.draw_image(screen,"./picture/Action.png",540,60)
  city_candidate = cld.draw_candidate_city(screen,yourturn,Mapdata_Edge)
  while city_running[0]:
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
      if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if 481<=x and x<=540 and 61<=y and y<=120: #枠内左クリックでwhileを抜け、次のページへ
          city_running[0]=False #ループから抜ける
        else:
          for i in city_candidate:
            if (Mapdata_Edge[i][4][0]-x)*(Mapdata_Edge[i][4][0]-x)+(Mapdata_Edge[i][4][1]-y)*(Mapdata_Edge[i][4][1]-y)<=500:
              i_str = str(i)
              Mapdata_Edge[i][0]=yourturn*2+1
              Player_Data[yourturn][1] -= 5
              Player_Data[yourturn][2][3] -= 2
              Player_Data[yourturn][2][4] -= 3
              Player_Data[yourturn][5] += 1
              Player_Data[yourturn][6] -= 1
              player_str = str(yourturn)
              sock.send("City".encode('utf-8')) #都市の情報を送信する
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8')) #どこに都市を置くのか
              sock.recv(bufsize)
              sock.send(player_str.encode('utf-8')) #誰が都市を置くのか
              sock.recv(bufsize)           
              city_running[0]=False
              if pc.pointget(Player_Data,yourturn)>=10:
                sock.send("Win".encode('utf-8'))
                sock.recv(bufsize)
                sock.send(str(yourturn).encode('utf-8'))
                sock.recv(bufsize)
                Winner[0]=yourturn
                running1[0]=False
                running[0]=False
              break

        if city_running[0]==False:
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
          cld.draw_image(screen,"./picture/Action.png",540,60)
          pygame.display.update()

    if city_running[0] == False:  #サイコロフリフリメッセージ送信後は即ループ脱出
      break 
        
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()