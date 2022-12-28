from __future__ import print_function
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing

def draw_image(screen,image,x,y): #画像(image)を座標(x,y)に描画
  im = pygame.image.load(image).convert_alpha()
  im_rect = im.get_rect()
  im_rect.center = (x,y)
  screen.blit(im,im_rect)

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

def draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside): #現在のマップ状況を全て表示する関数
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
      mapmasn = pygame.image.load(".picturespace5050.png").convert_alpha()
    mapmasn_rect = mapmasn.get_rect()
    mapmasn_rect.center = (xx,yy)
    screen.blit(mapmasn,mapmasn_rect)

  if backlog == 3:
    if yourturn == 0:
      draw_image(screen,"./picture/Background/back_white.png",300,560)
      draw_image(screen,"./picture/Background/back_red2.png",40,300)
      draw_image(screen,"./picture/Background/back_blue2.png",560,300)
    elif yourturn == 1:
      draw_image(screen,"./picture/Background/back_red.png",300,560)
      draw_image(screen,"./picture/Background/back_blue2.png",40,300)
      draw_image(screen,"./picture/Background/back_white2.png",560,300)
    elif yourturn == 2:
      draw_image(screen,"./picture/Background/back_blue.png",300,560)
      draw_image(screen,"./picture/Background/back_white2.png",40,300)
      draw_image(screen,"./picture/Background/back_red2.png",560,300)
  else:
    if yourturn == 0:
      draw_image(screen,"./picture/Background/back_white.png",300,560)
      draw_image(screen,"./picture/Background/back_red2.png",40,300)
      draw_image(screen,"./picture/Background/back_blue.png",300,40)
      draw_image(screen,"./picture/Background/back_orange2.png",560,300)
    elif yourturn == 1:
      draw_image(screen,"./picture/Background/back_red.png",300,560)
      draw_image(screen,"./picture/Background/back_blue2.png",40,300)
      draw_image(screen,"./picture/Background/back_orange.png",300,40)
      draw_image(screen,"./picture/Background/back_white2.png",560,300)
    elif yourturn == 2:
      draw_image(screen,"./picture/Background/back_blue.png",300,560)
      draw_image(screen,"./picture/Background/back_orange2.png",40,300)
      draw_image(screen,"./picture/Background/back_white.png",300,40)
      draw_image(screen,"./picture/Background/back_red2.png",560,300)
    elif yourturn == 3:
      draw_image(screen,"./picture/Background/back_orange.png",300,560)
      draw_image(screen,"./picture/Background/back_white2.png",40,300)
      draw_image(screen,"./picture/Background/back_red.png",300,40)
      draw_image(screen,"./picture/Background/back_blue2.png",560,300)

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

  draw_image(screen,select_num_image(Player_Data[yourturn][2][0]),150,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][1]),210,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][2]),270,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][3]),330,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][4]),390,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][3]),450,560)

  draw_image(screen,select_num_image(Player_Data[leftside][2][0]),40,150)
  draw_image(screen,select_num_image(Player_Data[leftside][2][1]),40,210)
  draw_image(screen,select_num_image(Player_Data[leftside][2][2]),40,270)
  draw_image(screen,select_num_image(Player_Data[leftside][2][3]),40,330)
  draw_image(screen,select_num_image(Player_Data[leftside][2][4]),40,390)
  draw_image(screen,select_num_image(Player_Data[leftside][3]),40,450)

  if backlog == 3:
    draw_image(screen,select_num_image(Player_Data[rightside][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[rightside][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[rightside][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[rightside][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[rightside][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[rightside][3]),560,150)
  else:
    draw_image(screen,select_num_image(Player_Data[front][2][0]),450,40)
    draw_image(screen,select_num_image(Player_Data[front][2][1]),390,40)
    draw_image(screen,select_num_image(Player_Data[front][2][2]),330,40)
    draw_image(screen,select_num_image(Player_Data[front][2][3]),270,40)
    draw_image(screen,select_num_image(Player_Data[front][2][4]),210,40)
    draw_image(screen,select_num_image(Player_Data[front][3]),150,40)

    draw_image(screen,select_num_image(Player_Data[rightside][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[rightside][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[rightside][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[rightside][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[rightside][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[rightside][3]),560,150)
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

def draw_candidate_settlement(screen,player,Mapdata_Edge,Mapdata_Side,x): #配置可能候補地を描写、x==0は初動の開拓地配置、x==1はゲーム本体の開拓地配置
  l = []
  for i in range(54):
    if x == 0:
      if Mapdata_Edge[i][0]==-1:
        Judge = True
        for j in Mapdata_Edge[i][3]:
          if Mapdata_Edge[j][0]!=-1:
            Judge = False
            break
        if Judge:
          draw_image(screen,"./picture/candidate.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
          l.append(i)
    else:
      if Mapdata_Edge[i][0]==-1:
        Judge = True
        for j in Mapdata_Edge[i][3]: #隣接点探索,隣に開拓地や都市が無いことを確認
          if Mapdata_Edge[j][0]!=-1:
            Judge = False
            break

        if Judge:
          Judge = False
          for j in Mapdata_Edge[i][2]: #隣接辺探索、隣に道があることを確認
            if Mapdata_Side[j][0] == player:
              Judge = True
              break

          if Judge:
            draw_image(screen,"./picture/candidate.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
            l.append(i)
  return l

def draw_candidate_city(screen,player,Mapdata_Edge):
  l = []
  for i in range(54):
    if Mapdata_Edge[i][0] == player*2:
      draw_image(screen,"./picture/candidate.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
      l.append(i)
  return l

def draw_candidate_road(screen,player,Mapdata_Edge,Mapdata_Side):
  l = []
  for i in range(72):
    Judge = False
    for j in Mapdata_Side[i][1]:
      if Mapdata_Edge[j][0]==player or Mapdata_Edge[j][0]==player+1:
        Judge = True
        break
    if Judge:
      draw_image(screen,"./picture/candidate.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      l.append(i)
      continue
    for j in Mapdata_Side[i][2]:
      if Mapdata_Side[j][0]==player:
        Judge = True
        break
    if Judge:
      draw_image(screen,"./picture/candidate.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
      l.append(i)
  return l

def draw_candidate_road_0(screen,Mapdata_Edge,Mapdata_Side,settlement):
  l = []
  for i in Mapdata_Edge[settlement][2]:
    draw_image(screen,"./picture/candidate.png",Mapdata_Side[i][3][0],Mapdata_Side[i][3][1])
    l.append(i)
  return l

def draw_candidate_bandit(screen,Mapdata_Mass):
  l = []
  for i in range(19):
    if Mapdata_Mass[i][2]==0:
      draw_image(screen,"./picture/candidate2.png",Mapdata_Mass[i][4][0],Mapdata_Mass[i][4][1])


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

  Player_Data = [[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]],[0,0,[0,0,0,0,0],0,[0,0,0,0,0,0,0,0,0],5,4,15,0,0,[0,0,0,0,0,0]]]
  #所持ポイント、所持資源カード合計枚数、所持資源カード枚数内訳(木、レンガ、羊、小麦、石)、所持発展カード合計枚数,その内訳(騎士、街道建設、発見、独占、大聖堂、図書館、市場、議会、大学),残り建設可能開拓地数、残り建設可能都市数、残り建設可能街道数、交易路の長さ、騎士力,優位トレード所持(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),0(3-1))(所持しているときは1(デフォルト0))

  yourturn = -1 #プレイヤーのターン、後々サーバーから通知が来る。

  with closing(sock):
    running = True
    while running:
      pygame.display.update() #ディスプレイ更新
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
        msg1 = sock.recv(bufsize).decode('utf-8')
        print("msg1,",msg1)
        sock.send("ok".encode('utf-8'))
        if msg1 == "plwt":
          msg2 = sock.recv(bufsize).decode('utf-8')
          print("msg2,",msg2)
          connections = int(msg2)
          print("connections,",connections)
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
        elif msg1 == "serverdown":
          pygame.quit()
          sys.exit()

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
    for i in range(19):
      land[i] = int(land[i])
      landnumber[i] = int(landnumber[i])
      xx = Mapdata_Mass[i][4][0]
      yy = Mapdata_Mass[i][4][1]
      mapmas = mapmass[i]
      mapmasn = mapmassnum[i]
      l = land[i]
      n = landnumber[i]
      if l == 0:   #資源描画
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
      if n == 2:    #数字描画
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

    for i in range(19):
      if land[i]==0:
        Mapdata_Mass[i][2] = 1
      Mapdata_Mass[i][0]=land[i]
      Mapdata_Mass[i][1]=landnumber[i]

    draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside)
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

    while running: #初動、開拓地&街道建設フェーズ
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
        elif msg == "Yourturn": #ターン通知を受け取った時、自分のターンを開始する。
          print("ok")
          myturn = True
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
            Mapdata_Edge[pos][0]=player*2 #クライアント側のデータ更新完了
            if once[player]!=0:
              for i in range(19):
                if pos in Mapdata_Mass[i][3]:
                  x = Mapdata_Mass[i][0]
                  if x != 0:
                    Player_Data[player][2][x-1] += 1
                    Player_Data[player][1] += 1
            once[player]=1
            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
          elif msg1 == "road":
            msg2 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            msg3 = sock.recv(bufsize).decode('utf-8')
            sock.send("ok".encode('utf-8'))
            pos = int(msg2)
            player = int(msg3)
            Mapdata_Side[pos][0]=player #クライアント側のデータ更新完了
            draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
        elif msg == "firstphaseend":
          running = False


      if myturn == False:
        continue

      player_str = str(yourturn)

      print(yourturn)

      settlement = -1
      settlement_candidates = draw_candidate_settlement(screen,yourturn,Mapdata_Edge,Mapdata_Side,0)

      while myturn: #開拓地を置く
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
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in settlement_candidates:
              if (Mapdata_Edge[i][4][0]-x)*(Mapdata_Edge[i][4][0]-x)+(Mapdata_Edge[i][4][1]-y)*(Mapdata_Edge[i][4][1]-y)<=500:
                settlement = i
                i_str = str(i)
                sock.send("Mapdata".encode('utf-8'))
                sock.recv(bufsize)
                sock.send("settlement".encode('utf-8'))
                sock.recv(bufsize)
                sock.send(i_str.encode('utf-8'))
                sock.recv(bufsize)
                sock.send(player_str.encode('utf-8'))
                sock.recv(bufsize)
                myturn = False
                break
        if myturn == False:
          break
        rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
        for sock in rready:                                   #選択された処理を順次遂行
          msg = sock.recv(bufsize).decode('utf-8')
          print(msg)
          sock.send("ok".encode('utf-8'))
          if msg == "serverdown":
            pygame.quit()
            sys.exit()

      msg = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      if msg == "Mapdata":
        msg1 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        if msg1 == "settlement":
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          pos = int(msg2)
          print(pos)
          player = int(msg3)
          Mapdata_Edge[pos][0]=player*2 #クライアント側のデータ更新完了
          if once[player]!=0:
            for i in range(19):
              if pos in Mapdata_Mass[i][3]:
                x = Mapdata_Mass[i][0]
                if x != 0:
                  Player_Data[player][2][x-1] += 1
                  Player_Data[player][1] += 1
          once[player]=1
          draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新
      road_candidates = draw_candidate_road_0(screen,Mapdata_Edge,Mapdata_Side,settlement)
      myturn = True

      while myturn: #街道を置く
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
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in road_candidates:
              if (Mapdata_Side[i][3][0]-x)*(Mapdata_Side[i][3][0]-x)+(Mapdata_Side[i][3][1]-y)*(Mapdata_Side[i][3][1]-y)<=500:
                i_str = str(i)
                sock.send("Mapdata".encode('utf-8'))
                sock.recv(bufsize)
                sock.send("road".encode('utf-8'))
                sock.recv(bufsize)
                sock.send(i_str.encode('utf-8'))
                sock.recv(bufsize)
                sock.send(player_str.encode('utf-8'))
                sock.recv(bufsize)
                myturn = False
                break
        if myturn == False:
          break
        rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
        for sock in rready:                                   #選択された処理を順次遂行
          msg = sock.recv(bufsize).decode('utf-8')
          print(msg)
          sock.send("ok".encode('utf-8'))
          if msg == "serverdown":
            pygame.quit()
            sys.exit()

      msg = sock.recv(bufsize).decode('utf-8')
      sock.send("ok".encode('utf-8'))
      if msg == "Mapdata":
        msg1 = sock.recv(bufsize).decode('utf-8')
        sock.send("ok".encode('utf-8'))
        if msg1 == "road":
          msg2 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          msg3 = sock.recv(bufsize).decode('utf-8')
          sock.send("ok".encode('utf-8'))
          pos = int(msg2)
          print(pos)
          player = int(msg3)
          Mapdata_Side[pos][0]=player #クライアント側のデータ更新完了
          draw_server(screen,Mapdata_Mass,Mapdata_Side,Mapdata_Edge,Player_Data,land,landnumber,backlog,yourturn,rightside,front,leftside) #データをもとに描画更新

    running = True

    while running: #ゲーム本体
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
          sock.send("ok".encode('utf-8'))

          ##########################
          ## Start  others Myturn ##　
          ##########################
          
          Dice_msg=sock.recv(bufsize).decode('utf-8')         
          Dice_nums_str = Dice_msg.split("/")
          Dice1 = int(Dice_nums_str[0])
          Dice2 = int(Dice_nums_str[1])

          running1=True
          while running1:
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
              if "??" <= x and x <= "??" and "??" <= y and y <= "??": #枠内左クリックでwhileを抜け、次のページへ
                sock.send("Dice".encode('utf-8')) #サイコロを振る
                sock.recv(bufsize)
                sock.send("ok".encode(''))
                running1=False #ループから抜ける

          ##################################
          ## Start  others Myturn (終了)  ##　
          ##################################  

        elif msg == "Yourturn": ##ここからocchiiが書いてるよ💛💛★(⋈◍＞◡＜◍)。✧♡★✌
          sock.send("ok".encode('utf-8'))

          ############
          ## Myturn ##　
          ############
          
          #####################
          ## サイコロフリフリ ##
          #####################
          
          running1=True
          while running1:
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
              if "??" <= x and x <= "??" and "??" <= y and y <= "??": #枠内左クリックでwhileを抜け、次のページへ
                sock.send("Dice".encode('utf-8')) #サイコロを振る
                sock.recv(bufsize)
                sock.send("ok".encode(''))
                running1=False #ループから抜ける
            
            if running1 == False:  #サイコロフリフリメッセージ送信後は即ループ脱出
              break 

            rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
            for sock in rready:                                   #選択された処理を順次遂行
              msg = sock.recv(bufsize).decode('utf-8')
              print(msg)
              sock.send("ok".encode('utf-8'))
              if msg == "serverdown":
                pygame.quit()
                sys.exit()

          ###########################
          ## サイコロフリフリ(終了) ##
          ###########################
          
          ##データの更新
          Dice_msg=sock.recv(bufsize).decode('utf-8')  
          Dice_nums_str = Dice_msg.split("/")
          Dice1 = int(Dice_nums_str[0])
          Dice2 = int(Dice_nums_str[1])



          ##################
          ## Myturn(終了) ##　
          ##################
          
          
          
  return

if __name__ == '__main__':
  main()
