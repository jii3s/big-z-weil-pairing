##################################################################
# Fpクラス mod p
#                               2025.5.14 ~ 2025.5.20 Daiji Sanai                                                 
##################################################################
class Fp : 
    def __init__(self, a ,p):
        self.a = ((a % p) + p) %p   # マイナス入力、オーバーフローを補正
        self.p = p

#############################################################
#### 基本演算子のオーバーロード
#############################################################

### neg -x マイナス表記を使えるように 
    def __neg__(op1):
        # 負の要素を計算する
        return Fp(-op1.a, op1.p)

### + add
    def __add__(op1, op2):       # +
        if isinstance(op2, Fp):
            return Fp( (op1.a + op2.a) % op1.p , op1.p )
        elif isinstance(op2, int):
            return Fp( (op1.a + op2) % op1.p , op1.p)  
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2).__name__))
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __radd__(op2, op1):  # 右側のオペランドがFpのときに呼ばれる
        return op2.__add__(op1)  # 通常の__add__メソッドを利用

### sub -
    def __sub__(op1, op2):       # -
        if isinstance(op2, Fp):
            return Fp( (op1.a - (op2.a % op1.p) + op1.p) % op1.p , op1.p )  # アンダーフローを考慮
        if isinstance(op2, int):
            return Fp( (op1.a - (op2 % op1.p) + op1.p) % op1.p , op1.p )  # アンダーフローを考慮
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2).__name__))        
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __rsub__(op2, op1):  # 右辺がFpのときに呼ばれる
        if isinstance(op1, int):
            # op2 - op1.a を計算
            return Fp((op1 - op2.a + op2.p) % op2.p, op2.p)
        raise TypeError("Unsupported operand type(s) for -: '{}' and 'Fp'".format(type(op1).__name__))

### mul *
    def __mul__(op1, op2):       # *
        if isinstance(op2, Fp):
            return Fp( (op1.a * op2.a) % op1.p ,op1.p)          
        elif isinstance(op2, int):
            return Fp( (op1.a * op2) % op1.p ,op1.p)              
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2).__name__))  
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __rmul__(op2, op1):  # 右側のオペランドがFpのときに呼ばれる
        return op2.__mul__(op1)  # 通常の__mul__メソッドを利用

### truediv / 
    def __truediv__(op1, op2):   # / = a * inverse(b) 
        if isinstance(op2, Fp):
            return op1.a * mod_inverse(op2.a,op1.p)            
        if isinstance(op2, int):
            return op1.a * mod_inverse(op2,op1.p)               
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2).__name__))  
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __rtruediv__(op2, op1):  # 右辺がFpのときに呼ばれる
        if isinstance(op1, int):
            # op2 / op1.a を計算するために、逆元を用いて計算
            return mod_inverse(op2.a, op2.p) * op1
        raise TypeError("Unsupported operand type(s) for /: '{}' and 'Fp'".format(type(op1).__name__))

### floordiv //
    def __floordiv__(op1, op2):  # // = a // b :切り捨て
        if isinstance(op2, Fp):
            return Fp( (op1.a // op2.a) ,op1.p)         
        if isinstance(op2, int):
            return Fp( (op1.a // op2) ,op1.p)              
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2).__name__))  
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __rfloordiv__(op2, op1):  # 右辺がFpのときに呼ばれる
        if isinstance(op1, int):
            # op2 // op1.a を計算
            return Fp(op1 // op2.a, op2.p)
        raise TypeError("Unsupported operand type(s) for //: '{}' and 'Fp'".format(type(op2).__name__))

### mod %
    def __mod__(op1,op2):        # % a % b :mod pではなく mod b であることに注意
        if isinstance(op2, Fp):
            return Fp( (op1.a % op2.a) ,op1.p) 
        elif isinstance(op2, int):
            return Fp(op1.a % abs(op2))  # intがマイナスであることを考慮しなければ？ abs(int)でいいのか？
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2)))  
    # 変数型の順序が入れ替わった場合のオーバーロード   
    def __rmod__(op2, op1):  # 右辺がFpのときに呼ばれる
        if isinstance(op1, int):
            return Fp(op1 % op2.a, op2.p)
        raise TypeError("Unsupported operand type(s) for %: '{}' and 'Fp'".format(type(op2)))

