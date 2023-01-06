from __future__ import print_function        ########クライアント(ターンでない人)のサイコロフェーズを担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import longest_road
import client_draw as cld
import client_start_setting
import client_map_display
import client_first_phase
import random

def client_others_dice(running1,sock,bufsize,readfds,Dice1,Dice2,Mapdata_Mass,Mapdata_Edge,Mapdata_Side,Player_Data,Dice7,bandit,screen,land,landnumber,backlog,yourturn,rightside,front,leftside,burst,waiting,bandit_pos):
  while running1[0]:
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

    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
      elif msg == "Dice":
        Dice_msg=sock.recv(bufsize).decode('utf-8')  
        sock.send("ok".encode('utf-8'))
        Dice_nums_str = Dice_msg.split("/")
        Dice1[0] = int(Dice_nums_str[0])
        Dice2[0] = int(Dice_nums_str[1])
        Dicesum = Dice1[0]+Dice2[0]
        if Dicesum != 7:     #7以外の出目の時
          for i in range(19):
            if Mapdata_Mass[i][0]!=0 and Mapdata_Mass[i][1]==Dicesum and Mapdata_Mass[i][2]==0:
              for x in Mapdata_Mass[i][3]:
                resouce_getter = Mapdata_Edge[x][0]
                if resouce_getter!=-1:
                  a = resouce_getter/2
                  a = int(a)
                  b = resouce_getter%2
                  b += 1
                  Player_Data[a][1] += b
                  Player_Data[a][2][Mapdata_Mass[i][0]-1] += b
        else:
          Dice7[0] = True
          bandit[0] = True
        running1[0]=False
        if Dice7[0]:
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          cld.draw_image(screen,"./picture/frame.png",540,540)
          pygame.display.update()

  ###########################
  ## サイコロフリフリ(終了) ##
  ###########################

  ################################
  ###　7が出た時の処理(バースト) ###
  ################################

  if Dice7[0]:
    msg = sock.recv(bufsize).decode('utf-8')
    if msg == "Burst":
      sock.send("ok".encode('utf-8'))

  if Dice7[0]:
    if Player_Data[yourturn][1]>=8:
      burst[0] = True
      waiting[0] = False
    else:
      waiting[0] = True

  burst_num=0
          
  if burst[0]:
    burst_num = Player_Data[yourturn][1]//2
    burst_num = int(burst_num)
    Discard_Data=[0,0,0,0,0]
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])
    cld.burst_discard(screen,yourturn,Player_Data,Discard_Data)
    pygame.display.update()
    
  while burst[0]:
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
        if 160<=x and x<=200 and 220<=y and y<=280 and Discard_Data[0]>=1:
          Discard_Data[0] -= 1
          Player_Data[yourturn][1] += 1
          Player_Data[yourturn][2][0] += 1
        if 220<=x and x<=260 and 220<=y and y<=280 and Discard_Data[1]>=1:
          Discard_Data[1] -= 1
          Player_Data[yourturn][1] += 1
          Player_Data[yourturn][2][1] += 1
        if 280<=x and x<=320 and 220<=y and y<=280 and Discard_Data[2]>=1:
          Discard_Data[2] -= 1
          Player_Data[yourturn][1] += 1
          Player_Data[yourturn][2][2] += 1
        if 340<=x and x<=380 and 220<=y and y<=280 and Discard_Data[3]>=1:
          Discard_Data[3] -= 1
          Player_Data[yourturn][1] += 1
          Player_Data[yourturn][2][3] += 1
        if 400<=x and x<=440 and 220<=y and y<=280 and Discard_Data[4]>=1:
          Discard_Data[4] -= 1
          Player_Data[yourturn][1] += 1
          Player_Data[yourturn][2][4] += 1
        if 160<=x and x<=200 and 320<=y and y<=380 and Player_Data[yourturn][2][0]>=1:
          Discard_Data[0] += 1
          Player_Data[yourturn][1] -= 1
          Player_Data[yourturn][2][0] -= 1
        if 220<=x and x<=260 and 320<=y and y<=380 and Player_Data[yourturn][2][1]>=1:
          Discard_Data[1] += 1
          Player_Data[yourturn][1] -= 1
          Player_Data[yourturn][2][1] -= 1
        if 280<=x and x<=320 and 320<=y and y<=380 and Player_Data[yourturn][2][2]>=1:
          Discard_Data[2] += 1
          Player_Data[yourturn][1] -= 1
          Player_Data[yourturn][2][2] -= 1
        if 340<=x and x<=380 and 320<=y and y<=380 and Player_Data[yourturn][2][3]>=1:
          Discard_Data[3] += 1
          Player_Data[yourturn][1] -= 1
          Player_Data[yourturn][2][3] -= 1
        if 400<=x and x<=440 and 320<=y and y<=380 and Player_Data[yourturn][2][4]>=1:
          Discard_Data[4] += 1
          Player_Data[yourturn][1] -= 1
          Player_Data[yourturn][2][4] -= 1
        cld.burst_discard(screen,yourturn,Player_Data,Discard_Data)
        pygame.display.update()
        xx = Discard_Data[0]+Discard_Data[1]+Discard_Data[2]+Discard_Data[3]+Discard_Data[4]
        if xx == int(burst_num):
          msg1 = ""
          msg1 += str(Player_Data[yourturn][2][0])
          msg1 += "/"
          msg1 += str(Player_Data[yourturn][2][1])
          msg1 += "/"     
          msg1 += str(Player_Data[yourturn][2][2])
          msg1 += "/"
          msg1 += str(Player_Data[yourturn][2][3])
          msg1 += "/"
          msg1 += str(Player_Data[yourturn][2][4])
          sock.send("Discard".encode('utf-8'))
          sock.recv(bufsize).decode('utf-8')
          sock.send(str(yourturn).encode('utf-8'))
          sock.recv(bufsize).decode('utf-8')
          sock.send(msg1.encode('utf-8'))
          burst[0] = False
          waiting[0] = True
  
    if burst[0] == False:
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
  if waiting[0]:
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])

  while waiting[0]:
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

    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
      if msg == "BurstEnd":
        Dice7[0] = True
        waiting[0] = False
      if msg == "NoBurst":
        Dice7[0] = False
        waiting[0] = False
          
  if Dice7[0]:
    for j in range(4):
      msg = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      msg_split=msg.split("/")
      Player_Data[j][2][0] = int(msg_split[0])
      Player_Data[j][2][1] = int(msg_split[1])
      Player_Data[j][2][2] = int(msg_split[2])
      Player_Data[j][2][3] = int(msg_split[3])
      Player_Data[j][2][4] = int(msg_split[4])
      Player_Data[j][1] = Player_Data[j][2][0]+Player_Data[j][2][1]+Player_Data[j][2][2]+Player_Data[j][2][3]+Player_Data[j][2][4]
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])

  #####################################
  ###　7が出た時の処理(バースト)(終了) ###
  #####################################

  ################################
  ###　7が出た時の処理(蛮族移動) ###
  ################################
  if bandit[0]:
    while bandit[0]:
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
  
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
        if msg == "Bandit":
          msg1 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          Mapdata_Mass[bandit_pos[0]][2]=0
          Mapdata_Mass[int(msg2)][2]=1
          bandit_pos[0]=int(msg2)
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0]) 
          pygame.display.update() 
          bandit[0]=False
    bandit[0]=True
    while bandit[0]:
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
  
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()
        if msg == "Rob":
          msg1 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          player03 = int(msg1)
          player04 = int(msg2)
          card_num = int(msg3)
          Player_Data[player03][1]-=1
          Player_Data[player03][2][card_num]-=1
          Player_Data[player04][1]+=1
          Player_Data[player04][2][card_num]+=1
          bandit[0]=False
        if msg == "NoRob":
          bandit[0]=False
  #####################################
  ###　7が出た時の処理(蛮族移動)(終了) ###
  #####################################