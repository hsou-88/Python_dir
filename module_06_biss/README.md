# Code Nexus - PM6

Python 3.10以上。実行時の外部ライブラリは不要です。

## 実行

`src/module_06_biss/` を作業ディレクトリにして、次を実行します。

```sh
python3 data_processor.py
python3 data_stream.py
python3 data_pipeline.py
python3 battle.py
python3 capacitor.py
python3 tournament.py
```

## 検証

module_06_biss直下で実行します。

```sh
python3 -m pip install flake8 mypy
python3 -m flake8 .
python3 -m mypy .
```

ex0の不正なingestの実演は、subjectが意図的な型エラーを求める箇所です。
mypyは `numeric.ingest("foo")` の1行についてarg-typeエラーを報告します。
これはsubjectが求める実演なので抑制していません。
実行時はValueErrorを捕捉し、それ以外の型エラーはない状態です。

## 構成

- ex0: data_processor.py — 抽象Processorと入力検証
- ex1: data_stream.py — 多態的な振り分けと統計
- ex2: data_pipeline.py — ProtocolとCSV/JSON出力
- ex3/: Abstract Factoryと独立した変身能力
- ex4/: 通常・変身戦略と専用例外
- battle.py / capacitor.py / tournament.py: 各実演

提出時はsubject指定のPythonファイルとex3・ex4パッケージを
提出先Gitリポジトリの直下へ置いてください。
仮想環境、キャッシュ、検証ツール、学習用資料は提出しません。
