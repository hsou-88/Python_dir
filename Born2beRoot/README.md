*This project has been created as part of the 42 curriculum by shirano.*

# Born2beRoot

## Description

Born2beRootは、仮想マシン上にGUIのないLinuxサーバーを構築し、仮想化、ストレージ管理、ユーザー認証、セキュリティ、ネットワーク、監視を学習する42のシステム管理課題である。本プロジェクトでは**VirtualBox上にRocky Linux 9.8**を構築した。

> **検証上の注意**：本書は会話で確認した端末出力とSubject v5.2を基に記載した。「確認済み」と「Subjectが要求するが未検証」を区別する。特にOSの「最新安定版」要件、パスワードの複雑性、ファイアウォールの実効設定、SHA-1署名は提出前に再確認する。

### OS選定とDebianとの比較

Rocky Linuxを選んだ理由は、RHEL系で使われるSELinux、firewalld、RPM/dnf、サービス管理などを実践するためである。

| 観点 | Debian | Rocky Linux |
| --- | --- | --- |
| 系統 | 独立したコミュニティLinux | RHEL互換Linux |
| パッケージ管理 | `apt` / `dpkg` | `dnf` / `rpm` |
| 強制アクセス制御 | 主にAppArmor | 主にSELinux |
| Subject指定のファイアウォール | UFW | firewalld |
| 利点 | 資料が豊富で導入しやすい | 企業向けRHEL系の管理方式を学べる |
| 欠点・留意点 | RHEL系とは管理方法が異なる | SELinuxやパッケージ・ネットワーク設定の理解が必要 |

DebianもRockyもLinuxカーネルを使用するが、ユーザー空間のソフトウェア、既定の設定、パッケージ管理、更新方針が異なる。なお、実際に導入したRocky 9.8がSubjectの「latest stable version of Rocky」に該当するかは提出前に確認する。

### 採用技術と設計理由

| 項目 | 採用技術 | 理由 |
| --- | --- | --- |
| 仮想化 | VirtualBox | ホストから独立した実験環境を作る |
| OS | Rocky Linux 9.8 | RHEL系のサーバー管理を学ぶ |
| GUI | 使用しない | 不要な常駐サービス・攻撃対象を減らす |
| ストレージ | LVM、LUKS | 論理領域の管理と保存データ暗号化を分離する |
| ファイルシステム | XFS、swap | root/homeとスワップ領域を別々に管理する |
| アクセス制御 | SELinux Enforcing | UNIX権限とは別の強制アクセス制御を適用する |
| ファイアウォール | firewalld | 許可通信を制御する |
| リモート管理 | OpenSSH、4242/tcp | 暗号化されたリモートアクセスを行う |
| 権限昇格 | sudo | 管理権限の使用を制御・記録する |
| 監視 | Bash、cron、wall | 起動時と10分ごとに状態を通知する |

**AppArmorとSELinux**：いずれも強制アクセス制御（MAC）である。AppArmorは主にパスベースのプロファイルを使う。SELinuxはプロセスやファイルのセキュリティコンテキストとポリシーを利用し、通常のUNIX権限で許可される操作も制限できる。

**UFWとfirewalld**：どちらもLinuxのパケットフィルタ機能を管理するフロントエンドである。UFWは比較的単純なルール管理を志向し、firewalldはゾーンやサービス定義などで構成する。Rocky LinuxではSubjectに従いfirewalldを採用した。

**VirtualBoxとUTM**：VirtualBoxは汎用の仮想化製品である。UTMは主にmacOSでQEMUなどを利用する仮想化・エミュレーション環境である。今回のホスト環境ではVirtualBoxを採用した。

### ディスク構成

以下は `lsblk` と `pvs/vgs/lvs` の結果から確認した構成（概数）である。

```text
/dev/sda                          約30 GiB
├── sda1                          約1 GiB   XFS  → /boot
└── sda2                          約28.1 GiB  LVM Physical Volume
    └── VG: rlm_shirano42
        ├── LV: root               約21 GiB   LUKS → XFS  → /
        ├── LV: swap               約2 GiB    LUKS → swap
        └── LV: home               約5 GiB    LUKS → XFS  → /home
```

