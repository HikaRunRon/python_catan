from __future__ import print_function      ########クライアントの画像描画を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import longest_road

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
      mapmasn = pygame.image.load("./picture/space5050.png").convert_alpha()
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
  draw_image(screen,"./picture/Army.png",450,450)
  draw_image(screen,"./picture/Road.png",450,500)

  draw_image(screen,"./picture/Resource_Card/woodcard2.png",40,150)
  draw_image(screen,"./picture/Resource_Card/brickcard2.png",40,210)
  draw_image(screen,"./picture/Resource_Card/sheepcard2.png",40,270)
  draw_image(screen,"./picture/Resource_Card/wheatcard2.png",40,330)
  draw_image(screen,"./picture/Resource_Card/orecard2.png",40,390)
  draw_image(screen,"./picture/Resource_Card/secretcard2.png",40,450)
  draw_image(screen,"./picture/Army.png",150,450)
  draw_image(screen,"./picture/Road.png",100,450)

  draw_image(screen,"./picture/Resource_Card/woodcard2.png",560,450)
  draw_image(screen,"./picture/Resource_Card/brickcard2.png",560,390)
  draw_image(screen,"./picture/Resource_Card/sheepcard2.png",560,330)
  draw_image(screen,"./picture/Resource_Card/wheatcard2.png",560,270)
  draw_image(screen,"./picture/Resource_Card/orecard2.png",560,210)
  draw_image(screen,"./picture/Resource_Card/secretcard2.png",560,150)
  draw_image(screen,"./picture/Army.png",450,150)
  draw_image(screen,"./picture/Road.png",500,150)

  if backlog == 4:
    draw_image(screen,"./picture/Resource_Card/woodcard.png",450,40)
    draw_image(screen,"./picture/Resource_Card/brickcard.png",390,40)
    draw_image(screen,"./picture/Resource_Card/sheepcard.png",330,40)
    draw_image(screen,"./picture/Resource_Card/wheatcard.png",270,40)
    draw_image(screen,"./picture/Resource_Card/orecard.png",210,40)
    draw_image(screen,"./picture/Resource_Card/secretcard.png",150,40)
    draw_image(screen,"./picture/Army.png",150,150)
    draw_image(screen,"./picture/Road.png",150,100)

  draw_image(screen,select_num_image(Player_Data[yourturn][2][0]),150,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][1]),210,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][2]),270,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][3]),330,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][4]),390,560)
  draw_image(screen,select_num_image(Player_Data[yourturn][3]),450,560)
  if Player_Data[yourturn][11]==1:
    draw_image(screen,"./picture/Largest_Army.png",450,450)
  if Player_Data[yourturn][9]==1:
    draw_image(screen,"./picture/Longest_Road.png",450,500)
  draw_image(screen,select_num_image(Player_Data[yourturn][10]),450,450)
  draw_image(screen,select_num_image(Player_Data[yourturn][8]),450,500)
  

  draw_image(screen,select_num_image(Player_Data[leftside][2][0]),40,150)
  draw_image(screen,select_num_image(Player_Data[leftside][2][1]),40,210)
  draw_image(screen,select_num_image(Player_Data[leftside][2][2]),40,270)
  draw_image(screen,select_num_image(Player_Data[leftside][2][3]),40,330)
  draw_image(screen,select_num_image(Player_Data[leftside][2][4]),40,390)
  draw_image(screen,select_num_image(Player_Data[leftside][3]),40,450)
  if Player_Data[leftside][11]==1:
    draw_image(screen,"./picture/Largest_Army.png",150,450)
  if Player_Data[leftside][9]==1:
    draw_image(screen,"./picture/Longest_Road.png",100,450)
  draw_image(screen,select_num_image(Player_Data[leftside][10]),150,450)
  draw_image(screen,select_num_image(Player_Data[leftside][8]),100,450)

  if backlog == 3:
    draw_image(screen,select_num_image(Player_Data[rightside][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[rightside][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[rightside][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[rightside][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[rightside][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[rightside][3]),560,150)
    if Player_Data[rightside][11]==1:
      draw_image(screen,"./picture/Largest_Army.png",450,150)
    if Player_Data[rightside][9]==1:
      draw_image(screen,"./picture/Longest_Road.png",500,150)
    draw_image(screen,select_num_image(Player_Data[rightside][10]),450,150)
    draw_image(screen,select_num_image(Player_Data[rightside][8]),500,150)
  else:
    draw_image(screen,select_num_image(Player_Data[front][2][0]),450,40)
    draw_image(screen,select_num_image(Player_Data[front][2][1]),390,40)
    draw_image(screen,select_num_image(Player_Data[front][2][2]),330,40)
    draw_image(screen,select_num_image(Player_Data[front][2][3]),270,40)
    draw_image(screen,select_num_image(Player_Data[front][2][4]),210,40)
    draw_image(screen,select_num_image(Player_Data[front][3]),150,40)
    if Player_Data[front][11]==1:
      draw_image(screen,"./picture/Largest_Army.png",150,150)
    if Player_Data[front][9]==1:
      draw_image(screen,"./picture/Longest_Road.png",150,100)
    draw_image(screen,select_num_image(Player_Data[front][10]),150,150)
    draw_image(screen,select_num_image(Player_Data[front][8]),150,100)

    draw_image(screen,select_num_image(Player_Data[rightside][2][0]),560,450)
    draw_image(screen,select_num_image(Player_Data[rightside][2][1]),560,390)
    draw_image(screen,select_num_image(Player_Data[rightside][2][2]),560,330)
    draw_image(screen,select_num_image(Player_Data[rightside][2][3]),560,270)
    draw_image(screen,select_num_image(Player_Data[rightside][2][4]),560,210)
    draw_image(screen,select_num_image(Player_Data[rightside][3]),560,150)
    if Player_Data[rightside][11]==1:
      draw_image(screen,"./picture/Largest_Army.png",450,150)
    if Player_Data[rightside][9]==1:
      draw_image(screen,"./picture/Longest_Road.png",500,150)
    draw_image(screen,select_num_image(Player_Data[rightside][10]),450,150)
    draw_image(screen,select_num_image(Player_Data[rightside][8]),500,150)
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

def burst_discard(screen,yourturn,Player_Data,Discard_Data):
  draw_image(screen,"./picture/Discard.png",300,300)
  draw_image(screen,"./picture/Resource_Card/woodcard.png",180,250)
  draw_image(screen,"./picture/Resource_Card/brickcard.png",240,250)
  draw_image(screen,"./picture/Resource_Card/sheepcard.png",300,250)
  draw_image(screen,"./picture/Resource_Card/wheatcard.png",360,250)
  draw_image(screen,"./picture/Resource_Card/orecard.png",420,250)
  draw_image(screen,"./picture/Resource_Card/woodcard.png",180,350)
  draw_image(screen,"./picture/Resource_Card/brickcard.png",240,350)
  draw_image(screen,"./picture/Resource_Card/sheepcard.png",300,350)
  draw_image(screen,"./picture/Resource_Card/wheatcard.png",360,350)
  draw_image(screen,"./picture/Resource_Card/orecard.png",420,350)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][0]),180,350)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][1]),240,350)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][2]),300,350)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][3]),360,350)
  draw_image(screen,select_num_image(Player_Data[yourturn][2][4]),420,350)
  draw_image(screen,select_num_image(Discard_Data[0]),180,250)
  draw_image(screen,select_num_image(Discard_Data[1]),240,250)
  draw_image(screen,select_num_image(Discard_Data[2]),300,250)
  draw_image(screen,select_num_image(Discard_Data[3]),360,250)
  draw_image(screen,select_num_image(Discard_Data[4]),420,250)
  

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
    if Mapdata_Side[i][0]!=-1:
      continue
    for j in Mapdata_Side[i][1]:
      if Mapdata_Edge[j][0]==player*2 or Mapdata_Edge[j][0]==player*2+1:
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
      l.append(i)
  return l

