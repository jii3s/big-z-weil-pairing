"""
WeilPairing_Fp.py

World's first practical implementation of the Weil Pairing over the base field 
F_p x F_p (k=1), enabled exclusively by the parameters discovered through 
the Big-Z Method.

While finding massive pairing-friendly curves with k=1 was previously deemed 
unfeasible, the Big-Z Method successfully solves this challenge, unlocking 
direct Weil pairing computation over F_p without any extension fields.

========================================================================
[Translation Note / 翻訳についての注記]
This code, including comments and CLI prompts, has been translated 
from the original Japanese implementation for global availability. 
The math and logic remain strictly untouched.
========================================================================

Author:     Daiji Sanai (big-z / hyler / GitHub: @jii3z)
Date:       2026-06-09
License:    MIT License
Copyright: Copyright (c) 2026 Daiji Sanai. All rights reserved.
"""

########################################################################
#  Pairing for Weil Pairing e(Fp,Fp), k=1
#  * Pre-set the parameters for the fp1 pairing curve: p0, r0, a0, b0
########################################################################
# pip install ecdsa
# pip install sympy (mpmath-1.3.0 sympy-1.13.3)

from ecdsa.ellipticcurve import CurveFp, Point
# from sympy import isprime, nextprime
from Fp import Fp

###################################################################
# Setup: EC parameter sample (256-bit class)
#   Obtained separately via Big-Z_method.py
p0 = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFAF1D000000000000000000000000000000000000000000000000000000000663AA53", 16)
r0 = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD78F", 16)
a0 = 0
b0 = 18
###################################################################


######   Functions   ######
# Euler's criterion test to check if 'a' is a quadratic residue
def legendre(a):    # a : Fp
    if a.a == 0:
        return 0
    else:
        # Calculate using Euler's criterion
        exponent = (a.p - 1) // 2
        lp = a ** exponent              
        return 1 if lp == 1 else -1
    

# Find the first point on the elliptic curve
def getNewPoint(curve, x1):         # x1 is the initial x-coordinate to search from. 1 is fine.
    
    p = curve.p()
    a = Fp(curve.a(),p)
    b = Fp(curve.b(),p)
    x = Fp(x1,p)

    uhen = x**3 + a * x + b
    while legendre(uhen) != 1:
        x = x + 1
        uhen = x**3 + a * x + b     

    # Calculate square root. Limited to prime p where mod 4 = 3. Error handling is not implemented.
    exponent = (p + 1) // 4
    y = uhen ** exponent        
    return Point(curve,x.a, y.a)      # Point( int , int )


# Convert to bit string for Miller's algorithm
def bit_str(n):
    # Get the bit length of n
    bit_length = n.bit_length()
    # Convert n to a binary string representation, padded with zeros to match the bit length
    bin_str = format(n, '0{}b'.format(bit_length))

    return bin_str      # str      

    
# Slope λ of the line
def calc_slope(P1,P2):
    
    # Since x and y of the elliptic curve points are int, convert them to Fp type
    x1,y1 = Fp(P1.x(),p0) , Fp(P1.y(),p0)
    x2,y2 = Fp(P2.x(),p0) , Fp(P2.y(),p0)

    if P1 == P2:    # x1 == x2 and y1 == y2:
        # If P = Q, calculate the slope of the tangent line
        if y1 == 0:
            raise ValueError("If the y-coordinate is 0, the tangent slope becomes infinite.")
        slope = (3 * (x1**2) + a0) / (2 * y1) 
    else:
        # If P ≠ Q, calculate the slope of the line
        if x1 == x2:
            raise ValueError("The line is vertical. Please select points with different x-coordinates.")
        slope = (y2 - y1) / (x2 - x1)    
    
    return slope        # Fp

