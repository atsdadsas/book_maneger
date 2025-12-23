#===================================
#           失敗例
#   1:プログラムにおける欠点
#       1:[操作要求]の部分が長い
#       2:コメントが少ない(なにをしてるのか他の人が分からない)
#   2:消費者視点の欠点
#       1:操作方法がない
#       2:ストーリー何もわからず、終わる
#           ->楽しくない
#
#===================================


scene=0
choice=0
pushKey=0
player=[1,1,0]#プレイヤーのx座標とy座標と向き
mapSize_x=6
mapSize_y=6
nextmap=0

#マップ
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

while(1):
    match(scene):
        #=====================
        #       タイトル
        #=====================
        case 0:
            if choice==0:
                print("\n秘宝を狙え\nダンジョン探索記\n\n攻略開始<-\n探索終了\n")
            else:
                print("\n秘宝を狙え\nダンジョン探索記\n\n攻略開始\n探索終了<-\n")
            pushKey=input()
            if pushKey=='s' and choice!=1:
                choice+=1
            elif pushKey=='w' and choice!=0:
                choice-=1
            else:
                if choice == 0:
                    scene=1
                else:
                    print("じゃぁね～\n")
                    break
        #======================
        #       プレイ画面
        #======================
        case 1:
            if player[2]==0:
                print("1F\tプレイヤー:@\t壁:#")
            if nextmap==0:
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        if x==player[0] and y==player[1]:
                            print("@",end="")
                        else:
                            if map1[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")
            if nextmap==1:
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        if x==player[0] and y==player[1]:
                            print("@",end="")
                        else:
                            if map2[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")
            if nextmap==2:
                for y in range(0,mapSize_y,1):
                    for x in range(0,mapSize_x,1):
                        if x==player[0] and y==player[1]:
                            print("@",end="")
                        else:
                            if map3[y][x]==1:
                                print("#",end="")
                            else:
                                print(" ",end="")
                    print("")
            
            #操作要求
            pushKey=input()
            if pushKey=='w':
                if nextmap==0:
                    if map1[player[1]-1][player[0]]==0 or map1[player[1]-1][player[0]]==3:
                        player[1]-=1
                    elif map1[player[1]-1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                if nextmap==1:
                    if map2[player[1]-1][player[0]]==0 or map2[player[1]-1][player[0]]==3:
                        player[1]-=1
                    elif map2[player[1]-1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                if nextmap==2:
                    if map3[player[1]-1][player[0]]==0 or map3[player[1]-1][player[0]]==3:
                        player[1]-=1
                    elif map3[player[1]-1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
            elif pushKey=='a':
                if nextmap==0:
                    if map1[player[1]][player[0]-1]==0 or map1[player[1]][player[0]-1]==3:
                        player[0]-=1
                    elif map1[player[1]][player[0]-1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                elif nextmap==1:
                    if map2[player[1]][player[0]-1]==0 or map2[player[1]][player[0]-1]==3:
                        player[0]-=1
                    elif map2[player[1]][player[0]-1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                elif nextmap==2:
                    if map3[player[1]][player[0]-1]==0 or map3[player[1]][player[0]-1]==3:
                        player[0]-=1
                    elif map3[player[1]][player[0]-1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
            elif pushKey=='d':
                if nextmap==0:
                    if map1[player[1]][player[0]+1]==0 or map1[player[1]][player[0]+1]==3:
                        player[0]+=1
                    elif map1[player[1]][player[0]+1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                elif nextmap==1:
                    if map2[player[1]][player[0]+1]==0 or map2[player[1]][player[0]+1]==3:
                        player[0]+=1
                    elif map2[player[1]][player[0]+1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                elif nextmap==2:
                    if map3[player[1]][player[0]+1]==0 or map3[player[1]][player[0]+1]==3:
                        player[0]+=1
                    elif map3[player[1]][player[0]+1]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
            elif pushKey=='s':
                if nextmap==0:
                    if map1[player[1]+1][player[0]]==0 or map1[player[1]+1][player[0]]==3:
                        player[1]+=1
                    elif map1[player[1]+1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                if nextmap==1:
                    if map2[player[1]+1][player[0]]==0 or map2[player[1]+1][player[0]]==3:
                        player[1]+=1
                    elif map2[player[1]+1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
                elif nextmap==2:
                    if map3[player[1]+1][player[0]]==0 or map3[player[1]+1][player[0]]==3:
                        player[1]+=1
                    elif map3[player[1]+1][player[0]]==2:
                        print("\n*財宝見つけるまで帰るわけにはいかねぇ*\n")
                    else:
                        print("\n*壁だ*\n")
            #ゴールしたか確認
            if map1[player[1]][player[0]]==3 and nextmap==0:
                print("\n階段だ、どうやら下に繋がってるようだ。\n向かいますか\ns:行かない/w:行く")
                pushKey=input()
                if pushKey=='w':
                    nextmap+=1
                    player[0]=2
                    player[1]=1
                elif pushKey=='s':
                    player[1]-=1
            elif map2[player[1]][player[0]]==3 and nextmap==1:
                print("\n階段だ、どうやら下に繋がってるようだ。\n向かいますか\ns:行かない/w:行く")
                pushKey=input()
                if pushKey=='w':
                    nextmap+=1
                    player[0]=4
                    player[1]=1
                elif pushKey=='s':
                    player[1]-=1
            elif map2[player[1]][player[0]]==3 and nextmap==2:
                print("\n何かが光っている\n向かいますか\ns:行かない/w:行く")
                pushKey=input()
                if pushKey=='w':
                    scene+=1
                elif pushKey=='s':
                    player[1]-=1
        case 2:
            print("暗く湿った階段を一段一段降りていく。")
            input()
            print("「あっあれは!」")
            input()
            print("光を求めて近づいてみると、そこには伝説と言われた宝庫があった")
            input()
            print("「黄金色のブレスレットにエメラルドやルビーまである」")
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