PVは `/dev/sda2`、VGは `rlm_shirano42`、LVは `root`、`swap`、`home` の3つである。各LV上にそれぞれLUKSがあり、**LVM → LUKS → ファイルシステム**という順序である。暗号化領域は3つ存在する。ただし、Subjectの「少なくとも2つの暗号化されたパーティションをLVMで作成する」という表現に対しては、物理パーティション2つを暗号化した構成ではなく、1つのPV内の3つの暗号化LVであることを正確に説明する。

`/` と `/home` を分離することで、容量枯渇の影響をある程度限定できる。swapは独立した領域として確保した。`/boot` はカーネルとinitramfsを読み込むため今回の構成では暗号化していない。

### ユーザーとセキュリティ

- **ホスト名**：`shirano42`。
- **通常ユーザー**：`shirano`（rootとは別のユーザー）。`user42`、`sudo`、`wheel` の各グループへの所属を設定した。最終的な所属は `id shirano` で検証する。
- **SSH**：TCP 4242での `shirano` のログイン成功を確認済み。rootによるSSHログインを禁止する設定の実効状態は `sshd -T` で確認する。
- **SELinux**：Enforcing状態を確認した。
- **firewalld**：稼働し、`services: ssh` と `ports: 4242/tcp` が表示されることを確認した。ただし、`ssh` サービス定義が22/tcpを許可していないかは別途確認が必要である。
- **sudo**：3回までの認証試行、認証失敗時の独自メッセージ、入出力ログ、`use_pty`、`secure_path`を設定した。

### パスワードポリシー

Subject v5.2が要求する値は次のとおりである。期限と文字品質は異なる設定に関係するため、双方を検証する。

| 要件 | 値 |
| --- | --- |
| 有効期限 | 最大30日 |
| パスワード変更の最小間隔 | 2日 |
| 有効期限の事前警告 | 7日前 |
| 最小長 | 10文字 |
| 必須文字種 | 英大文字・英小文字・数字 |
| 同じ文字の連続 | 3文字を超えない |
| ユーザー名 | パスワードに含めない |
| 過去のパスワードとの差分 | 以前のパスワードになかった文字を7文字以上含む（rootには適用しない） |
| root | その他の該当規則を満たす |

設定後は、**rootを含む既存の全アカウントのパスワードを変更する**。`chage -l` だけでは文字品質や履歴制約を検証できないため、PAMとpwqualityの設定も確認する。

### sudoポリシー

`/etc/sudoers.d/20-sudo-policy` において、以下の設定を確認した。

```text
Defaults passwd_tries=3
Defaults badpass_message="Authentication failed: try again."
Defaults use_pty
Defaults log_input
Defaults log_output
Defaults iolog_dir="/var/log/sudo"
Defaults logfile="/var/log/sudo/sudo.log"
```

`secure_path` も設定済みである。値はVM上で再確認する。ログディレクトリは `/var/log/sudo/`。`visudo -c` による構文確認と、実際のsudo実行後のログ記録も確認する。

### 監視スクリプト

`/usr/local/bin/monitoring.sh` はBashで作成した。`wall` で全端末に情報を通知する。rootのcrontabは次の構成である。

```cron
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
@reboot sleep 30 && /usr/local/bin/monitoring.sh
*/10 * * * * /usr/local/bin/monitoring.sh
```

出力する情報は、(1) OSアーキテクチャとカーネル、(2)物理プロセッサ数、(3)vCPU数、(4)メモリ容量・使用率、(5)ディスク容量・使用率、(6)CPU使用率、(7)最終起動日時、(8)LVMの使用有無、(9)TCP接続数、(10)ログインユーザー数、(11)IPv4とMACアドレス、(12)sudoコマンドの実行回数である。実行結果の表示とcronの設定を確認したが、すべての集計値の算出式を監査したわけではない。

