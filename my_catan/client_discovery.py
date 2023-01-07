from __future__ import print_function    ########クライアントの発見(発展カード)を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
import client_draw as cld
import point_calculation as pc
def client_discovery(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,Discovery,sock,disc_resource,bufsize,readfds,Thisturn_draw):
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  Discovery_list = cld.draw_candidate_choose(screen)
  while Discovery[0]:
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
        for i in range(5):
          if (Discovery_list[i][0]-x)*(Discovery_list[i][0]-x)+(Discovery_list[i][1]-y)*(Discovery_list[i][1]-y)<=400:
            disc_resource[0]=i
            Player_Data[yourturn][1] +=1
            Player_Data[yourturn][2][i] += 1
            cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
            cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            cld.draw_image(screen,"./picture/frame.png",540,540)
            cld.draw_Dice(screen,Dice1[0],Dice2[0])
            Discovery[0]=False
            break
    if Discovery[0]==False:
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
  Discovery = [True]
  Discovery_list = cld.draw_candidate_choose(screen)
  while Discovery[0]:
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
        for i in range(5):
          if (Discovery_list[i][0]-x)*(Discovery_list[i][0]-x)+(Discovery_list[i][1]-y)*(Discovery_list[i][1]-y)<=400:
            disc_resource[1]=i
            Player_Data[yourturn][1] +=1
            Player_Data[yourturn][2][i] += 1
            cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
            cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            cld.draw_image(screen,"./picture/frame.png",540,540)
            cld.draw_Dice(screen,Dice1[0],Dice2[0])
            cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
            cld.draw_image(screen,"./picture/Action.png",540,60)
            cld.draw_image(screen,"./picture/client_trade.png",60,60)
            cld.draw_client_development(screen,Player_Data,yourturn,Thisturn_draw)
            pygame.display.update()
            Discovery[0]=False
            break
    if Discovery[0]==False:
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()
  sock.send("Discovery".encode('utf-8'))
  sock.recv(bufsize)
  sock.send(str(yourturn).encode('utf-8'))
  sock.recv(bufsize)
  sock.send(str(disc_resource[0]).encode('utf-8'))
  sock.recv(bufsize)
  sock.send(str(disc_resource[1]).encode('utf-8'))
  sock.recv(bufsize)