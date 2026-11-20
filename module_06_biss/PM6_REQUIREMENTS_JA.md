# pm6 要件整理: Code Nexus

出典: `C:\Users\sic42\Downloads\pm6.pdf`

この文書は実装前の確認用です。実装の完成度を判定したものではありません。
「必須」は本文で要求された内容、「出力例」は例から確認できる動作、「前提知識」は理解のための説明です。出力例の文字列や追加仕様を、そのまま新たな必須要件として扱わないでください。

ページ番号は **PDF上のページ / 紙面に印刷されたページ** の順で表記します。たとえば「PDF 9 / 本文 8」です。

## 1. 共通要件

出典: PDF 6–7 / 本文 5–6。

| 確認 | 必須要件 | 原文の対応箇所 |
| --- | --- | --- |
| [ ] | Python 3.10以上で作成する。 | “Python 3.10 or later” |
| [ ] | flake8のコーディング規約に従う。 | “adhere to the flake8 coding standard” |
| [ ] | コード全体に十分な型注釈を付け、mypyで確認する。 | “comprehensive type annotations. Check this using mypy” |
| [ ] | 例外処理によってデータストリームの破損を防ぐ。 | “Exception handling should protect the data streams from corruption.” |
| [ ] | 許可されるライブラリのimportは `abc` と `typing`。外部ライブラリは禁止。 | “Authorized imports: abc and typing. External libraries are forbidden.” |
| [ ] | 標準のクラス・コレクションとそのメソッドは使用可能。 | “All standard classes and collections are authorized” |
| [ ] | 組み込み関数は `eval()` と `exec()` 以外使用可能。 | “except for eval() and exec()” |
| [ ] | ex0〜ex2は、それぞれリポジトリ直下の単一ファイルとし、前の課題を改善する。 | “single files at the root of the repository, each one improving on the previous” |
| [ ] | ex3とex4はパッケージにし、それぞれ `__init__.py` を置く。 | “a __init__.py file is MANDATORY for each of them” |
| [ ] | テスト・実演用スクリプトはリポジトリ直下に置く。 | “All testing scripts live at the root of the repository.” |

ex3/ex4では、課題で指定された自作パッケージ間のimportも必要です。ライブラリの許可リストとは区別してください。

指定された提出構成:

```text
リポジトリ直下/
├── data_processor.py
├── data_stream.py
├── data_pipeline.py
├── battle.py
├── capacitor.py
├── tournament.py
├── ex3/
│   ├── __init__.py
│   └── 課題に必要なファイル
└── ex4/
    ├── __init__.py
    └── 課題に必要なファイル
```

注意: ex0では、不正な型のデータを `ingest()` に渡す実演によって、意図的にmypyの警告が残ることが本文で認められています。「すべてのmypy警告を消す」と読み替えないでください。

## 2. ex0: Data Processor

出典: PDF 8–10 / 本文 7–9。提出: `data_processor.py`。

### 必須の構造

- [ ] `ABC` を継承する抽象クラス `DataProcessor` を作る。
- [ ] `NumericProcessor`、`TextProcessor`、`LogProcessor` が `DataProcessor` を継承する。
- [ ] 親の `validate()` と `ingest()` を抽象メソッドにし、各子クラスでオーバーライドする。
- [ ] 親に通常のメソッド `output()` を実装する。子でのオーバーライドは不要。

原文: “Two abstract methods in DataProcessor: validate ... and ingest” / “One standard method ... output”。

本文で指定された親クラスのシグネチャ:

```python
validate(self, data: Any) -> bool
ingest(self, data: Any) -> None
output(self) -> tuple[int, str]
```

### 各メソッドの必須動作

| メソッド | 要件 |
| --- | --- |
| `validate()` | 自分が受け入れられるデータかをboolで返す。子でも引数型は `Any` のままにする。 |
| `ingest()` | データを受け取り、要素を個別に内部保存する。子では受け入れる型を型注釈に反映する。 |
| 不正データの `ingest()` | 事前に `validate()` を呼んでいなくても、不正な入力なら例外を送出する。 |
| `output()` | 最も古い1要素を、そのプロセッサ内の処理順位と組にして取り出す。取り出した要素は内部から削除する。 |

原文: “an exception must be raised” / “extract the oldest piece of data ... along with the associated processing rank” / “then removed”。出典: PDF 9 / 本文 8。

### 各プロセッサの入力

