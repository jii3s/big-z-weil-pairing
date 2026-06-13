---
author: Daiji Sanai (hyler / @jii3s)
date: 2026-06-07
---

> **Disclaimer / Notice**
> This document has been automatically translated from the original Japanese text. While care has been taken to maintain technical accuracy, some phrasing or terminology may reflect characteristics of automated translation. For rigorous research or implementation purposes, please verify against the original mathematical definitions.

---

# Weil Pairing

## 1. Definition

### 1.1 Fundamental Definition
### $$e(P,Q)=\dfrac{f_P(A_Q)}{f_Q(A_P)}$$

* Find the rational function $f_P$ representing the point $P$, evaluate it at the divisor $A_Q$ representing the point $Q$, and set this calculated value as the numerator.
* Find the rational function $f_Q$ representing the point $Q$, evaluate it at the divisor $A_P$ representing the point $P$, and set this calculated value as the denominator.
* The resulting value of this fraction constitutes the Weil Pairing value ${e(P,Q)}$.

However:
* $P$ and $Q$ must belong to distinct $n$-torsion subgroups. Pairing cannot be established between points within the same elliptic $n$-torsion subgroup.
* On standard elliptic curves, only a single $n$-torsion group exists, which makes pairing impossible.
* Discovering elliptic curves that possess multiple $n$-torsion groups is a non-trivial and critical challenge.
* In the Tate Pairing, which brought the Weil Pairing into practical application, extension fields are utilized to artificially construct these multiple required groups.
* ##### The Weil Pairing is defined not only over elliptic curves over finite fields $\mathbb{F}_p$ but across all elliptic curves, including those over real numbers. This is a fundamental distinction from the Tate Pairing.
* ##### In practical applications, due to computational complexity, the evaluation of the Weil Pairing is typically restricted to finite fields rather than infinite fields (such as rational or real numbers). This document will also assume finite fields for specific computational explanations.

### 1.2 Input and Output Ranges

### $e_n: E[n] \times E[n] \to \mu_n$

* $E[n]$: The group of elliptic points with a torsion order of $n$.
* The first $E[n]$ and the second $E[n]$ must belong to distinct $n$-torsion cyclic subgroups.
* $\mu_n$: The group of $n$-th roots of unity (values that yield $1$ when raised to the power of $n$).
* ##### Raising the pairing calculation result to the power of $n$ always yields 1. $\Rightarrow$ This is a mandatory condition for bilinearity.

---

## 2. Divisor
### 2.1 Basic Divisors $A_P$
Let us define the divisors $A_P$ and $A_Q$ representing the points $P$ and $Q$ on the elliptic curve as follows:
* $A_P=[P]-[O]$
* $A_Q=[Q]-[O]$

### 2.2 Alternative Divisors $D_P$

The divisors representing the points $P$ and $Q$ on the elliptic curve can also be defined alternatively as:

* $D_P=[P+R_1]-[R_1]$
* $D_Q=[Q+R_2]-[R_2]$

* Using the relationship between the elliptic curve and its intersecting lines, these can be derived via divisors representing $P$ and the helper point $R_1$:
    * $[l]:[P]+[R_1]+[-(P+R_1)]-3[O]=0$
    * $[v]:[P+R_1]+[-(P+R_1)]-2[O]=0$
    * $[l/v]:[P]+[R_1]+[-(P+R_1)]-3[O]-[P+R_1]-[-(P+R_1)]+2[O]$
    * $[P]-[O]+[R_1]-[P+R_1]=0$  
      $[P]-[O]=[P+R_1]-[R_1]$

### 2.3 Equivalence of $A_P$ and $D_P$
#### [Theorem] Two divisors are equivalent when their difference is a principal divisor.

Calculating the difference between $D_P$ and $A_P$ yields:
* $D_P-A_P=\underline{[P+R_1]-[R_1]-[P]+[O]}$ $\leftarrow$ Principal Divisor
* $D_P \sim A_P$

Therefore, the initially defined basic divisor $A_P=[P]-[O]$ can be substituted with $D_P$:

* $A_P=[P]-[O] \sim [P+R_1]-[R_1]$
* $A_Q=[Q]-[O] \sim [Q+R_2]-[R_2]$

### 2.4 Transformation of the Definition Equation
Let us focus strictly on the numerator portion of the Weil Pairing definition and transform the equation. (The denominator can be transformed identically by swapping P and Q).

