from __future__ import print_function  ########クライアントの発展アクションを担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import point_calculation as pc
import client_draw as cld
import client_roadroad
import client_knight
import client_discovery
import client_monopoly
def client_development(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,Thisturn_draw,development_running,secretcard_pos,sock,bufsize,Winner,running,running1,Thiturn_development,readfds,bandit_pos):
  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
  cld.draw_image(screen,"./picture/frame.png",540,540)
  cld.draw_Dice(screen,Dice1[0],Dice2[0])
  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
  cld.draw_image(screen,"./picture/Action.png",540,60)
  cld.draw_client_development(screen,Player_Data,yourturn,Thisturn_draw)
  pygame.display.update()
     
  while development_running[0]:
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
        if 541<=x and x<=600 and 61<=y and y<=120: #枠内左クリックでwhileを抜け、次のページへ
          development_running[0]=False #ループから抜ける
        ###################
        ### カードドロー ###
        ###################
        if (x-175)*(x-175)+(y-175)*(y-175) <= 5625 and secretcard_pos[0]<=24 and Player_Data[yourturn][2][2]>=1 and Player_Data[yourturn][2][3]>=1 and Player_Data[yourturn][2][4]>=1:
          sock.send("Card_Draw".encode('utf-8'))
          sock.recv(bufsize).decode('utf-8')
          sock.send(str(yourturn).encode('utf-8'))
          sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
        
          msg = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          if msg == "Card_Draw":
            msg1 = sock.recv(bufsize).decode('utf-8') #誰が
            sock.send("ok".encode('utf-8'))
            msg2 = sock.recv(bufsize).decode('utf-8') #なんのカードを引いたか
            sock.send("ok".encode('utf-8'))
             
            secretcard_pos[0] += 1
            player02 = int(msg1)
            card_num = int(msg2)
            Player_Data[player02][3] += 1
            if card_num >= 4:
              Player_Data[player02][4][card_num] += 1
            else:
              Thisturn_draw[card_num] += 1
            Player_Data[player02][1] -= 3
            Player_Data[player02][2][2] -= 1
            Player_Data[player02][2][3] -= 1
            Player_Data[player02][2][4] -= 1
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
        ########################
        ### カードドロー(終了) ###
        ########################
         
        ############
        ### 騎士 ###
        ############
        if 205<=x and x<=245 and 300<=y and y<=360 and Player_Data[yourturn][4][0]>=1 and Thiturn_development[0]==False:
          Knight = [True]
          Thiturn_development[0]=True
          client_knight.client_knight(Knight,screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,bufsize,bandit_pos,sock,readfds,Winner,running,running1,Thisturn_draw)
        #################
        ### 騎士(終了) ###
        #################
           
        ################
        ### 街道建設 ###
        ################
        if 255<=x and x<=295 and 300<=y and y<=360 and Player_Data[yourturn][4][1]>=1 and Thiturn_development[0]==False and Player_Data[yourturn][7]>=1:
          road_running = [True]
          Thiturn_development[0]=True
          sock.send("roadroad".encode('utf-8'))
          sock.recv(bufsize)
          sock.send(str(yourturn).encode('utf-8'))
          sock.recv(bufsize)
          Player_Data[yourturn][3] -= 1
          Player_Data[yourturn][4][1] -= 1
          client_roadroad.client_roadroad(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,road_running,sock,bufsize,Winner,running1,running,readfds)
          if Player_Data[yourturn][7]>=1:
            road_running[0] = True
          client_roadroad.client_roadroad(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,road_running,sock,bufsize,Winner,running1,running,readfds)
          cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
          cld.draw_image(screen,"./picture/Action.png",540,60)
          cld.draw_client_development(screen,Player_Data,yourturn,Thisturn_draw)
          pygame.display.update()
        #####################
        ### 街道建設(終了) ###
        #####################
          
        ############
        ### 発見 ###
        ############
        if 305<=x and x<=345 and 300<=y and y<=360 and Player_Data[yourturn][4][2]>=1 and Thiturn_development[0]==False:
          Discovery = [True]
          Thiturn_development[0]=True
          Player_Data[yourturn][3] -= 1
          Player_Data[yourturn][4][2] -= 1
          disc_resource = [-1,-1]
          client_discovery.client_discovery(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,Discovery,sock,disc_resource,bufsize,readfds,Thisturn_draw)
        #################
        ### 発見(終了) ###
        #################
          
        ############
        ### 独占 ###
        ############
        if 355<=x and x<=395 and 300<=y and y<=360 and Player_Data[yourturn][4][3]>=1 and Thiturn_development[0]==False:
          Monopoly = [True]
          Thiturn_development[0]=True
          Player_Data[yourturn][3] -= 1
          Player_Data[yourturn][4][3] -= 1
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          Monopoly_list = cld.draw_candidate_choose(screen)
          client_monopoly.client_monopoly(Monopoly,sock,screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Monopoly_list,Dice1,Dice2,bufsize,readfds,Thisturn_draw)   
        #################
        ### 独占(終了) ###
        #################
    if development_running[0] == False:  #サイコロフリフリメッセージ送信後は即ループ脱出
      cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
      cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
      cld.draw_image(screen,"./picture/frame.png",540,540)
      cld.draw_Dice(screen,Dice1[0],Dice2[0])
      cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
      cld.draw_image(screen,"./picture/Action.png",540,60)
      pygame.display.update()
      break 
        
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      sock.send("ok".encode('utf-8'))
      if msg == "serverdown":
        pygame.quit()
        sys.exit()