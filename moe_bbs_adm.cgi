#!/usr/bin/perl -T

$Settingfile = './moe_bbs_cnf.pl';

#for sysyopen()
use Fcntl;

#require "./jcode.pl";
#use Jcode;

# 設定ファイル読み込み
if ( -f "$Settingfile" ){
	require $Settingfile;
}else{
	require './moe_bbs_cnf.pl.org';
}

require './cgi-lib.pl';

$SCRIPT = './moe_bbs_adm.cgi';
$method = 'POST';
&form_decode;
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

if ($buffer) {
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		#&jcode'convert(*value,$charset);
		#Jcode::convert(*value,$charset);
		$value =~ s/\r//g;
		$FORM{$name} = $value;
	}
}

   if ($FORM{"mode"} eq "changeAdminPass") {&pass;&changeAdminPass;}
elsif ($FORM{"mode"} eq "editAdminPass")   {&pass;&editAdminPass;}
elsif ($FORM{"mode"} eq "changeConfig")    {&pass;&changeConfig;}
elsif ($FORM{"mode"} eq "editConfig")      {&pass;&editConfig;}

# 管理メニューの表示 #
&header;
print qq(
	[<a href=$script>掲示板に戻る</a>]
	<form action="$SCRIPT" method="$method">
    <input type=hidden name=bg_img value="$bg_img">
	<center><h4>$titleの管理</h4>
	　　各種設定の変更:<input type="radio" name="mode" value="editConfig" checked>
        管理用パスワードの変更:<input type="radio" name="mode" value="editAdminPass"><br><br>
	　　現在の管理用パスワード： <input type="password" name="plainAdminPass" size="20"><input type="submit" value="送信" $css_style>
	    <br><font size=2>（初期状態ではパスワード無しになっています）</font>
	</form></center><P><hr><P>
);
&footer;
exit;

sub pass { # 管理用パスワードによる認証 

#	if ($adminPass ne crypt($FORM{'plainAdminPass'},$adminPass) 
        if ($adminPass ne crypt($FORM{'plainAdminPass'},substr($adminPass,0,2))
	&& $adminPass) {

&header;
	print qq(
		<center><br><br><br><br>
		<h3 align="center">パスワードが間違っています。</h3>
		<h3 align="center">ブラウザのBACKボタンで戻ってやり直してください。</h3></center><P><hr><P>
	);
&footer;
	exit;
	}
}

sub changeAdminPass { # 管理用パスワードの書き換え

srand(time);
$crypted = crypt($FORM{'newAdminPass'},int(rand(90))+10);

if (!$FORM{'newAdminPass'}) {$crypted = '';}
#open(LOG,"$Settingfile") || die;
if ( -f "$Settingfile" ){
	sysopen(LOG,$Settingfile,O_RDONLY) || die;
}else{
	sysopen(LOG,"./moe_bbs_cnf.pl.org",O_RDONLY) || die;
}

@lines = <LOG>;
close(LOG);
for ($i=0; $i<=$#lines; $i++) {
	if ($lines[$i] =~ /^\$adminPass.*=/) { last; }
}
$lines[$i] = "\$adminPass = '$crypted';\n";

#open(LOG,">$Settingfile") || die;
sysopen(LOG,"$Settingfile",O_WRONLY |O_TRUNC |O_CREAT ) || die;
print LOG @lines;
close(LOG);

&header;
print qq(
    <center>
	<META HTTP-EQUIV="Refresh" CONTENT="0;URL=$SCRIPT?bg_img=$bg_img">
	<a href="admin.cgi">Please click here.</a></center><P><hr><P>
);
&footer;
exit;
}

sub editAdminPass { # 管理用パスワード変更フォームの表示

&header;
print qq(
	<form action="$SCRIPT" method="$method">
    
	<center><h4>管理用パスワードの変更</h4>
	新しい管理用パスワード： <input type="password" name="newAdminPass" size="20">
	<input type="hidden" name="plainAdminPass" value="$FORM{'plainAdminPass'}">
	<input type="hidden" name="mode" value="changeAdminPass">
    <input type=hidden name=bg_img value="$bg_img">
	<input type="submit" value="送信" $css_style>
	<br><br><br>
	</form></center><P><hr><P>
);
&footer;
exit;
}

