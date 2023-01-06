from __future__ import print_function          ########クライアントのマップ描画を担うファイル
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
import longest_road
import client_draw as cld

def client_map_display(land,landnumber,Mapdata_Mass,mapmass,mapmassnum,screen):
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