$$
\begin{align*}
f_P(A_Q)&=f_P(D_Q)\\
&=f_P ([Q+R_2]-[R_2])\\
&=\dfrac{f_P([Q+R_2])}{f_P([R_2])}\\
&=\dfrac{f_P(Q+R_2)}{f_P(R_2)}
\end{align*}
$$

*Note: Since the divisors $[Q+R_2]$ and $[R_2]$ are decomposed into single points, we can use the "point values" instead of the divisors themselves when evaluating them in the rational function.  
As a result of transforming the arguments into points, it becomes clear that if we can determine the rational function $f_P$, we can compute it directly by substituting the concrete coordinate values $x, y$ of $Q$ and $R_2$.

---
## 3. Searching for Rational Functions
In order to realize the Weil Pairing, it is necessary to find the rational function $f_P$ that represents the point $P$.

##### [Theorem]
##### A rational function corresponding to a given divisor expression exists if and only if the divisor expression satisfies the following two conditions:
1. The degree of the divisor expression is 0.
2. Summing up the points in the divisor expression (by removing the brackets $[ ]$ and performing elliptic curve group addition) yields the point at infinity $O$.

### 3.1 Basic Rational Functions

A rational function that corresponds directly to the basic divisor $A_P = [P] - [O]$ representing $P$ does not exist.
* Although its degree is 0, the elliptic curve addition $P - O$ does not equal $O$.

However, multiplying $A_P$ by $n$ allows it to satisfy the conditions, guaranteeing the existence of a corresponding rational function (where $n$ is the torsion order).

$$\begin{align*}
A_P &= [P] - [O] \\
nA_P &= n[P] - n[O] \quad \dots \text{(multiplied by } n\text{)} \\
[f_P] &= n[P] - n[O]
\end{align*}$$

Thus, we define the rational function $f_P$ representing the target point $P$ to be searched as:

$$[f_P] = n[P] - n[O]$$

### 3.2 Divisors of Lines

It is a well-known fact that geometric lines intersecting an elliptic curve can be expressed as functions:
* Line $l: y = ax + b$
* Vertical line $v: x = c$

Expressing these lines $l$ and $v$ as divisor expressions yields:
* $[l] = [P] + [R_1] + [-(P+R_1)] - 3[O]$
* $[v] = [P+R_1] + [-(P+R_1)] - 2[O]$

### 3.3 Principal Divisor of Point $iP$ [The $i$-th Multiple of Point $P$]

Based on the definitions of divisors $A_P$ and $D_P$ representing point $P$, let us derive the divisor representing the point $iP$ (the $i$-th multiple of point $P$).

The definition of divisor $D_P$ is:

$$D_P = [P+R_1] - [R_1]$$

Multiplying this divisor $D_P$ by $i$ gives:

$$iD_P = i[P+R_1] - i[R_1]$$

Additionally, substituting with the point $S = iP$, the divisor $A_S$ is expressed as:

$$A_S = [S] - [O]$$

Restoring $S$ back to its original form $iP$ yields:

$$A_{iP} = [iP] - [O]$$

Since $A_{iP} \sim iD_P$ (linearly equivalent), their difference forms a principal divisor. Therefore, the function $f_{iP}$ representing the point $iP$ can be defined by the following divisor expression:

$$[f_{iP}] = i[P+R_1] - i[R_1] - [iP] + [O]$$

### 3.4 Principal Divisor of Point $nP$

Let us evaluate $[f_{nP}]$ for the $n$-torsion point where $i = n$.

$$\begin{align*}
[f_{nP}] &= n[P+R_1] - n[R_1] - [nP] + [O] \\
&= n[P+R_1] - n[R_1] - [O] + [O] \quad (\because nP = O) \\
&= n[P+R_1] - n[R_1]
\end{align*}$$

On the other hand, multiplying $D_P = [P+R_1] - [R_1]$ by $n$ yields:

$$nD_P = n[P+R_1] - n[R_1]$$

Consequently, $[f_{nP}]$ and $nD_P$ share the identical value:

$$[f_{nP}] = nD_P$$

Furthermore, since $D_P$ and $A_P$ are linearly equivalent as principal divisors:

$$[f_{nP}] = nA_P$$

By the definition of scalar multiplication of divisors, $nA_P$ is expressed as:

$$nA_P = n[P] - n[O]$$

The standard definition for the divisor (principal divisor) of the function $f_P$ is given by:

$$(f_P) = n[P] - n[O]$$

Thus, $(f_P)$ is equal to $nA_P$, which ultimately means it equals $[f_{nP}]$.

