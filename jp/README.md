# Big-Z Weil Pairing: e(F_p, F_p) Implementation

> [!WARNING]
> **リポジトリのメンテナンスステータス: 読み取り専用 / サポート対象外**
> 本リポジトリは、個人の研究成果および実装をオープンソースのアーカイブとして公開しているものです。
> **このプロジェクトは完全に未メンテナンスであり、一切の監視を行っていません。** 質問、バグ報告、機能要望、プルリクエスト（Issue/PR）は一切閲覧・対応・受け付けいたしません。ライセンスの範囲内でコードを複製（フォーク）して利用することは自由ですが、すべて自己責任でお願いいたします。いかなる場合もコミュニケーションやサポートは提供されません。
> 
> **Repository Maintenance Status: Read-Only / No Support**
> This repository is published strictly as an open-source archive of my personal research and implementation. **This project is completely unmaintained and unsupervised.** I will not read, respond to, or accept any inquiries, bug reports, feature requests, or pull requests. Feel free to fork the code and use it under the license, but do so entirely at your own risk. No communication or support will be provided under any circumstances.

---

## 前書き

楕円曲線暗号は、**「暗号値の足し算が成立する」**という画期的なものです。これにより、公開鍵暗号は格段に使いやすくなりました。

さらに進化させた「楕円曲線ペアリング暗号」は、**「暗号値の掛け算が1度限りだが成立する」**という超画期的な暗号です。この「1回の掛け算後の暗号値の照合」が可能になったことによって、ゼロ知識証明（ZKP）の最終証明が現実のものとなりました。

しかし、この楕円ペアリング暗号を理解しようとすると、とてつもない高度数学の壁が現れます。理論を元にゼロから自作しようとしても、その高度数学（代数幾何や数論）を理解するだけで数年は掛かってしまうでしょう。

現在、デファクトスタンダードとして利用されているTateペアリングのソースコードはネット上にいくらでも存在しますが、プログラマがそれを見ても以下のような絶望に直面します。

* **いきなり「12乗根拡大体 $\mathbb{F}_{p^{12}}$ 」の解釈と実装が登場し、脳が吹き飛んでしまう。**
* **実用化コードは、計算量の削減と実行時間短縮のために、世界中の数学者たちが極限まで最適化した「元の基礎理論とは程遠いパズル」になっており、プログラマが構造を理解することは不可能。**

結果として、プログラマは中身を理解できず、ただ既存のライブラリを盲目的に利用する（使わされている）ことしかできないのが現状です。

---

## Big-Z Weil Pairing とは

Tate Pairingの元となっている **Weil Pairing（ウェイル・ペアリング）** においては、もし「ペアリングフレンドリーな曲線」を見つけることさえできれば、**整数 $\times$ 整数のペアリングも理論上可能なはず**です。つまり、プログラマを苦しめる12乗根（拡大体）の実装を一切必要としないペアリングができるはずです。

そこで本プロジェクトでは、複素数や多項式の配列を一切使わない、**純粋な整数ベース（ $\mathbb{F}_p \times \mathbb{F}_p$ ）でのWeil Pairingの実装**を、基礎理論に忠実に行ってみました。

しかし、ここで次の巨大な課題が立ちはだかります。
そもそも数学の世界において、 $\mathbb{F}_p \times \mathbb{F}_p$ で完結するような都合の良い「ペアリングフレンドリーな曲線」は、極めて小さい基数（おもちゃのようなサイズ）の上でしか見つけられないとされており、暗号として実用できるような巨大なものは一般に知られてもいません。

---

## Big-Z Method による突破

様々なアプローチから研究を重ねた結果、暗号レベルで実用可能な**数百bit級の素数を基数とした、 $\mathbb{F}_p \times \mathbb{F}_p$ のペアリングフレンドリー曲線を確定的に見つけ出す手法（Big-Z Method）**を確立しました。

本リポジトリには、その曲線探索アルゴリズムと、それによって得られた曲線上で「ただの整数（BigInt）演算だけ」でMiller Loopを素直に回すWeilペアリングの正解ソースコードを格納しています。

複雑な構造体も、巨大な多項式のループ計算も不要です。すべての計算は、特定の素数 $p$ で割った余り（modulo $p$）の、単一の整数の範囲内だけで完結します。

---

## 使い方

1. **Big-Z_Method.py** を起動し、ペアリングで利用したい整数の大きさをbit数として入力する。
2. 指定bit数の楕円曲線パラメータがプリントされる。
3. 2でプリントされたパラメータを、**WeilPairing_Fp.py** のソースコード中にコピーしてから、**WeilPairing.py** を実行する。

以上。

---

## Author & Contact

**Daiji Sanai**
* **Handle / Pseudonym:** hyler (Black Hat USA) / big-z (jii3)
* **GitHub:** [@jii3z](https://github.com/jii3z)

> *"The Big-Z Method — Bridging the legacy of early hacking with the future of pairing-friendly cryptography."*