def draw_candidate_rob(screen,Mapdata_Mass,Player_Data,Mapdata_Edge,pos,yourturn):
  l = []
  for i in Mapdata_Mass[pos][3]:
    if Mapdata_Edge[i][0]!=-1:
      x = Mapdata_Edge[i][0]/2
      x = int(x)
      if x==yourturn:
        continue
      if Player_Data[x][1]!=0:
        draw_image(screen,"./picture/candidate.png",Mapdata_Edge[i][4][0],Mapdata_Edge[i][4][1])
        l.append(i)
  return l

def draw_client_development(screen,Player_Data,yourturn,Thisturn_Draw):
  draw_image(screen,"./picture/Development.png",300,300)

  if Player_Data[yourturn][4][4]==1:
    draw_image(screen,"./picture/Resource_Card/Chapel_card.png",280,200)
  if Player_Data[yourturn][4][5]==1:
    draw_image(screen,"./picture/Resource_Card/Library_card.png",330,200)
  if Player_Data[yourturn][4][6]==1:
    draw_image(screen,"./picture/Resource_Card/Market_card.png",380,200)
  if Player_Data[yourturn][4][7]==1:
    draw_image(screen,"./picture/Resource_Card/Hall_card.png",430,200)
  if Player_Data[yourturn][4][8]==1:
    draw_image(screen,"./picture/Resource_Card/University_card.png",480,200)
  
  draw_image(screen,select_num_image(Player_Data[yourturn][4][0]),225,330)
  draw_image(screen,select_num_image(Player_Data[yourturn][4][1]),275,330)
  draw_image(screen,select_num_image(Player_Data[yourturn][4][2]),325,330)
  draw_image(screen,select_num_image(Player_Data[yourturn][4][3]),375,330)

  draw_image(screen,select_num_image(Thisturn_Draw[0]),225,450)
  draw_image(screen,select_num_image(Thisturn_Draw[1]),275,450)
  draw_image(screen,select_num_image(Thisturn_Draw[2]),325,450)
  draw_image(screen,select_num_image(Thisturn_Draw[3]),375,450)

def draw_candidate_choose(screen):
  draw_image(screen,"./picture/candidate3.png",150,560)
  draw_image(screen,"./picture/candidate3.png",210,560)
  draw_image(screen,"./picture/candidate3.png",270,560)
  draw_image(screen,"./picture/candidate3.png",330,560)
  draw_image(screen,"./picture/candidate3.png",390,560)
  return [[150,560],[210,560],[270,560],[330,560],[390,560]]

def draw_candidate_choose2(screen):
  draw_image(screen,"./picture/candidate4.png",150,560)
  draw_image(screen,"./picture/candidate4.png",210,560)
  draw_image(screen,"./picture/candidate4.png",270,560)
  draw_image(screen,"./picture/candidate4.png",330,560)
  draw_image(screen,"./picture/candidate4.png",390,560)
  return [[150,560],[210,560],[270,560],[330,560],[390,560]]


  



  


