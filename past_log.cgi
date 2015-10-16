#!/usr/bin/perl

# 設定ファイル読み込み
require './moe_bbs_cnf.pl';

## 設定完了

# 過去ログカウントファイルを読み込み
#open(NUM,"$nofile") || &error("Can't open $nofile");
open(NUM,"$nofile") || open(NUM,"+>$nofile");
$count = <NUM>;
close(NUM);


## -------- メイン処理 --------------------------------- ##

&get_form;
if (!$buffer) { &frame; }
&form_decode;

if ($mode eq 'ue_html') { &ue_html; }
if ($mode eq 'find_html') { &find_html; }
if ($mode eq 'do_find') { &do_find; }
exit;

## --------- 処理完了 ---------------------------------- ##

## 検索処理ルーチン
sub do_find {
	@lines = ();
	foreach (1 .. $count) {
		open(DB,"$past_dir\/$_\.html");
		@new_data = <DB>;
		close(DB);

		push(@lines,@new_data);
	}

	$word =~ s/　/ /g;
	$word =~ s/\t/ /g;
	@pairs = split(/ /,$word);

	# 過去ログファイルを読み込み
	foreach $line (@lines) {
		$flag = 0;
		foreach $pair (@pairs){
			if (index($line,$pair) >= 0){
				$flag = 1;
				if ($cond eq 'or') { last ; }
			} else {
				if ($cond eq 'and'){ $flag = 0; last; }
			}
		}
		# ヒットした行を新規配列(@new)に格納
		if ($flag) { push(@new,$line) ; }
	}

	# 検索結果の配列数を数える
	$count = @new;

	# 該当なしの場合
	if ($count == 0) { &nainai; }

	# 結果を出力
	&header;
	print <<"HTML";
<center><table border=1>
<tr><td bgcolor=#FFFFFF>
[<a href="$past_log?mode=find_html">検索画面に戻る</a>]</td>
<td nowrap>キーワード <font color=#FF0080><b>$word</b></font> は
<b>$count</b>件見つかりました。</td></tr></table>
</center><hr>
HTML

	foreach $new_line (@new) {
		($title,$msg) = split(/<\!--T-->/,$new_line);
		print "$title $msg\n";
	}

	print "</body></html>\n";
	if($nobanner){print "<noembed>";}
	exit;
}

## フレーム部
sub frame {

	# 過去ログ用カウントファイルをチェック
	unless (-e $nofile) { &error("Don't exist $nofile"); }

	print "Content-type: text/html\n\n";
	print <<"HTML";
<html>
<head><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8"><title>過去ログ</title></head>
<frameset rows="110\,*" FRAMEBORDER=no BORDER=0>
<frame name="ue" src="$past_log?mode=ue_html" target="sita">
<frame name="sita" src="$past_dir\/$count\.html">
<noframes>
<body>
<h3>フレーム非対応のブラウザの方は利用できません。</h3>
</body></noframes></frameset>
</html>
HTML

	if($nobanner){print "<noembed>";}
	exit;
}

## 上フレーム（メニュー部）
sub ue_html {
	&header;
	print <<"HTML";
[<a href="$script?cnt=no" target=_parent>掲示板へもどる</a>]
[<a href="$past_log?mode=find_html" target="sita">ワード検索</a>]
<table width=100%>
<tr><th bgcolor=#0000A0>
<font color=#FFFFFF>過 去 ロ グ</font>
</th></tr></table>
<hr size=2><center>
[<a href="$past_dir\/$count\.html" target="sita">最新</a>]
HTML
	# 過去ログの[リンク]を新規順に表示
	for ($i=$count-1; $i>0; $i--) {
		print "[<a href=\"$past_dir\/$i\.html\" target=\"sita\">$i</a>]\n";
	}

	print "</center><hr size=2>\n";
	print "</body></html>\n";
	if($nobanner){print "<noembed>";}
	exit;
}

## フォーム取得
sub get_form {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
}

## フォームからのデータ処理
sub form_decode {
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$FORM{$name} = $value;
	}
	$word = $FORM{'word'};
	$cond = $FORM{'cond'};
	$mode = $FORM{'mode'};
	$opt  = $FORM{'opt'};
	$chk  = $FORM{'chk'};
}

## 検索該当なし
sub nainai {
	&header;
	print "<center>見つかりませんでした。<hr>\n";
	print "<b>$word</b></center>\n";
	print "</body></html>\n";
	if($nobanner){print "<noembed>";}
	exit;
}

## 検索初期画面
sub find_html {
	&header;
	print <<"HTML";
<center>
<table border=0 cellpadding=10>
<tr><td bgcolor=#FFFFFF nowrap>
<center><B>過去ログ検索</B></center>
<OL>
<LI><b>キーワード</b>から該当記事を検索します。
<LI><b>半角スペース</b>で区切って複数のキーワード指定が可\能\です。
<LI><b>検索条件</b>を選択し「検索する」ボタンを押して下さい。
</OL>
</td></tr></table>
<form action="$past_log" method="$method">
<input type=hidden name=mode value="do_find">
<table border=1>
<tr><td>キーワード</td><td><input type=text name=word size=30></td></tr>
<tr><td>検索条件</td><td><input type=radio name=cond value="and" checked>AND
<input type=radio name=cond value="or">OR</td></tr>
<tr><th colspan=2><input type=submit value="検索する"></th></tr>
</table>
</form></center>
<hr>
</body></html>
HTML
	if($nobanner){print "<noembed>";}
	exit;
}

## --- HTMLのヘッダー
sub header {
	$pt_b = $pt + 2 . 'pt';
	$pt_s = $pt - 1 . 'pt';
	$pt .= pt;
	$t_point .= pt;

	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<meta http-equiv="pragma" content="no-cache">
<STYLE type="text/css">
<!--
$bdcss
body,tr,td,th { font-size: $pt }
a:link        { font-size: $pt; color:$link }
a:visited     { font-size: $pt; color:$vlink }
a:active      { font-size: $pt; color:$alink }
a:hover       { font-size: $pt; color:$alink }
span          { font-size: $t_point }
big           { font-size: $pt_b }
small         { font-size: $pt_s }
body{
scrollbar-arrow-color:#blue;
scrollbar-base-color:#ffffff;
scrollbar-highlight-color:#blue;
scrollbar-shadow-color:#blue;
scrollbar-darkshadow-color:#ffffff;
scrollbar-track-color:#ffffff;
}
input {
color : blown;border-width : 1px 1px 1px 1px;
border-style : solid solid solid solid;
border-color : #000000 #000000 #000000 #000000;
color : black;
background-color : #ffffff;
}
-->
</STYLE>
<title>$title</title>
</head>
EOM

	print "<body bgcolor=$bgcolor text=$text link=$link vlink=$vlink alink=$alink>\n";
}

## エラー処理
sub error {
	&header;
	print "<center><hr width=75%><h3>システムエラー発生！</h3>\n";
	print "<P><font color=#dd0000><B>$_[0]</B></font>\n";
	print "<P><hr width=75%></center>\n";
	print "</body></html>\n";
	if($nobanner){print "<noembed>";}
	exit;
}
