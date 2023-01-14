from __future__ import print_function           ########クライアント(ターン本人)のサイコロフェーズを担うファイル
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

def client_myturn_dice(running1,sock,bufsize,readfds,Dice1,Dice2,Mapdata_Mass,Mapdata_Edge,Mapdata_Side,Player_Data,Dice7,bandit,screen,land,landnumber,backlog,yourturn,rightside,front,leftside,burst,waiting,bandit_pos,volume):
  Bandit_sound = pygame.mixer.Sound("./music/Bandit.mp3")
  Dice_roll = pygame.mixer.Sound("./music/Dice_roll.mp3")
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
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #サイコロボタンのクリック
        x, y = event.pos
        if (x-540)*(x-540)+(y-540)*(y-540)<=2500: #枠内左クリックでwhileを抜け、次のページへ
          sock.send("Dice".encode('utf-8')) #サイコロを振る
          sock.recv(bufsize)
          sock.send("ok".encode('utf-8'))
          running1[0]=False #ループから抜ける
    
    if running1[0] == False:  #サイコロフリフリメッセージ送信後は即ループ脱出
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
          
  ##データの更新
  pygame.display.update()
  Dice_roll.play()
  sock.recv(bufsize).decode('utf-8')
  sock.send("ok".encode('utf-8'))
  Dice_msg=sock.recv(bufsize).decode('utf-8')
  sock.send("ok".encode('utf-8'))
  print(Dice_msg)
  Dice_nums_str = Dice_msg.split("/")
  Dice1[0] = int(Dice_nums_str[0])
  Dice2[0] = int(Dice_nums_str[1])
  Dicesum = Dice1[0]+Dice2[0]
  if Dicesum != 7:     #7以外の出目の時
    pygame.time.wait(500)
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
    pygame.time.wait(500)
    Dice7[0] = True
    bandit[0] = True
  if Dice7[0]:
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
    cld.draw_image(screen,"./picture/frame.png",540,540)
    cld.draw_Dice(screen,Dice1[0],Dice2[0])
    pygame.display.update()
    Bandit_sound.play()

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
    print("before_burst:",Player_Data[yourturn][1])
    burst_num = Player_Data[yourturn][1]//2
    burst_num = int(burst_num)
    print("after_burst:",burst_num)
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
    bandit_list = cld.draw_candidate_bandit(screen,Mapdata_Mass)
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
          for i in bandit_list:
            if (Mapdata_Mass[i][4][0]-x)*(Mapdata_Mass[i][4][0]-x)+(Mapdata_Mass[i][4][1]-y)*(Mapdata_Mass[i][4][1]-y)<=625:
              Bandit_sound.play()
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
              bandit[0]=False
              break
      if bandit[0]==False:
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
      bandit[0]=False
      sock.send("NoRob".encode('utf-8')) #カード奪取無し
      sock.recv(bufsize)
    else:
      bandit[0]=True #カード奪取あり
    ###############################
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
              bandit[0]=False
              break

      if bandit[0]==False:
        break
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        sock.send("ok".encode('utf-8'))
        if msg == "serverdown":
          pygame.quit()
          sys.exit()

  #####################################
  ###　7が出た時の処理(蛮族移動)(終了) ###
  #####################################