| クラス | 受け入れる型 | 保存する内容 |
| --- | --- | --- |
| `NumericProcessor` | `int`、`float`、それらのリスト。整数と浮動小数点数の混在リストも含む。 | 各数値を文字列に変換し、個別に保存。 |
| `TextProcessor` | `str`、文字列のリスト。 | 各文字列を個別に保存。 |
| `LogProcessor` | キーと値が文字列の辞書、そのような辞書のリスト。 | 各辞書を文字列に変換し、個別に保存。 |

受け入れる型を表す子の `ingest()` の引数注釈:

```python
# NumericProcessor
data: int | float | list[int | float]

# TextProcessor
data: str | list[str]

# LogProcessor
data: dict[str, str] | list[dict[str, str]]
```

### 必須の実演・確認

- [ ] 3種類すべての子クラスのインスタンスを作る。
- [ ] 各クラスで、正常な入力と不正な入力を `validate()` に渡す。
- [ ] 少なくとも1件、事前検証せず不正な入力を `ingest()` に渡し、例外が出ることを確認する。
- [ ] 各プロセッサで複数のデータを取り込み、`output()` で取り出す。

原文: “Test valid and invalid data for each class” / “without prior validation ... This will leave you with a mypy warning, on purpose.” 出典: PDF 9 / 本文 8。

### 出力例と未指定事項

- PDF 10 / 本文 9の例では、順位は0から始まる。
- ログの例は `log_level` と `log_message` を使い、`NOTICE: Connection to server` のように表示する。ただし本文の入力型は「文字列のキー・値の辞書」であり、この2キーだけを受け入れるという制限は明記されていない。
- 空のプロセッサに対する `output()`、空リスト、`bool` の扱い、例外クラス名は本文に具体的な指定がない。これらは実装上の判断と、必須要件を分けて考える。

前提知識: ABC、抽象メソッド、継承、オーバーライド、型のunion、FIFO、`raise` と `try/except`。

## 3. ex1: Polymorphic Processing of a Data Stream

出典: PDF 11–12 / 本文 10–11。提出: `data_stream.py`。

### 必須の構造・動作

- [ ] ex0のコードを利用・改善する。
- [ ] 異なる型のデータが混在した入力を受ける `DataStream` を作る。
- [ ] ポリモーフィズムを使い、各要素を適切な登録済みプロセッサへ振り分ける。
- [ ] プロセッサを登録できるようにする。
- [ ] 処理できるプロセッサがない要素では、エラーメッセージを表示する。
- [ ] 登録済みプロセッサの統計情報を表示する。

原文: “route each element to the appropriate data processor using polymorphic behavior” / “Error messages will be printed if no data processor can handle an element.”

指定シグネチャ:

```python
register_processor(self, proc: DataProcessor) -> None
process_stream(self, stream: list[typing.Any]) -> None
print_processors_stats(self) -> None
```

### 必須の実演・確認

- [ ] 混在するデータストリームを正しく処理するテストシナリオを作る。
- [ ] 登録済みプロセッサの統計を表示する。
- [ ] 各プロセッサの `output()` で要素を消費する。
- [ ] 消費後の統計を表示する。

### 出力例から確認できる内容

PDF 12 / 本文 11では、統計としてプロセッサごとの「累計処理件数」と「残件数」を表示している。出力で消費しても累計は減らず、残件数だけが減る。

例では数値リスト `[3.14, -1, 2.71]` と `42` を合わせて4件と数える。リスト全体を1件とは数えない。

前提知識: 共通インターフェースを通じた呼び出し、ポリモーフィズム、プロセッサの登録、累計と現在の保存件数の違い。

## 4. ex2: Data Pipeline

出典: PDF 13–14 / 本文 12–13。提出: `data_pipeline.py`。

### 必須の構造・動作

- [ ] ex1を改善し、入力から出力までのパイプラインにする。
- [ ] `Protocol` を継承する `ExportPlugin` を定義する。
- [ ] `ExportPlugin` に次のメソッドを定義する。

```python
process_output(self, data: list[tuple[int, str]]) -> None
```

- [ ] `DataStream` に次のメソッドを追加する。

```python
output_pipeline(self, nb: int, plugin: ExportPlugin) -> None
```

- [ ] `process_stream()` の後で、登録済みの各プロセッサから要素を取り出し、指定されたプラグインで出力する。
- [ ] 少なくともCSV出力とJSON出力の2種類のプラグインを作る。
- [ ] 有効なCSV・JSON文字列を手動で作る。`csv` や `json` のimportを追加しない。
- [ ] プラグインの互換性はduck typingで扱う。