$$(f_P) = nA_P = nD_P = [f_{nP}]$$

$$f_P = f_{nP}$$

This demonstrates that the rational function $f_P$ required for the pairing computation is mathematically identical to $f_{nP}$.

$$f_P = f_{nP}$$

### 3.5 Searching for the Rational Function $f_{nP}$
The divisors of the functions representing the $i$-th multiple of $P$ and the $j$-th multiple of $P$ are defined respectively as follows:

$$[f_{iP}] = i[P+R_1] - i[R_1] - [iP] + [O]$$

$$[f_{jP}] = j[P+R_1] - j[R_1] - [jP] + [O]$$

When multiplying $f_{iP}$ and $f_{jP}$, the resulting divisor becomes the sum of their individual divisors:

$$\begin{align*}
[{f_{iP}f_{jP}}] &= i[P+R_1] - i[R_1] - [iP] + [O] + j[P+R_1] - j[R_1] - [jP] + [O] \\
&= (i+j)[P+R_1] - (i+j)[R_1] - [iP] - [jP] + 2[O]
\end{align*}$$

Next, the divisor of the line function passing through both $iP$ and $jP$ is:

$$[l_{iP,jP}] = [iP] + [jP] + [-(i+j)P] - 3[O]$$

Furthermore, the divisor of the vertical line function passing through the point $[i+j]P$ is:

$$[v_{(i+j)P}] = [(i+j)P] + [-(i+j)P] - 2[O]$$

Now, let us compute the divisor for the following combined rational function $[f_{iP}f_{jP}\dfrac{l_{iP,jP}}{v_{(i+j)P}}]$:

$$\begin{align*}
[f_{iP}f_{jP}\dfrac{l_{iP,jP}}{v_{(i+j)P}}] &= (i+j)[P+R_1] - (i+j)[R_1] - [iP] - [jP] + 2[O] \\
&\quad + [iP] + [jP] + [-(i+j)P] - 3[O] \\
&\quad - [(i+j)P] - [-(i+j)P] + 2[O]
\end{align*}$$

By organizing and canceling out the matching terms, we get:

$$= (i+j)[P+R_1] - (i+j)[R_1] - [(i+j)P] + [O]$$

Conversely, by definition, the divisor of the function representing the $(i+j)$-th multiple of point $P$ is:

$$[f_{(i+j)P}] = (i+j)[P+R_1] - (i+j)[R_1] - [(i+j)P] + [O]$$

This proves that $[f_{iP}f_{jP}\dfrac{l_{iP,jP}}{v_{(i+j)P}}]$ matches $[f_{(i+j)P}]$ exactly.

Therefore:

$$f_{(i+j)P} = f_{iP}f_{jP}\dfrac{l_{iP,jP}}{v_{(i+j)P}}$$

This recursive formula indicates that if we can determine $f_{1P}$, we can compute $f_{nP}$ step-by-step through recursive calculations.

### 3.6 Deriving $f_{1P}$
*\*Note: Strictly speaking, we need to evaluate $f_{1P}(A_Q)$.*

First, by definition, $f_{iP}$ is given by:

$$[f_{iP}] = i[P+R_1] - i[R_1] - [iP] + [O]$$

Setting $i=1$ yields $f_{1P}$:

$$[f_{1P}] = [P+R_1] - [R_1] - [P] + [O]$$

Meanwhile, the divisor of the line $l_{P,R_1}$ passing through point $P$ and point $R_1$ is:

$$[l_{P,R_1}] = [P] + [R_1] + [-(P+R_1)] - 3[O]$$

And the divisor of the vertical line $v_{P+R_1}$ passing through the point $[P+R_1]$ is:

$$[v_{P+R_1}] = [P+R_1] + [-(P+R_1)] - 2[O]$$

Computing the divisor of the rational function obtained by dividing the vertical line $v$ by the line $l$ gives:

$$[\dfrac{v_{P+R_1}}{l_{P,R_1}}] = [P+R_1] - [R_1] - [P] + [O]$$

This perfectly matches $[f_{1P}]$. Thus, we have:

$$f_{1P} = \dfrac{v_{P+R_1}}{l_{P,R_1}}$$

More precisely, since we evaluate this function by substituting the divisor $A_Q$:

$$f_{1P}(A_Q) = \dfrac{v_{P+R_1}(A_Q)}{l_{P,R_1}(A_Q)}$$

