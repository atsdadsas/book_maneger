first=0 #初めの一回だけチュートリアル
scene=0
choice=0
pushKey=0
player=[1,1,0,0]#プレイヤーの[x座標,y座標],進む向き[x,y]
mapSize_x=6
mapSize_y=6
nextmap=0

#マップ
#   0:床 1:壁 2:帰り道 3:ゴール
map1=[
    [1,2,1,1,1,1],
    [1,0,0,0,0,1],
    [1,0,1,0,1,1],
    [1,0,1,0,0,1],
    [1,0,1,0,0,1],
    [1,1,1,1,3,1]]
map2=[
    [1,1,2,1,1,1],
    [1,1,0,0,0,1],
    [1,0,1,1,0,1],
    [1,0,0,0,0,1],
    [1,1,1,0,1,1],
    [1,1,1,3,1,1]]
map3=[
    [1,1,1,1,2,1],
    [1,0,0,0,0,1],
    [1,0,1,1,1,1],
    [1,0,0,0,0,1],
    [1,0,1,0,1,1],
    [1,1,1,3,1,1]]
#現在のマップ
nowMap = [[0 for _ in range(mapSize_x)] for _ in range(mapSize_y)]

#ループで行動を起こすたびに画面更新
while(1):
    match(scene):
        #=====================
        #       タイトル
        #=====================
        case 0:
            if first==0:#一回だけ表示
                print("\n\t===操作方法===")
                print("タイトルなど")
                print("\tEnterキー:決定 W/S:選択変更")
                print("ゲーム中")
                print("\tWASD:移動")
                print("\n\t\tPlease press enter")
                first=1
                input()
                print("====================================")
            if choice==0:
                print("\n秘宝を狙え\nダンジョン探索記\n\n攻略開始<-\n探索終了\n")
            else:
                print("\n秘宝を狙え\nダンジョン探索記\n\n攻略開始\n探索終了<-\n")
            
            #押されたボタンにより表示変更
            pushKey=input()
            if pushKey=='s' and choice!=1:
                choice+=1
            elif pushKey=='w' and choice!=0:
                choice-=1
            #   W/S以外で押されたら決定
            else:
                if pushKey=='w' or pushKey=='s':
                    print("それ以上は矢印が画面外行っちゃうよ～")
                elif choice == 0:
                    scene=1
                else:
                    print("じゃぁね～\n")
                    break

        #======================
        #       プレイ画面
        #======================

        case 1:
            if first==1:
                #間にinput()の中に文を入れて、Enterを押すと話が進む仕組みに
                input("あなた:「へぇ～ここが昔の王様が財宝を隠したっていう幻のダンジョンか～」")
                input("にしても、ここ。天然の洞窟を使って作ったとはいえ、\nいささかツタが絡まりすぎじゃないか？\n入るどころの騒ぎでないだが。")
                input("あなた:「まぁこのためにこれ持ってきたんだけどね」")
                input("そういって私はツタに松明をくべ、辺りを燃やす。")
                input("あなた:「よし、これでは入れる」")
                input("あなたは薄暗く湿った洞窟内部へ足を踏み入れることにした。\n")
                print("========================================\n")
                first+=1
            #===========
            #マップの表示
            #===========
            if nextmap==0:
                print("B1F\tプレイヤー:@\t壁:#")
                
                #二重のループで縦横のマップ表示
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        #マップ情報を更新
                        nowMap[y][x]=map1[y][x]
                        
                        #playerの位置であれば優先的に表示
                        if x==player[0] and y==player[1]:
                            print("@",end="")#  end=""は改行せずに表示させる
                        else:
                            if map1[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")

            if nextmap==1:
                print("B2F\tプレイヤー:@\t壁:#")
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        nowMap[y][x]=map2[y][x]
                        if x==player[0] and y==player[1]:
                            print("@",end="")
                        else:
                            if map2[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")
            if nextmap==2:
                print("B3F\tプレイヤー:@\t壁:#")
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        nowMap[y][x]=map3[y][x]
                        if x==player[0] and y==player[1]:
                            print("@",end="")
                        else:
                            if map3[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")

            #==============
            #プレイヤーの操作
            #==============

            pushKey=input()
            if pushKey=='w':#上
                if nowMap[player[1]-1][player[0]]==0 or nowMap[player[1]-1][player[0]]==3:
                    player[1]-=1
                elif nowMap[player[1]-1][player[0]]==2:
                    print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                else:
                    print("\n*壁だ*\n")

            elif pushKey=='a':#左
                if nowMap[player[1]][player[0]-1]==0 or nowMap[player[1]][player[0]-1]==3:
                    player[0]-=1
                elif nowMap[player[1]][player[0]-1]==2:
                    print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                else:
                    print("\n*壁だ*\n")

            elif pushKey=='d':#右
                if nowMap[player[1]][player[0]+1]==0 or nowMap[player[1]][player[0]+1]==3:
                    player[0]+=1
                elif nowMap[player[1]][player[0]+1]==2:
                    print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                else:
                    print("\n*壁だ*\n")

            elif pushKey=='s':#下
                if nowMap[player[1]+1][player[0]]==0 or nowMap[player[1]+1][player[0]]==3:
                    player[1]+=1
                elif nowMap[player[1]+1][player[0]]==2:
                    print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                else:
                    print("\n*壁だ*\n")

            #ゴールしたか確認
            if nowMap[player[1]][player[0]]==3 and nextmap!=2:
                print("\n階段だ、どうやら下に繋がってるようだ。\n向かいますか\ns:行かない/w:行く")
                pushKey=input()
                if pushKey=='w':
                    if nextmap==0:
                        player[0]=2
                        player[1]=1
                    else:
                        player[0]=4
                        player[1]=1
                    nextmap+=1
                else:
                    player[1]-=1
            elif nowMap[player[1]][player[0]]==3:
                print("\n何かが光っている\n向かいますか\ns:行かない/w:行く")
                pushKey=input()
                if pushKey=='w':
                    scene+=1
                else:
                    player[1]-=1

        case 2:#エンディング
            print("暗く湿った階段を一段一段降りていく。")
            input()
            print("「あっあれは!」")
            input()
            print("光を求めて近づいてみると、そこには大量の宝石や金貨があった")
            input()
            print("「やっっったーーー！」")
            print("GameClear\tEnterキーでタイトルに戻ります")
            input()
            #===================
            #       初期化
            #===================
            nextmap=0
            scene=0
            player[0]=1
            player[1]=1