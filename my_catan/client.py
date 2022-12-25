from __future__ import print_function
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing

def main(): #クライアント側
  (w,h)=(600,600)   #ゲーム画面の大きさ(幅600px,高さ600px)
  pygame.init()     #pygameを初期化
  pygame.display.set_mode((w,h),0,32)   #ディスプレイ設定
  screen = pygame.display.get_surface() #作成したディスプレイ情報をscreenが取得
  bg = pygame.image.load("clstr.jpg").convert_alpha() #背景画像設定   
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
  bg = pygame.image.load("setting.jpg").convert_alpha() #背景画像設定
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

  Mapdata_Mass = [[0,0,0,[0,1,2,8,9,10],[153,216]],[0,0,0,[2,3,4,10,11,12],[153,300]],[0,0,0,[4,5,6,12,13,14],[153,385]],[0,0,0,[7,8,9,17,18,19],[226,173]], #資源、サイコロ対応目、盗賊の有無、周囲の６つの頂点番号(const),中心座標(const)
  [0,0,0,[9,10,11,19,20,21],[226,258]],[0,0,0,[11,12,13,21,22,23],[226,342]],[0,0,0,[13,14,15,23,24,25],[226,427]],[0,0,0,[16,17,18,27,28,29],[300,132]],[0,0,0,[18,19,20,29,30,31],[300,216]],
  [0,0,0,[20,21,22,31,32,33],[300,300]],[0,0,0,[22,23,24,33,34,35],[300,385]],[0,0,0,[24,25,26,35,36,37],[300,469]],[0,0,0,[28,29,30,38,39,40],[374,173]],[0,0,0,[30,31,32,40,41,42],[374,258]],
  [0,0,0,[32,33,34,42,43,44],[374,342]],[0,0,0,[34,35,36,44,45,46],[374,427]],[0,0,0,[39,40,41,47,48,49],[447,216]],[0,0,0,[41,42,43,49,50,51],[447,300]],[0,0,0,[43,44,45,51,52,53],[447,385]]]

  Mapdata_Side = [[0,[0,1],[1,6]],[0,[1,2],[0,2,7]],[0,[2,3],[1,3,7]],[0,[3,4],[2,4,8]],[0,[4,5],[3,5,8]],[0,[5,6],[4,9]],[0,[0,8],[0,10,11]],[0,[2,10],[1,2,12,13]], #所有者、隣接点(const)、隣接辺(const)
  [0,[4,12],[3,4,14,15]],[0,[6,14],[5,16,17]],[0,[7,8],[6,11,18]],[0,[8,9],[6,10,12,19]],[0,[9,10],[7,11,13,19]],[0,[10,11],[7,12,14,20]],[0,[11,12],[8,13,15,20]],[0,[12,13],[8,14,16,21]],
  [0,[13,14],[9,15,17,21]],[0,[14,15],[9,16,22]],[0,[7,17],[10,23,24]],[0,[9,19],[11,12,25,26]],[0,[11,21],[13,14,27,28]],[0,[13,23],[15,16,29,30]],[0,[15,25],[17,31,32]],[0,[16,17],[18,24,33]],
  [0,[17,18],[18,23,25,34]],[0,[18,19],[19,24,26,34]],[0,[19,20],[19,25,27,35]],[0,[20,21],[20,26,28,35]],[0,[21,22],[20,27,29,36]],[0,[22,23],[21,28,30,36]],[0,[23,24],[21,29,31,37]],[0,[24,25],[22,30,32,37]],
  [0,[25,26],[22,31,38]],[0,[16,27],[23,39]],[0,[18,29],[24,25,40,41]],[0,[20,31],[26,27,42,43]],[0,[22,33],[28,29,44,45]],[0,[24,35],[30,31,46,47]],[0,[26,37],[32,48]],[0,[27,28],[33,40,49]],
  [0,[28,29],[34,39,41,49]],[0,[29,30],[34,40,42,50]],[0,[30,31],[35,41,43,50]],[0,[31,32],[35,42,44,51]],[0,[32,33],[36,43,45,51]],[0,[33,34],[36,44,46,52]],[0,[34,35],[37,45,47,52]],[0,[35,36],[37,46,48,53]],
  [0,[36,37],[38,47,53]],[0,[28,38],[39,40,54]],[0,[30,40],[41,42,55,56]],[0,[32,42],[43,44,57,58]],[0,[34,44],[45,46,59,60]],[0,[36,46],[47,48,61]],[0,[38,39],[49,55,62]],[0,[39,40],[50,54,56,62]],
  [0,[40,41],[50,55,57,63]],[0,[41,42],[51,56,58,63]],[0,[42,43],[51,57,59,64]],[0,[43,44],[52,58,60,64]],[0,[44,45],[52,59,61,65]],[0,[45,46],[53,60,65]],[0,[39,47],[54,55,66]],[0,[41,49],[56,57,67,68]],
  [0,[43,51],[58,59,69,70]],[0,[45,53],[60,61,71]],[0,[47,48],[62,67]],[0,[48,49],[63,66,68]],[0,[49,50],[63,67,69]],[0,[50,51],[64,68,70]],[0,[51,52],[64,69,71]],[0,[52,53],[65,70]]]

  Mapdata_Edge = [[0,6,[0,6],[1,8]],[0,6,[0,1],[0,2]],[0,0,[1,2,7],[1,3,10]],[0,1,[2,3],[2,4]],[0,1,[3,4,8],[3,5,12]],[0,0,[4,5],[4,6]],[0,0,[5,9],[5,14]],[0,4,[10,18],[8,17]],[0,0,[6,10,11],[0,7,9]], #所有者と建造物、優位トレード条件所有マス(const)(1(wood2-1),2(brick2-1),3(sheep2-1),4(wheat2-1),5(ore2-1),6(3-1))、隣接辺、隣接点
  [0,0,[11,12,19],[8,10,19]],[0,0,[7,12,13],[2,9,11]],[0,0,[13,14,20],[10,12,21]],[0,0,[8,14,15],[4,11,13]],[0,0,[15,16,21],[12,14,23]],[0,0,[9,16,17],[6,13,15]],[0,6,[17,22],[14,25]],[0,0,[23,33],[17,27]],[0,4,[18,23,24],[7,16,18]],
  [0,0,[24,25,34],[17,19,29]],[0,0,[19,25,26],[9,18,20]],[0,0,[26,27,35],[19,21,31]],[0,0,[20,27,28],[11,20,22]],[0,0,[28,29,36],[21,23,33]],[0,0,[21,29,30],[13,22,24]],[0,0,[30,31,37],[23,25,35]],[0,6,[22,31,32],[15,24,26]],[0,0,[32,38],[25,37]],
  [0,0,[33,39],[16,28]],[0,5,[39,40,49],[27,29,38]],[0,0,[34,40,41],[18,28,30]],[0,0,[41,42,50],[29,31,40]],[0,0,[35,42,43],[20,30,32]],[0,0,[43,44,51],[31,33,42]],[0,0,[36,44,45],[22,32,34]],[0,0,[45,46,52],[33,35,44]],[0,0,[37,46,47],[24,34,36]],
  [0,3,[47,48,53],[35,37,46]],[0,0,[38,48],[26,36]],[0,5,[49,54],[28,39]],[0,0,[54,55,62],[38,40,47]],[0,0,[50,55,56],[30,39,41]],[0,0,[56,57,63],[40,42,49]],[0,0,[51,57,58],[32,41,43]],[0,0,[58,59,64],[42,44,51]],[0,0,[52,59,60],[34,43,45]],
  [0,0,[60,61,65],[44,46,53]],[0,3,[53,61],[36,45]],[0,6,[62,66],[39,48]],[0,6,[66,67],[47,49]],[0,0,[63,67,68],[41,48,50]],[0,2,[68,69],[49,51]],[0,2,[64,69,70],[43,50,52]],[0,6,[70,71],[51,53]],[0,6,[65,71],[45,52]]]

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
              bg = pygame.image.load("0-3.jpg").convert_alpha() #背景画像設定
            elif connections == 1:
              bg = pygame.image.load("1-3.jpg").convert_alpha() #背景画像設定
            elif connections == 2:
              bg = pygame.image.load("2-3.jpg").convert_alpha() #背景画像設定
            else:
              bg = pygame.image.load("3-3.jpg").convert_alpha() #背景画像設定
              running = False
          else:
            if connections == 0:
              bg = pygame.image.load("0-4.jpg").convert_alpha() #背景画像設定
            elif connections == 1:
              bg = pygame.image.load("1-4.jpg").convert_alpha() #背景画像設定
            elif connections == 2:
              bg = pygame.image.load("2-4.jpg").convert_alpha() #背景画像設定
            elif connections == 3:
              bg = pygame.image.load("3-4.jpg").convert_alpha() #背景画像設定
            else:
              bg = pygame.image.load("4-4.jpg").convert_alpha() #背景画像設定
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
        bg = pygame.image.load("start3.jpg").convert_alpha() #背景画像設定
      else:
        bg = pygame.image.load("start4.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新
    pygame.time.wait(2000)
    startmap = sock.recv(bufsize).decode('utf-8')
    print("startmap,",startmap)
    if startmap == "MAPSTART":
      bg = pygame.image.load("catanmap.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新

    mapmass = []
    mapmassnum = []

    for i in range(19): #初期マップデータ描画
      xx = Mapdata_Mass[i][4][0]
      yy = Mapdata_Mass[i][4][1]
      mapmas = pygame.image.load("desertmap.png").convert_alpha()
      mapmas_rect = mapmas.get_rect()
      mapmas_rect.center = (xx,yy)
      screen.blit(mapmas,mapmas_rect)

      mapmasn = pygame.image.load("card0.png").convert_alpha()
      mapmasn_rect = mapmasn.get_rect()
      mapmasn_rect.center = (xx,yy)
      screen.blit(mapmasn,mapmasn_rect)

      mapmass.append(mapmas)
      mapmassnum.append(mapmasn)

    mapgenebutton = pygame.image.load("mapgene.png").convert_alpha()
    mapgenebutton_rect = mapgenebutton.get_rect()
    mapgenebutton_rect.center = (90,510)
    screen.blit(mapgenebutton,mapgenebutton_rect)

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
    msg = sock.recv(bufsize).decode('utf-8')
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
      if l == 0:
        mapmas = pygame.image.load("desertmap.png").convert_alpha()
      elif l == 1:
        mapmas = pygame.image.load("woodmap.png").convert_alpha()
      elif l == 2:
        mapmas = pygame.image.load("brickmap.png").convert_alpha()
      elif l == 3:
        mapmas = pygame.image.load("sheepmap.png").convert_alpha()             
      elif l == 4:
        mapmas = pygame.image.load("wheatmap.png").convert_alpha()
      else:
        mapmas = pygame.image.load("oremap.png").convert_alpha()
      mapmas_rect = mapmas.get_rect()
      mapmas_rect.center = (xx,yy)
      screen.blit(mapmas,mapmas_rect)
      if n == 2:
        mapmasn = pygame.image.load("mass2.png").convert_alpha()
      elif n == 3:
        mapmasn = pygame.image.load("mass3.png").convert_alpha()
      elif n == 4:
        mapmasn = pygame.image.load("mass4.png").convert_alpha()
      elif n == 5:
        mapmasn = pygame.image.load("mass5.png").convert_alpha()             
      elif n == 6:
        mapmasn = pygame.image.load("mass6.png").convert_alpha()
      elif n == 8:
        mapmasn = pygame.image.load("mass8.png").convert_alpha()
      elif n == 9:
        mapmasn = pygame.image.load("mass9.png").convert_alpha()
      elif n == 10:
        mapmasn = pygame.image.load("mass10.png").convert_alpha()             
      elif n == 11:
        mapmasn = pygame.image.load("mass11.png").convert_alpha()
      elif n == 12:
        mapmasn = pygame.image.load("mass12.png").convert_alpha()
      else:
        mapmasn = pygame.image.load("space.png").convert_alpha()
      mapmasn_rect = mapmasn.get_rect()
      mapmasn_rect.center = (xx,yy)
      screen.blit(mapmasn,mapmasn_rect)


    running = True

    while running: #map自動生成
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

  return

if __name__ == '__main__':
  main()
