"""
WeilPairing_Fp.py

World's first practical implementation of the Weil Pairing over the base field 
F_p x F_p (k=1), enabled exclusively by the parameters discovered through 
the Big-Z Method.

While finding massive pairing-friendly curves with k=1 was previously deemed 
unfeasible, the Big-Z Method successfully solves this challenge, unlocking 
direct Weil pairing computation over F_p without any extension fields.

Author:    Daiji Sanai (big-z / hyler / GitHub: @jii3s)
Date:      2026-06-09
License:   MIT License
Copyright: Copyright (c) 2026 Daiji Sanai. All rights reserved.
"""

########################################################################
#  Weil Pairing e(Fp,Fp),k=1 用ペアリング 
#  ※fp1用のペアリング曲線のパラメータを予めセットする　p0,r0,a0,b0
########################################################################
# pip install ecdsa
# pip install sympy (mpmath-1.3.0 sympy-1.13.3)

from ecdsa.ellipticcurve import CurveFp, Point
# from sympy import isprime, nextprime
from Fp import Fp

###################################################################
# セットアップ　ECパラメータ サンプル (256bit class)
#   別途 Big-Z_method.py で求める
p0 = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFAF1D000000000000000000000000000000000000000000000000000000000663AA53", 16)
r0 = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD78F", 16)
a0 = 0
b0 = 18
###################################################################


######   関数   ######
# aが平方剰余かどうかオイラー基準テストする
def legendre(a):    # a : Fp
    if a.a == 0:
        return 0
    else:
        # オイラー基準を使って計算
        exponent = (a.p - 1) // 2
        lp = a ** exponent              
        return 1 if lp == 1 else -1
    

# 楕円曲線上の最初の点をみつける
def getNewPoint(curve, x1):         #x1は、探索するx座標の初期値。1でOK
    
    p = curve.p()
    a = Fp(curve.a(),p)
    b = Fp(curve.b(),p)
    x = Fp(x1,p)

    uhen = x**3 + a * x + b
    while legendre(uhen) != 1:
        x = x + 1
        uhen = x**3 + a * x + b     

    # 平方根を計算　mod4=3の素数pに限る、エラー処理は未実装
    exponent = (p + 1) // 4
    y = uhen ** exponent        
    return Point(curve,x.a, y.a)      # Point( int ,int )


# ミラーアルゴリズム用ビット文字列変換
def bit_str(n):
    # nのビット長を取得
    bit_length = n.bit_length()
    # nをバイナリ表現の文字列に変換し、ビット長に0を埋めて整形
    bin_str = format(n, '0{}b'.format(bit_length))

    return bin_str      # str      

    
# 直線の傾きλ
def calc_slope(P1,P2):
    
    # 楕円点のx,yがintなので、Fp型に変換
    x1,y1 = Fp(P1.x(),p0) , Fp(P1.y(),p0)
    x2,y2 = Fp(P2.x(),p0) , Fp(P2.y(),p0)

    if P1 == P2:    # x1 == x2 and y1 == y2:
        # P = Qの場合、接線の傾きを計算
        if y1 == 0:
            raise ValueError("y座標が0の場合、接線の傾きは無限大になります。")
        slope = (3 * (x1**2) + a0) / (2 * y1) 
    else:
        # P ≠ Qの場合、直線の傾きを計算
        if x1 == x2:
            raise ValueError("直線が垂直です。異なるx座標を持つ点を選択してください。")
        slope = (y2 - y1) / (x2 - x1)    
    
    return slope        # Fp

# 直線l評価関数
def l(iP,jP,Q):
    
    # 楕円点のx,yがintなので、Fp型に変換
    iPx,iPy = Fp(iP.x(),p0) ,Fp(iP.y(),p0) 
    jPx,jPy = Fp(jP.x(),p0) ,Fp(jP.y(),p0) 
    Qx,Qy = Fp(Q.x(),p0) ,Fp(Q.y(),p0) 

    if (iPx == jPx) and (iPy != jPy): #無限遠点の時
        line_1 = Fp(1,p0)   #Fp 定数1のFp
    else:
        lamda = calc_slope(iP,jP)
        line_1 = (lamda * (Qx - iPx)) + iPy - Qy    

    return line_1   #Fp

