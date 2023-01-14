from __future__ import print_function    ########サーバーのサイコロフェーズを担うファイル
import pygame
from pygame.locals import *
import socket
import select
import sys
from modules import mapgene
import random
from modules import server_draw as svd
def server_dice(running1,clients_socks,bufsize,readfds,Dice1,Dice2,Mapdata_Mass,Mapdata_Edge,Player_Data,Dice7,bandit,screen,Mapdata_Side,land,landnumber,bandit_pos,backlog,Dice7_2):
  while running1[0]:
        
    pygame.display.update()
    pygame.time.wait(50)
    for event in pygame.event.get():  #キーボード操作　または　マウス操作
      if event.type == QUIT:
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
          receiver.recv(bufsize)
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            receiver.recv(bufsize)
          pygame.quit()
          sys.exit()  

    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択

    for sock in rready:                 #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      print(msg)
      if msg == "QUIT":
        sock.close()
        readfds.remove(sock)
        clients_socks.remove(sock)
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
          msg = receiver.recv(bufsize).decode('utf-8')
        pygame.quit()
        sys.exit()
      elif msg == "Dice":
        sock.recv(bufsize)
        Dice1[0]=random.randint(1,6)
        Dice2[0]=random.randint(1,6)
        Dicesum=Dice1[0]+Dice2[0]
        Dice1_str = str(Dice1[0])
        Dice2_str = str(Dice2[0])
        Dice_msg = ""
        Dice_msg += Dice1_str
        Dice_msg += "/"
        Dice_msg += Dice2_str
        for receiver in clients_socks:
          receiver.send("Dice".encode('utf-8'))
          receiver.recv(bufsize)        
          receiver.send(Dice_msg.encode('utf-8'))
          receiver.recv(bufsize)

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
        svd.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
        svd.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
        svd.draw_Dice(screen,Dice1[0],Dice2[0])
        pygame.display.update()
     
  ##########################################################
  ###　サイコロの出目をクライアントから受け取るフェーズ(終了) ###
  ##########################################################

  ################################
  ###　7が出た時の処理(バースト) ###
  ################################
  burst_player_num = 0
  if Dice7[0]:
    for receiver in clients_socks: #バースト処理の開始をクライアントに通知
      receiver.send("Burst".encode('utf-8'))
      receiver.recv(bufsize)

  if Dice7[0]:
    Dice7_2[0] = True
    for i in range(4):
      if Player_Data[i][1]>=8:
        burst_player_num += 1
      
  if burst_player_num==0 and Dice7[0]:
    Dice7[0]=False
    Dice7_2[0]=False
    for receiver in clients_socks: #バースト処理の開始をクライアントに通知
      receiver.send("NoBurst".encode('utf-8'))
      receiver.recv(bufsize)

  while Dice7[0]:
        
    pygame.display.update()
    pygame.time.wait(50)
    for event in pygame.event.get():  #キーボード操作　または　マウス操作
      if event.type == QUIT:
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
          receiver.recv(bufsize)
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            receiver.recv(bufsize)
          pygame.quit()
          sys.exit()  

    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択

    for sock in rready:                 #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      print(msg)
      if msg == "QUIT":
        sock.close()
        readfds.remove(sock)
        clients_socks.remove(sock)
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
          msg = receiver.recv(bufsize).decode('utf-8')
        pygame.quit()
        sys.exit()
      if msg == "Discard":
        msg1 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        msg2 = sock.recv(bufsize).decode('utf-8')
        msg2_split = msg2.split("/")
        Player02 = int(msg1)
        Player_Data[Player02][2][0] = int(msg2_split[0])
        Player_Data[Player02][2][1] = int(msg2_split[1])
        Player_Data[Player02][2][2] = int(msg2_split[2])
        Player_Data[Player02][2][3] = int(msg2_split[3])
        Player_Data[Player02][2][4] = int(msg2_split[4])
        Player_Data[Player02][1] = Player_Data[Player02][2][0]+Player_Data[Player02][2][1]+Player_Data[Player02][2][2]+Player_Data[Player02][2][3]+Player_Data[Player02][2][4]
        burst_player_num -= 1
        if burst_player_num == 0:
          Dice7[0] = False
    
  if Dice7_2[0]:
    Dice7[0] = True
    for receiver in clients_socks:
      receiver.send("BurstEnd".encode('utf-8'))
      receiver.recv(bufsize).decode('utf-8')
    msg0 = str(Player_Data[0][2][0])+"/"+str(Player_Data[0][2][1])+"/"+str(Player_Data[0][2][2])+"/"+str(Player_Data[0][2][3])+"/"+str(Player_Data[0][2][4])
    msg1 = str(Player_Data[1][2][0])+"/"+str(Player_Data[1][2][1])+"/"+str(Player_Data[1][2][2])+"/"+str(Player_Data[1][2][3])+"/"+str(Player_Data[1][2][4])
    msg2 = str(Player_Data[2][2][0])+"/"+str(Player_Data[2][2][1])+"/"+str(Player_Data[2][2][2])+"/"+str(Player_Data[2][2][3])+"/"+str(Player_Data[2][2][4])
    msg3 = str(Player_Data[3][2][0])+"/"+str(Player_Data[3][2][1])+"/"+str(Player_Data[3][2][2])+"/"+str(Player_Data[3][2][3])+"/"+str(Player_Data[3][2][4])
    for receiver in clients_socks:
      receiver.send(msg0.encode('utf-8'))
      receiver.recv(bufsize).decode('utf-8')
      receiver.send(msg1.encode('utf-8'))
      receiver.recv(bufsize).decode('utf-8')
      receiver.send(msg2.encode('utf-8'))
      receiver.recv(bufsize).decode('utf-8')
      receiver.send(msg3.encode('utf-8'))
      receiver.recv(bufsize).decode('utf-8')


  #####################################
  ###　7が出た時の処理(バースト)(終了) ###
  ####################################
  ################################
  ###　7が出た時の処理(蛮族移動) ###
  ################################

  if bandit[0]:
    while bandit[0]:
      pygame.display.update()
      pygame.time.wait(50)
      for event in pygame.event.get():  #キーボード操作　または　マウス操作
        if event.type == QUIT:
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            receiver.recv(bufsize)
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            for receiver in clients_socks:
              receiver.send("serverdown".encode('utf-8'))
              receiver.recv(bufsize)
            pygame.quit()
            sys.exit()    
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
  
      for sock in rready:                 #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        print(msg)
        if msg == "QUIT":
          sock.close()
          readfds.remove(sock)
          clients_socks.remove(sock)
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            msg = receiver.recv(bufsize).decode('utf-8')
          pygame.quit()
          sys.exit()
        if msg == "Bandit":
          msg1 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          for receiver in clients_socks:
            if receiver!=sock:
              receiver.send(msg.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
              receiver.send(msg1.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
              receiver.send(msg2.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
          Mapdata_Mass[bandit_pos[0]][2]=0
          Mapdata_Mass[int(msg2)][2]=1
          bandit_pos[0]=int(msg2)
          svd.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
          svd.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          svd.draw_image(screen,"./picture/frame.png",540,540)
          svd.draw_Dice(screen,Dice1[0],Dice2[0]) 
          pygame.display.update()
          bandit[0]=False
    bandit[0]=True
    while bandit[0]:
      pygame.display.update()
      pygame.time.wait(50)
      for event in pygame.event.get():  #キーボード操作　または　マウス操作
        if event.type == QUIT:
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            receiver.recv(bufsize)
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            for receiver in clients_socks:
              receiver.send("serverdown".encode('utf-8'))
              receiver.recv(bufsize)
            pygame.quit()
            sys.exit()  

      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
  
      for sock in rready:                 #選択された処理を順次遂行
        msg = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        print("rob:",msg)
        if msg == "QUIT":
          sock.close()
          readfds.remove(sock)
          clients_socks.remove(sock)
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
            msg = receiver.recv(bufsize).decode('utf-8')
          pygame.quit()
          sys.exit()
        if msg == "Rob":
          msg1 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          for receiver in clients_socks:
            if receiver!=sock:
              receiver.send(msg.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
              receiver.send(msg1.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
              receiver.send(msg2.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
              receiver.send(msg3.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
          player03 = int(msg1)
          player04 = int(msg2)
          card_num = int(msg3)
          Player_Data[player03][1]-=1
          Player_Data[player03][2][card_num]-=1
          Player_Data[player04][1]+=1
          Player_Data[player04][2][card_num]+=1
          bandit[0]=False
        if msg == "NoRob":
          for receiver in clients_socks:
            if receiver!=sock:
              receiver.send(msg.encode('utf-8'))
              receiver.recv(bufsize).decode('utf-8')
          bandit[0]=False
                

  #####################################
  ###　7が出た時の処理(蛮族移動)(終了) ###
  #####################################