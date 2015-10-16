#!/usr/bin/perl

# jcode.plが同一ディレクトリにある場合
#require './jcode.pl';
#use Jcode;

# 設定ファイル読み込み
require './moe_bbs_cnf.pl';
require './cgi-lib.pl';

## 管理者pass
$master_pass ="siosio";

## 萌え板と同じクッキー名に
$COOKIE_name = 'MOE_BBS';

&form_decode;

$num=0;

## YYBBSからのコメント読み込み処理 ##

if($date){
$siori = length $date;
if($siori eq '30'){ $date = substr($date,0,-6) ;}
open(SUM,"$sum_up_log");
@lines=<SUM>;
close(SUM);
chop(@lines);
foreach $key (@lines) {
	($up_date,$up_name,$up_url,$up_count,$person,$limit,$ango) = split(/<>/,$key);
$sayuri = length $up_date;
if($sayuri eq '30'){ $up_date = substr($up_date,0,-6) ;}
if ($date eq $up_date){$up_count = $up_count+1;$up{$date}="$up_name<>$up_url<>$up_count<>$person<>$limit<>$ango<>";$exist=1;}
$newlines[$num]="$up_date<>$up_name<>$up_url<>$up_count<>$person<>$limit<>$ango<>\n";
$num=$num+1;
}
open(NEWSUM,">$sum_up_log");
foreach(@newlines){
print NEWSUM "$_";
}
close(NEWSUM);

($new_up_name,$new_up_url,$new_up_count,$new_person,$new_limit,$dmy)=split(/<>/,$up{$date});

&header;
if (($new_limit < $new_up_count) && (($new_limit >= '1') && ($new_limit <= '999'))) {print "<BR><BR><BR><p align=center><B><font color = blue>提供終了したよ〜</font></B></p></center><BR><P><hr><P>\n";}
elsif ($exist==1){
print "<center><B>提供者：$new_person</B><BR>\n";
print "<B>提供品名：$new_up_name　提供数：$new_limit　現在のDL数:$new_up_count</B><BR><BR>\n";
print "<pre><B><font color = blue>コメント</font></B><BR>$new_up_url</pre>\n";}
else {print "<BR><BR><BR><p align=center><B><font color = blue>$date、$up_date削除されました</font></B></p></center><BR><P><hr><P>\n";}
&footer;

## ＤＬ数順表示 ##

}elsif($mode eq 'num'){

open(SUM,"$sum_up_log");
@newlines=<SUM>;
close(SUM);
chop(@newlines);
&header;
print "<p align = center><font size =+2>ＤＬ数順</font></p>\n";
print "<table border =1 align = center><tr align=center><td>日付</td><td>提供者</td><td>提供品名</td><td>提供数</td><td>ＤＬ数</td></tr>\n";
	foreach $key (@newlines) {
		($up_date,$up_name,$up_url,$up_count,$person,$limit) = split(/<>/,$key);
		$count{$up_date}=$up_count;
		$name{$up_date}=$up_name;
		$person{$up_date}=$person;
        $limit{$up_date}=$limit
	}
@key = keys(%count);
@sorted_up_count = sort by_num @key;
sub by_num{$count{$b} <=> $count{$a};}
$num=0;
	foreach(@sorted_up_count){
		$cut_date=substr($sorted_up_count[$num],5);
		print "<tr><td>$cut_date</td><td>$person{$sorted_up_count[$num]}</td><td>$name{$sorted_up_count[$num]}</td><td align = right>$limit{$sorted_up_count[$num]}</td><td align = right>$count{$sorted_up_count[$num]}</td></tr>\n";
		$num=$num+1;
	}
print "</table><P><hr><P>\n";
&footer;

## 複数コメント閲覧 ##

}elsif($mode eq 'get'){
if(defined(@get_up)){
open(SUM,"$sum_up_log");
@lines=<SUM>;
close(SUM);

@r_lines = reverse(@lines);
	foreach(@get_up){chop($r_lines[$_]);
		($up_date,$up_name,$up_url,$up_count,$person,$limit,$ango) = split(/<>/,$r_lines[$_]);
		$new_up_count=$up_count+1;
		$r_lines[$_] = "$up_date<>$up_name<>$up_url<>$new_up_count<>$person<>$limit<>$ango<>\n";
		$get_lines[$_] = $r_lines[$_];
	}

@newlines = reverse(@r_lines);
open(NEWSUM,">$sum_up_log");

	foreach(@newlines){
		print NEWSUM "$_";
	}
close(NEWSUM);

&header;

	foreach $key (@get_lines) {
		if($key eq ''){print"\n";}
		else{($up_date,$up_name,$up_url,$up_count,$person,$limit) = split(/<>/,$key);
		print "<center><B>提供者：$person</B><BR>\n";
		print "<B>提供品名：$up_name　提供数：$limit　現在のＤＬ数:$up_count</B><BR><BR>\n";
		print "<pre><B><font color = blue>コメント</font></B><br>$up_url</pre></center><hr>\n";
	}
	}

&footer;

}else{
&header;
print "<BR><BR><P align = center><font color = red><B>チェックボタンが選択されてません</B></font></P><P><hr><P>\n";
&footer;
}

## ユーザー削除 ##

}elsif($mode eq 'usr_del'){

if(defined($u_pass_check)){
	open(SUM,"$sum_up_log");
	@lines=<SUM>;
	close(SUM);
	@r_lines = reverse(@lines);
	($up_date,$up_name,$up_url,$up_count,$person,$limit,$ango) = split(/<>/,$r_lines[$usr_del]);
	$plain_text=$u_pass_check;
	&passwd_decode($ango);
	if($ango eq ''){$check="no";}
	}

if(defined($usr_del) && $check eq "yes"){
	open(SUM,"$sum_up_log");
	@lines=<SUM>;
	close(SUM);
	@r_lines = reverse(@lines);
		foreach $key(@r_lines){
			if($num == $usr_del){$key_on =1;}
			if($key_on != 1){push(@new_del_up,$r_lines[$num]);}
			$num=$num+1;$key_on=0;
		}
	$num=0;
	@newlines = reverse(@new_del_up);
	open(NEWSUM,">$sum_up_log");
		foreach(@newlines){
			print NEWSUM "$_";
		}
	close(NEWSUM);
&usr;

}
elsif(defined($usr_del) && $check ne "yes"){
&header;
	print "<BR><BR><BR><p align=center><font color = red size =+2>passが違います</font></p><P><hr><P>\n";
&footer;
}else{
open(SUM,"$sum_up_log");
@newlines=<SUM>;
close(SUM);
chop(@newlines);
&usr;
}

## 管理人削除 ##

}elsif($mode eq 'master_del'){

if(defined(@del_up) && $m_pass_check eq $master_pass){
	open(SUM,"$sum_up_log");
	@lines=<SUM>;
	close(SUM);
	@r_lines = reverse(@lines);
		foreach $key(@r_lines){
			foreach(@del_up){if($num == $_){$key_on =1;}}
			if($key_on != 1){push(@new_del_up,$r_lines[$num]);}
			$num=$num+1;$key_on=0;
		}
	$num=0;
	@newlines = reverse(@new_del_up);
	open(NEWSUM,">$sum_up_log");
		foreach(@newlines){
			print NEWSUM "$_";
		}
	close(NEWSUM);
&kanri;

}
elsif(defined(@del_up) && $m_pass_check ne $master_pass){
&header;
	print "<BR><BR><BR><p align=center><font color = red size =+2>passが違います</font></p><P><hr><P>\n";
&footer;
}else{
open(SUM,"$sum_up_log");
@newlines=<SUM>;
close(SUM);
chop(@newlines);
&kanri;
}

## 新着順表示

}else{
open(SUM,"$sum_up_log");
@newlines=<SUM>;
close(SUM);
chop(@newlines);
@r_newlines = reverse(@newlines);
&header;
	print "<center><font size =+2>新着順ＤＬ集計</font>\n";
	print "<hr width='220pt' size=2>\n";
	print "<center><small>[<a href=$sum_up_script?mode=usr_del&bg_img=$bg_img target=_top>記事削除</a>][<a href=$sum_up_script?mode=master_del&bg_img=$bg_img target=_top>管理者削除</a>][<a href=$sum_up_script?mode=num&bg_img=$bg_img target=_top>ＤＬ数順</a>]</small>\n";
	print "<hr width='220pt' size=2></center>\n";
	print "<table border =1 align = center><tr align=center><td> </td><td>日付</td><td>提供者</td><td>提供品名</td><td>提供数</td><td>ＤＬ数</td></tr>\n";
	print "<form method='POST' action=$sum_up_script><input type=hidden name=bg_img value='$bg_img'><input type=hidden name=mode value='get'>\n";
		foreach $key (@r_newlines) {
		($up_date,$up_name,$up_url,$up_count,$person,$limit,$dmy) = split(/<>/,$key);
		$cut_date=substr($up_date,5);
        
    if (($limit >= '1') && ($limit <= '999')) {
        if ($limit <= $up_count) { print "<tr><td>完</td><td>$cut_date</td><td>$person</td><td>$up_name</td><td align = right>$limit</td><td align = right>$up_count</td></tr>\n";}
		else { print "<tr><td><input type='checkbox' name=get_up value=$num></td><td>$cut_date</td><td>$person</td><td>$up_name</td><td align = right>$limit</td><td align = right>$up_count</td></tr>\n";}}
    else { print "<tr><td><input type='checkbox' name=get_up value=$num></td><td>$cut_date</td><td>$person</td><td>$up_name</td><td align = right>無制限</td><td align = right>$up_count</td></tr>\n";}
    
		$num=$num+1;
		}
	print "</table><BR>\n";
	print "<p align=center>複数チェックして下の送信ボタンを押すとまとめてコメントが見れます<BR><BR>\n";
	foreach(@get_up){
		($up_date,$up_name,$up_url,$up_count,$person,$limit,$dmy) = split(/<>/,$r_newlines[$_]);
			
			print "<B>提供者：$person</B><BR>\n";
			print "<B>提供品名：$up_name　提供数：$limit　現在のＤＬ数:$up_count</B><BR><BR>\n";
			print "<B><font color = blue>コメント</font></B><BR>$up_url<BR>\n";
		}
	print "<input type='submit' value='まとめてget♪' $css_style><input type=hidden name=bg_img value=$bg_img></form><BR><BR><P><hr><P>\n";
	print "</p>\n";
&footer;
}

