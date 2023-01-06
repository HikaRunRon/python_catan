from __future__ import print_function         ########クライアントの街道建設(発展カード)を担うファイル
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
def client_roadroad(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,road_running,sock,bufsize,Winner,running1,running,readfds):
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  road_candidate = cld.draw_candidate_road(screen,yourturn,Mapdata_Edge,Mapdata_Side)

  while road_running[0]:
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
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #サイコロボタンのクリック
        x, y = event.pos
        if 481<=x and x<=540 and 1<=y and y<=60: #枠内左クリックでwhileを抜け、次のページへ
          road_running[0]=False #ループから抜ける
        else:
          for i in road_candidate:
            if (Mapdata_Side[i][3][0]-x)*(Mapdata_Side[i][3][0]-x)+(Mapdata_Side[i][3][1]-y)*(Mapdata_Side[i][3][1]-y)<=500:
              i_str = str(i)
              Mapdata_Side[i][0]=yourturn
              road_length = longest_road.longestroad(Mapdata_Side,yourturn)
              Player_Data[yourturn][8] = road_length
              Player_Data[yourturn][7] -= 1
              if Player_Data[yourturn][9]==0 and Player_Data[yourturn][8]>=5:
                longest_judge = True
                for j in range(4):
                  if j!=yourturn:
                    if Player_Data[j][8]>=Player_Data[yourturn][8]:
                      longest_judge = False
                if longest_judge:
                  for j in range(4):
                    Player_Data[j][9]=0
                  Player_Data[yourturn][9]=1
                      
              player_str = str(yourturn)
              road_length_str = str(road_length)
              sock.send("Road2".encode('utf-8')) #道の情報を送信する
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8')) #どこに道を置くのか
              sock.recv(bufsize)
              sock.send(player_str.encode('utf-8')) #誰が道を置くのか
              sock.recv(bufsize)
              sock.send(road_length_str.encode('utf-8')) #更新された交易路の長さ
              sock.recv(bufsize)  
              sock.send("MsgEnd".encode('utf-8')) #情報のやり取りを終了
              sock.recv(bufsize)                          
              road_running[0]=False
              if pc.pointget(Player_Data,yourturn)>=10:
                sock.send("Win".encode('utf-8'))
                sock.recv(bufsize)
                sock.send(str(yourturn).encode('utf-8'))
                sock.recv(bufsize)
                Winner[0]=yourturn
                running1[0]=False
                running[0]=False
              break

        if road_running[0]==False:
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])

    if road_running[0] == False:  
      break 
        
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()