# 垂線v評価関数
def v(P,Q):
    # ここは、Fpに事前変換はせずに、戻り値をFp化

    if (P.x() == None):  #無限遠点の時
        vert_1 = Fp(1,p0)
    else:       
        vert_1 = Fp(P.x() - Q.x(),p0)
    return vert_1   # Fp

# Weil Pairing one part *** ミラーアルゴリズム ***
# frP(Q)  r:ねじれ
def weil_1(r,P,Q):
    str_r0 = bit_str(r)    # ねじれ数r0のビット文字列 ex. 100010111

    R1 = (r0 // 2) * P      # 補助点R1の生成　  (r-1)/2 倍点
    R2 = (r0 // 2) * Q      # 補助点R2の生成    (r-1)/2 倍点

    f1 = v(P+R1,(Q+R2)) / l(P,R1,(Q+R2)) * l(P,R1,(R2)) / v(P+R1,(R2))     # fの初期値 f_{1P}
    f = f1                      # 再帰計算用変数 f 
    T = P                       # P からスタート

    # ミラーループ
    for bit_char in str_r0[1:]:     # 2文字目から最後の文字までループ（１文字目はf1計算で処理済の為）
             
        f =  f * f * l(T,T,(Q+R2)) / v(T+T,(Q+R2)) * v(T+T,(R2)) / l(T,T,(R2))                 
        T = T+T                     # Tを2Tで更新

        if bit_char == '1':
            f =  f * f1 * l(T,P,(Q+R2)) / v(T+P,(Q+R2)) * v(T+P,(R2)) / l(T,P,(R2)) 
            T = T+P                 # TをT+Pで更新

    return f   

# Weil Pairing 統合
def weil(r,P,Q):    # r:ねじれ
    e1 = weil_1(r,P,Q) 
    e2 = weil_1(r,Q,P)

    if (e1 == 0) and (e2 == 0):
        e = 1
    else:
        e = e1 / e2
    return e        # Fp

#################################################################################
# ここから、実行テストのメイン
#################################################################################

# 楕円曲線の定義
curve = CurveFp(p0, a0, b0) 
# 点を見つける
G1 = getNewPoint(curve,1)
G2 = getNewPoint(curve, (G1.x() + 1) )      # 違うサブグループになるように G1のｘ座標+1 から G2 を探索してみる

# pが小さいとき、G1,G2が偶然同じグループになる可能性がある。
# 同じグループの時ペアリング結果は１

# 同じグループをテストする場合にコメントアウト
# G2 = 6589 * G1

print(f"原点G1: ({G1.x():X}, {G1.y():X})") 
print(f"原点G2: ({G2.x():X}, {G2.y():X})") 

e0 = weil(r0,G1,G2)                        # 原点G1,G2のペアリング
print(f"e( G1 , G2 ) = {e0:X}")

if e0 == 1:
    print(f"エラー： G1、G2 が同じサブグループの可能性あり") 

# スカラー倍 i倍,j倍で双線形テスト
i = 565
j = 1198

e = weil(r0, i * G1, j * G2)               # スカラー倍、i倍、j倍値でペアリング
print(f"e( [{i}]G1 , [{j}]G2 ) = {e:X}")

e = weil(r0, j * G1, i * G2)                # スカラー倍 iとjを入れ替える
print(f"e( [{j}]G1 , [{i}]G2 ) = {e:X}")

e = e0 ** (i*j)                         # 原点のペアリング値を i*j乗
print(f"e( G1,G2 ) ^ ({i}*{j}) = {e:X}")