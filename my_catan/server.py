from __future__ import print_function
import pygame
from pygame.locals import *
import socket
import select
import sys
import mapgene
import random

def draw_image(screen,image,x,y): #画像(image)を座標(x,y)に描画
  im = pygame.image.load(image).convert_alpha()
  im_rect = im.get_rect()
  im_rect.center = (x,y)
  screen.blit(im,im_rect)

def draw_Dice(screen,a,b):
  if a == 1:
    draw_image(screen,"./picture/Dice/Dice1.png",35,560)
  if a == 2:
    draw_image(screen,"./picture/Dice/Dice2.png",35,560)
  if a == 3:
    draw_image(screen,"./picture/Dice/Dice3.png",35,560)
  if a == 4:
    draw_image(screen,"./picture/Dice/Dice4.png",35,560)
  if a == 5:
    draw_image(screen,"./picture/Dice/Dice5.png",35,560)
  if a == 6:
    draw_image(screen,"./picture/Dice/Dice6.png",35,560)
  if b == 1:
    draw_image(screen,"./picture/Dice/Dice1.png",85,560)
  if b == 2:
    draw_image(screen,"./picture/Dice/Dice2.png",85,560)
  if b == 3:
    draw_image(screen,"./picture/Dice/Dice3.png",85,560)
  if b == 4:
    draw_image(screen,"./picture/Dice/Dice4.png",85,560)
  if b == 5:
    draw_image(screen,"./picture/Dice/Dice5.png",85,560)
  if b == 6:
    draw_image(screen,"./picture/Dice/Dice6.png",85,560)

def select_num_image(x):  #数字　→　対応する画像
  if x == 0:
    return "./picture/Card_Number/card0.png"
  elif x == 1:
    return "./picture/Card_Number/card1.png"
  elif x == 2:
    return "./picture/Card_Number/card2.png"
  elif x == 3:
    return "./picture/Card_Number/card3.png"
  elif x == 4:
    return "./picture/Card_Number/card4.png"
  elif x == 5:
    return "./picture/Card_Number/card5.png"
  elif x == 6:
    return "./picture/Card_Number/card6.png"
  elif x == 7:
    return "./picture/Card_Number/card7.png"
  elif x == 8:
    return "./picture/Card_Number/card8.png"
  elif x == 9:
    return "./picture/Card_Number/card9.png"
  elif x == 10:
    return "./picture/Card_Number/card10.png"
  elif x == 11:
    return "./picture/Card_Number/card11.png"
  elif x == 12:
    return "./picture/Card_Number/card12.png"
  elif x == 13:
    return "./picture/Card_Number/card13.png"
  elif x == 14:
    return "./picture/Card_Number/card14.png"
  elif x == 15:
    return "./picture/Card_Number/card15.png"
  elif x == 16:
    return "./picture/Card_Number/card16.png"
  elif x == 17:
    return "./picture/Card_Number/card17.png"
  elif x == 18:
    return "./picture/Card_Number/card18.png"
  elif x == 19:
    return "./picture/Card_Number/card19.png"
  elif x == 20:
    return "./picture/Card_Number/card20.png"
  elif x == 21:
    return "./picture/Card_Number/card21.png"
  elif x == 22:
    return "./picture/Card_Number/card22.png"
  elif x == 23:
    return "./picture/Card_Number/card23.png"
  elif x == 24:
    return "./picture/Card_Number/card24.png"
  elif x == 25:
    return "./picture/Card_Number/card25.png"
  elif x >= 26:
    return "./picture/Card_Number/card25+.png"
  else:
    return "./picture/space5050.png"


def draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog): #現在のマップ状況を全て表示する関数
  bg = pygame.image.load("./picture/catanmap.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新
  for i in range(19): #それぞれのマスに対して描画開始
    xx = Mapdata_Mass[i][4][0]
    yy = Mapdata_Mass[i][4][1]
    l = land[i]
    n = landnumber[i]
    if l == 0: #資源描画
      mapmas = pygame.image.load("./picture/Resource_Tile/desertmap.png").convert_alpha()
    elif l == 1:
      mapmas = pygame.image.load("./picture/Resource_Tile/woodmap.png").convert_alpha()
    elif l == 2:
      mapmas = pygame.image.load("./picture/Resource_Tile/brickmap.png").convert_alpha()
    elif l == 3:
      mapmas = pygame.image.load("./picture/Resource_Tile/sheepmap.png").convert_alpha()             
    elif l == 4:
      mapmas = pygame.image.load("./picture/Resource_Tile/wheatmap.png").convert_alpha()
    else:
      mapmas = pygame.image.load("./picture/Resource_Tile/oremap.png").convert_alpha()
    mapmas_rect = mapmas.get_rect()
    mapmas_rect.center = (xx,yy)
    screen.blit(mapmas,mapmas_rect)
    if n == 2: #数字描画
      mapmasn = pygame.image.load("./picture/Tile_Number/mass2.png").convert_alpha()
    elif n == 3:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass3.png").convert_alpha()
    elif n == 4:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass4.png").convert_alpha()
    elif n == 5:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass5.png").convert_alpha()             
    elif n == 6:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass6.png").convert_alpha()
    elif n == 8:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass8.png").convert_alpha()
    elif n == 9:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass9.png").convert_alpha()
    elif n == 10:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass10.png").convert_alpha()             
    elif n == 11:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass11.png").convert_alpha()
    elif n == 12:
      mapmasn = pygame.image.load("./picture/Tile_Number/mass12.png").convert_alpha()
    else:
      mapmasn = pygame.image.load("./picture/space5050.png").convert_alpha()
    mapmasn_rect = mapmasn.get_rect()
    mapmasn_rect.center = (xx,yy)
    screen.blit(mapmasn,mapmasn_rect)
  if backlog == 3:
    draw_image(screen,"./picture/Background/back_white.png",300,560)
    draw_image(screen,"./picture/Background/back_red2.png",40,300)
    draw_image(screen,"./picture/Background/back_blue2.png",560,300)
  else:
    draw_image(screen,"./picture/Background/back_white.png",300,560)
    draw_image(screen,"./picture/Background/back_red2.png",40,300)
    draw_image(screen,"./picture/Background/back_blue.png",300,40)
    draw_image(screen,"./picture/Background/back_orange2.png",560,300)

  draw_image(screen,"./picture/Resource_Card/woodcard.png",150,560)
  draw_image(screen,"./picture/Resource_Card/brickcard.png",210,560)
  draw_image(screen,"./picture/Resource_Card/sheepcard.png",270,560)
  draw_image(screen,"./picture/Resource_Card/wheatcard.png",330,560)
  draw_image(screen,"./picture/Resource_Card/orecard.png",390,560)
  draw_image(screen,"./picture/Resource_Card/secretcard.png",450,560)

  draw_image(screen,"./picture/Resource_Card/woodcard2.png",40,150)
  draw_image(screen,"./picture/Resource_Card/brickcard2.png",40,210)
  draw_image(screen,"./picture/Resource_Card/sheepcard2.png",40,270)
  draw_image(screen,"./picture/Resource_Card/wheatcard2.png",40,330)
  draw_image(screen,"./picture/Resource_Card/orecard2.png",40,390)
  draw_image(screen,"./picture/Resource_Card/secretcard2.png",40,450)

  draw_image(screen,"./picture/Resource_Card/woodcard2.png",560,450)
  draw_image(screen,"./picture/Resource_Card/brickcard2.png",560,390)
  draw_image(screen,"./picture/Resource_Card/sheepcard2.png",560,330)
  draw_image(screen,"./picture/Resource_Card/wheatcard2.png",560,270)
  draw_image(screen,"./picture/Resource_Card/orecard2.png",560,210)
  draw_image(screen,"./picture/Resource_Card/secretcard2.png",560,150)

  if backlog == 4:
    draw_image(screen,"./picture/Resource_Card/woodcard.png",450,40)
    draw_image(screen,"./picture/Resource_Card/brickcard.png",390,40)
    draw_image(screen,"./picture/Resource_Card/sheepcard.png",330,40)
    draw_image(screen,"./picture/Resource_Card/wheatcard.png",270,40)
    draw_image(screen,"./picture/Resource_Card/orecard.png",210,40)
    draw_image(screen,"./picture/Resource_Card/secretcard.png",150,40)

  draw_image(screen,select_num_image(Player_Data[0][2][0]),150,560)
  draw_image(screen,select_num_image(Player_Data[0][2][1]),210,560)
  draw_image(screen,select_num_image(Player_Data[0][2][2]),270,560)
  draw_image(screen,select_num_image(Player_Data[0][2][3]),330,560)
  draw_image(screen,select_num_image(Player_Data[0][2][4]),390,560)
  draw_image(screen,select_num_image(Player_Data[0][3]),450,560)

  draw_image(screen,select_num_image(Player_Data[1][2][0]),40,150)
  draw_image(screen,select_num_image(Player_Data[1][2][1]),40,210)
  draw_image(screen,select_num_image(Player_Data[1][2][2]),40,270)
  draw_image(screen,select_num_image(Player_Data[1][2][3]),40,330)
  draw_image(screen,select_num_image(Player_Data[1][2][4]),40,390)
  draw_image(screen,select_num_image(Player_Data[1][3]),40,450)

  if backlog == 3:
    draw_image(screen,select_num_image(Player_Data[2][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[2][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[2][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[2][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[2][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[2][3]),560,150)
  else:
    draw_image(screen,select_num_image(Player_Data[2][2][0]),450,40)
    draw_image(screen,select_num_image(Player_Data[2][2][1]),390,40)
    draw_image(screen,select_num_image(Player_Data[2][2][2]),330,40)
    draw_image(screen,select_num_image(Player_Data[2][2][3]),270,40)
    draw_image(screen,select_num_image(Player_Data[2][2][4]),210,40)
    draw_image(screen,select_num_image(Player_Data[2][3]),150,40)

    draw_image(screen,select_num_image(Player_Data[3][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[3][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[3][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[3][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[3][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[3][3]),560,150)
  for i in range(19):
    if Mapdata_Mass[i][2]==1:
      draw_image(screen,"./picture/Tile_Number/bandit.png",Mapdata_Mass[i][4][0],Mapdata_Mass[i][4][1])
  for i in range(72):
    if Mapdata_Side[i][0]==-1:
      continue
    elif Mapdata_Side[i][0]==0:
      if Mapdata_Side[i][4]==0:
        draw_image(screen,"./picture/Building/road_white_0.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      elif Mapdata_Side[i][4]==1:
        draw_image(screen,"./picture/Building/road_white_120.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      else:
        draw_image(screen,"./picture/Building/road_white_240.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
    elif Mapdata_Side[i][0]==1:
      if Mapdata_Side[i][4]==0:
        draw_image(screen,"./picture/Building/road_red_0.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      elif Mapdata_Side[i][4]==1:
        draw_image(screen,"./picture/Building/road_red_120.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      else:
        draw_image(screen,"./picture/Building/road_red_240.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
    elif Mapdata_Side[i][0]==2:
      if Mapdata_Side[i][4]==0:
        draw_image(screen,"./picture/Building/road_blue_0.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      elif Mapdata_Side[i][4]==1:
        draw_image(screen,"./picture/Building/road_blue_120.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      else:
        draw_image(screen,"./picture/Building/road_blue_240.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
    else:
      if Mapdata_Side[i][4]==0:
        draw_image(screen,"./picture/Building/road_orange_0.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      elif Mapdata_Side[i][4]==1:
        draw_image(screen,"./picture/Building/road_orange_120.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      else:
        draw_image(screen,"./picture/Building/road_orange_240.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
  for i in range(54):
    if Mapdata_Edge[i][0]==-1:
      continue
    elif Mapdata_Edge[i][0]==0:
      draw_image(screen,"./picture/Building/settlement_white.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==1:
      draw_image(screen,"./picture/Building/city_white.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==2:
      draw_image(screen,"./picture/Building/settlement_red.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==3:
      draw_image(screen,"./picture/Building/city_red.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==4:
      draw_image(screen,"./picture/Building/settlement_blue.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==5:
      draw_image(screen,"./picture/Building/city_blue.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    elif Mapdata_Edge[i][0]==6:
      draw_image(screen,"./picture/Building/settlement_orange.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
    else:
      draw_image(screen,"./picture/Building/city_orange.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])


def main(): #サーバー側
  print(socket.gethostbyname(socket.gethostname()))
  (w,h)=(600,600)   #ゲーム画面の大きさ(幅600px,高さ600px)
  pygame.init()     #pygameを初期化
  pygame.display.set_mode((w,h),0,32)   #ディスプレイ設定
  screen = pygame.display.get_surface() #作成したディスプレイ情報をscreenが取得
  bg = pygame.image.load("./picture/Setting_Screen/svstr.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #while続行bool

  while running: #初期画面(server起動画面)
    pygame.time.wait(50) #20fps(50ms(0.05秒間)に一回に入出力を制限)

    for event in pygame.event.get(): #何か入力があった場合、その入力に対して処理を行う。
      if event.type == QUIT: #ウィンドウ右上の×がクリックされた時、pygameを閉じ、プログラムそのものも終了。
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN: #キー入力
        if event.key == K_ESCAPE: #escapeキーが押された場合も上記と同様の終了。
          pygame.quit()
          sys.exit()
        if event.key == K_RETURN: #Enterキーが押された場合、whileを抜け、次のページへ
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #マウス入力、右クリック
        x, y = event.pos
        if 110 <= x and x <= 490 and 330 <= y and y <= 485: #枠内左クリックでwhileを抜け、次のページへ
          running = False

  bg = pygame.image.load("./picture/Setting_Screen/svstr2.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

  backlog = 0  #接続可能クライアント数(初期値0)

  running = True #while続行bool

  while running: #プレイヤー数選択画面
    pygame.time.wait(50) #20fps

    for event in pygame.event.get(): #上記同様↓
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()                 #ここまで↑
        if event.key == K_3: #キーボード3が押されたとき、3playerとしてゲーム開始
          backlog = 3
          running = False
        if event.key == K_4: #キーボード4が押されたとき、4playerとしてゲーム開始
          backlog = 4
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #右クリ
        x, y = event.pos
        if 50 <= x and x <= 280 and 190 <= y and y <= 435: #3player枠内判定
          backlog = 3
          running = False
        if 320 <= x and x <= 550 and 190 <= y and y <= 435: #4player枠内判定
          backlog = 4
          running = False

  bg = pygame.image.load("./picture/Setting_Screen/setting.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

  backlogs = str(backlog)      
  #backlog(int型)をstr型にしたものbacklogsを作成。backlog = プレイヤー数なので、そのデータを後々clientアカウントに送りつける。
  #そのためにstr化したものを作成。

  host = "0.0.0.0"   #ホスト(server)のIPアドレス、今回は俺のPC、状況によって変更可能
  port = 55992                #ポート番号 今回は55992に設定
  bufsize = 4096               #デフォルト4096

  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPアドレスと通信プロトコルはIPv4,TCPを採択                                    #処理候補にサーバーソケットを追加
  clients_socks = []                   #人数分のクライアントを格納するためのリスト
  readfds = set([server_sock])         #処理候補(socket)を格納したset、後々select関数にぶち込む為だけに作成
  server_sock.bind((host, port))       #ソケットをアドレスに結び付ける(IPアドレス = host , ポート番号 = port)
  server_sock.listen(backlog)          #入力された接続可能クライアント数を設定(今回は3or4)

  pygame.time.wait(500)                #意味のない0.5秒間、それっぽさ演出。

  if backlog == 3: #3playerの時、それ用の待機画面画像をセット
    bg = pygame.image.load("./picture/Setting_Screen/0-3.jpg").convert_alpha() #背景画像設定
  else:            #4playerの時も、それ用の待機画面画像をセット
    bg = pygame.image.load("./picture/Setting_Screen/0-4.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #while続行bool

  while running: #プレイヤー待機画面
    pygame.display.update() #ディスプレイ更新
    pygame.time.wait(50)
    for event in pygame.event.get():
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
    for sock in rready:                                   #選択された処理を順次遂行
      if sock is server_sock: #サーバー(ホスト)に対する処理の時
        conn, address = server_sock.accept() #サーバーがクライアントの情報を受け取る(connは新しいソケットオブジェクト、addressはクライアントのアドレス)
        readfds.add(conn)                    #新しく処理候補にクライアントのソケットを登録する
        clients_socks.append(conn)
        conn.send(backlogs.encode('utf-8'))
        connections = len(clients_socks)
        c = str(connections)
        for receiver in clients_socks:
          receiver.send("plwt".encode('utf-8'))
          msg = receiver.recv(bufsize).decode('utf-8')
          receiver.send(c.encode('utf-8'))

        if backlog == 3:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-3.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-3.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-3.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/3-3.jpg").convert_alpha() #背景画像設定
            running = False
        else:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-4.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-4.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-4.jpg").convert_alpha() #背景画像設定
          elif connections == 3:
            bg = pygame.image.load("./picture/Setting_Screen/3-4.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/4-4.jpg").convert_alpha() #背景画像設定
            running = False
        rect_bg = bg.get_rect() #背景画像の大きさを取得
        screen.blit(bg,rect_bg) #背景描画
      else:
        msg = sock.recv(bufsize).decode('utf-8')
        print(msg)
        if msg == "QUIT":
          sock.close()
          readfds.remove(sock)
          clients_socks.remove(sock)
        connections = len(clients_socks)
        c = str(connections)
        for receiver in clients_socks:
          receiver.send("plwt".encode('utf-8'))
          msg = receiver.recv(bufsize).decode('utf-8')
          receiver.send(c.encode('utf-8'))

        if backlog == 3:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-3.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-3.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-3.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/3-3.jpg").convert_alpha() #背景画像設定
            running = False
        else:
          if connections == 0:
            bg = pygame.image.load("./picture/Setting_Screen/0-4.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            bg = pygame.image.load("./picture/Setting_Screen/1-4.jpg").convert_alpha() #背景画像設定
          elif connections == 2:
            bg = pygame.image.load("./picture/Setting_Screen/2-4.jpg").convert_alpha() #背景画像設定
          elif connections == 3:
            bg = pygame.image.load("./picture/Setting_Screen/3-4.jpg").convert_alpha() #背景画像設定
          else:
            bg = pygame.image.load("./picture/Setting_Screen/4-4.jpg").convert_alpha() #背景画像設定
            running = False
        rect_bg = bg.get_rect() #背景画像の大きさを取得
        screen.blit(bg,rect_bg) #背景描画

  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新
  pygame.time.wait(500)
  for receiver in clients_socks:
    receiver.send("STRT".encode('utf-8'))
  if backlog == 3:
    bg = pygame.image.load("./picture/Setting_Screen/start3.jpg").convert_alpha() #背景画像設定
  else:
    bg = pygame.image.load("./picture/Setting_Screen/start4.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新
  pygame.time.wait(2000)
  for receiver in clients_socks:
    receiver.send("MAPSTART".encode('utf-8'))
  bg = pygame.image.load("./picture/catanmap.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

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

  Player_Data = [[2,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[2,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[2,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[2,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]]]
  #所持ポイント、所持資源カード合計枚数、所持資源カード枚数内訳(木、レンガ、羊、小麦、石)、所持発展カード合計枚数,その内訳(騎士、街道建設、発見、独占、大聖堂、図書館、市場、議会、大学),残り建設可能開拓地数、残り建設可能都市数、残り建設可能街道数、交易路の長さ、騎士力,優位トレード所持(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),0(3-1))(所持しているときは1(デフォルト0))

  secretcard=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,3,3,4,5,6,7,8] #発展カード順番決め(騎士14、街道建設2、発見2、独占2、大聖堂1、図書館1、市場1、議会1、大学1)
  random.shuffle(secretcard)

  random.shuffle(clients_socks) #ここでシャッフルされたものがそのままプレイヤーの順番になる。

  mapmass = [] #画像のオブジェクトを格納するリスト（最終的には19個の要素が入る）
  mapmassnum = [] #画像のオブジェクトを格納するリスト（最終的には19個の要素が入る）

  for i in range(19): #初期マップデータ描画、「砂漠の上に０」
    xx = Mapdata_Mass[i][4][0] #マスのx座標
    yy = Mapdata_Mass[i][4][1] #マスのy座標
    mapmas = pygame.image.load("./picture/Resource_Tile/desertmap.png").convert_alpha() #資源の画像を描画
    mapmas_rect = mapmas.get_rect()
    mapmas_rect.center = (xx,yy) #座標(xx,yy)に描画
    screen.blit(mapmas,mapmas_rect)

    mapmasn = pygame.image.load("./picture/Card_Number/card0.png").convert_alpha() #資源の上に数字を描画
    mapmasn_rect = mapmasn.get_rect()
    mapmasn_rect.center = (xx,yy) #座標(xx,yy)に描画
    screen.blit(mapmasn,mapmasn_rect)

    mapmass.append(mapmas) #格納
    mapmassnum.append(mapmasn) #格納

  mapgenebutton = pygame.image.load("./picture/mapgene.png").convert_alpha() #Mapgenerateボタンを画面左下に描画
  mapgenebutton_rect = mapgenebutton.get_rect()
  mapgenebutton_rect.center = (90,510)
  screen.blit(mapgenebutton,mapgenebutton_rect)
  gamestbutton = pygame.image.load("./picture/space150150.png").convert_alpha() #ゲームスタートボタンを描画
  gamestbutton_rect = mapgenebutton.get_rect()
  gamestbutton_rect.center = (510,510)
  screen.blit(gamestbutton,gamestbutton_rect)

  land = [0,1,1,1,1,2,2,2,3,3,3,3,4,4,4,4,5,5,5] #マップデータ(資源の種類)を格納するためのリスト
  landnumber = [-1 for i in range(19)] #マップデータ(資源上の数字)を格納するためのリスト

  mapmade = False
  running = True

  while running: #map自動生成
    pygame.display.update()
    pygame.time.wait(50)
    for event in pygame.event.get():
      if event.type == QUIT:
        for receiver in clients_socks: #サーバーを消すときはクライアントも道連れ
          receiver.send("serverdown".encode('utf-8'))
          receiver.recv(bufsize)
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          for receiver in clients_socks: #サーバーを消すときはクライアントも道連れ
            receiver.send("serverdown".encode('utf-8'))
            receiver.recv(bufsize)
          pygame.quit()
          sys.exit()
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #右クリ
        x, y = event.pos
        print(x,y)
        if (x-90)*(x-90)+(y-510)*(y-510) <= 5625: #Mapgene枠内判定
          land = mapgene.landform()
          landnumber = mapgene.numberform(land)
          gamestbutton = pygame.image.load("./picture/gamestart.png").convert_alpha() #ゲームスタートボタンを描画
          gamestbutton_rect = mapgenebutton.get_rect()
          gamestbutton_rect.center = (510,510)
          screen.blit(gamestbutton,gamestbutton_rect)
          mapmade = True
          for i in range(19): #それぞれのマスに対して描画開始
            xx = Mapdata_Mass[i][4][0]
            yy = Mapdata_Mass[i][4][1]
            mapmas = mapmass[i]
            mapmasn = mapmassnum[i]
            l = land[i]
            n = landnumber[i]
            if l == 0: #資源描画
              mapmas = pygame.image.load("./picture/Resource_Tile/desertmap.png").convert_alpha()
            elif l == 1:
              mapmas = pygame.image.load("./picture/Resource_Tile/woodmap.png").convert_alpha()
            elif l == 2:
              mapmas = pygame.image.load("./picture/Resource_Tile/brickmap.png").convert_alpha()
            elif l == 3:
              mapmas = pygame.image.load("./picture/Resource_Tile/sheepmap.png").convert_alpha()             
            elif l == 4:
              mapmas = pygame.image.load("./picture/Resource_Tile/wheatmap.png").convert_alpha()
            else:
              mapmas = pygame.image.load("./picture/Resource_Tile/oremap.png").convert_alpha()
            mapmas_rect = mapmas.get_rect()
            mapmas_rect.center = (xx,yy)
            screen.blit(mapmas,mapmas_rect)
            if n == 2: #数字描画
              mapmasn = pygame.image.load("./picture/Tile_Number/mass2.png").convert_alpha()
            elif n == 3:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass3.png").convert_alpha()
            elif n == 4:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass4.png").convert_alpha()
            elif n == 5:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass5.png").convert_alpha()             
            elif n == 6:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass6.png").convert_alpha()
            elif n == 8:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass8.png").convert_alpha()
            elif n == 9:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass9.png").convert_alpha()
            elif n == 10:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass10.png").convert_alpha()             
            elif n == 11:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass11.png").convert_alpha()
            elif n == 12:
              mapmasn = pygame.image.load("./picture/Tile_Number/mass12.png").convert_alpha()
            else:
              mapmasn = pygame.image.load("./picture/space5050.png").convert_alpha()
            mapmasn_rect = mapmasn.get_rect()
            mapmasn_rect.center = (xx,yy)
            screen.blit(mapmasn,mapmasn_rect)
        elif (x-510)*(x-510)+(y-510)*(y-510) <= 5625 and mapmade: #Gamestart枠内判定＋マップが一度は生成されている
          running = False #Map確定
          for sock in clients_socks:
            sock.send("gamestart".encode('utf-8')) #マップが確定しゲーム開始の旨をクライアントに通知
            sock.recv(bufsize)
    if running == False:
      break
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      msg = sock.recv(bufsize).decode('utf-8')
      print(msg)
      if msg == "QUIT": #クライアントが落ちた時の全体終了処理
        sock.close()
        readfds.remove(sock)
        clients_socks.remove(sock)
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
          msg = receiver.recv(bufsize).decode('utf-8')

  for i in range(19):
    if land[i]==0:
      Mapdata_Mass[i][2] = 1
    Mapdata_Mass[i][0]=land[i]
    Mapdata_Mass[i][1]=landnumber[i]

  landdatastr = "" #クライアントに送信するメッセージの準備
  landnumberstr = ""
  for i in range(18):
    x = str(land[i])
    y = str(landnumber[i])
    landdatastr += x
    landdatastr += "/" #スラッシュ区切りで数字を送信、クライアント側でsplit関数で解凍
    landnumberstr += y
    landnumberstr += "/" #上に同じ
  landdatastr += str(land[18])
  landnumberstr += str(landnumber[18])

  print(landdatastr)
  print(landnumberstr)

  for i in range(backlog): #それぞれのクライアントに対してマップデータを送信
    sock = clients_socks[i]
    ii = str(i)
    sock.send("mapdata1".encode('utf-8'))
    sock.recv(bufsize)
    sock.send(landdatastr.encode('utf-8'))
    sock.recv(bufsize)
    sock.send("mapdata2".encode('utf-8'))
    sock.recv(bufsize)
    sock.send(landnumberstr.encode('utf-8'))
    sock.recv(bufsize)
    sock.send("mapdata3".encode('utf-8'))
    sock.recv(bufsize)
    sock.send(ii.encode('utf-8'))
    sock.recv(bufsize)

  draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)

  pygame.display.update()

  if backlog == 3:
    firstphaseturn = [0,1,2,2,1,0]
    once = [0,0,0]
  else:
    firstphaseturn = [0,1,2,3,3,2,1,0]
    once = [0,0,0,0]



  for sock in clients_socks: #開拓地と街道を置くフェーズの開始を全クライアントに通知
    sock.send("firstphasestart".encode('utf-8'))
    sock.recv(bufsize)

  for i in firstphaseturn: #開拓地と街道を置く順番

    this_turn_sock = clients_socks[i]

    this_turn_sock.send("Yourturn".encode('utf-8')) #次のターンの人にターン通知
    this_turn_sock.recv(bufsize)

    running = True

    while running: #初動、開拓地&街道建設フェーズ


      pygame.display.update()
      pygame.time.wait(50)

      for event in pygame.event.get():
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

      for sock in rready:                                   #選択された処理を順次遂行
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
        elif msg == "Mapdata":
          msg1 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          if msg1 == "settlement":
            msg2 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            msg3 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            pos = int(msg2)
            player = int(msg3)
            print(pos)
            Mapdata_Edge[pos][0]=player*2 #サーバー側のデータ更新完了
            if once[player] != 0:
              for i in range(19):
                if pos in Mapdata_Mass[i][3]:
                  x = Mapdata_Mass[i][0]
                  if x != 0:
                    Player_Data[player][2][x-1] += 1
                    Player_Data[player][1] += 1
            once[player] = 1
            
            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
            for sock in clients_socks:
              sock.send(msg.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg1.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg2.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg3.encode('utf-8'))
              sock.recv(bufsize)

          elif msg1 == "road":
            msg2 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            msg3 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            pos = int(msg2)
            player = int(msg3)
            print(pos)
            Mapdata_Side[pos][0]=player #サーバー側のデータ更新完了
            
            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
            for sock in clients_socks:
              sock.send(msg.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg1.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg2.encode('utf-8'))
              sock.recv(bufsize)
              sock.send(msg3.encode('utf-8'))
              sock.recv(bufsize)
            running = False
        
  for sock in clients_socks: #開拓地と街道を置くフェーズの終了を全クライアントに通知
    sock.send("firstphaseend".encode('utf-8'))
    sock.recv(bufsize)

  running = True

  if backlog == 3:
    Turn = [0,1,2]
  else:
    Turn = [0,1,2,3]

  ###################################
  ####  　　 ゲーム開始           ####
  ###################################
  draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)

  while running: #ゲーム本体
    for i in Turn:
      pygame.display.update()
      pygame.time.wait(50)

      ################################################
      ###  ターン開始の合図をクライアントと送受信する  ###
      ################################################

      Thisturn_player = clients_socks[i]  #Thisturn_playerには、このターンのプレイヤークライアントのアドレスを格納
      Thisturn_player.send("Yourturn".encode('utf-8')) #"Yourturn"を対象クライアントに対して送信
      Thisturn_player.recv(bufsize) #送信確認メッセージの受け取り

      for j in range(backlog):
        if clients_socks[j]!=Thisturn_player:
          clients_socks[j].send("others".encode('utf-8')) #"others"を対象クライアントに対して送信
          clients_socks[j].recv(bufsize) #送信確認メッセージの受け取り
          clients_socks[j].send(str(i).encode('utf-8')) #誰のターンか、情報を現在ターンでないクライアントに対して一斉送信
          clients_socks[j].recv(bufsize) #送信確認メッセージの受け取り


      ######################################################
      ###   ターン開始の合図をクライアントと送受信する(終了) ###
      ######################################################


      ######################################################
      ###　サイコロの出目をクライアントから受け取るフェーズ  ###
      ######################################################
      running1 = True
      Dice7 = False
      while running1:
        
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
            Dice1=random.randint(1,6)
            Dice2=random.randint(1,6)
            Dicesum=Dice1+Dice2
            Dice1_str = str(Dice1)
            Dice2_str = str(Dice2)
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
              Dice7 = True
            running1=False
            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
            draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            draw_Dice(screen,Dice1,Dice2)
            pygame.display.update()
     
      ##########################################################
      ###　サイコロの出目をクライアントから受け取るフェーズ(終了) ###
      ##########################################################

      ################################
      ###　7が出た時の処理(バースト) ###
      ################################
      Dice7_2=False
      burst_player_num = 0
      if Dice7:
        for receiver in clients_socks: #バースト処理の開始をクライアントに通知
          receiver.send("Burst".encode('utf-8'))
          receiver.recv(bufsize)

      if Dice7:
        Dice7_2 = True
        for i in range(4):
          if Player_Data[i][1]>=8:
            burst_player_num += 1
      
      if burst_player_num==0:
        Dice7=False
        Dice7_2=False
        for receiver in clients_socks: #バースト処理の開始をクライアントに通知
          receiver.send("NoBurst".encode('utf-8'))
          receiver.recv(bufsize)

      while Dice7:
        
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
              Dice7 = False
      
      if Dice7_2:
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

      #####################################
      ###　7が出た時の処理(蛮族移動)(終了) ###
      #####################################

      ##################
      ###  本体処理  ###
      ##################
      running1=True
      while running1:
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
          elif msg == "TurnEnd":
            sock.recv(bufsize)
            for receiver in clients_socks:
              if receiver!=sock:
                receiver.send("TurnEnd".encode('utf-8'))
                receiver.recv(bufsize)
            running1=False
          
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

            for receiver in clients_socks:           #他のクライアントへ一斉送信
              if sock!=receiver:
                receiver.send("Road".encode('utf-8'))
                receiver.recv(bufsize)        
                receiver.send(msg1.encode('utf-8'))
                receiver.recv(bufsize)
                receiver.send(msg2.encode('utf-8'))
                receiver.recv(bufsize)        
                receiver.send(msg3.encode('utf-8'))
                receiver.recv(bufsize)
                receiver.send("MsgEnd".encode('utf-8'))
                receiver.recv(bufsize)
            
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

            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog)
            draw_image(screen,"./picture/Dice/Roll_of_Dice.png",60,540)
            draw_Dice(screen,Dice1,Dice2)
            draw_image(screen,"./picture/frame.png",540,540)
            pygame.display.update()
            
          ######################
          ###  街道建設(終了) ###
          ######################

      #######################
      ###  本体処理(終了)  ###
      #######################

  return

if __name__ == '__main__':
  main()