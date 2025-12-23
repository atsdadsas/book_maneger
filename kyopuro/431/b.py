# import sys
# import io

# # テストしたい入力例をここに貼り付ける
# test_input = """31
# 4
# 15 92 65 35
# 4
# 3
# 1
# 4
# 1
# """

# # 標準入力をこの文字列に置き換える（提出時はここをコメントアウトする）
# sys.stdin = io.StringIO(test_input)
x=int(input())
n=int(input())
w=list(map(int,input().split()))
q=int(input())
ans=x
c=[1]*len(w)
for i in range(q):
    p=int(input())
    if c[p-1]==1:
        c[p-1]=0
        ans=ans+w[p-1]
        print(ans)
    elif c[p-1]==0:
        c[p-1]=1
        ans=ans-w[p-1]
        print(ans)


    