原文: “made export-compatible through duck typing” / “Create at least a CSV export plugin and a JSON export plugin” / “manually create valid CSV and JSON strings”。

### 出力例で補足される動作

- PDF 14 / 本文 13では、`nb` は全プロセッサ合計ではなく、**各プロセッサから取り出す件数**になっている。
- `nb=3` でもログが2件しかなければ、その2件を出力している。例と合わせるなら、残件数まで取り出す。
- プロセッサごとに、取り出したタプルのリストをプラグインに渡す構成になっている。
- 取り出した分だけ残件数が減る。次のバッチでも処理順位は継続する。
- JSON例では `"item_3": "42"` のように順位をキーに利用している。このキー形式自体は本文の必須指定ではない。
- 文字列にカンマ・引用符・改行などが含まれても、「有効なCSV・JSON」という要件を満たす必要がある。

具体的なプラグインのクラス名や、プラグイン側が `ExportPlugin` を明示的に継承することは指定されていない。

前提知識: `Protocol`、構造的部分型、duck typing、ABCとの違い、CSV・JSONのエスケープ。

## 5. ex3: Entity Factories and Capabilities

出典: PDF 15–17 / 本文 14–16。
提出: リポジトリ直下の `battle.py` と `capacitor.py`、必要なファイルを含む `ex3/` パッケージ。

### 必須のクラス構造

| クラス | 継承・役割 | 必須の内容 |
| --- | --- | --- |
| `Creature` | `ABC` を継承 | 名前・タイプの属性、抽象 `attack()`、名前とタイプから標準メッセージを返す通常の `describe()`。 |
| `Flameling` / `Pyrodon` | `Creature` を継承 | それぞれ適切な攻撃メッセージを返す `attack()`。 |
| `TransformCapability` | `ABC` を継承。`Creature` は継承しない。 | 抽象 `transform()` と `revert()`。 |
| `Shiftling` / `Morphagon` | `Creature` と `TransformCapability` の両方を継承 | 変身・解除できる。属性で変身状態を保持し、状態で `attack()` の戻り値が変わる。 |
| `CreatureFactory` | `ABC` を継承 | 抽象 `create_base()` と `create_evolved()`。 |
| `FlameFactory` | `CreatureFactory` を継承 | 基本形 `Flameling` と進化形 `Pyrodon` を生成する。 |
| `TransformCreatureFactory` | `CreatureFactory` を継承 | 基本形 `Shiftling` と進化形 `Morphagon` を生成する。 |

- [ ] `ex3/__init__.py` を置く。
- [ ] パッケージが外部公開するものはファクトリだけとし、具体的なエンティティクラスは公開しない。

原文: “It must not inherit from Creature” / “Your ex3 package must only expose the factories, never the concrete entities.”

**名前についての明示的な許容:** エンティティとファクトリの名前は変更してよい。ただしAbstract Factoryと、`Creature` を継承しない能力クラスの設計を正しく実装する必要がある。出典: PDF 16 / 本文 15。

### battle.py の必須要件

- [ ] 2種類のファクトリをインスタンス化する。
- [ ] ファクトリを1つ受け取る共通の関数を作る。
- [ ] その関数で基本形、次に進化形を作り、それぞれ `describe()` と `attack()` を実行する。
- [ ] 別の関数でファクトリを2つ受け取り、それぞれの基本形を戦わせる。

原文: “A single function that receives a factory” / “Another function that receives two factories”。

### capacitor.py の必須要件

- [ ] 変身可能なエンティティを作るファクトリを用意する。
- [ ] 基本形と進化形を生成する。
- [ ] 両方について `describe → attack → transform → attack → revert` を実演する。

原文: “For each one: describe, attack, transform, attack again, revert.”

### 出力例と未指定事項

PDF 16–17 / 本文 15–16の例では、通常時と変身後で攻撃メッセージが変わる。`revert()` は通常の状態へ戻す。
HP、ダメージ計算、勝敗判定を実装する指示はない。具体的な攻撃文の完全一致も必須とは明記されていない。

前提知識: Abstract Factory、抽象クラスと具体クラス、能力を表す独立したクラス、多重継承、状態、`__init__.py` と公開インターフェース。

## 6. ex4: Abstract Strategy

出典: PDF 18–20 / 本文 17–19。
提出: リポジトリ直下の `tournament.py`、必要なファイルを含む `ex4/` パッケージ。

