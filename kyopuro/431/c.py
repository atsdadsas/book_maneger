import bisect
# import sys
# import io


# # # テストしたい入力例をここに貼り付ける
# test_input = """12 15 12
# 748 169 586 329 972 529 432 519 408 587 138 249
# 656 114 632 299 984 755 404 772 155 506 832 854 353 465 387

# """
# sys.stdin = io.StringIO(test_input)
ans=0
# n=頭パーツ数、ｍ＝カラダパーツ数、k=作りたいロボット数
n,m,k=map(int,input().split())
# ｈ＝頭の入力
h=list(map(int,input().split()))
# ｂ＝体の入力
b=list(map(int,input().split()))
b.sort()
for i in range(n):
    count = bisect.bisect_left(b, h[i]) 
    ans+=(m-count)
if ans>=k:
    print("Yes")
elif ans<k:
    print("No")


# メモ
# 頭と体のパターンは最大10^18になる


# bisect . bisect_left( b,  h[i] )

# 番号パーツ意味(1)bisectモジュール名。
# 「二分探索（Bisection algorithm）」という便利な機能が詰まった道具箱の名前です。
# これを呼ぶには、コードの最初で import bisect が必要です。(2)bisect_left関数名。
# 道具箱の中にある特定の「技」の名前です。リストの中から、指定した数字が「どこに入るか」を左側から探します。
# (3)b探されるリスト。ここには必ずソート（小さい順に並べ替え）されたリストを入れます。並んでいないと、正しい結果が出ません。
# (4)h[i]探したい数値。今注目している「頭パーツの重さ」など、基準となる数字です。  