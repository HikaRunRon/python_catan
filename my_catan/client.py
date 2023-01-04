from __future__ import print_function
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

def main(): #クライアント側
  (w,h)=(600,600)   #ゲーム画面の大きさ(幅600px,高さ600px)
  pygame.init()     #pygameを初期化
  pygame.display.set_mode((w,h),0,32)   #ディスプレイ設定
  screen = pygame.display.get_surface() #作成したディスプレイ情報をscreenが取得
  bg = pygame.image.load("./picture/Setting_Screen/clstr.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #event発生までTrue

  while running: #初期画面(server起動画面)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.key == K_RETURN:
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if 145 <= x and x <= 460 and 350 <= y and y <= 510:
          running = False
  bg = pygame.image.load("./picture/Setting_Screen/setting.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新
  pygame.time.wait(300)
  host = "192.168.11.3" 
  port = 55992         #ポート番号 今回は55992に設定
  bufsize = 4096      #デフォルト4096

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPアドレスと通信プロトコルはIPv4,TCPを採択
  sock.connect((host, port)) #サーバーに接続(host = ホストのIPアドレス、port = ポート番号)
  backlogs = sock.recv(bufsize).decode('utf-8')
  print("backlogs,",backlogs)
  backlog = int(backlogs)
  readfds = set([sock])

  Mapdata_Mass = [[0,0,0,[0,1,2,8,9,10],[153,216]],[0,0,0,[2,3,4,10,11,12],[153,300]],[0,0,0,[4,5,6,12,13,14],[154,384]],[0,0,0,[7,8,9,17,18,19],[226,173]], #資源、サイコロ対応目、盗賊の有無、周囲の６つの頂点番号(const),中心座標(const)
  [0,0,0,[9,10,11,19,20,21],[227,257]],[0,0,0,[11,12,13,21,22,23],[227,342]],[0,0,0,[13,14,15,23,24,25],[227,427]],[0,0,0,[16,17,18,27,28,29],[300,132]],[0,0,0,[18,19,20,29,30,31],[300,216]],
  [0,0,0,[20,21,22,31,32,33],[300,300]],[0,0,0,[22,23,24,33,34,35],[300,385]],[0,0,0,[24,25,26,35,36,37],[300,469]],[0,0,0,[28,29,30,38,39,40],[374,173]],[0,0,0,[30,31,32,40,41,42],[374,258]],
  [0,0,0,[32,33,34,42,43,44],[374,342]],[0,0,0,[34,35,36,44,45,46],[374,427]],[0,0,0,[39,40,41,47,48,49],[447,216]],[0,0,0,[41,42,43,49,50,51],[447,300]],[0,0,0,[43,44,45,51,52,53],[447,385]]]

  Mapdata_Side = [[-1,[0,1],[1,6],[117,195],1],[-1,[1,2],[0,2,7],[117,237],2],[-1,[2,3],[1,3,7],[117,279],1],[-1,[3,4],[2,4,8],[117,321],2],[-1,[4,5],[3,5,8],[117,363],1],[-1,[5,6],[4,9],[117,405],2],[-1,[0,8],[0,10,11],[153,173],0],[-1,[2,10],[1,2,12,13],[153,258],0], #所有者、隣接点(const)、隣接辺(const)、中心座標(const),角度(0,1(120),2(240))
  [-1,[4,12],[3,4,14,15],[153,342],0],[-1,[6,14],[5,16,17],[153,427],0],[-1,[7,8],[6,11,18],[190,153],1],[-1,[8,9],[6,10,12,19],[190,195],2],[-1,[9,10],[7,11,13,19],[190,237],1],[-1,[10,11],[7,12,14,20],[190,279],2],[-1,[11,12],[8,13,15,20],[190,321],1],[-1,[12,13],[8,14,16,21],[190,363],2],
  [-1,[13,14],[9,15,17,21],[190,405],1],[-1,[14,15],[9,16,22],[190,447],2],[-1,[7,17],[10,23,24],[226,132],0],[-1,[9,19],[11,12,25,26],[226,216],0],[-1,[11,21],[13,14,27,28],[226,300],0],[-1,[13,23],[15,16,29,30],[226,384],0],[-1,[15,25],[17,31,32],[226,469],0],[-1,[16,17],[18,24,33],[263,111],1],
  [-1,[17,18],[18,23,25,34],[263,153],2],[-1,[18,19],[19,24,26,34],[263,195],1],[-1,[19,20],[19,25,27,35],[263,237],2],[-1,[20,21],[20,26,28,35],[263,279],1],[-1,[21,22],[20,27,29,36],[263,321],2],[-1,[22,23],[21,28,30,36],[263,363],1],[-1,[23,24],[21,29,31,37],[263,405],2],[-1,[24,25],[22,30,32,37],[263,447],1],
  [-1,[25,26],[22,31,38],[263,489],2],[-1,[16,27],[23,39],[300,90],0],[-1,[18,29],[24,25,40,41],[300,173],0],[-1,[20,31],[26,27,42,43],[300,258],0],[-1,[22,33],[28,29,44,45],[300,342],0],[-1,[24,35],[30,31,46,47],[300,427],0],[-1,[26,37],[32,48],[300,510],0],[-1,[27,28],[33,40,49],[337,111],2],
  [-1,[28,29],[34,39,41,49],[337,153],1],[-1,[29,30],[34,40,42,50],[337,195],2],[-1,[30,31],[35,41,43,50],[337,237],1],[-1,[31,32],[35,42,44,51],[337,279],2],[-1,[32,33],[36,43,45,51],[337,321],1],[-1,[33,34],[36,44,46,52],[337,363],2],[-1,[34,35],[37,45,47,52],[337,405],1],[-1,[35,36],[37,46,48,53],[337,447],2],
  [-1,[36,37],[38,47,53],[337,489],1],[-1,[28,38],[39,40,54],[374,132],0],[-1,[30,40],[41,42,55,56],[374,216],0],[-1,[32,42],[43,44,57,58],[374,300],0],[-1,[34,44],[45,46,59,60],[374,384],0],[-1,[36,46],[47,48,61],[374,469],0],[-1,[38,39],[49,55,62],[410,153],2],[-1,[39,40],[50,54,56,62],[410,195],1],
  [-1,[40,41],[50,55,57,63],[410,237],2],[-1,[41,42],[51,56,58,63],[410,279],1],[-1,[42,43],[51,57,59,64],[410,321],2],[-1,[43,44],[52,58,60,64],[410,363],1],[-1,[44,45],[52,59,61,65],[410,405],2],[-1,[45,46],[53,60,65],[410,447],1],[-1,[39,47],[54,55,66],[447,173],0],[-1,[41,49],[56,57,67,68],[447,258],0],
  [-1,[43,51],[58,59,69,70],[447,342],0],[-1,[45,53],[60,61,71],[447,427],0],[-1,[47,48],[62,67],[483,195],2],[-1,[48,49],[63,66,68],[483,237],1],[-1,[49,50],[63,67,69],[483,279],2],[-1,[50,51],[64,68,70],[483,321],1],[-1,[51,52],[64,69,71],[483,363],2],[-1,[52,53],[65,70],[483,405],1]]

  Mapdata_Edge = [[-1,0,[0,6],[1,8],[128,173]],[-1,0,[0,1],[0,2],[104,216]],[-1,-1,[1,2,7],[1,3,10],[128,258]],[-1,1,[2,3],[2,4],[104,300]],[-1,1,[3,4,8],[3,5,12],[128,342]],[-1,-1,[4,5],[4,6],[104,384]],[-1,-1,[5,9],[5,14],[128,427]],[-1,4,[10,18],[8,17],[202,132]],[-1,-1,[6,10,11],[0,7,9],[177,173]], #所有者と建造物、優位トレード条件所有マス(const)(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),0(3-1),-1(港無し))、隣接辺、隣接点、中心座標(const)
  [-1,-1,[11,12,19],[8,10,19],[202,216]],[-1,-1,[7,12,13],[2,9,11],[177,258]],[-1,-1,[13,14,20],[10,12,21],[202,300]],[-1,-1,[8,14,15],[4,11,13],[177,342]],[-1,-1,[15,16,21],[12,14,23],[202,384]],[-1,-1,[9,16,17],[6,13,15],[177,427]],[-1,0,[17,22],[14,25],[202,469]],[-1,-1,[23,33],[17,27],[275,90]],[-1,4,[18,23,24],[7,16,18],[251,132]],
  [-1,-1,[24,25,34],[17,19,29],[275,173]],[-1,-1,[19,25,26],[9,18,20],[251,216]],[-1,-1,[26,27,35],[19,21,31],[275,258]],[-1,-1,[20,27,28],[11,20,22],[251,300]],[-1,-1,[28,29,36],[21,23,33],[275,342]],[-1,-1,[21,29,30],[13,22,24],[251,384]],[-1,-1,[30,31,37],[23,25,35],[275,427]],[-1,0,[22,31,32],[15,24,26],[251,469]],[-1,-1,[32,38],[25,37],[275,510]],
  [-1,-1,[33,39],[16,28],[325,90]],[-1,5,[39,40,49],[27,29,38],[349,132]],[-1,-1,[34,40,41],[18,28,30],[325,173]],[-1,-1,[41,42,50],[29,31,40],[349,216]],[-1,-1,[35,42,43],[20,30,32],[325,258]],[-1,-1,[43,44,51],[31,33,42],[349,300]],[-1,-1,[36,44,45],[22,32,34],[325,342]],[-1,-1,[45,46,52],[33,35,44],[349,384]],[-1,-1,[37,46,47],[24,34,36],[325,427]],
  [-1,3,[47,48,53],[35,37,46],[349,469]],[-1,-1,[38,48],[26,36],[325,510]],[-1,5,[49,54],[28,39],[398,132]],[-1,-1,[54,55,62],[38,40,47],[423,173]],[-1,-1,[50,55,56],[30,39,41],[398,216]],[-1,-1,[56,57,63],[40,42,49],[423,258]],[-1,-1,[51,57,58],[32,41,43],[398,300]],[-1,-1,[58,59,64],[42,44,51],[423,342]],[-1,-1,[52,59,60],[34,43,45],[398,384]],
  [-1,-1,[60,61,65],[44,46,53],[423,427]],[-1,3,[53,61],[36,45],[398,469]],[-1,0,[62,66],[39,48],[472,173]],[-1,0,[66,67],[47,49],[496,216]],[-1,-1,[63,67,68],[41,48,50],[472,258]],[-1,2,[68,69],[49,51],[496,300]],[-1,2,[64,69,70],[43,50,52],[472,342]],[-1,0,[70,71],[51,53],[496,384]],[-1,0,[65,71],[45,52],[472,427]]]

  Player_Data = [[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,0,0,[0,0,0,0,0,0]]]
  #所持ポイント、所持資源カード合計枚数、所持資源カード枚数内訳(木、レンガ、羊、小麦、石)、所持発展カード合計枚数,その内訳(騎士、街道建設、発見、独占、大聖堂、図書館、市場、議会、大学),残り建設可能開拓地数、残り建設可能都市数、残り建設可能街道数、交易路の長さ、最長交易路の有無、騎士力,最大騎士力の有無、優位トレード所持(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),0(3-1))(所持しているときは1(デフォルト0))

  yourturn = -1 #プレイヤーのターン、後々サーバーから通知が来る。

  with closing(sock):
    running = True
    client_start_setting.client_start_setting(running,sock,readfds,bufsize,backlog,screen) #setting画面

    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新
    pygame.time.wait(500)
    startsign = sock.recv(bufsize).decode('utf-8')
    print("startsign,",startsign)
    if startsign == "STRT":
      if backlog == 3:
        bg = pygame.image.load("./picture/Setting_Screen/start3.jpg").convert_alpha() #背景画像設定
      else:
        bg = pygame.image.load("./picture/Setting_Screen/start4.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新
    pygame.time.wait(2000)
    startmap = sock.recv(bufsize).decode('utf-8')
    print("startmap,",startmap)
    if startmap == "MAPSTART":
      bg = pygame.image.load("./picture/catanmap.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新

    mapmass = []
    mapmassnum = []

    for i in range(19): #初期マップデータ描画,サーバーと同じ
      xx = Mapdata_Mass[i][4][0]
      yy = Mapdata_Mass[i][4][1]
      mapmas = pygame.image.load("./picture/Resource_Tile/desertmap.png").convert_alpha()
      mapmas_rect = mapmas.get_rect()
      mapmas_rect.center = (xx,yy)
      screen.blit(mapmas,mapmas_rect)

      mapmasn = pygame.image.load("./picture/Card_Number/card0.png").convert_alpha()
      mapmasn_rect = mapmasn.get_rect()
      mapmasn_rect.center = (xx,yy)
      screen.blit(mapmasn,mapmasn_rect)

      mapmass.append(mapmas)
      mapmassnum.append(mapmasn)

    land = [0,1,1,1,1,2,2,2,3,3,3,3,4,4,4,4,5,5,5]
    landnumber = [-1 for i in range(19)]

    running = True

    while running:
      pygame.display.update()
      pygame.time.wait(20)
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
        elif msg == "gamestart":
          running = False
    msg = sock.recv(bufsize).decode('utf-8')     #マップデータ受け取り
    sock.send("ok".encode('utf-8'))
    if msg == "mapdata1":
      landdatastr = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      print(landdatastr)
    msg = sock.recv(bufsize).decode('utf-8')
    sock.send("ok".encode('utf-8'))
    if msg == "mapdata2":
      landnumberstr = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      print(landnumberstr)
    msg = sock.recv(bufsize).decode('utf-8')
    sock.send("ok".encode('utf-8'))
    if msg == "mapdata3":
      yourturn = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      yourturn = int(yourturn)
      print(yourturn)
    yourturn  #yourturn 0(白),1(赤),2(青),3(橙)
    if backlog == 3:
      if yourturn == 0:
        leftside = 1
        front = -1
        rightside = 2
      elif yourturn == 1:
        leftside = 2
        front = -1
        rightside = 0
      else:
        leftside = 0
        front = -1
        rightside = 1
    else:
      if yourturn == 0:
        leftside = 1
        front = 2
        rightside = 3
      elif yourturn == 1:
        leftside = 2
        front = 3
        rightside = 0
      elif yourturn == 2:
        leftside = 3
        front = 0
        rightside = 1
      else:
        leftside = 0
        front = 1
        rightside = 2


    land = landdatastr.split('/')
    landnumber = landnumberstr.split('/')
    client_map_display.client_map_display(land,landnumber,Mapdata_Mass,mapmass,mapmassnum,screen) #map描画関数
    bandit_pos = [-1]
    for i in range(19):
      if land[i]==0:
        Mapdata_Mass[i][2] = 1
        bandit_pos[0]=i
      Mapdata_Mass[i][0]=land[i]
      Mapdata_Mass[i][1]=landnumber[i]

    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    pygame.display.update()

    msg = sock.recv(bufsize).decode('utf-8')
    if msg == "firstphasestart":
      sock.send("ok".encode('utf-8'))

    running = True

    myturn = False

    if backlog == 3:
      once = [0,0,0]
    else:
      once = [0,0,0,0]
    
    client_first_phase.client_first_phase(running,myturn,sock,readfds,bufsize,Mapdata_Edge,once,Mapdata_Mass,Player_Data,screen,Mapdata_Side,land,landnumber,backlog,yourturn,rightside,leftside,front)

  ###################################
  ####  　　 ゲーム開始           ####
  ###################################


    running = True
    turn = 0

    while running: #ゲーム本体
      turn += 1
      print(turn)
      Dice1 = [0]
      Dice2 = [0]
      pygame.display.update()
      pygame.time.wait(50)
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
        
        elif msg == "others":
          Playingnumber=sock.recv(bufsize).decode('utf-8')
          Playingnumber = int(Playingnumber)
          sock.send("ok".encode('utf-8'))
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          if Playingnumber==0:
            cld.draw_image(screen,"./picture/Turn_display/WhiteTurn.png",300,300)
          if Playingnumber==1:
            cld.draw_image(screen,"./picture/Turn_display/RedTurn.png",300,300)
          if Playingnumber==2:
            cld.draw_image(screen,"./picture/Turn_display/BlueTurn.png",300,300)
          if Playingnumber==3:
            cld.draw_image(screen,"./picture/Turn_display/OrangeTurn.png",300,300)
          pygame.display.update()
          pygame.time.wait(1500)
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)

        ###################
        ## Start  others ##　
        ###################

          #####################
          ## サイコロフリフリ ##
          #####################

          running1=[True]
          Dice7 = [False]
          burst=[False]
          waiting=[False]
          bandit=[False]
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
          
          if burst[0]:
            before_num = Player_Data[yourturn][1]
            if before_num%2==0:
              burst_num = Player_Data[yourturn][1]/2
            else:
              burst_num = (Player_Data[yourturn][1]+1)/2
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
                x = Discard_Data[0]+Discard_Data[1]+Discard_Data[2]+Discard_Data[3]+Discard_Data[4]
                if x == burst_num:
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

          ################
          ### 本体処理　###
          ################

          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          cld.draw_image(screen,"./picture/frame.png",540,540)
          running1[0] = True

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
              elif msg=="TurnEnd":
                running1[0]=False

              elif msg == "Road":

                #################
                ###  街道建設  ###
                #################
    
                msg1=sock.recv(bufsize).decode(('utf-8')) #操作しているクライアント側からの送信
                sock.send("ok".encode('utf-8'))
                msg2=sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
                msg3=sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
                sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
    
                position = int(msg1)
                player01 = int(msg2)
                road_length = int(msg3)
    
                Mapdata_Side[position][0]=player01
                Player_Data[player01][8] = road_length
                Player_Data[player01][1] -= 2
                Player_Data[player01][2][0] -= 1
                Player_Data[player01][2][1] -= 1
                Player_Data[player01][7] -= 1
                if Player_Data[player01][9]==0 and Player_Data[player01][8]>=5:
                  for j in range(4):
                    if j!=player01:
                      if Player_Data[j][8]<Player_Data[player01][8]:
                        Player_Data[player01][9]=1
                cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                cld.draw_Dice(screen,Dice1[0],Dice2[0])
                cld.draw_image(screen,"./picture/frame.png",540,540)
                pygame.display.update()

                ######################
                ###  街道建設(終了) ###
                ######################

          ######################
          ### 本体処理(終了)　###
          ######################

        ##########################
        ## Start  others(終了)  ##　
        ##########################

        elif msg == "Yourturn": ##ここからocchiiが書いてるよ💛💛★(⋈◍＞◡＜◍)。✧♡★✌
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Turn_display/YourTurn.png",300,300)
          pygame.display.update()
          pygame.time.wait(1500)
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_image(screen,"./picture/Dice/Dice_button.png",540,540)
          

        ############
        ## Myturn ##　
        ############

          #####################
          ## サイコロフリフリ ##
          #####################
          
          running1=[True]
          Dice7=[False]
          burst=[False]
          waiting=[False]
          bandit=[False]
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
          pygame.time.wait(50)
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
          if Dice7[0]:
            cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
            cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            cld.draw_image(screen,"./picture/frame.png",540,540)
            cld.draw_Dice(screen,Dice1[0],Dice2[0])
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
          
          if burst[0]:
            before_num = Player_Data[yourturn][1]
            if before_num%2==0:
              burst_num = Player_Data[yourturn][1]/2
            else:
              burst_num = (Player_Data[yourturn][1]-1)/2
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
                x = Discard_Data[0]+Discard_Data[1]+Discard_Data[2]+Discard_Data[3]+Discard_Data[4]
                if x == burst_num:
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
                if event.type == MOUSEBUTTONDOWN and event.button == 1: #蛮族の場所を選択
                  x, y = event.pos
                  for i in bandit_list:
                    if (Mapdata_Mass[i][4][0]-x)*(Mapdata_Mass[i][4][0]-x)+(Mapdata_Mass[i][4][1]-y)*(Mapdata_Mass[i][4][1]-y)<=500:
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

          ################
          ### 本体処理　###
          ################
          running1[0]=True
          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
          cld.draw_image(screen,"./picture/frame.png",540,540)
          cld.draw_Dice(screen,Dice1[0],Dice2[0])
          cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
          cld.draw_image(screen,"./picture/Action.png",540,60)

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
              if event.type == MOUSEBUTTONDOWN and event.button == 1: #サイコロボタンのクリック
                x, y = event.pos
                if (x-540)*(x-540)+(y-540)*(y-540)<=2500: #枠内左クリックでwhileを抜け、次のページへ
                  sock.send("TurnEnd".encode('utf-8')) #ターンエンド
                  sock.recv(bufsize)
                  sock.send("ok".encode('utf-8'))
                  running1[0]=False #ループから抜ける

                #################
                ###  街道建設  ###
                #################

                if 481<=x and x<=540 and 1<=y and y<=60 and Player_Data[yourturn][2][0]>=1 and Player_Data[yourturn][2][1]>=1 and Player_Data[yourturn][7]>=1: #街道建設

                  road_running = [True]
                  cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                  cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                  cld.draw_image(screen,"./picture/frame.png",540,540)
                  cld.draw_Dice(screen,Dice1[0],Dice2[0])
                  cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
                  cld.draw_image(screen,"./picture/Action.png",540,60)
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
                              Player_Data[yourturn][1] -= 2
                              Player_Data[yourturn][2][0] -= 1
                              Player_Data[yourturn][2][1] -= 1
                              Player_Data[yourturn][7] -= 1
                              if Player_Data[yourturn][9]==0 and Player_Data[yourturn][8]>=5:
                                for j in range(4):
                                  if j!=yourturn:
                                    if Player_Data[j][8]<Player_Data[yourturn][8]:
                                      Player_Data[yourturn][9]=1
                              player_str = str(yourturn)
                              road_length_str = str(road_length)
                              sock.send("Road".encode('utf-8')) #道の情報を送信する
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
                              break

                        if road_running[0]==False:
                          cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                          cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                          cld.draw_image(screen,"./picture/frame.png",540,540)
                          cld.draw_Dice(screen,Dice1[0],Dice2[0])
                          cld.draw_image(screen,"./picture/Turnend_button.png",540,540)
                          cld.draw_image(screen,"./picture/Action.png",540,60)
                          pygame.display.update()

                    if road_running[0] == False:  #サイコロフリフリメッセージ送信後は即ループ脱出
                      break 
        
                    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
                    for sock in rready:                                   #選択された処理を順次遂行
                      msg = sock.recv(bufsize).decode('utf-8')
                      print(msg)
                      sock.send("ok".encode('utf-8'))
                      if msg == "serverdown":
                        pygame.quit()
                        sys.exit()

                ######################
                ###  街道建設(終了) ###
                ######################

                if 541<=x and x<=600 and 1<=y and y<=60: #開拓地建設
                  settlement_running = True
                if 481<=x and x<=540 and 61<=y and y<=120: #都市建設
                  city_running = True
                if 541<=x and x<=600 and 61<=y and y<=120: #発展
                  development_running = True

            if running1[0] == False:  #ターンエンドメッセージ送信後は即ループ脱出
              break 

            rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
            for sock in rready:                                   #選択された処理を順次遂行
              msg = sock.recv(bufsize).decode('utf-8')
              print(msg)
              sock.send("ok".encode('utf-8'))
              if msg == "serverdown":
                pygame.quit()
                sys.exit()

          ######################
          ### 本体処理(終了)　###
          ######################


        ##################
        ## Myturn(終了) ##　
        ##################
          
          
          
  return

if __name__ == '__main__':
  main()
