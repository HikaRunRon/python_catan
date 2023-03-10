from __future__ import print_function         ########サーバーの画像描写を担うファイル
import pygame
from pygame.locals import *
import socket
import select
import sys
from modules import mapgene
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