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

## 追加した防御

- Processor以外の登録、同一インスタンスの重複登録を拒否します。
- ストリーム本体はlist、出力件数はbool以外の非負整数に限定します。
- 数値・ログは全件を文字列化してから保存し、変換途中の部分保存を防ぎます。
- Processor内の処理に失敗した場合、そのProcessorのitemsとindexを復元し、
  エラーを表示して次の入力へ進みます。
- 出力プラグインは継承を求めず、process_outputが呼び出せることを確認します。
- プラグインへの出力に失敗すると、失敗したProcessorのitemsとindexを復元し、
  PipelineExportErrorを送出します。成功済みProcessorの出力は確定済みです。
- 外部へすでに書き出した文字やファイル内容までは巻き戻せません。
  再実行時の外部出力の重複防止は、各プラグイン側の責任です。
- CSV/JSONプラグインへの直接入力も、タプルの形・番号・文字列を検証します。
- 不正な対戦相手の構成を拒否し、戦闘中の予期しない例外でも大会を中止します。
- 変身・攻撃が失敗しても、finallyで変身解除を試みます。

例外は無条件に握りつぶさず、入力の誤りはTypeError/ValueErrorで通知します。
公開された内部属性の意図的な書き換えや、外部装置の障害までは保証しません。