Since $A_Q$ can be substituted with $D_Q = [Q+R_2] - [R_2]$, the equation transforms as follows:

$$\begin{align*}
f_{1P}(A_Q) &= \dfrac{v_{P+R_1}([Q+R_2]-[R_2])}{l_{P,R_1}([Q+R_2]-[R_2])} \\
&= \dfrac{v_{P+R_1}([Q+R_2]) / v_{P+R_1}([R_2])}{l_{P,R_1}([Q+R_2]) / l_{P,R_1}([R_2])} \\
&= \dfrac{v_{P+R_1}([Q+R_2])}{l_{P,R_1}([Q+R_2])} \cdot \dfrac{l_{P,R_1}([R_2])}{v_{P+R_1}([R_2])}
\end{align*}$$

Abbreviating the notation yields:

$$\begin{align*}
f_{1P}(A_Q) &= \dfrac{v([Q+R_2])}{l([Q+R_2])} \cdot \dfrac{l([R_2])}{v([R_2])} \\
&= \dfrac{v(Q+R_2)}{l(Q+R_2)} \cdot \dfrac{l(R_2)}{v(R_2)}
\end{align*}$$

*\*Note: Since the divisors $[Q+R_2]$ and $[R_2]$ are fully decomposed into prime divisors representing specific "points", we can directly substitute the actual coordinate values of the points into the rational function instead of evaluating the divisors abstractly.*

Because the $(x, y)$ coordinate values for $P, Q, R_1$, and $R_2$ are all known, the value of $f_{1P}(A_Q)$ can be directly computed over a finite field using basic arithmetic:

* The coefficients of the line function $l and vertical line function $v$ (such as the slope $\lambda$ and y-intercept $\nu$) are determined using the $(x, y)$ coordinates of $P$ and $R_1$.
* The coordinates for the point $(Q+R_2)$ can be mechanically derived using the standard elliptic curve addition formulas (group law).
* Finally, the evaluation is completed by substituting the specific $(x, y)$ coordinates of the two points $(Q+R_2)$ and $R_2$ into the derived functions $l$ and $v$ and performing modular arithmetic.

## 4. Concrete Computation Method
When computing the Weil Pairing in practice, assume that the following four points are already given:
* $P = (P.x, P.y)$
* $R_1 = (R_1.x, R_1.y)$
* $Q = (Q.x, Q.y)$
* $R_2 = (R_2.x, R_2.y)$

If $R_1$ and $R_2$ are not provided, empirical results show that selecting them using the following formulas consistently ensures that bilinearity holds true:
* $R_1 = (\dfrac{n-1}{2})P$
* $R_2 = (\dfrac{n-1}{2})Q$

### 4.1 Evaluation of Lines $l$ and $v$
#### 4.1.1 The Line $l_{iP,jP}$

$l_{iP,jP}$ is the line passing through the points $iP$ and $jP$. Let the variables for the coordinates be $X$ and $Y$.

The Weierstrass equation of the elliptic curve is:

$$Y^2 = X^3 + aX + b$$

The standard equation for the line is:

$$Y = \lambda X + \nu$$

The slope $\lambda$ is computed as follows:

$$\lambda = \dfrac{\Delta y}{\Delta x}$$

$$\lambda = \dfrac{(jP)_y - (iP)_y}{(jP)_x - (iP)_x}$$

*\*Note: If $(iP)$ and $(jP)$ are the exact same point, the line becomes a "tangent line" to the curve. In this case, the slope $\lambda$ is derived using implicit differentiation:*

$$\lambda = \dfrac{3 \{(iP)_x\}^2 + a}{2 (iP)_y}$$

Next, the y-intercept $\nu$ is expressed as:

$$\nu = Y - \lambda X$$

Substituting the coordinates of point $(iP)$ into $X$ and $Y$ yields:

$$\nu = (iP)_y - \lambda (iP)_x$$

Therefore, the equation for the target line $l$ is:

$$Y = \lambda X + (iP)_y - \lambda (iP)_x$$

Moving $Y$ to the right-hand side gives:

$$0 = \lambda X + (iP)_y - \lambda (iP)_x - Y$$

Consequently, the line function $l$ used as a rational function for evaluation is defined as:

$$l: \quad \lambda X + (iP)_y - \lambda (iP)_x - Y$$

For example, when substituting point $Q$ into this function, the evaluated value $l(Q)$ is computed as:

$$l(Q) = \lambda Q_x + (iP)_y - \lambda (iP)_x - Q_y$$

