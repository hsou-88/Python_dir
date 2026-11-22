# PM9 - Cosmic Data

既存の `src/module_09/` 内に、ex0・ex1・ex2を実装しています。
Python 3.10以上と、pipで導入したPydantic 2.xを使用します。

## 仮想環境と実行

module_09直下で実行します。

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/module_09/ex0/space_station.py
python3 src/module_09/ex1/alien_contact.py
python3 src/module_09/ex2/space_crew.py
```

Windowsでは `.venv\Scripts\Activate.ps1` で有効化します。
各スクリプトで、正常モデルの情報と、意図した検証エラーを表示します。
検証エラーはValidationErrorとして捕捉するため、実演は正常終了します。

## 学習ポイント

- ex0: BaseModel、Field、ISO日時文字列の自動変換、既定値
- ex1: Enum、afterのmodel_validatorによる複数フィールドの検証
- ex2: 入れ子モデル、役職と活動状態、長期ミッションの経験者比率

365日を超えるミッションでは、経験5年以上の乗員が半数以上必要です。
3人なら2人、4人なら2人が必要です。365日ちょうどには適用しません。
受信メッセージ必須の条件は信号強度7.0超で、7.0ちょうどではありません。
Optionalな文字列はNoneを既定値とし、省略できるようにしています。

## 検証と提出

```sh
python3 -m pip install flake8 mypy
python3 -m flake8 .
python3 -m mypy .
```

提出対象は3つのPythonファイルだけです。提出先では、ex0/・ex1/・ex2/の
指定ディレクトリへ配置してください。仮想環境は提出しません。

## 追加した防御と更新方法

全モデルはextra="forbid"で未定義フィールドを拒否し、frozen=Trueで
生成後の直接代入を禁止します。NaN・無限大も受け付けません。
型変換は引き続き有効なので、crew_size="6"は整数6になります。
ただし、数値フィールドにTrue/Falseを渡すことは拒否します。

乗員は変更不可のCrewMember、crewは通常の変更操作を拒否するlist派生型です。
append・削除・要素の置き換えで、ミッションの安全条件を後から壊せません。

変更する場合は新しいモデルとして再検証します。

```python
updated_station = station.model_copy(update={"crew_size": 7})
data = mission.model_dump()
data["crew"].append(new_member.model_dump())
updated_mission = SpaceMission.model_validate(data)
```

model_copyも独自に再検証するため、不正なupdateはValidationErrorになります。
すでにモデルになっている入力も、model_validateで再検証します。
失敗しても元のモデルは変更されません。

model_construct、object.__setattr__、__dict__の直接編集など、
検証を明示的に迂回する操作は、通常の入力経路として使わないでください。