sub form_decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }

	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# 文字コードをS-JIS変換
		#&jcode'convert(*value,'sjis');
		#Jcode::convert(*value,'sjis');
		if($name eq 'get_up'){push(@get_up,$value);}
		if($name eq 'del_up'){push(@del_up,$value);}
		$FORM{$name} = $value;
	}
    

	$date    = $FORM{'sumu_up'};
	$mode    = $FORM{'mode'};
	$m_pass_check = $FORM{'m_pass_check'};
	$u_pass_check = $FORM{'u_pass_check'};
	$usr_del = $FORM{'u_del_up'};

	&ReadParse;
	while (($name,$value) = each %in) {

		if ($name !~ /icon_file/){

		# 文字コードをEUC変換
		#&jcode'convert(*value,'euc');
		#Jcode::convert(*value,'euc');

		# 一括削除用
		if($name eq 'del'){@del=split(/\0/,$value);}

		# タグ処理
		$value =~ s/&/&amp;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\"/&quot;/g;
		$value =~ s/\r//g;
		$value =~ s/\n//g;

		$FORM{$name} = $value;

		}
	}
}

## 管理者削除共通出力
sub kanri{
@r_newlines = reverse(@newlines);
&header;
	print "<p align = center><font color = blue size =+2>管理者削除</font><BR><BR>\n";
	print "<table border =1 align = center><tr align=center><td> </td><td>日付</td><td>提供者</td><td>提供品名</td><td>提供数</td><td>ＤＬ数</td></tr>\n";
	print "<form method='POST' action=$sum_up_script><input type=hidden name=mode value='master_del'>\n";
		foreach $key (@r_newlines) {
		($up_date,$up_name,$up_url,$up_count,$person,$limit) = split(/<>/,$key);
		$cut_date=substr($up_date,5);
		print "<tr><td><input type='checkbox' name=del_up value=$num></td><td>$cut_date</td><td>$person</td><td>$up_name</td><td align = right>$limit</td><td align = right>$up_count</td></tr>\n";
		$num=$num+1;
		}
	print "</table><BR>\n";
	print "<p align=center>複数チェックしてからpassを入れて下の送信ボタンを押すとまとめて削除できます<BR><BR>\n";
	print "pass：<input type='password' name='m_pass_check' size=10>\n";
	print "<input type='submit' value='まとめて削除♪' $css_style></form></p><P><hr><P>\n";
&footer;
}