**$$l(Q) = \lambda (Q_x - (iP)_x) + (iP)_y - Q_y$$**

#### 4.1.2 The Vertical Line $v_{[i+j]P}$

The line $v_{(i+j)P}$ represents a vertical line passing through the point $[i+j]P$ on the elliptic curve.

By first computing the point $T = iP + jP$ via the elliptic curve group addition law, the formula for the vertical line is given by:

$$X = T.x$$

Moving $X$ to the right-hand side yields:

$$0 = T.x - X$$

Thus, the corresponding rational function $v$ is:

$$v: \quad T.x - X$$

When evaluating this function $v$ at a specific point $Q$, it is computed as:

**$$v(Q) = (iP + jP).x - Q.x$$**

As shown, the functions $l(Q)$ and $v(Q)$ can be evaluated numerically directly from the actual coordinate values of each point.

---
### 4.2 How to Compute the Value of $f_{nP}(A_Q)$
*\*Note: $f_{nQ}(A_P)$ can be derived using the identical procedure.*

As described in the previous section, the value of $f_{1P}$ can be computed numerically using the specific $(x, y)$ coordinate values of each point:
* $f_{1P}$
* Points $P, Q, R_1, R_2$

Additionally, the following line functions (and their coefficients) can also be determined once the $(x, y)$ coordinates of each point are known:
* $l_{P,R_1}()$
* $v_{P+R_1}()$

By applying these principles and starting from $f_{1P}$ as the base case, we can compute $f_{nP}$ through recursive calculations.

#### 4.2.1 Recursive Formula
The Weil Pairing calculation is performed by leveraging the recursive formula derived earlier:

$$f_{(i+j)P} = f_{iP} f_{jP} \dfrac{l_{iP,jP}}{v_{(i+j)P}} \quad \text{(Abbreviated Notation)}$$

In practice, since we substitute the divisor $A_Q$ (or its equivalent $D_Q$) representing the point $Q$ into the function, the recursive formula becomes:

$$f_{(i+j)P} = f_{iP} f_{jP} \dfrac{l_{iP,jP}(A_Q)}{v_{(i+j)P}(A_Q)}$$  

Specifically, by substituting $D_Q$ and transforming the equation, the concrete recursive formula used for implementation is given by:

$${f_{(i+j)P} = f_{iP} f_{jP} \dfrac{l_{iP,jP}(Q+R_2)}{v_{(i+j)P}(Q+R_2)} \cdot \dfrac{v_{(i+j)P}(R_2)}{l_{iP,jP}(R_2)}}$$

<br>

#### 4.2.2 Naive Recursive Concept
Although this approach is computationally infeasible for real-world cryptographic applications, the conceptual framework dictates that since $f_{1P}$ is known, $f_{nP}$ can (theoretically) be obtained by repeatedly accumulating additions:

1. $f_{1P}$ $\leftarrow$ Known Base Case

2. $f_{2P} = f_{(1+1)P} = f_{1P} f_{1P} \dfrac{l_{1P,1P}(Q+R_2)}{v_{2P}(Q+R_2)} \cdot \dfrac{v_{2P}(R_2)}{l_{1P,1P}(R_2)}$

3. $f_{3P} = f_{(1+2)P} = f_{1P} f_{2P} \dfrac{l_{1P,2P}(Q+R_2)}{v_{3P}(Q+R_2)} \cdot \dfrac{v_{3P}(R_2)}{l_{1P,2P}(R_2)}$

4. $f_{4P} = f_{(1+3)P} = f_{1P} f_{3P} \dfrac{l_{1P,3P}(Q+R_2)}{v_{4P}(Q+R_2)} \cdot \dfrac{v_{4P}(R_2)}{l_{1P,3P}(R_2)}$

5. < Repeat Loop >

6. $f_{nP} = f_{(1+(n-1))P} = f_{1P} f_{(n-1)P} \dfrac{l_{1P,(n-1)P}(Q+R_2)}{v_{nP}(Q+R_2)} \cdot \dfrac{v_{nP}(R_2)}{l_{1P,(n-1)P}(R_2)}$

<br>

### 4.3 Miller's Algorithm

Miller's Algorithm is widely used to accelerate the recursive computation of $f_{nP}$.  
By expanding the torsion order $n$ into its binary representation and performing a sequence of double-and-add operations, it significantly speeds up the recursive calculation.

