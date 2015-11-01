package Teikyo;

;######################################################################
;#
;# このライブラリはえうのすさん制作のDL集計互換のログファイルを書き込む
;# ためのものです
;# 
;# 原作者：えうのす
;# 関数化：R七瀬
;# バ〜ジョン：4.01
;#
;######################################################################
;#
;# ☆関数リファレンス☆
;#
;# DL集計ログに書き込む
;#	&Teikyo'regist(ログファイル名,共有認識名,提供品名,URL＆コメント,UP者名,削除パス) 
;# 
;# DL集計ログから読み出す
;#	&Teikyo'get_num(ログファイル名,共有認識名) 
;# 戻り値は
;# $Teikyo'SUM_title	提供品名です
;# $Teikyo'SUM_coment	URLとコメントです
;# $Teikyo'SUM_num	提供数です
;# $Teikyo'SUM_name	提供者名です
;# $Teikyo'SUM_pwd	暗号化されたPASSです
;#
;# DL集計ログ内の数値を修正する
;#	&Teikyo'rest(ログファイル名,共有認識名,修正後の提供品名,修正後のコメント,修正後のDLカウント数,修正後の共有認識名,修正後の追加者名,修正後の削除PASS) 
;#
;# DL集計ログから削除する
;#	&Teikyo'del(ログファイル名,共有認識名) 
;######################################################################
;#
;# ☆注意☆
;#
;# 共有認識名は重複しないように注意してください
;#
;######################################################################


# ログファイルへの書き込み
sub regist {
	local($sum_log,$SUM_date,$up_title,$up_comment,$geta,$R_name,$up_limit,$pwd) = @_;

	# 集計ログ作成
	open(SUM,">>$sum_log") || &error("Can't open $logfile");
	print SUM "$SUM_date<>$up_title<>$up_comment<>0<>$R_name<>$up_limit<>$pwd<>¥n";
	close (SUM);
}

# ログファイルからの読み出し
sub get_num {
	local($sum_log,$Aline) = @_;

	# 集計ログ確認
	open(SUM,"$sum_log") || return ("Can't open $sum_log");
	@Sum_Up = <SUM>;
	close (SUM);

	foreach $Sum_Up (@Sum_Up) {
		($a,$b,$c,$d,$e,$f,$g) = split(/<>/,$Sum_Up);
if ($a eq $Aline) {
$SUM_title = $b;
$SUM_coment = $c;
$SUM_num = $d;
$SUM_name = $e;
$SUM_limit = $f;
$SUM_pwd = $g;
last;
}
	}
}

# ログファイルの書き換え
sub rest {
	local($sum_log,$Aline,$up_name,$up_url,$up_count,$up_date,$R_name,$up_limit,$pwd) = @_;

	# 集計ログ確認
	open(SUM,"$sum_log") || return ("Can't open $sum_log");
	@Sum_Up = <SUM>;
	close (SUM);

	foreach $Sum_Up (@Sum_Up) {
		($a,$b,$c,$d) = split(/<>/,$Sum_Up);
if ($a eq $Aline) {
$Sum_Up = "$up_date<>$up_name<>$up_url<>$up_count<>$R_name<>$up_limit<>$pwd<>¥n";
}
push(@up_new,$Sum_Up);
	}

	# ログを更新
	$T_Tmp_File = "./$$.Ttmp";
	open (DB,">$T_Tmp_File") || &print_error('テンポラリファイル作成失敗');
	print DB @up_new;
	close (DB);

	rename ($T_Tmp_File,$sum_log) || &print_error('りねーむ失敗');
	chmod 0600,".$sum_log";

}

sub del {
	local($sum_log,$Aline) = @_;

	# 集計ログ読み出し
	open(SUM,"$sum_log") || return ("Can't open $sum_log");
	@Sum_Up = <SUM>;
	close (SUM);

	foreach $Sum_Up (@Sum_Up) {
		($a,$b,$c,$d) = split(/<>/,$Sum_Up);
if ($a eq $Aline) {
next;
}
push(@up_new,$Sum_Up);
	}

	# ログを更新
	$T_Tmp_File = "./$$.Ttmp";
	open (DB,">$T_Tmp_File") || &print_error('テンポラリファイル作成失敗');
	print DB @up_new;
	close (DB);

	rename ($T_Tmp_File,$sum_log) || &print_error('りねーむ失敗');
	chmod 0600,".$sum_log";
}

1;
