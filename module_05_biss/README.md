# PM5 - The Codex

実装は既存の `src/module_05_biss/` の下に配置しています。
以下はこのディレクトリを作業ディレクトリにして実行します。
Python 3.10以上を使用してください。

## ex0: 仮想環境と依存関係

```sh
python3 ex0/construct.py
python3 -m venv lab_env
source lab_env/bin/activate
python3 ex0/construct.py
python3 ex0/loading.py
python3 -m pip install -r ex0/requirements.txt
python3 ex0/loading.py
```

Windowsでは `lab_env\Scripts\Activate.ps1` で有効化します。
環境の外と内、ライブラリ未導入と導入済みの違いを確認できます。

Poetryは `ex0/` をプロジェクトとして扱います。

```sh
cd ex0
poetry install
poetry run python loading.py
cd ..
```

pipとPoetryには同じ依存制約を記述しています。
Poetryは解決したバージョンをpoetry.lockに記録します。

## ex1: 設定

```sh
python3 -m pip install -r ex1/requirements.txt
python3 ex1/oracle.py
cp ex1/.env.example ex1/.env
python3 ex1/oracle.py
MATRIX_MODE=production LOG_LEVEL=INFO python3 ex1/oracle.py
```

`.env.example` の値はダミーです。実際のAPIを利用する必要はありません。
外部サービスへの接続は行わず、設定の有無とモード差を表示します。
環境変数は.envより優先され、APIキー・接続文字列は表示しません。
.envや仮想環境は提出・コミットしません。

## ex2〜ex4: import

```sh
python3 ft_alembic_0.py
python3 ft_alembic_1.py
python3 ft_distillation_0.py
python3 ft_transmutation_0.py
python3 ft_kaboom_0.py
python3 ft_kaboom_1.py
```

`ft_alembic_1.py` は未公開の関数を呼ぶためAttributeErrorで終了します。
`ft_kaboom_1.py` はトップレベルの循環importによってImportErrorで終了します。
この2つはsubject指定の意図的な失敗です。
light側は関数内importで相互依存の解決を実行時まで遅らせています。
`sys.path` は一切変更していません。

## 検証と提出

module_05_biss直下で、開発用の仮想環境から実行します。

```sh
python3 -m pip install flake8 mypy python-dotenv
python3 -m flake8 .
python3 -m mypy .
```

mypyの `alchemy.create_earth()` に対するattr-definedエラーは意図的です。
それ以外のエラーはない状態を維持します。
提出時は `src/module_05_biss/` 内のsubject指定ファイルを
提出先Gitリポジトリのルートに配置してください。
ルートの雛形 `__init__.py`、開発設定、README、仮想環境は提出対象外です。

## 追加した防御

- MATRIX_MODE・LOG_LEVELの空白と大文字小文字を正規化します。
- 不正なLOG_LEVELは警告し、developmentはDEBUG、productionはINFOへ戻します。
- 空白だけの設定は未設定として扱います。
- DATABASE_URLのscheme://value構造と、ZION_ENDPOINTのHTTP(S)・ホストの有無を
  確認します。接続成功や、すべてのDBドライバ固有の構文は保証しません。
- .envと.gitignoreは、読み取り失敗・文字コード不正でも警告して続行します。
- 外部ライブラリのimport中に通常の例外が起きても、導入案内を表示します。
- light側の呪文名・材料は文字列であることを検証します。
- subject指定の未公開属性とdark側の循環importの失敗は、そのまま残します。
