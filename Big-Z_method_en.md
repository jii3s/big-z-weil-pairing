---
author: Daiji Sanai (hyler / @jii3z)
date: 2026-06-07
---

> **Disclaimer / Notice**
> This document has been automatically translated from the original Japanese text. While care has been taken to maintain technical accuracy, some phrasing or terminology may reflect characteristics of automated translation. For rigorous research or implementation purposes, please verify against the original mathematical definitions.

---

# Big-Z Method
# Finding Pairing-Friendly Elliptic Curves $E(\mathbb{F}_p)$
---

The Weil Pairing can sometimes be established even over elliptic curves $E(\mathbb{F}_p)$ defined on a prime base field $\mathbb{F}_p$. 
However, since pairing-friendly curves over $E(\mathbb{F}_p)$ are extremely rare, they must be discovered through custom search methods. 
This document outlines the required conditions and the search strategy for such curves.

### 1. Characteristics of Pairing-Friendly Curves $E(\mathbb{F}_p)$

* There exist $r+1$ subgroups of torsion order $r$.  
  Since the point at infinity $O$ is a single point shared among all groups, the order of the curve $\lvert E \rvert$ is given by:

$$\lvert E \rvert = (r-1)(r+1) + 1$$

*\*Note: The $+1$ accounts for the point at infinity.*

* The order of the curve becomes a perfect square. Setting the cofactor to $h=r$, it yields:

$$\lvert E \rvert = r \times r$$

* Since the embedding degree is $k=1$, the following condition is satisfied:

$$p \pmod r = 1$$

### 2. Parameter Constraints for Practical Implementation

These additional constraints are introduced to improve programming efficiency and computational performance:

* For the prime number $p$:

$$p \pmod 4 = 3$$

*\*Note: This is the prerequisite condition for efficiently computing quadratic residues algebraically.*

* Based on historical data, the relation $h=r$ holds true under the following condition:

$$p \pmod{12} = 7$$

* For the elliptic curve equation $y^2 = x^3 + ax + b$, we set $a=0$. Thus, the curve is defined as:

$$EC: y^2 = x^3 + b$$

* When $k=1$, a small parameter $b$ within the range of $b < 50$ typically exists in over 98% of cases.

### 3. General Approach

* Determine the target prime $r$ based on the required cryptographic security bit-length.
* The order of the elliptic curve is uniquely determined by $\lvert E \rvert = r \times r$.
* According to Hasse's Theorem, the relationship between the curve order $\lvert E \rvert$ and the base prime $p$ must satisfy:

$$| \lvert E \rvert - (p + 1) | \le 2\sqrt{p}$$

$$|r^2 - (p + 1)| \le 2\sqrt{p}$$

* Search for a base prime $p$ that falls within this valid range.
* Once a suitable $p$ is identified, perform a brute-force test on the parameter $b$ to find a curve where $r=h$.
* If no matching prime $p$ is found for the given $r$, select the next prime $r_2$, set $r=r_2$, and repeat the search.

### 4. Accelerated Search Strategy

When aiming for a 256-bit class prime for $r$, the base prime $p$ scales up to a 512-bit class integer. Consequently, optimization techniques are necessary to accelerate the search.

#### 4.1 $k=1$ and Hasse's Theorem

Once the target prime $r$ is chosen, the curve order is fixed at $\lvert E \rvert = r^2$. By applying Hasse's Theorem, the search space for the base prime $p$ is tightly bounded to the following range:

$$r^2 - 2r < p < r^2 + 2r$$

$$r(r-2) < p < r(r+2)$$

Furthermore, due to the $k=1$ embedding degree constraint ($p \pmod r = 1$), $p$ must be a multiple of $r$ plus 1:

$$p = mr + 1$$

As a result, there are only 5 possible candidates for $p$ that fall within the bounds of Hasse's Theorem:

$$r(r-2) + 1$$

$$r(r-1) + 1$$

$$r^2 + 1$$

$$r(r+1) + 1$$

$$r(r+2) + 1$$

Given that $r$ is a prime number, the only two candidates that yield an odd integer for $p$ are:

$$r(r-1) + 1$$

$$r(r+1) + 1$$

##### Only Two Candidates for the Base Prime $p$

When a torsion prime $r$ is specified, primality testing only needs to be performed on the following two points:

$$p_1 = r(r-1) + 1$$

$$p_2 = r(r+1) + 1$$

#### 4.2 Practical Suitability Filtering via $\pmod{12} = 7$

Performing primality tests on 512-bit class integers like $p_1$ and $p_2$ incurs a heavy computational load. To optimize this, a efficiency filter is applied prior to the primality test.

To guarantee that the prime $6x+1$ satisfies $p \pmod 4 = 3$, we apply the following filter:

$$p \pmod{12} = 7$$

*\*The reason for enforcing $p \pmod 4 = 3$ is that it enables a straightforward direct calculation of modular square roots (quadratic residues) required during elliptic curve operations:*

$$a^{\frac{1}{2}} = a^{\frac{p+1}{4}} \pmod p$$

#### 4.3 Primality Testing

If either $p_1$ or $p_2$ passes the primality test, that value is selected as the base prime $p$.

#### 4.4 Fast Search for Elliptic Curve Parameter $b$

Since the parameters $p, r$, the curve order $\lvert E \rvert$, and $a \ (a=0)$ have already been determined, the final step is to discover the remaining parameter $b$.

The search space is defined as:

$$3 \le b \le 50$$

Empirically, a valid $b$ that satisfies the conditions almost always exists within this small range. Thus, a brute-force loop is sufficient to find $b$.

```pascal
function search_b(p, r: BigInt): BigInt;
var
    b: BigInt;
    S, T: ECPoint;
begin
    // Set up EC parameters
    EC.p := p;
    EC.r := r;
    EC.a := 0;                  // Fixed to a=0

    for b := 3 to 50 do         // Expand the range if necessary
    begin
        EC.b := b;              // Update EC parameter b
        S := getECPoint(EC);    // Find a single point on the curve (EC)
        T := ECScalar(S, r);    // Multiply point S by the torsion order r
        if T = Infinity then    // If it maps to the point at infinity, valid b is found.
        begin
            result := b;
            exit;
        end;
    end;

    result := 0;                // Return 0 if not found
end.

```