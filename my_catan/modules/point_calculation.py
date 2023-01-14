########所持ポイントを計算する関数(made by ochii)

def pointget(Player_Data,playernumber):
    point=0
    for i in range(4,9):
        point+=Player_Data[playernumber][4][i] #発展カードのうちの得点カードの枚数を足していく。
    point+=(5-Player_Data[playernumber][5])#現在建てている開拓地の数分１ポイント足す
    point+=(4-Player_Data[playernumber][6])*2 #現在建てている都市の数分追加で１ポイント足す
    if Player_Data[playernumber][9]!=0:#最長交易路の有無
        point+=2
    if Player_Data[playernumber][11]!=0:#最大騎士力の有無
        point+=2
    return point