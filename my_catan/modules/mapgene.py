import random   ########マップをランダムで生成する関数(made by ochii)

def landform(): ##資源を配置する関数
    resourse=[0,1,1,1,1,2,2,2,3,3,3,3,4,4,4,4,5,5,5]#資源の配置を決めるリスト
    random.shuffle(resourse)
    return resourse
land=landform()
numberlist=[5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]#numberlist[0]=Aの裏側の数字,numberlist[1]=Bの裏側の数字,...として対応する数字をリストに入れた。
nextnumber=[[1,4],[2,5],[6,5],[0,4],[5,9],[10,9],[11,10],[3,8],[4,9],[-1,-1],
            [14,9],[15,10],[7,8],[8,9],[13,9],[18,14],[12,13],[16,13],[17,14]]#次に進む候補
def numberform(land):#nから始める。つまりマップを作るときに"A"を置く場所
    numberseen=[False for i in range(19)]#一度アルファベットを置いた場所をTrueに変える。
    n = random.choice([0,1,2,3,6,7,11,12,15,16,17,18])
    print(n)
    landnumber=[-1 for i in range(19)]#最終的なアルファベット（番号）の配置を格納
    running=True
    number=0 #numberlistのポインタ
    while running:
        if land[n]!=0:#もし砂漠でなかったら
            landnumber[n]=numberlist[number]#サイコロの目を割り当てる。
        numberseen[n]=True #一度通ったのでTrueに
        if n==9: #9は中心のマスなので確実にここで終了
            running=False #ループから抜ける
        elif land[n]==0:#もし砂漠だったらポインタ（ゲーム的にはアルファベット）は進めたくない
            if numberseen[nextnumber[n][0]]: #一つ内側のマスに入る
                n=nextnumber[n][1]
            else:
                n=nextnumber[n][0]
        else: #砂漠以外かつ中心でない資源マス
            number+=1 #ポインタを進める。
            if numberseen[nextnumber[n][0]]: #一つ内側のマスに入る
                n=nextnumber[n][1]
            else:
                n=nextnumber[n][0]
    return landnumber