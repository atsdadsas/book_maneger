# size =int(input()) 
# for x in range(1, size + 1):
#     row = []
#     for y in range(1, size + 1):
#         if x >= y:
#             if x % 2 == 0:
#                 ans = x**2 - y + 1
#             else:
#                 ans = (x-1)**2 + y
#         else:
#             if y % 2 == 1:
#                 ans = y**2 - x + 1
#             else:
#                 ans = (y-1)**2 + x
#         row.append(ans)
#     print(row)
size = int(input())

# 表を生成
for y in range(1, size + 1):
    row = []
    for x in range(1, size + 1):
        # 以前作成したロジック
        if x >= y:
            if x % 2 == 1:
                ans = x**2 - y + 1
            else:
                ans = (x - 1)**2 + y
        else:
            if y % 2 == 0:
                ans = y**2 - x + 1
            else:
                ans = (y - 1)**2 + x
        
        # 数値を5桁分の幅を確保して右寄せにする（{:>5}）
        # sizeが大きい場合はこの数値を調整してください
        row.append(f"{ans:>4}") 
    
    # リストの中身をスペースで結合して表示
    print(" ".join(row))