## ユーザー削除共通出力
sub usr{
@r_newlines = reverse(@newlines);
&header;
	print "<p align = center><font color = blue size =+2>ユーザー削除</font><BR><BR>\n";
	print "<table border =1 align = center><tr align=center><td> </td><td>日付</td><td>提供者</td><td>提供品名</td><td>提供数</td><td>ＤＬ数</td></tr>\n";
	print "<form method='POST' action=$sum_up_script><input type=hidden name=mode value='usr_del'>\n";
		foreach $key (@r_newlines) {
		($up_date,$up_name,$up_url,$up_count,$person,$limit) = split(/<>/,$key);
		$cut_date=substr($up_date,5);
		print "<tr><td><input type='radio' name=u_del_up value=$num checked></td><td>$cut_date</td><td>$person</td><td>$up_name</td><td align = right>$limit</td><td align = right>$up_count</td></tr>\n";
		$num=$num+1;
		}
	print "</table><BR>\n";
	print "<p align=center>チェックしてから書き込み時のpassを入れて下の送信ボタンを押すと削除できます<BR><BR>\n";
	&get_cookie;
	print "pass：<input type='password' name='u_pass_check' value=\"$c_pwd\" size=10>\n";
	print "<input type='submit' value='削除♪' $css_style></form></p><P><hr><P>\n";
&footer;
}
## パスワード照合
sub passwd_decode {
	if ($_[0] =~ /^\$1\$/) { $key = 3; }
	else { $key = 0; }

	$check = "no";
	if (crypt($plain_text, substr($_[0],$key,2)) eq "$_[0]") {
		$check = "yes";
	}
}