## Instructions

### 必要なもの・実行方法

- VirtualBoxを利用できるホストPC
- 構築済みのRocky Linux仮想マシン
- コンソールまたはSSHによるログイン手段

本課題はサーバーの設定が成果物であり、ソースコードのコンパイルは不要である。VirtualBoxからVMを起動し、通常ユーザー `shirano` でログインする。VM内からのSSH接続確認例は次のとおりである。

```bash
ssh -p 4242 shirano@localhost
```

この接続は実際に成功した。ホストからのアクセスにはVirtualBoxのネットワーク方式に応じたNATポートフォワーディングなどの設定が必要な場合がある。

### 設定の検証

```bash
# OS、カーネル、ホスト名、ユーザー・グループ
cat /etc/os-release
uname -a
hostnamectl
id shirano

# GUIとサービス、SELinux
systemctl get-default
systemctl is-enabled sshd firewalld crond
systemctl is-active sshd firewalld crond
getenforce
sestatus

# SSHとファイアウォール
sudo sshd -T | grep -Ei '^(port|permitrootlogin) '
sudo ss -tlnp
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --info-service=ssh

# ディスク・暗号化・LVM
lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
sudo pvs
sudo vgs
sudo lvs
findmnt -T /home

# パスワード期限・品質
sudo chage -l shirano
sudo chage -l root
sudo grep -E '^(PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE)' /etc/login.defs
sudo grep -RniE 'pam_pwquality|pam_pwhistory|difok|minlen|ucredit|lcredit|dcredit|maxrepeat|usercheck' /etc/security /etc/pam.d/system-auth /etc/pam.d/password-auth 2>/dev/null

# sudo設定・ログ
sudo visudo -c
sudo grep -RnE 'passwd_tries|badpass_message|log_input|log_output|logfile|iolog_dir|use_pty|secure_path' /etc/sudoers /etc/sudoers.d
sudo whoami
sudo ls -la /var/log/sudo/

# 監視
sudo bash -n /usr/local/bin/monitoring.sh
sudo bash /usr/local/bin/monitoring.sh
sudo crontab -l
```

**重要**：設定の記述、サービスの起動、ネットワーク越しの実際の到達性は別々に確認する。特にfirewalldの`services: ssh`が22/tcpを意図せず許可していないか確認する。

### Peer evaluationに向けた操作

評価では、ホスト名の変更、ユーザー・グループ作成、SSH接続、監視スクリプトの説明と無編集での停止が求められる。

```bash
# ホスト名変更の例（元に戻す）
sudo hostnamectl set-hostname example42
sudo hostnamectl set-hostname shirano42

# 評価用アカウント・グループの作成例
sudo groupadd examplegroup
sudo useradd -m testuser42
sudo passwd testuser42
sudo usermod -aG user42 testuser42
id testuser42

# 監視を編集せず一時停止・再開
sudo systemctl stop crond
sudo systemctl start crond
```

`crond`の停止は監視以外のcronジョブも停止させるため注意する。上記のアカウント名・グループ名は例であり、実際の評価指示に合わせる。

### 提出とsignature.txt

Gitリポジトリのルートには次の**2ファイル**を提出する。

```text
.
├── README.md
└── signature.txt
```

仮想ディスクをGitに含めてはならない。**VMを停止した状態**で、ホスト上にあるVDIファイルのSHA-1を計算し、実際の40桁のハッシュ値を `signature.txt` に記載する。

```bash
# Linuxホスト
sha1sum "/path/to/disk.vdi"

# macOSホスト
shasum "/path/to/disk.vdi"
```

```powershell
# Windowsホスト
certUtil -hashfile "C:\path\to\disk.vdi" SHA1
```

評価開始時にはスナップショットが存在してはならない。VMを起動・変更するとディスクの署名が変わる可能性があるため、署名と評価に使用するディスクが一致することを検証する。本READMEの作成時点で `signature.txt` の実値は未取得である。

