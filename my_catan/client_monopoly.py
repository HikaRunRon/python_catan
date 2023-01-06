from __future__ import print_function    ########クライアントの独占(発展カード)を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
import client_draw as cld
def client_monopoly(Monopoly,sock,screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Monopoly_list,Dice1,Dice2,bufsize,readfds,Thisturn_draw):
  while Monopoly[0]:
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
          if (Monopoly_list[i][0]-x)*(Monopoly_list[i][0]-x)+(Monopoly_list[i][1]-y)*(Monopoly_list[i][1]-y)<=400:
            sum = Player_Data[0][2][i]+Player_Data[1][2][i]+Player_Data[2][2][i]+Player_Data[3][2][i]
            Player_Data[0][1] -= Player_Data[0][2][i]
            Player_Data[1][1] -= Player_Data[1][2][i]
            Player_Data[2][1] -= Player_Data[2][2][i]
            Player_Data[3][1] -= Player_Data[3][2][i]
               
            Player_Data[0][2][i] = 0
            Player_Data[1][2][i] = 0
            Player_Data[2][2][i] = 0
            Player_Data[3][2][i] = 0
            Player_Data[yourturn][1] += sum
            Player_Data[yourturn][2][i] = sum
  
            sock.send("Monopoly".encode('utf-8'))
            sock.recv(bufsize)
            sock.send(str(yourturn).encode('utf-8'))
            sock.recv(bufsize)
            sock.send(str(i).encode('utf-8'))
            sock.recv(bufsize)
       
            cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
            cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            cld.draw_image(screen,"./picture/frame.png",540,540)
            cld.draw_Dice(screen,Dice1[0],Dice2[0])
            cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
            cld.draw_image(screen,"./picture/Action.png",540,60)
            cld.draw_client_development(screen,Player_Data,yourturn,Thisturn_draw)
            pygame.display.update()
       
            Monopoly[0]=False
            break
    if [0]==False:
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()  