sub changeConfig { # 設定の書き換え

#open(LOG,"$Settingfile") || die;
if ( -f "$Settingfile" ){
	sysopen(LOG,$Settingfile,O_RDONLY) || die;
}else{
	sysopen(LOG,"./moe_bbs_cnf.pl.org",O_RDONLY) || die;
}

@lines = <LOG>;
close(LOG);
for ($i=0; $i<=$#lines; $i++) {
	if ($lines[$i] =~ /^#\(SYSTEM\)/) { last; }

	if ($_DATA_ == 1 && $lines[$i] !~ "_DATA_") {$lines[$i] = ''; next;}
	$_DATA_ = 0;

	if ($lines[$i] =~ /^\$(\w+).*=.*<<"_DATA_";/) {
	$lines[$i] = "\$$1 = <<\"_DATA_\";\n$FORM{$1}\n";
	$_DATA_ = 1;
	}
	elsif ($lines[$i] =~ /^\$(\w+).*=.*'.*'/) {
		$FORM{$1} =~ s/'/&#39;/g;
		$lines[$i] = "\$$1 = '$FORM{$1}';\n";
	}
	elsif ($lines[$i] =~ /^\$(\w+).*=.*".*"/) {
		$FORM{$1} =~ s/"/&quot;/g;
		$lines[$i] = "\$$1 = \"$FORM{$1}\";\n";
	}
	elsif ($lines[$i] =~ /^\@(\w+).*=.*\(.*\)/) {
		@FORM = ();
		$name = $1;
		$FORM{$name} =~ s/'/&#39;/g;
		@FORM = split (/\n/, $FORM{$name});
		$FORM{$name} = join("','" , @FORM);
		if ($FORM{$name}) {$FORM{$name} = "'$FORM{$name}'";}
		$lines[$i] = "\@$name = ($FORM{$name});\n";
		$name = '';
	}
}
#open(LOG,">$Settingfile") || die;
sysopen(LOG,"$Settingfile", O_WRONLY | O_TRUNC |O_CREAT ) || die;
print LOG @lines;
close(LOG);

&header;
print qq(
	<center>
	<META HTTP-EQUIV="Refresh" CONTENT="0;URL=$SCRIPT?bg_img=$bg_img">
	<a href="$SCRIPT?bg_img=$bg_img">Please click here.</a></center>
);
&footer;
exit;

}

sub editConfig {
# 設定変更フォームの表示 #
&form_decode;
&header;
print qq(
[<a href=$script>掲示板に戻る</a>]
<form action="$SCRIPT" method="$method">
<input type=hidden name=bg_img value="$bg_img">
<div align="center">
<font size=2>（<font size=3 color="#ff0000">*</font> 印のある項目は必ず入力してください）</font>
</div>
);

$system = 0;
#open(LOG,"$Settingfile") || die;
if ( -f "$Settingfile" ){
	sysopen(LOG,$Settingfile,O_RDONLY) || die;
}else{
	sysopen(LOG,"./moe_bbs_cnf.pl.org",O_RDONLY) || die;
}

foreach $logline (<LOG>) {
	if ($logline eq "\n") {next;}
	if ($_DATA_ == 1 && $logline !~ "_DATA_") {next;}
	$_DATA_ = 0;
	if ($logline =~ "#【(.+)】") {
	if ($opentable == 1) {$opentable = 0;print "</table></div><br><br>";}
	print "■ $1<B></B><p>\n";
	print "<div align='center'>\n";
	print "<table border=1 width=97% cellpadding=2 cellspacing=0 bordercolorlight='#999999' bordercolordark='#999999'>\n";
	$opentable = 1;
	} elsif ($logline eq "#(SYSTEM)\n") {
		$system = 1;
	} elsif ($logline =~ /^#/) {
		if ($logline =~ /(###)/) { next; }
		if ($logline =~ /(^##|^#)(.+)/) {$menu = $2;}
		print "<tr><td>";
		if ($logline !~ /##/) { print "<font color='#ff0000'>*</font>"; }
		print "<font size=2>$menu</font></td>";
	} elsif (!$system) {
	if ($logline =~ /<<"_DATA_";/) {
	if ($logline =~ /^\$(\w+).*=/) {$name = $1;}
	$$name =~ s/\s*$//;
	print "<td><TEXTAREA NAME='$name' ROWS=4 COLS=40>$$name</textarea></td></tr>\n";
	$_DATA_ = 1;
	}
	elsif ($logline =~ /^\$(\w+).*=/) {
	$name = $1;
print <<"_HTML_";
	<td>
	<input name='$name' value='$$name' size='40'>
	</td></tr>
_HTML_
		}
	elsif ($logline =~ /^\@(\w+).*=/) {
	$name = $1;
	$$name = join("\n" , @$name);
print <<"_HTML_";
	<td>
	<TEXTAREA NAME='$name' ROWS=4 COLS=40>$$name</textarea>
	</td></tr>
_HTML_
		}	} else {
		/^\$(\w+).*=.*"(.*)"/;
		print "<input type=\"hidden\" name=\"$1\" value=\"$2\">\n";
	}
}
close(LOG);
		print qq(
			</table>
			</div><center><p>
			<input type="hidden" name="plainAdminPass" value="$FORM{'plainAdminPass'}">
			<input type="hidden" name="mode" value="changeConfig">
			<br>
			<input type="submit" value="送信" $css_style>
			<br><br><br>
			</form></center><P><hr><P>
		);
&footer;
		exit;
		
}

## --- HTMLのヘッダー
sub header {
$bg_img = $in{'bg_img'};
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
<title>$titleの管理</title>
<STYLE type="text/css">
<!--
$bdcss
body,tr,td,th { font-size: 10pt }
a:link        { font-size: 10pt; color:$link }
a:visited     { font-size: 10pt; color:$vlink }
a:active      { font-size: 10pt; color:$alink }
a:hover       { font-size: 10pt; color:$alink }
span          { font-size: 18pt }
big           { font-size: 12pt }
small         { font-size: 9pt }
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
<br>
萌々ぼ〜ど2001 by えうのす ＆ R七瀬<BR>
（正式名：被羅目板2001萌え萌えVer 〜了承♪ by 被羅目〜）<br><font size=2>Customized By 月読 Ver 6.0</font>
<br>Customized By <a href=https://github.com/sina2/moe/ target=_blank>しなしな</a>
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
sub form_decode {

	&ReadParse;
	while (($name,$value) = each %in) {

		if ($name !~ /icon_file/){

		# 文字コードをEUC変換
		#&jcode'convert(*value,'euc');
                #Jcode::convert(*value,'euc');

		# 一括削除用
		if($name eq 'del'){@del=split(/\0/,$value);}

		$FORM{$name} = $value;

		}
	}
}