# Line l evaluation function
def l(iP,jP,Q):
    
    # Since x and y of the elliptic curve points are int, convert them to Fp type
    iPx,iPy = Fp(iP.x(),p0) ,Fp(iP.y(),p0) 
    jPx,jPy = Fp(jP.x(),p0) ,Fp(jP.y(),p0) 
    Qx,Qy = Fp(Q.x(),p0) ,Fp(Q.y(),p0) 

    if (iPx == jPx) and (iPy != jPy): # At the point at infinity
        line_1 = Fp(1,p0)   # Fp constant 1 as Fp type
    else:
        lamda = calc_slope(iP,jP)
        line_1 = (lamda * (Qx - iPx)) + iPy - Qy    

    return line_1   # Fp

# Vertical line v evaluation function
def v(P,Q):
    # Convert the return value to Fp here, instead of pre-converting to Fp

    if (P.x() == None):  # At the point at infinity
        vert_1 = Fp(1,p0)
    else:       
        vert_1 = Fp(P.x() - Q.x(),p0)
    return vert_1   # Fp

# Weil Pairing one part *** Miller's Algorithm ***
# frP(Q)  r: torsion
def weil_1(r,P,Q):
    str_r0 = bit_str(r)    # Bit string of torsion number r0, e.g., 100010111

    R1 = (r0 // 2) * P      # Generate helper point R1: (r-1)/2 times point
    R2 = (r0 // 2) * Q      # Generate helper point R2: (r-1)/2 times point

    f1 = v(P+R1,(Q+R2)) / l(P,R1,(Q+R2)) * l(P,R1,(R2)) / v(P+R1,(R2))     # Initial value of f: f_{1P}
    f = f1                      # Variable for recursive calculation f 
    T = P                       # Start from P

    # Miller Loop
    for bit_char in str_r0[1:]:     # Loop from the 2nd character to the last (1st character is already processed in f1 calculation)
             
        f =  f * f * l(T,T,(Q+R2)) / v(T+T,(Q+R2)) * v(T+T,(R2)) / l(T,T,(R2))                 
        T = T+T                     # Update T to 2T

        if bit_char == '1':
            f =  f * f1 * l(T,P,(Q+R2)) / v(T+P,(Q+R2)) * v(T+P,(R2)) / l(T,P,(R2)) 
            T = T+P                 # Update T to T+P

    return f   

# Weil Pairing integration
def weil(r,P,Q):    # r: torsion
    e1 = weil_1(r,P,Q) 
    e2 = weil_1(r,Q,P)

    if (e1 == 0) and (e2 == 0):
        e = 1
    else:
        e = e1 / e2
    return e        # Fp

#################################################################################
# Main Execution Test
#################################################################################

# Define the elliptic curve
curve = CurveFp(p0, a0, b0) 
# Find points
G1 = getNewPoint(curve,1)
G2 = getNewPoint(curve, (G1.x() + 1) )      # Try searching for G2 from G1's x-coordinate + 1 to ensure it belongs to a different subgroup

# When p is small, there is a chance that G1 and G2 might accidentally fall into the same subgroup.
# In the same subgroup, the pairing result will be 1.

# Uncomment when testing for the same subgroup
# G2 = 6589 * G1

print(f"Base Point G1: ({G1.x():X}, {G1.y():X})") 
print(f"Base Point G2: ({G2.x():X}, {G2.y():X})") 

e0 = weil(r0,G1,G2)                        # Pairing of base points G1 and G2
print(f"e( G1 , G2 ) = {e0:X}")

if e0 == 1:
    print(f"Error: G1 and G2 might be in the same subgroup") 

# Bilinear test with scalar multiplications: i times and j times
i = 565
j = 1198

e = weil(r0, i * G1, j * G2)               # Pairing with scalar multiplied values (i times and j times)
print(f"e( [{i}]G1 , [{j}]G2 ) = {e:X}")

e = weil(r0, j * G1, i * G2)                # Swap i and j for scalar multiplication
print(f"e( [{j}]G1 , [{i}]G2 ) = {e:X}")

e = e0 ** (i*j)                          # Raise the pairing value of the base points to the power of (i*j)
print(f"e( G1,G2 ) ^ ({i}*{j}) = {e:X}")