### 最終チェックリスト

- [ ] Rockyの版がSubjectの最新安定版要件を満たすか確認した。
- [ ] GUIサーバーがインストールされていない。
- [ ] LVMと複数の暗号化領域を説明・確認できる。
- [ ] SELinuxが起動時から有効で、Enforcingである。
- [ ] SSHは4242で動作し、rootによるSSHログインができない。
- [ ] firewalldは起動時に有効で、**4242以外のポートを許可していない**。
- [ ] ホスト名は`shirano42`、ユーザーは`shirano`、必要なグループ所属を満たす。
- [ ] パスワードの期限・品質・履歴とrootへの適用を確認した。
- [ ] sudoの認証制限・メッセージ・ログ・TTY・secure_pathが実際に動作する。
- [ ] monitoring.shは起動時と10分ごとに正しい値を表示する。
- [ ] 評価中のユーザー追加、ホスト名変更、SSH、新規グループ、監視停止を説明できる。
- [ ] README.mdと正確なsignature.txtを提出し、VMディスクやスナップショットを提出しない。

## Resources

### 参考資料

- **Born2beRoot Subject v5.2**（42から配布された原本PDF。要件の一次資料）
- [Rocky Linux Documentation](https://docs.rockylinux.org/)
- [Red Hat Enterprise Linux 9 Documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9)
- [Debian Documentation](https://www.debian.org/doc/)
- [Oracle VirtualBox Manual](https://www.virtualbox.org/manual/)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [SELinux Project](https://selinuxproject.org/)
- [firewalld Documentation](https://firewalld.org/documentation/)
- [LVM2](https://sourceware.org/lvm2/)
- [cryptsetup / LUKS](https://gitlab.com/cryptsetup/cryptsetup)
- ローカルマニュアル：`man sshd_config`、`man sudoers`、`man crontab`、`man lvm`、`man cryptsetup`。

### AIの使用（用途と対象箇所）

ChatGPTは**概念理解、口頭試問の練習、設定レビュー、README下書き**の補助に使用した。具体的には、Linuxカーネルとディストリビューション、VirtualBox、LVM/LUKS/XFS、UNIX権限、SELinux、firewalld、SSH、sudo、PAM、Bash、cron、監視スクリプトの仕組みを質疑応答で整理した。また、ユーザー名変更に伴うホームディレクトリ・グループ設定のトラブルシューティング、端末画像の読み取り、検証コマンドの検討を支援した。

このREADMEの構成と文章作成にもAIを利用した。**AIはVMの設定を直接実行していない**。会話で示された画面・コマンド出力から確認できる事実を記し、未確認箇所には注意を付した。最終判断では配布Subjectと実機での動作を優先する。

## Appendix — このチャットで学んだこと

以下はSubjectの必須README項目とは別の復習資料であり、**本書の最後の章**である。

### A. Linuxカーネル、ディストリビューション、ユーザー空間

- **カーネル**：CPU、メモリ、プロセス、ファイルシステム、ネットワークなどを管理する中心部分。ユーザープログラムはシステムコールを通してカーネルの機能を使う。
- **ユーザー空間**：シェル、ライブラリ、管理コマンド、デーモン、アプリケーションなどが動く領域。`ls`、`sshd`、`sudo` はカーネルそのものではない。
- **ディストリビューション**：カーネルとソフトウェア、管理ツール、初期設定、保守方式を組み合わせたもの。同じLinuxカーネル系でもDebianとRockyで操作や既定の構成が異なる。
- **sudoとroot**：rootは原則UID 0の管理者。sudoは認可されたコマンドを別の権限で実行する仕組みであり、システムコールそのものではない。

### B. 仮想化とハードウェア

VirtualBoxはゲストOSに仮想CPU、仮想ディスク、仮想NICを提供する。ホストOSとゲストOSは区別される。**vCPU**はゲストに提供する論理的なCPU数であり、必ずしもホストの物理CPU数と一致しない。**RAM**は実行時の主記憶、**swap**はメモリページの退避先に使われる補助的な記憶領域である。swapはRAMより遅い。

### C. Linuxの起動順序

```text
電源投入
  → BIOS/UEFI
  → GRUBなどのブートローダー
  → Linuxカーネルとinitramfsの読み込み
  → 暗号化領域の復号とルートファイルシステムの準備
  → systemdによるサービス起動
  → ログイン
```

`/boot`まで暗号化すると、カーネルとinitramfsを読み込む段階で復号手段が必要になる。今回の設計は`/boot`を非暗号化とする。ただし、対応するブートローダーを使えば暗号化された`/boot`の構成も可能である。

### D. PV・VG・LV、LUKS、ファイルシステム

- **パーティション**：ディスクの区画。
- **PV**：LVMが扱う物理ボリューム。
- **VG**：PVから作る容量プール。
- **LV**：VGから切り出した論理ブロックデバイス。
- **LUKS**：ブロックデバイスの暗号化を管理する仕組み。
- **XFS/ext4**：ファイル・ディレクトリ・空き領域などを管理するファイルシステム。
- **マウント**：ファイルシステムを`/`や`/home`などのパスに接続すること。

LVMが提供する容量と、XFSが認識するファイル保存領域の容量は別である。**LVを拡張しただけではXFSも自動的に拡張されるとは限らない**。今回のようにLVとXFSの間にLUKSがある場合は、それぞれの階層の整合が必要となる。

**XFSは拡張できるが、既存のXFSファイルシステムを縮小できない**。ext4はアンマウントした状態で縮小可能である。`/home`が5GiBで満杯になれば、`/`に空きがあってもその領域を直接使えない。論理ボリュームを分ける利点は容量枯渇の影響を限定できること、独立したマウントオプションを設定できること、swapを専用の領域にできることなどである。

```bash
lsblk -f
sudo pvs
sudo vgs
sudo lvs
findmnt -T /home
```

### E. ユーザー、グループ、権限

ユーザーとグループの識別にはUID/GIDが用いられる。通常のUNIX権限は所有者・グループ・その他に対する読み取り(`r`)、書き込み(`w`)、実行(`x`)で管理する。ディレクトリの`x`はそのディレクトリを通過して内部パスにアクセスする権限、`r`は名前の列挙に関係する。

`chmod`はパーミッション、`chown`は所有者・所有グループを変更する。`useradd`、`usermod`、`groupadd`、`id`、`getent`などはアカウント管理に使う。Rockyで管理者グループとしてよく使われる`wheel`と、Subjectが要求する`sudo`、`user42`は別のグループである。

今回のユーザー名変更では、`shirano42`から`shirano`への`usermod -l`だけでホームディレクトリ実体が移動せず、`/home/shirano`への移動、グループ名の変更、SELinuxラベルの修復を確認した。**ユーザー名・ホームディレクトリ・グループ名・ホスト名・VG名は独立した設定である**。

### F. SELinuxとUNIX権限

UNIX権限（DAC）とSELinux（MAC）は異なるアクセス制御の層である。通常の権限でアクセスできるファイルでも、SELinuxのポリシーによって操作が拒否されることがある。`getenforce`で状態を確認し、必要に応じて`ls -Z`でコンテキストを調べる。移動したホームディレクトリなどのラベル修正に`restorecon`が使える。

```bash
getenforce
ls -Z /home
sudo restorecon -RFv /home/shirano
```

### G. ネットワーク、SSH、ポート、firewalld

**IPアドレス**は宛先のネットワークインターフェースを識別し、**ポート番号**は通信先のサービスを区別する。ポートはsudoの権限ではない。SSHは暗号化されたリモート通信を提供し、`sshd`がTCP 4242で待ち受ける。

**TCP**は順序制御、再送、接続状態などを提供し、**UDP**はTCPのような接続確立を前提としない。`ss -tlnp`などで待受ソケットを確認する。外部から接続できるかは、待受、ルーティング、firewalld、SELinux等を組み合わせて判断する。

`firewall-cmd --list-all`の`services: ssh`はサービス定義に基づく許可である。`ports: 4242/tcp`の表示だけでは22/tcpが閉じていると断定できない。`firewall-cmd --info-service=ssh`でサービス定義も確認する。`127.0.0.1:323`等のループバックだけで待ち受けるUDPソケットは、外部向けの公開ポートと区別する。

### H. プロセス、PID、systemd、サービス

実行中のプログラムのインスタンスを**プロセス**と呼び、PIDで識別する。バックグラウンドで継続動作するサービスをデーモンと呼ぶ。systemdは多くのLinuxでサービス起動と依存関係を管理する。

| コマンド | 意味 |
| --- | --- |
| `systemctl start` | 今すぐ開始する |
| `systemctl stop` | 今すぐ停止する |
| `systemctl enable` | 次回起動時の自動起動を設定する |
| `systemctl is-active` | 現在の稼働状態を調べる |
| `systemctl is-enabled` | 自動起動の設定状態を調べる |

サービスを一度起動したことと、再起動後も自動で起動することは異なる。

### I. Bash、パイプ、リダイレクト、テキスト処理

| 記法・コマンド | 意味 |
| --- | --- |
| `A && B` | Aが成功した場合にBを実行する |
| `A \| B` | Aの標準出力をBの標準入力に渡す |
| `>` / `>>` | 標準出力を上書き／追記する |
| `2>/dev/null` | 標準エラー出力を破棄する |
| `grep` | 条件に合う行を検索する |
| `awk` | テキストを行・フィールド単位で処理する |
| `tail -f` | ファイル末尾の更新を追跡する |
| `Ctrl+C` | 通常、前景プロセスにSIGINTを送る |

パイプはシェルの表示上の文字連結ではなく、プロセス間のデータの流れである。`&&`は直前のコマンドの終了ステータスに基づく条件付き実行である。

### J. cron、wall、monitoring.sh

cronは時刻を指定してコマンドを実行し、wallは端末へメッセージを一斉送信する。

```cron
@reboot sleep 30 && /usr/local/bin/monitoring.sh
*/10 * * * * /usr/local/bin/monitoring.sh
```

`@reboot`はcronデーモン起動時、`*/10 * * * *`は毎時0・10・20・30・40・50分を表す。`sudo crontab -l`はrootのcrontabを確認する手段である。監視を無編集で止めるには`systemctl stop crond`を利用できるが、他のcronジョブも止まる点に注意する。

監視項目の代表的な取得方法は、`uname`（OS/カーネル）、`lscpu`（CPU）、`free`（RAM）、`df`（ディスク）、`/proc/stat`（CPU使用率）、`uptime -s`（最終起動）、`lsblk/lvs`（LVM）、`ss`（TCP）、`who`（ログイン人数）、`ip`（IP/MAC）などである。sudo回数はsudoのログ記録方式に応じて集計する。**実際のスクリプトの算出方法は、コードを見て説明する必要がある。**

### K. 検証とトラブルシューティングから学んだこと

1. ユーザー名変更では、UID/GID、ホームディレクトリ実体、SELinuxラベル、SSHログインまで確認する。
2. SSHでは、サービス起動、ポート待受、firewalld、root接続拒否、実際の接続を別々に検証する。
3. sudoでは、設定ファイルの存在、`visudo -c`、認証失敗時の挙動、入出力ログの記録を分けて確認する。
4. 暗号化では、`lsblk`のLUKS表示と`pvs/vgs/lvs`の階層、起動時の復号を確認する。
5. 監視では、手動実行の成功とcronによる起動・周期実行の成功を区別する。
6. 提出では、READMEの内容だけでなく、仮想ディスクと`signature.txt`のSHA-1一致、スナップショット制限を満たす。

**結論：設定の記述、起動中のサービス状態、外部から観測できる動作、Subjectの要件は、互いに区別して確認する必要がある。**
