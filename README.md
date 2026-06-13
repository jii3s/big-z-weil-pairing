# Big-Z Weil Pairing: e(F_p, F_p) Implementation

> [!WARNING]
> **Repository Maintenance Status: Read-Only / No Support**
> This repository is published strictly as an open-source archive of my personal research and implementation. **This project is completely unmaintained and unsupervised.** I will not read, respond to, or accept any inquiries, bug reports, feature requests, or pull requests. Feel free to fork the code and use it under the license, but do so entirely at your own risk. No communication or support will be provided under any circumstances.

> [!NOTE]
> **Translation Notice**
> This README has been automatically translated from the original Japanese text. While every effort has been made to ensure accuracy, some technical nuances or phrasing may differ from the original.
---

## Preface

Elliptic Curve Cryptography (ECC) was a groundbreaking milestone because it **"allows addition of encrypted values."** This characteristic significantly improved the usability of public-key cryptography.

An even further advancement is "Elliptic Curve Pairing Cryptography," a hyper-revolutionary cryptography that **"allows multiplication of encrypted values, albeit only once."** Enabling the verification of encrypted values after a single multiplication is what ultimately made the final proof of Zero-Knowledge Proofs (ZKP) a reality.

However, attempting to understand elliptic curve pairing cryptography immediately pits you against a wall of incredibly advanced mathematics. Even if you try to build it from scratch based on theory, simply understanding the advanced mathematics involved (algebraic geometry and number theory) would take years.

While source codes for Tate Pairing—the current de facto standard—are widely available on the internet, a programmer looking at them will face total despair due to the following realities:

* **Out of nowhere, the interpretation and implementation of the "12th-degree extension field $\mathbb{F}_{p^{12}}$" appear, blowing the programmer's mind.**
* **Production-grade code is optimized to the absolute limit by mathematicians worldwide to reduce computational complexity and execution time. As a result, it becomes a "puzzle far removed from the foundational theory," making it virtually impossible for a programmer to grasp its structure.**

Consequently, programmers currently cannot understand the inner workings and are left blindly using (or rather, being forced to use) existing libraries as black boxes.

---

## What is Big-Z Weil Pairing?

In **Weil Pairing**, which is the origin of Tate Pairing, **pairing of integer $\times$ integer should theoretically be possible**, provided that a "pairing-friendly curve" can be found. In other words, it should be possible to achieve pairing without requiring any implementation of the 12th-degree extension fields that torment programmers.

Therefore, in this project, I have implemented Weil Pairing strictly adhering to the foundational theory, using a **pure, integer-based approach ($\mathbb{F}_p \times \mathbb{F}_p$)** that completely eliminates the use of complex numbers or polynomial arrays.

However, another massive challenge stands in the way here.
In the mathematical world, it is widely believed that a convenient "pairing-friendly curve" that completely resolves within $\mathbb{F}_p \times \mathbb{F}_p$ can only be found on extremely small, toy-sized bases. Huge curves viable for practical cryptography are generally not even known to exist.

---

## Breakthrough via the Big-Z Method

Through extensive research utilizing various approaches, I have established a method (**Big-Z Method**) to **deterministically discover $\mathbb{F}_p \times \mathbb{F}_p$ pairing-friendly curves with a cryptographic-grade prime base of several hundred bits.**

This repository contains the curve search algorithm, along with the definitive source code for Weil Pairing that straightforwardly runs the Miller Loop using "nothing but integer (BigInt) arithmetic" on the discovered curves.

No complex structures or loops over massive polynomials are required. All computations are completely self-contained within the scope of a single integer modulo a specific prime $p$ (modulo $p$).

---

## Usage

1. Launch **Big-Z_Method.py** and enter the size of the integer you want to use for pairing as the number of bits.
2. The elliptic curve parameters for the specified bit size will be printed.
3. Copy the parameters printed in step 2 into the source code of **WeilPairing_Fp.py**, then execute **WeilPairing_Fp.py**.

That's it.

---

## Author & Contact

**Daiji Sanai**
* **Handle / Pseudonym:** hyler (Black Hat USA) / big-z (jii3)
* **GitHub:** [@jii3s](https://github.com/jii3s)

> *"The Big-Z Method — Bridging the legacy of early hacking with the future of pairing-friendly cryptography."*