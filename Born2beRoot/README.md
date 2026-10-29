 # やること
 - Rocky or Debianの安定版のオペレーティングシステムを選び，それを準備する
 	- 今回はRocky 10 Linuxをチョイスした
 - LVMを用いて，暗号化されたパーティションを作成する
 - SSHをrootからは接続できないようにして，4242ポートで動くようにする
 - firewalldを使いvirtual machineをlaunchした時点でfirewallを有効化しなければならない．
 - hostnameはMy loginにしないといけない
 - hostnameを変更する方法も知っていないといけない
 - sudoをinstall, 設定しないといけない
 - root userに加えて，My loginがusernameとして存在しなければならない
 - そのユーザーはuser42とsudoグループに所属しているようにしなければならない
 - 新しいユーザーを作り，グループに所属させる方法も知っていなければならない
 - #### passwordにおいていくつかの条件が課される
	- passwordの有効期限は30日
	- passwordを一度変更した場合，2日以上間隔をあけなければ再度変更できない
	- 有効期限7日前には，パスワード変更の警告メッセージを出力しなければならない
	- パスワードは10文字以上で，英数字，小文字，大文字を含み同じ文字を3回連続で並べることはできない
	- usernameは含めてはいけない
	- rootのパスワードには適応させないが，それ以外のパスワードは前回のパスワードの部分文字列が7文字以上含まれていてはいけない
 - #### sudoグループに強固な設定をするために，いくつかの条件が課される
	 - パスワード入力は間違えた入力が3回の時点で終了する
	 - 間違えた入力がされたらcustom massageを出力する
	 - inputsもoutputsも/var/log/sudo/folderに記録されている必要がある
	 - TTY modeは有効化されている必要がある
	 - sudoが使うことのできるpathたちは制限されていないといけない具体例としては,
	 /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
	 など
 - #### monitoring.shといわれるscriptを作成する必要がある
 - server startupでscriptがterminalsに以下にリストアップされた情報を表示しなければならない，また10分毎に表示されなければならない，バナーは任意でどのように動き，書き換えを行うとなく中断できるようになる必要がある
 
	 - kernelのバージョンとオペレーティングシステムのアーキテクチャ
	 - 物理processorの個数
	 - 仮想processorの個数
	 - サーバ上で現在使用可能なRAMと利用率
	 - サーバ上で現在使用可能なstorageと利用率
	 - 現在のCPUの使用率
	 - 最後にrebootした日付と時刻
	 - LVMが有効化されているか否か
	 - 接続の数
	 - サーバを利用しているユーザーの数
	 - サーバーのIPv4のaddressとMac address
	 - sudoによって実行されたcommandの数

