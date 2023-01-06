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
import client_start_setting
import client_map_display
import client_first_phase
import client_myturn_dice
import client_others_dice
import point_calculation as pc
import client_road_building
import client_settlement_building
import client_city_building

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

  Player_Data = [[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],3,4,13,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],3,4,13,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],3,4,13,0,0,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],3,4,13,0,0,0,0,[0,0,0,0,0,0]]]
  #所持ポイント、所持資源カード合計枚数、所持資源カード枚数内訳(木、レンガ、羊、小麦、石)、所持発展カード合計枚数,その内訳(騎士、街道建設、発見、独占、大聖堂、図書館、市場、議会、大学),残り建設可能開拓地数、残り建設可能都市数、残り建設可能街道数、交易路の長さ、最長交易路の有無、騎士力,最大騎士力の有無、優位トレード所持(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),0(3-1))(所持しているときは1(デフォルト0))

  yourturn = -1 #プレイヤーのターン、後々サーバーから通知が来る。
  secretcard_pos=[0]

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

    running = [True]

    myturn = [False]

    if backlog == 3:
      once = [0,0,0]
    else:
      once = [0,0,0,0]
    
    client_first_phase.client_first_phase(running,myturn,sock,readfds,bufsize,Mapdata_Edge,once,Mapdata_Mass,Player_Data,screen,Mapdata_Side,land,landnumber,backlog,yourturn,rightside,leftside,front)

  ###################################
  ####  　　 ゲーム開始           ####
  ###################################


    running = [True]
    turn = [0]
    Winner = [-1]

    while running[0]: #ゲーム本体
      turn[0] += 1
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
          client_others_dice.client_others_dice(running1,sock,bufsize,readfds,Dice1,Dice2,Mapdata_Mass,Mapdata_Edge,Mapdata_Side,Player_Data,Dice7,bandit,screen,land,landnumber,backlog,yourturn,rightside,front,leftside,burst,waiting,bandit_pos)
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
              elif msg=="Gameset":
                msg1=sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
                winner = int(msg1)
                Winner[0] = winner
                running1[0]=False
                running[0]=False

              #################
              ###  街道建設  ###
              #################
              elif msg == "Road":
    
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
                  longest_judge = True
                  for j in range(4):
                    if j!=player01:
                      if Player_Data[j][8]>=Player_Data[player01][8]:
                        longest_judge = False
                  if longest_judge:
                    for j in range(4):
                      Player_Data[j][9]=0
                    Player_Data[player01][9]=1
                cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                cld.draw_Dice(screen,Dice1[0],Dice2[0])
                cld.draw_image(screen,"./picture/frame.png",540,540)
                pygame.display.update()

              ######################
              ###  街道建設(終了) ###
              ######################
        
              ###################
              ###  開拓地建設  ###
              ###################
              elif msg == "Settlement":
    
                msg1=sock.recv(bufsize).decode(('utf-8')) #操作しているクライアント側からの送信
                sock.send("ok".encode('utf-8'))
                msg2=sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
    
                position = int(msg1)
                player01 = int(msg2)
    
                Mapdata_Edge[position][0]=player01*2
                Player_Data[player01][1] -= 4
                Player_Data[player01][2][0] -= 1
                Player_Data[player01][2][1] -= 1
                Player_Data[player01][2][2] -= 1
                Player_Data[player01][2][3] -= 1
                Player_Data[player01][5] -= 1
                cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                cld.draw_Dice(screen,Dice1[0],Dice2[0])
                cld.draw_image(screen,"./picture/frame.png",540,540)
                pygame.display.update()
              ########################
              ###  開拓地建設(終了)  ###
              ########################

              #################
              ###  都市建設  ###
              #################
              elif msg == "City":
    
                msg1=sock.recv(bufsize).decode(('utf-8')) #操作しているクライアント側からの送信
                sock.send("ok".encode('utf-8'))
                msg2=sock.recv(bufsize).decode(('utf-8'))
                sock.send("ok".encode('utf-8'))
    
                position = int(msg1)
                player01 = int(msg2)
    
                Mapdata_Edge[position][0]=player01*2+1
                Player_Data[player01][1] -= 5
                Player_Data[player01][2][3] -= 2
                Player_Data[player01][2][4] -= 3
                Player_Data[player01][5] += 1
                Player_Data[player01][6] -= 1
                cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                cld.draw_Dice(screen,Dice1[0],Dice2[0])
                cld.draw_image(screen,"./picture/frame.png",540,540)
                pygame.display.update()
              #######################
              ###  都市建設(終了)  ###
              #######################

              ###################
              ### カードドロー ###
              ###################
              elif msg == "Card_Draw":
                msg1 = sock.recv(bufsize).decode('utf-8') #誰が
                sock.send("ok".encode('utf-8'))
                msg2 = sock.recv(bufsize).decode('utf-8') #なんのカードを引いたか
                sock.send("ok".encode('utf-8'))
    
                secretcard_pos[0] += 1
                player02 = int(msg1)
                Player_Data[player02][3] += 1
                Player_Data[player02][1] -= 3
                Player_Data[player02][2][2] -= 1
                Player_Data[player02][2][3] -= 1
                Player_Data[player02][2][4] -= 1

                cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
                cld.draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
                cld.draw_image(screen,"./picture/frame.png",540,540)
                cld.draw_Dice(screen,Dice1[0],Dice2[0])
                cld.draw_image(screen,"./picture/Action.png",540,60)
                pygame.display.update()

              #########################
              ### カードドロー(終了) ###
              #########################

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
          client_myturn_dice.client_myturn_dice(running1,sock,bufsize,readfds,Dice1,Dice2,Mapdata_Mass,Mapdata_Edge,Mapdata_Side,Player_Data,Dice7,bandit,screen,land,landnumber,backlog,yourturn,rightside,front,leftside,burst,waiting,bandit_pos)
          ################
          ### 本体処理　###
          ################
          running1[0]=True
          Thisturn_draw=[0,0,0,0]
          Thiturn_development=[False]
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

                if 481<=x and x<=540 and 1<=y and y<=60 and Player_Data[yourturn][2][0]>=1 and Player_Data[yourturn][2][1]>=1 and Player_Data[yourturn][7]>=1: #街道建設
                  road_running = [True]
                  #################
                  ###  街道建設  ###
                  #################
                  client_road_building.client_road_building(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,road_running,sock,bufsize,Winner,running1,running,readfds)
                  ######################
                  ###  街道建設(終了) ###
                  ######################

                if 541<=x and x<=600 and 1<=y and y<=60 and Player_Data[yourturn][2][0]>=1 and Player_Data[yourturn][2][1]>=1 and Player_Data[yourturn][2][2]>=1 and Player_Data[yourturn][2][3]>=1 and Player_Data[yourturn][5]>=1: #開拓地建設
                  settlement_running = [True]
                  ###################
                  ###  開拓地建築  ###
                  ###################
                  client_settlement_building.client_settlement_building(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,settlement_running,sock,bufsize,Winner,running1,running,readfds)
                  ########################
                  ###  開拓地建設(終了) ###
                  ########################
                
                if 481<=x and x<=540 and 61<=y and y<=120 and Player_Data[yourturn][2][3]>=2 and Player_Data[yourturn][2][4]>=3 and Player_Data[yourturn][6]>=1 and Player_Data[yourturn][5]<=4: #都市建設
                  city_running = [True]
                  #################
                  ###  都市建築  ###
                  #################
                  client_city_building.client_city_building(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside,Dice1,Dice2,city_running,sock,bufsize,Winner,running,running1,readfds)
                  ######################
                  ###  都市建設(終了) ###
                  ######################
                  
                if 541<=x and x<=600 and 61<=y and y<=120: #発展
                  development_running = [True]
                  ##############
                  ###  発展  ###
                  ##############

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
                        #################
                        ### 騎士(終了) ###
                        #################
                        if 255<=x and x<=295 and 300<=y and y<=360 and Player_Data[yourturn][4][1]>=1 and Thiturn_development[0]==False:
                          Road_building = [True]
                        ################
                        ### 街道建設 ###
                        ################
                        if 255<=x and x<=295 and 300<=y and y<=360 and Player_Data[yourturn][4][1]>=1 and Thiturn_development[0]==False:
                          Road_building = [True]
                        #####################
                        ### 街道建設(終了) ###
                        #####################

                        ############
                        ### 発見 ###
                        ############
                        if 305<=x and x<=345 and 300<=y and y<=360 and Player_Data[yourturn][4][2]>=1 and Thiturn_development[0]==False:
                          Discovery = [True]
                        #################
                        ### 発見(終了) ###
                        #################

                        ############
                        ### 独占 ###
                        ############
                        if 355<=x and x<=395 and 300<=y and y<=360 and Player_Data[yourturn][4][3]>=1 and Thiturn_development[0]==False:
                          Monopoly = [True]
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
                  ##################
                  ###  発展(終了) ###
                  ##################

            if running1[0] == False:  #ターンエンドメッセージ送信後は即ループ脱出
              for j in range(4):
                Player_Data[yourturn][4][j] += Thisturn_draw[j]
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
    #################
    ### ゲーム終了 ###
    #################

    ###############
    ### 終了処理 ###
    ###############
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)

    if Winner[0]==yourturn:
      cld.draw_image(screen,"./picture/Gameset/win.png",300,300)
    else:
      cld.draw_image(screen,"./picture/Gameset/lose.png",300,300)
    
    pygame.display.update()
    pygame.time.wait(2000)
    cld.draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
    
    running[0]=True
    while running[0]: #ゲーム終了
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

if __name__ == '__main__':
  main()