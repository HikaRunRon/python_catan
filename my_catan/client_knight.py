from __future__ import print_function
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import point_calculation as pc
import longest_road
import random
import client_draw as cld

def client_knight(Knight,screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,bufsize,bandit_pos,sock,readfds,Winner,running,running1,Thisturn_draw):
  if Knight[0]:
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])
    cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
    cld.draw_image(screen,"./picture/Action.png",540,60)
    bandit_list = cld.draw_candidate_bandit(screen,Mapdata_Mass)
    while Knight[0]:
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1: #蛮族の場所を選択
          x, y = event.pos
          for i in bandit_list:
            if (Mapdata_Mass[i][4][0]-x)*(Mapdata_Mass[i][4][0]-x)+(Mapdata_Mass[i][4][1]-y)*(Mapdata_Mass[i][4][1]-y)<=625:
              i_str = str(i)
              sock.send("Bandit".encode('utf-8')) #蛮族の情報を送信する事を通知
              sock.recv(bufsize)
              sock.send(str(bandit_pos).encode('utf-8')) #どこから蛮族を動かすのか
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8')) #どこに蛮族を置くのか
              sock.recv(bufsize)
              Mapdata_Mass[bandit_pos[0]][2]=0
              Mapdata_Mass[i][2]=1
              bandit_pos[0]=i
              cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
              cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
              cld.draw_image(screen,"./picture/frame.png",540,540)
              cld.draw_Dice(screen,Dice1[0],Dice2[0])
              pygame.display.update() 
              Knight[0]=False
              break
      if Knight[0]==False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
    ###############################
    rob_list = cld.draw_candidate_rob(screen,Mapdata_Mass,Player_Data,Mapdata_Edge,bandit_pos[0],yourturn)
    if len(rob_list)==0:
      Knight[0]=False
      sock.send("NoRob".encode('utf-8')) #カード奪取無し
      sock.recv(bufsize)
      sock.send(str(yourturn).encode('utf-8')) #カード奪取無し
      sock.recv(bufsize)
    else:
      Knight[0]=True #カード奪取あり
    ###############################
    while Knight[0]:
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
        if event.type == MOUSEBUTTONDOWN and event.button == 1: #蛮族の場所を選択
          x, y = event.pos
          for i in rob_list:
            if (Mapdata_Edge[i][4][0]-x)*(Mapdata_Edge[i][4][0]-x)+(Mapdata_Edge[i][4][1]-y)*(Mapdata_Edge[i][4][1]-y)<=500:
              i_str = str(i)
              player02 = Mapdata_Edge[i][0]/2
              player02 = int(player02)
              card_list = []
              for j in range(5):
                card_counter = Player_Data[player02][2][j]
                for k in range(card_counter):
                  card_list.append(j)
              x = random.choice(card_list) #player02からyourturnにxのカードがrob
              sock.send("Rob".encode('utf-8')) #カード奪取の情報を送信する事を通知
              sock.recv(bufsize)
              sock.send(str(player02).encode('utf-8')) #誰から
              sock.recv(bufsize)
              sock.send(str(yourturn).encode('utf-8')) #誰に
              sock.recv(bufsize)
              sock.send(str(x).encode('utf-8')) #なんのカード
              sock.recv(bufsize)
              Player_Data[player02][1]-=1
              Player_Data[player02][2][x]-=1
              Player_Data[yourturn][1]+=1
              Player_Data[yourturn][2][x]+=1
              Knight[0]=False
              break  
      if Knight[0]==False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
  Player_Data[yourturn][10] += 1
  Player_Data[yourturn][3] -= 1
  Player_Data[yourturn][4][0] -= 1
  if Player_Data[yourturn][11]==0 and Player_Data[yourturn][10]>=3:
    largest_judge = True
    for j in range(4):
      if j!=yourturn:
        if Player_Data[j][10]>=Player_Data[yourturn][10]:
          largest_judge = False
    if largest_judge:
      for j in range(4):
        Player_Data[j][11]=0
      Player_Data[yourturn][11]=1
  if pc.pointget(Player_Data,yourturn)>=10:
    sock.send("Win".encode('utf-8'))
    sock.recv(bufsize)
    sock.send(str(yourturn).encode('utf-8'))
    sock.recv(bufsize)
    Winner[0]=yourturn
    running1[0]=False
    running[0]=False
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
  cld.draw_image(screen,"./picture/Action.png",540,60)
  cld.draw_client_development(screen,Player_Data,yourturn,Thisturn_draw)
  pygame.display.update()