## --- クッキーを取得
sub get_cookie { 
	@pairs = split(/\;/, $ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		local($name, $value) = split(/\=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/\,/, $DUMMY{"$COOKIE_name"});
	foreach $pair (@pairs) {
		local($name, $value) = split(/\:/, $pair);
		$COOKIE{$name} = $value;
	}
	$c_pwd   = $COOKIE{'pwd'};
}
## --- HTMLのヘッダー
sub header {
$bg_img = $in{'bg_img'};
	$pt_b = $pt + 2 . 'pt';
	$pt_s = $pt - 1 . 'pt';
	$pt .= pt;
	$t_point .= pt;

	if($css){
	if ($backgif) { $bgpic = $backgif; }
	elsif ($bg_img) { $bgpic = $bg_img; }
	$bdcss="body{ background:url($bgpic) $bgrep $bgatc $bg_pos}";
	if($ENV{'HTTP_USER_AGENT'} !~ /MSIE/){$css = 0;}
	}

	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<title>DL集計〜ヽ(´ー｀)ノ</title>
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
<NOSCRIPT><SCRIPT>/*<BODY>*/</SCRIPT></NOSCRIPT>
<noembed><body></noembed>
EOM

	# bodyタグ
	if ($backgif && !$css) { $bgkey = "background=\"$backgif\" bgcolor=$bgcolor"; }
	elsif ($bg_img && !$css) { $bgkey = "background=\"$bg_img\" bgcolor=$bgcolor"; }
	else { $bgkey = "bgcolor=$bgcolor"; }
	print "<body $bgkey text=$text link=$link vlink=$vlink alink=$alink>\n";
}

## --- HTMLのフッター
sub footer {
	print <<"_HTML_";
<center>$banner2<P><small>
萌々ぼ〜ど2001 by えうのす ＆ R七瀬<BR>
（正式名：被羅目板2001萌え萌えVer 〜了承♪ by 被羅目〜）<br><br><font size=2>Customized By <a href=http://powder-snow.milk.tc/ target=_blank>月読</a> Ver 6.0</font>
</small></center>
_HTML_

	$id1 = "$yeart$mont$mdayt$hourt$mint$sect";
	$id2 = rand(1000000000);
	$id2 = sprintf("%.10d",$id2);
	for( $t=0; $t<32; $t++ ){ 
	$id3 .= $st_table[ int( @string_table * rand() ) ]; }
print "</body></html>";
if($nobanner){print "<noembed>";}
}
