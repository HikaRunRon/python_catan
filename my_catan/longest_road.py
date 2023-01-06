########最長交易路の長さを返す関数(made by ochii)

def dfs(Mapdata_Side,playernumber,startnumber,alreadypass=[],lastedge=[]):#startnumberから探索開始、alreadypassに通った辺を格納（多分引数に入れないと上手くいかない）、lastedgeに一つ前の辺の隣接点を格納（１→２→７のような例を防止したい）
    howlong=0
    for nextnumber in Mapdata_Side[startnumber][2]: #次に進む辺の候補
        if nextnumber in alreadypass: #既に通っている辺はパス
            continue
        if Mapdata_Side[nextnumber][1][0] in lastedge or Mapdata_Side[nextnumber][1][1] in lastedge: #１→２→７のような場合を隣接頂点の条件式で表し、除外
            continue
        if Mapdata_Side[nextnumber][0]==playernumber: #playerが辺を所有している場合
            howlong=max(howlong,dfs(Mapdata_Side,playernumber,nextnumber,alreadypass+[startnumber],Mapdata_Side[startnumber][1])) #現在の辺から進める最長の長さを求める
    return 1+howlong #交易路の長さ
    
    
def longestroad(Mapdata_Side,playernumber): #最長の長さを求める関数
    road=[]#playerが所有している道の番号を格納
    for i in range(72): #改良の余地あり
        if Mapdata_Side[i][0]==playernumber:
                road=road+[i]
    ##格納終了
    longestvalue=0 #最長の値
    for roadnumber in road: #それぞれの辺をスタートにしてdfsをして最長を求める
        alreadypass=[]
        ##dfsで最長の長さを求める。
        longestvalue=max(longestvalue,dfs(Mapdata_Side,playernumber,roadnumber,alreadypass,[-1,-1]))
    return longestvalue