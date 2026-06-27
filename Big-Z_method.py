"""
Big-Z_method.py

The Big-Z Method: An efficient discovery algorithm for pairing-friendly 
elliptic curves (k=1) using massive torsion primes.
Generates parameters p, r, and b for the Weil Pairing e(Fp, Fp).

========================================================================
[Translation Note / 翻訳についての注記]
This code, including comments and CLI prompts, has been translated 
from the original Japanese implementation for global availability. 
The math and logic remain strictly untouched.
========================================================================

Author:    Daiji Sanai (big-z / hyler / GitHub: @jii3z)
Date:      2026-06-12
License:   MIT License
Copyright: Copyright (c) 2026 Daiji Sanai. All rights reserved.
"""

# Required Dependencies:
# pip install ecdsa
# pip install sympy

from ecdsa.ellipticcurve import CurveFp, Point
from sympy import isprime, prevprime

def legendre(a, p):
    """
    Euler's criterion test for quadratic residue.
    """
    if a % p == 0:
        return 0
    else:
        return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

def getNewPoint(curve, x1):
    """
    Finds the first valid point on the elliptic curve.
    x1: Initial x-coordinate to start the search (1 is sufficient).
    """
    p = curve.p()
    a = curve.a()
    b = curve.b()
    xx = x1
    uhen = (xx**3 + a * xx + b) % p
    while legendre(uhen, p) != 1:
        xx += 1
        uhen = (xx**3 + a * xx + b) % p     
    
    # Compute square root modulo p (optimized for primes where p % 4 == 3)
    exponent = (p + 1) // 4
    yy = pow(uhen, exponent, p)        
    return Point(curve, xx, yy)

def all_bits_set(n):
    """
    Generates an integer with all n bits set to 1.
    """
    n = int(n)
    return (1 << n) - 1

###############################################################################
# Main Execution Pipeline
###############################################################################

# CUI Input
size_input = input("Enter target size for torsion prime r (in bits) [Default: 256]: ")
if size_input == "":
    size_input = "256"

n = int(size_input, 10)
rb = all_bits_set(n)

# Step 1: Brute-force search for primes p and r
while True:
    pb = rb * (rb - 1) + 1
    
    if (pb % 12) == 7:       # Modulo test for r*(r-1)+1
        if isprime(pb) == True:
            break

    pb = pb + rb + rb
    if (pb % 12) == 7:       # Modulo test for r*(r+1)+1
        if isprime(pb) == True:
            break

    rb = prevprime(rb)      # Test the next lower prime candidate for r

# Step 2: Brute-force search for curve parameter b
p0 = pb
r0 = rb
a0 = 0
b0 = 3

while True:                 # Test candidates starting from b=3
    # Define the elliptic curve
    curve = CurveFp(p0, a0, b0) 
    
    # Generate a base point
    G = getNewPoint(curve, 1)
    
    # Torsion multiplication test
    result = r0 * G

    if result.x() is None:  # Check if the result is the point at infinity
        break
    b0 += 1

# CUI Output (Prints valid parameters ready for inclusion)
print(f"\n# **** Weil Pairing Elliptic Curve Parameters ({size_input} bits class) ****")
print(f"p0 = int(\"{p0:X}\", 16)")
print(f"r0 = int(\"{r0:X}\", 16)")
print(f"a0 = 0")
print(f"b0 = {b0}\n")