Example: When $n = 83$  
The binary representation of 83 is `1010011`.  
Processing this binary sequence from the most significant bit (MSB) to the least significant bit (LSB), the algorithm performs repeated doubling and adding to compute the recursion up to 83.

| n = 83 | bin $\to$ | 1 | 0 | 1 | 0 | 0 | 1 | 1 |  
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $iP$ | Carry down | $O$ | $2P$ | $4P$ | $10P$ | $20P$ | $40P$ | $82P$ |
| $jP$ | $\small{1P \times \text{bit}}$ | $1P$ | $O$ | $1P$ | $O$ | $O$ | $1P$ | $1P$ |
| $(i+j)P$ | Addition Point | $\scriptsize{(0+1)P}$ | $\scriptsize{(2+0)P}$ | $\scriptsize{(4+1)P}$ | $\scriptsize{(10+0)P}$ | $\scriptsize{(20+0)P}$ | $\scriptsize{(40+1)P}$ | $\scriptsize{(82+1)P}$ |
| $\small{(i+j)P \times 2}$ | Doubled Point <br>new $iP$ | $2P$ | $4P$ | $10P$ | $20P$ | $40P$ | $82P$ | $83P$ |

##### \*Note: If the point at infinity $O$ appears during the evaluation of $l$ and $v$, standard calculation methods cannot be applied. In such scenarios, the evaluated result is defined to be "1":
* $v_\infty(Q) = 1$
* $l_\infty(Q) = 1$

```python
# Weil Pairing part 1 *** Miller's Algorithm ***
def weil_1(P, Q):
    str_r0 = bit_str(r0)    # Binary string representation of the torsion order r0 (e.g., "100010111")

    R1 = (r0 // 2) * P      # Generate helper point R1
    R2 = (r0 // 2) * Q      # Generate helper point R2

    # Initial value of f: f_{1P}
    f1 = v(P+R1, (Q+R2)) / l(P, R1, (Q+R2)) * l(P, R1, (R2)) / v(P+R1, (R2))     
    f = f1                  # Variable f for recursive computation
    T = P                   # Start from point P

    # Miller Loop
    for bit_char in str_r0[1:]:     # Loop from the 2nd bit to the last bit (1st bit is already processed in f1)
             
        f = f * f * l(T, T, (Q+R2)) / v(T+T, (Q+R2)) * v(T+T, (R2)) / l(T, T, (R2))                 
        T = T + T                   # Update T to 2T (Doubling step)

        if bit_char == '1':
            f = f * f1 * l(T, P, (Q+R2)) / v(T+P, (Q+R2)) * v(T+P, (R2)) / l(T, P, (R2)) 
            T = T + P               # Update T to T + P (Addition step)

    return f

```

---
## Appendix: Interpretation of the Formula

$$
\dfrac{v([Q+R_2])}{l([Q+R_2])} \times \dfrac{l([R_2])}{v([R_2])}
$$

The following explains the mathematical reasoning behind why the equation above can be computed identically using the following simplified point-evaluation form:

$$
\dfrac{v(Q+R_2)}{l(Q+R_2)} \times \dfrac{l(R_2)}{v(R_2)}
$$

### Divisors and Rational Functions

1. **The Role of a Divisor**:
   - A divisor is a formal sum of points on an elliptic curve, uniquely characterizing the zeros and poles of a specific rational function.
   - Each divisor explicitly maps the complete configuration of these zeros and poles for its corresponding function.

2. **Function Evaluation**:
   - Evaluating the line functions $v$ or $l$ at a concrete point such as $(Q + R_2)$ or $R_2$ simply yields the scalar value of that function at the given coordinates.
   - When the formula takes specific points as arguments, the overall values of these functions are calculated based on direct evaluation at those coordinates.

### Decomposition into Zeros and Poles

- **Prime Divisor Decomposition**:
  - The divisor of a rational function completely defines its zeros and poles. Therefore, a divisor can be understood as being fully decomposed into its underlying prime divisors (individual points).
  - Consequently, evaluating a function over a divisor naturally reduces to, and is directly linked with, evaluating the function's value at those specific individual points.

### Formula Evaluation Summary

The reason both expressions yield identical computational results is that these functions are evaluated based on the exact zeros and poles dictated by the divisor. Specifically, by performing arithmetic using the function's scalar values at each individual point, it is mathematically guaranteed that the evaluation over the entire divisor yields the same final output.

In summary, because the divisor is fundamentally decomposed into the function's zeros and poles, evaluating the function at each distinct point produces the exact same result as evaluating the divisor as a whole.

