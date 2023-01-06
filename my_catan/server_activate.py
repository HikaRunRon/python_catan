from __future__ import print_function ########サーバー最初期画面を担うファイル
import pygame
from pygame.locals import *
import socket
import select
import sys
import mapgene
import random
import server_draw as svd

def server_activate(running):
  while running[0]: #初期画面(server起動画面)
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
          running[0] = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #マウス入力、右クリック
        x, y = event.pos
        if 110 <= x and x <= 490 and 330 <= y and y <= 485: #枠内左クリックでwhileを抜け、次のページへ
          running[0] = False