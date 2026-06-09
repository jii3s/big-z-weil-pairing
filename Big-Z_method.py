"""
Big-Z_method.py

The Big-Z Method: An efficient discovery algorithm for pairing-friendly 
elliptic curves (k=1) using massive torsion primes.

This method efficiently searches for the nearest valid torsion prime r, 
the base prime p, and the curve parameter b for the curve y^2 = x^3 + b.

Author:    Daiji Sanai (big-z / hyler / GitHub: @jii3s)
Date:      2026-06-07
License:   MIT License
Copyright: Copyright (c) 2025 Daiji Sanai. All rights reserved.
"""


########################################################################
#
# Big-Z Method
#  
# Weil Pairing e(Fp,Fp),k=1 用ペアリング曲線の生成プログラム 
#  ※　必要な素数rのサイズを指定する
#                                             
########################################################################
# pip install ecdsa
# pip install sympy (mpmath-1.3.0 sympy-1.13.3)

from ecdsa.ellipticcurve import CurveFp, Point
from sympy import isprime, nextprime

# 平方剰余かどうかオイラー基準テストする
def legendre(a, p):
    if a % p == 0:
        return 0
    else:
        # オイラー基準を使って計算
        return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

# 楕円曲線上の最初の点をみつける
def getNewPoint(curve, x1):         #x1は、探索するx座標の初期値。1でOK
    p = curve.p()
    a = curve.a()
    b = curve.b()
    xx = x1
    uhen = (xx**3 + a * xx + b) % p
    while legendre(uhen, p) != 1:
        xx += 1
        uhen = (xx**3 + a * xx + b) % p     
    # 平方根を計算　mod4=3の素数pに限る
    exponent = (p + 1) // 4
    yy = pow(uhen, exponent, p)        
    return Point(curve,xx, yy)

# ビット数から数を作る
def all_bits_set(n):
    n = int(n)
    # 2のn乗から1を引くことで、nビットすべてが1の数を得る
    return (1 << n) - 1

###############################################################################
# ここからメイン
###############################################################################

# rb = 0xfffffffffffffffffffffffffffffffff00ffffffffff000000000

# キーボードから16進数の文字列を入力
size_input = input("素数rのサイズ(bits): ")
if size_input == "":
    size_input = "256"

zero_input = input("探索開始点の零マスク(bits): ")
if zero_input == "":
    zero_input = "0"

n = int(size_input,10)
m = int(zero_input,10)
# 16進数の文字列を整数に変換
rb = all_bits_set(n) - all_bits_set(m)
print(f"{rb:X}")
# 素数rから素数pを探索する（ブルートフォース）
while True :
    pb = rb * (rb - 1) + 1
    
    if (pb % 12) == 7:       #r*(r-1)+1のmod test
        if isprime(pb) == True:
            break

    pb = pb + rb + rb
    if (pb % 12) == 7:       #r*(r+1)+1のmod test
        if isprime(pb) == True:
            break

    rb = nextprime(rb)      #次の素数rをテスト


####### ここから b を探索（ブルートフォース）
p0 = pb
r0 = rb
a0 = 0
b0 = 3

while True:                         # b=3 からブルートフォーステストする

    # 楕円曲線の定義
    curve = CurveFp(p0, a0, b0) 
    # 点を見つける
    G = getNewPoint(curve,1)
    # ねじれ倍テスト
    result = r0 * G

    if result.x() == None:          #ねじれ倍が無限遠点なら
        break
    b0 += 1

# 見つかった 楕円曲線 をプリント
print(f"\n# **** Weil Pairing 楕円曲線パラメータ {size_input} bits class ****")
print(f"p0 = int(\"{p0:X}\",16)")
print(f"r0 = int(\"{r0:X}\",16)")
print(f"a0 = 0")
print(f"b0 = {b0}\n" ) 