### pow **
    def __pow__(op1, op2):       # ** a^b mod p
        if isinstance(op2, Fp):
            return Fp( pow(op1.a,op2.a,op1.p) ,op1.p) 
        elif isinstance(op2, int):
            return Fp( pow(op1.a , op2, op1.p) ,op1.p)  # intは巨大で構わない、最終べき乗などを考慮      
        raise TypeError("Unsupported operand type(s) for +: 'Fp' and '{}'".format(type(op2)))  
    # 変数型の順序が入れ替わった場合のオーバーロード  
    def __rpow__(op1, op2):  # 右辺がFpのときに呼ばれる
        if isinstance(op2, int):
            return Fp(pow(op2, op1.a, op1.p), op1.p)
        raise TypeError("Unsupported operand type(s) for **: '{}' and 'Fp'".format(type(op2)))

### eq ==
    def __eq__(op1, op2):        # == 比較
        if isinstance(op2, Fp):
            return op1.a == op2.a
        elif isinstance(op2, int):
            return op1.a == op2
        return False
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __req__(op1, op2):  # 右側のオペランドがFpのときに呼ばれる
        return op1.__eq__(op2)  # 通常の__eq__メソッドを利用

### ne !=
    def __ne__(op1, op2):        # != 比較（ 
        if isinstance(op2, Fp):
            return op1.a != op2.a 
        if isinstance(op2, int):
            return op1.a != op2
        return False
    # 変数型の順序が入れ替わった場合のオーバーロード    
    def __rne__(op2, op1):  # 右側のオペランドがFpのときに呼ばれる
        return op2.__ne__(op1)  # 通常の__add__メソッドを利用

### set用のハッシュ関数
    def __hash__(self):
        return hash((self.a, self.p))

### Print
    def __repr__(self):
        return f"{self.a}"
    
    def __format__(self, format_spec):
        if format_spec == "X":
            # 16進数表示
            return hex(self.a).upper().replace("0X", "0x")
        else:
            # デフォルトの表示
            return str(self.a)
        
### 組み込み独自関数        
### sqrt a
    def sqrt(self):
        if self.p % 4 ==3:
            res = self ** ((self.p + 1) //4)   # a ^ ((p+1)/4) で直接計算
            return res,-res
        else:
            return tonelli_shanks(self)             # tonelli_shanks探索


#####################################################
#  外部関数 (クラスに組み込むべきか) 
#####################################################

### 拡張ユークリッド互除法を用いて a と b の最大公約数を求める。さらに、x と y を見つける。
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

### 素数 p における a の逆元を求める
def mod_inverse(a, p):
    ## まず、変数をintに統一
    if isinstance(a,Fp):
        aa = a.a
    else:
        aa = a

    if isinstance(p,Fp):
        pp = p.a
    else:
        pp = p

    gcd, x, y = extended_gcd(aa, pp)
    if gcd != 1:
        raise ValueError(f"{aa} の逆元は存在しません。")
    else:
        # x が逆元だが、負の数の可能性があるので正の値にするために p を足す
        return Fp(x , pp)

def tonelli_shanks(fp1):
    """
    トネリ–シュタルム法によって有限体 F_p で平方剰余 a の平方根を求める。

    引数:
    a -- 平方剰余 (a ∈ F_p)
    p -- 素数 (p > 2)

    戻り値:
    (r, -r % p) -- a の平方根 (平方根が存在する場合)
    None -- 平方根が存在しない場合
    """
    if not isinstance(fp1,Fp):
        raise TypeError("Fp型ではありません @tonelli_shanks")

    a = fp1.a       # intに変換
    p = fp1.p       

    # ルジャンドル記号を計算
    def legendre_symbol(a, p):
        return pow(a, (p - 1) // 2, p)

    # 平方剰余であることを確認
    if legendre_symbol(a, p) != 1:
        #raise ValueError(f"{a} is not a quadratic residue modulo {p}")
        return []
    
    # p-1 = q * 2^s を計算
    s = 0
    q = p - 1
    while q % 2 == 0:
        q //= 2
        s += 1

    # 平方非剰余 z を見つける
    z = 2
    while legendre_symbol(z, p) == 1:
        z += 1

    # 初期値の設定
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)  # 整数除算を保証

    # 反復計算
    while t != 1:
        # t^(2^i) ≡ 1 (mod p) となる最小の i を見つける
        t2i = t
        i = 0
        while t2i != 1:
            t2i = pow(t2i, 2, p)
            i += 1

        # 確認: m - i - 1 が負数にならないようにする
        if m - i - 1 < 0:
            raise ValueError("Negative shift count or invalid state encountered during calculation.")

        # 2^(m-i-1) を直接計算せず、逐次更新
        exponent = 1 << (m - i - 1)  # 2^(m-i-1) をビットシフトで計算
        b = pow(c, exponent, p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    
    # 平方根を返す
    res_list = []
    res_list.append(Fp(r,p))
    res_list.append(Fp(-r,p))
    return res_list