### 必須のクラス構造・動作

- [ ] `ex4/__init__.py` を置く。
- [ ] `ABC` を継承する抽象クラス `BattleStrategy` を作る。
- [ ] 抽象メソッド `act()` と `is_valid()` を定義する。
- [ ] `is_valid()` は、その戦略を対象エンティティに適用できるかをboolで返す。
- [ ] `NormalStrategy` はすべてのエンティティに適用でき、`attack()` を呼ぶ。
- [ ] `AggressiveStrategy` は変身能力を持つエンティティに適用でき、`transform → attack → revert` の順に実行する。
- [ ] 適用できないエンティティで `act()` が呼ばれたら、明確なメッセージを伴う専用例外を送出する。
- [ ] 戦略は `isinstance()` で能力を調べ、具体的なエンティティの系統によって判定しない。

原文: “raise a dedicated exception with a clear message” / “A strategy checks capabilities with isinstance, never the concrete family.”

たとえば変身可能かの判断対象は `TransformCapability` という能力であり、`Shiftling` など特定クラス名の列挙にはしない。

追加戦略は許可されているが、通常の戦略と能力を利用する戦略が少なくとも1つずつ必要。専用例外のクラス名は指定されていない。

### tournament.py の必須要件

- [ ] ex3のエンティティファクトリと、戦略を生成する。
- [ ] 対戦相手のリストを受け取る共通の対戦関数を1つ定義する。
- [ ] 各対戦相手を `(CreatureFactory, BattleStrategy)` のタプルで表す。
- [ ] 各対戦相手が、他の対戦相手それぞれと1回ずつ対戦する。
- [ ] 各エンティティに、それぞれの戦略を適用する。
- [ ] エンティティと戦略の不適切な組み合わせがあれば、大会を中止する。

原文: “a single battle function” / “makes each opponent face every other one once” / “aborts on an invalid entity-strategy pair”。出典: PDF 19 / 本文 18。

### 出力例から確認できる内容

PDF 20 / 本文 19には、通常の大会と、エラーで中止する大会の例がある。

| 組み合わせ | 例での結果 |
| --- | --- |
| Flameling + Normal / Shiftling + Aggressive | それぞれの戦略で行動する。 |
| Shiftling + Aggressive / Flameling + Aggressive | Flamelingには変身能力がないため、明確なエラーを表示して大会を中止する。 |

大会側がエンティティの具体的な系統を調べて行動を分岐する構成にはしない。行動の選択を戦略に任せる。

前提知識: Strategyパターン、能力による適用可否の判定、専用例外、呼び出し元への例外伝播、重複のない対戦組み合わせ。

## 7. 提出・口頭説明

出典: PDF 21 / 本文 20。

- [ ] Gitリポジトリへ提出する。評価対象はリポジトリ内の作業のみ。
- [ ] ファイル名を確認する。
- [ ] 提出が必要なのは課題文で指定されたファイル。

原文: “Only the work inside your repository will be evaluated” / “You only need to submit the files requested by the subject”。

評価時に求められる可能性があること:

- ポリモーフィズムとメソッドのオーバーライドを説明・実演する。
- 新しいデータ型、エンティティの系統、戦略を追加する。
- 処理動作を変更する。
- 継承によるコード再利用と動作の特殊化を説明する。
- Abstract Factory、Capability、Abstract Strategyがそれぞれ必要な理由を説明する。
- ex1: 具体的な実装を知らずに、異なる入力型を扱える理由を説明する（PDF 12）。
- ex2: ABCとProtocolの違い、プラグインにProtocolを使う理由を説明する（PDF 14）。
- ex3: `transform/revert` を全Creatureに付ける設計の問題を説明する（PDF 17）。
- ex4: 行動を選ぶ判断がどこへ移ったか、新しい能力の追加時に何が便利かを説明する（PDF 20）。

## 8. 必須要件に追加しないもの

以下は、このPDFで必須とは指定されていない。必要なら実装上の判断として扱い、PDFの要求と混同しない。

- docstringの追加。
- pytestやHypothesisなどのテストフレームワークの導入。
- 出力例で使われる入力値・見出し・メッセージの一字一句の固定。
- 本文にない関数名、内部属性名、例外クラス名の固定。
- HP、ダメージ、勝敗判定などの戦闘機能の追加。

このMarkdown自体は学習用の整理資料であり、課題が要求する提出ファイルではない。
