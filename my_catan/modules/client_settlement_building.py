from __future__ import print_function        ########クライアントの開拓地建設を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
from modules import longest_road
import random
from modules import client_draw as cld
from modules import point_calculation as pc
def client_settlement_building(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,settlement_running,sock,bufsize,Winner,running1,running,readfds,volume):

  settlement_sound01 = pygame.mixer.Sound("./music/settlement_sound01.mp3")
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
  cld.draw_image(screen,"./picture/Action.png",540,60)
  cld.draw_image(screen,"./picture/client_trade.png",60,60)
  settlement_candidate = cld.draw_candidate_settlement(screen,yourturn,Mapdata_Edge,Mapdata_Side,1)
  while settlement_running[0]:
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
        if 541<=x and x<=600 and 1<=y and y<=60: #枠内左クリックでwhileを抜け、次のページへ
          settlement_running[0]=False #ループから抜ける
        else:
          for i in settlement_candidate:
            if (Mapdata_Edge[i][4][0]-x)*(Mapdata_Edge[i][4][0]-x)+(Mapdata_Edge[i][4][1]-y)*(Mapdata_Edge[i][4][1]-y)<=500:
              i_str = str(i)
              Mapdata_Edge[i][0]=yourturn*2
              Player_Data[yourturn][1] -= 4
              Player_Data[yourturn][2][0] -= 1
              Player_Data[yourturn][2][1] -= 1
              Player_Data[yourturn][2][2] -= 1
              Player_Data[yourturn][2][3] -= 1
              Player_Data[yourturn][5] -= 1
              trade_judge = Mapdata_Edge[i][1]
              if trade_judge!=-1:
                Player_Data[yourturn][12][trade_judge]=1
              player_str = str(yourturn)
              sock.send("Settlement".encode('utf-8')) #開拓地の情報を送信する
              sock.recv(bufsize)
              sock.send(i_str.encode('utf-8')) #どこに開拓地を置くのか
              sock.recv(bufsize)
              sock.send(player_str.encode('utf-8')) #誰が開拓地を置くのか
              sock.recv(bufsize)           
              settlement_running[0]=False
              settlement_sound01.play()
              pygame.time.wait(800)
              settlement_sound01.play()

              if pc.pointget(Player_Data,yourturn)>=10:
                sock.send("Win".encode('utf-8'))
                sock.recv(bufsize)
                sock.send(str(yourturn).encode('utf-8'))
                sock.recv(bufsize)
                Winner[0]=yourturn
                running1[0]=False
                running[0]=False
              break

        if settlement_running[0]==False:
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
          cld.draw_image(screen,"./picture/Action.png",540,60)
          cld.draw_image(screen,"./picture/client_trade.png",60,60)
          pygame.display.update()

    if settlement_running[0] == False: 
      break 
        
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()