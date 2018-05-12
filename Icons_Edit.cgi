#!/usr/bin/perl -T

#for sysopen()
use Fcntl;

# 設定ファイル読み込み
if ( -f "./moe_bbs_cnf.pl" ){
	require './moe_bbs_cnf.pl';
}else{
	require './moe_bbs_cnf.pl.org';
}

require './cgi-lib.pl';
$cgi_lib'maxdata = $ico_max * $ico_rv_num;
#'
$max_sz = $ico_max/1024;

&form_decode;
if($in{'icon_edit'}){&edit;}
elsif($in{'add_submit'}){&icon_add;}
elsif($in{'del_submit'} || $in{'rst1_submit'} || $in{'rst2_submit'} || $in{'pri_ico'} || $in{'pri_del'}){&icon_del;}
elsif($in{'icon_reg'}){&icon_reg;}
elsif($in{'rank'}){&rank;}

&pre_edit;

sub rank{

#open (LST,"$icofile") || &error("Can't open $icofile");
sysopen(LST,"$icofile",O_RDONLY) || &error("Can't open $icofile");
@Icons = <LST>;
close(LST);
$num = @Icons ;

foreach $ico(@Icons){
$add_ck=0;
($d1,$d2,$d3,$name) = split(/\t/,$ico);

foreach (keys(%rank)){
if($_ eq $name){++$rank{$name};$add_ck=1;last;}
}
if(!$add_ck){$rank{$name}=1;}

}

#open (LST,"$i_rank_log") || &error("Can't open $i_rank_log");
if ( -f "$i_rank_log" ){
	sysopen(LST,"$i_rank_log",O_RDONLY | O_REAT) 
}else{
	sysopen(LST,"$i_rank_log", O_WRONLY |O_TRUNC | O_CREAT )
}
@ico_rank = <LST>;
close(LST);

#open(IN,"$icofile") || &error("Can't open $icofile",'NOLOCK');
sysopen(IN,"$icofile",O_RDONLY) || &error("Can't open $icofile",'NOLOCK');

@icons = <IN>;
close(IN);
$i=0;
	foreach $icon (@icons) {
	if ($icon !~ /^#/) {
	($Inum[$i],$icon1[$i],$icon2[$i],$usr_n[$i],$usr_p[$i]) = split(/\t/,$icon);
	if($Inum[$i] =~ /pri_ico/){$icon2[$i] = "$icon2[$i]（$usr_n[$i]専用）";}
	$i++;
	}
}

foreach $ico_rank(@ico_rank){
($name,$cnt) = split(/<>/,$ico_rank);
$ico_rank{$name} = $cnt;

	foreach(0 .. $#icon1) {
	if($name eq $icon1[$_]){$ico_name{$name} = $icon2[$_];}
	}

}

if($icon_dir2){$icon_dir = $icon_dir2;}

$s_num = keys(%rank);
&header;
print <<EOM;
<a name=top>[<a href=$script?cnt=no>掲示板に戻る</a>]</a>
<br>
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>アイコンらんきんぐ〜</SPAN></b></font><br><br>
<a name=add><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌え総数 $num らんきんぐ参加人数 $s_num人</font><br><br>
<table width=\"100%\"><tr><td><b>※このランキングはアイコン追加ランキングです（ｗ</b><td align=right><a href=#ico>アイコン</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

@sort_rank = sort {$rank{$b} <=> $rank{$a}} keys(%rank);
foreach(@sort_rank){
++$rk;
	if($nex_jg == $rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $rank{$_};
$per = int((($rank{$_}/$num)*100)+0.5);
if(!$per){$per=1;}
$gif_w =int($rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
print "</table><br>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$ico_rank{$b} <=> $ico_rank{$a}} keys(%ico_rank);
foreach(@sort_rank){if($ico_rank{$_}){++$num;$all_num = $all_num + $ico_rank{$_};}}

print <<EOM;
<a name=ico><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">アイコン人気ランキング♪</font><br><br>
<table width="100%"><tr><td><b>※このランキングはアイコン使用頻度ランキングTOP50です（ｗ</b></td><td align=right><a href=#add>アイコン追加</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>アイコン名</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

$st_top = 49;
$st_num = @sort_rank;
if($st_num < 50){$st_top = $st_num;}

foreach(0 .. $st_top){
++$rk;$st_tp = $sort_rank[$_];
	if($nex_jg == $ico_rank{$st_tp}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $ico_rank{$st_tp};
$per = int((($ico_rank{$st_tp}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($ico_rank{$st_tp}){
$gif_w =int($ico_rank{$st_tp}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$ico_name{$st_tp}</b></td><td><b>$ico_rank{$st_tp}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}

print "</table>";
print "</cener>";

&footer;
exit;
}


sub icon_del{

if(!$del[0]){&error("チェックボックスにチェックがされてません");}

#open(AD,"$passfile");
sysopen(AD,"$passfile",O_RDONLY);
$ad_pass=<AD>;
close(AD);
$ad_pass =~ s/\n//;
($dm,$ad_pwd) = split(/:/,$ad_pass);
$ck_ad_pwd = &pwd_de("$ad_pwd");
if(($in{name} eq $ad_name) && $ck_ad_pwd){$ad_mode=1;}

if($fll){
	foreach (1 .. 10) {
		unless (-e $icolock) {last;}
			sleep(1);
	}
}
#open (LST,"$icofile") || &error("Can't open $icofile");
sysopen(LST,"$icofile",O_RDONLY) || &error("Can't open $icofile");
@Icons = <LST>;
close(LST);

#open(IN,"$rank_log") || &error("Can't open $rank_log");
sysopen(IN,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
@rank = <IN>;
close(IN);

	$cut_name = $in{'name'};
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;

if($pass_mode){
foreach(@rank){
($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
if($cut_name eq "$d1"){$d6 =~ s/\n//;
if($d6){$encode_pwd = $d6;}
last;}
}
}

foreach $del(@del){

foreach (@Icons){
($num,$file,$name,$register,$pwd) = split(/\t/,$_);

	if($num eq $del){
	if($encode_pwd){$pwd = $encode_pwd;}
	$ck_pwd = &pwd_de("$pwd");
	if(!$ck_pwd && !$ad_mode){&error("パスワードが違います");}

	if($in{'pri_ico'}){
	$num =~ s/^pri_ico//;
	$num = "pri_ico$num";
	$_ = "$num\t$file\t$name\t$register\t$pwd\t\n";
	next;
	}

	if($in{'pri_del'}){
	$num !~ s/^pri_ico//;
	$_ = "$num\t$file\t$name\t$register\t$pwd\t\n";
	next;
	}

	if($in{'del_submit'}){
	push(@del_img,$file);
	$_ ="";
	next;
	}

	if($in{'rst1_submit'}){
	push(@rst_img,$_);
	next;
	}

	if($in{'rst2_submit'}){
	$inm = "icon_name$num";
	$_ = "$num\t$file\t$in{$inm}\t$register\t$pwd\t\n";
	next;
	}

	}
}

}

if($in{'rst1_submit'}){&icon_add;}

if($fll){
	&fll("$icolock","$icofile",@Icons);
}else{
	#open (LST,">$icofile") || &error("Can't open $icofile");
	sysopen (LST,"$icofile", O_WRONLY | O_TRUNC | O_CREAT ) || &error("Can't open $icofile");
	print LST @Icons;
	close(LST);
}

if($in{'del_submit'}){
	foreach(@del_img){
	$del_img = "$icon_dir$_";
#	if( -e "$del_img"){unlink("$del_img");}
	}

#open (LEN,">rw_ck.chk");
sysopen (LEN,"rw_ck.chk" , O_WRONLY | O_TRUNC | O_CREAT);
print LEN ;
close(LEN);

if($fll){
	foreach (1 .. 10) {
		unless (-e $irklock) {last;}
		sleep(1);
	}
}
#open(RLT,"$i_rank_log") || &error("Can't open $i_rank_log");
sysopen(RLT,"$i_rank_log",O_RDONLY) || &error("Can't open $i_rank_log");
@i_rank = <RLT>;
close(RLT);

$d_roop = @del_img;

foreach $ir(@i_rank){
$del_on = 0;
($fl) = split(/<>/,$ir);
if($d_roop){foreach (@del_img){if($fl eq $_){$del_on = 1;--$d_roop;}}}
if(!$del_on){push(@new_ir,$ir);}
}

if($fll){
	&fll("$irklock","$i_rank_log",@new_ir);
}else{
	#open(RLT,">$i_rank_log") || &error("Can't open $i_rank_log");
	sysopen(RLT,"$i_rank_log", O_WRONLY | O_TRUNC | O_CREAT) || &error("Can't open $i_rank_log");
	print RLT @new_ir;
	close(RLT);
}
}

&edit;
}

sub icon_reg{
&up_icon;

#open(AD,"$passfile");
sysopen(AD,"$passfile",O_RDONLY);
$ad_pass=<AD>;
close(AD);
$ad_pass =~ s/\n//;
($dm,$ad_pwd) = split(/:/,$ad_pass);
$ck_ad_pwd = &pwd_de("$ad_pwd");

if (!$ck_ad_pwd || ($in{'name'} ne $ad_name)){&get_cookie;&set_cookie;}

$pwd = &pwd_en($in{pwd});

if($fll){
	foreach (1 .. 10) {
		unless (-e $icolock) {last;}
		sleep(1);
	}
}
#open (LST,"$icofile") || &error("Can't open $icofile");
sysopen(LST,"$icofile",O_RDONLY) || &error("Can't open $icofile");
@Icons = <LST>;
close(LST);

	$cut_name = $in{'name'};
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;

foreach(@reg_num){
($ic_nm,$tail) = split(/<>/,$_);
$upf_name="icon_name$ic_nm";
$new = "$date$ic_nm\tico$date$ic_nm$tail\t$in{$upf_name}\t$cut_name\t$pwd\t\n";
push(@new,$new);
}

$lp_num = $in{ad_pos};
foreach(@Icons){
if(!$lp_num && !$reg_off){push(@newline,@new);$reg_off=1;}
push(@newline,$_);
if($lp_num){--$lp_num;}
}
if(!$reg_off){push(@newline,@new);}

if($fll){
	&fll("$icolock","$icofile",@newline);
}else{
	#open (LST,">$icofile") || &error("Can't open $icofile");
	sysopen (LST,"$icofile",O_WRONLY |O_TRUNC |O_CREAT ) || &error("Can't open $icofile");
	print LST @newline;
	close(LST);
}

#open (LEN,">rw_ck.chk");
sysopen (LEN,"rw_ck.chk",O_WRONLY | O_TRUNC | O_CREAT );
print LEN $all_len;
close(LEN);

&header;
print "[<a href=$script?cnt=no>掲示板に戻る</a>]";
print"<br><center><h3><font color=blue>以下のアイコン登録が完了しました</font></h3>";
print "<table border=1 cellspacing=0><tr>";

foreach(@reg_num){
if(!($br % 5)){print"</tr><tr>";}
++$br;
($ic_nm,$tail) = split(/<>/,$_);
if($icon_dir2){$icon_dir = $icon_dir2;}
$img = "$icon_dir\ico$date$ic_nm$tail";
$upf_name="icon_name$ic_nm";
print"<td><img src=$img><br>$in{$upf_name}</td>"
}
print"</tr></table>";
&footer;
exit;
}

#open(IN,"$rank_log") || &error("Can't open $rank_log");
sysopen(IN,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
@rank = <IN>;
close(IN);

	$cut_name = $in{'name'};
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;
if($pass_mode){
foreach(@rank){
($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
if($cut_name eq "$d1"){$d6 =~ s/\n//;
if($d6){
$ck_pwd = &pwd_de("$d6");
if(!$ck_pwd){&error("$cut_nameさんのパスワードと一致しません");}
}
last;}
}
}

sub pre_edit{

&get_cookie;
&header;
print <<"EOM";
<br>
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>$titleアイコンこ〜な〜</SPAN></b></font></center><br>
<form method="POST" action="$iconCGI">
<center>
<table bgcolor=white cellspacing=0 border=1 bordercolor=black><tr><td>
<input type=hidden name=icon_edit value=on>
<input type=hidden name=bg_img value="$bg_img">
<table>
<tr><td>お名前</td><td><input type=text name=name size=12 value=\"$c_name\"></td></tr>
<tr><td>削除キー</td><td><input type=password name=pwd size=12 maxlength=8 value=$c_pwd></td></tr>
</table>

<br>
<center><input type=submit value=OK></center>

</td></tr></table>
EOM
&footer;
exit;
}

sub edit {
if(!$in{'name'}){$name_err="お名前";}
if(!$in{'pwd'}){$pwd_err="削除キー";}
if($name_err || $pwd_err){&error("$name_err $pwd_err が未記入です");}
#open (LST,"$icofile") || &error("Can't open $icofile");
sysopen(LST,"$icofile",O_RDONLY) || &error("Can't open $icofile");
@Icons = <LST>;
close(LST);

#open(IN,"$rank_log") || &error("Can't open $rank_log");
sysopen(IN,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
@rank = <IN>;
close(IN);

$ia_num = @Icons;
if($ia_num){

if($in{i_pg} eq "all"){$st_num = 0; $ed_num = $ia_num - 1;}
else{
if(!$in{i_pg}){$in{i_pg} = 1;}
$ict_num_ex = "page :";

$ict_num = int(($ia_num - 1)/100) + 1;

$st_num = ($in{i_pg} - 1) * 100;
$ed_num = $st_num + 99;
if($ed_num + 1 > $ia_num){$ed_num = $ia_num - 1;}

$pg_name = $in{name};
$pg_name =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2',$1)/ge;
$pg_name =~ s/\s/+/g;

$pg_pwd = $in{pwd};
$pg_pwd =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2',$1)/ge;
$pg_pwd =~ s/\s/+/g;

foreach(1 .. $ict_num){
if($in{i_pg} eq "$_"){$ict_num_ex = "$ict_num_ex <b>$_</b>";}
else{$ict_num_ex = "$ict_num_ex <a href=\"$iconCGI?i_pg=$_&icon_edit=on&name=$pg_name&pwd=$in{pwd}&bg_img=$in{bg_img}\">$_</a>";}
}

$ict_num_ex = "<br>$ict_num_ex <a href=\"$iconCGI?i_pg=all&icon_edit=on&name=$pg_name&pwd=$in{pwd}&bg_img=$in{bg_img}\">all</a>";
}

}

else{ $st_num=0; $ed_num=0;} ###

&header;
print <<"EOM";
[<a href=$script?cnt=no>掲示板に戻る</a>]
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>$titleアイコンこ〜な〜</SPAN></b></font></center><br>
<center>
<table border=1 cellspacing=0 bordercolor=black bgcolor=white><tr><td>

<PRE>
ここでアイコンの追加ができます<br>
追加したい場所のNo（このNoの下に追加されます。一番上に追加したい場合は場所Noは0）と
個数を入力してください（<b>一度に追加できる数は$ico_rv_num個までです</b>）

また、登録したアイコンを削除、編集、専用化、専用化解除したい場合にはチェックをして各種ボタンを押して下さい。
<b>アイコン専用化は複数可能\です。</b>
<font color=red><b>（削除、編集、専用化、専用化解除ボタンは一番下です。）</b></font>
</PRE>
<blockquote>
<FORM action="$iconCGI" METHOD=POST>
追加場所No <input type=text size="2" name=ad_pos value="0">
<span>　</span>
追加数 <input type=text size="2" maxlength="3" name=ad_num value="0">
<span>　</span>
<input type=submit name=add_submit value="追加する">
　
<a href=\"$script?mode=image&i_pg=$in{i_pg}&sort=rgd&bg_img=$in{bg_img}\" target=_blank>アイコン画像参照</a>
<input type=hidden name="name" value="$in{name}">
<input type=hidden name="pwd" value="$in{pwd}">
<input type=hidden name=bg_img value="$bg_img">
<table width="100%"><tr><td align=center>$ict_num_ex</td></tr></table>
<table>
 <tr>
  <td>
  </td>
  <th align=left>No.</th>
  <th align=left>名前</th>
 </tr>
EOM

#open(AD,"$passfile");
sysopen(AD,"$passfile",O_RDONLY);
$ad_pass=<AD>;
close(AD);
$ad_pass =~ s/\n//;
($dm,$ad_pwd) = split(/:/,$ad_pass);
$ck_ad_pwd = &pwd_de("$ad_pwd");

	$cut_name = $in{'name'};
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;

			if($pass_mode){
			foreach(@rank){
			($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
			if($cut_name eq "$d1"){
			$d6 =~ s/\n//;if($d6){$ck_mpwd=&pwd_de("$d6");}
			last;}
			}
			}
$i = $st_num ;
foreach $Icon ($st_num .. $ed_num) {
$i++;
		($num,$file,$name,$register,$pwd) = split(/\t/,$Icons[$Icon]);
if(!$ck_mpwd){$ck_pwd=&pwd_de("$pwd");}
if($num =~ /pri_ico/){$name = "$name\　<font color=blue><b>（$register専用）</b></font>";}
if((($register eq $cut_name) && ($ck_mpwd || $ck_pwd)) || ($ck_ad_pwd && ($in{'name'} eq $ad_name))){$ckbx="<input type=checkbox name=del value=$num>";}else{$ckbx="";}
print <<"EOM";
 <tr>
  <td>$ckbx</td>
  <td>No.$i</td>
  <td>$name</td>
 </tr>
EOM
}
print <<"EOM";
</table>
<br>
<input type=submit name=del_submit value="削除する">
<span>　</span>
<input type=submit name=rst1_submit value="編集する">
<span>　</span>
<input type=submit name=pri_ico value="専用化">
<span>　</span>
<input type=submit name=pri_del value="専用化解除">
</blockquote></td></tr></table></form></center>
EOM
&footer;
exit;
}


sub icon_add{
if ( ($in{'ad_pos'} !~ /\d+/) || ($in{'ad_num'} !~ /\d+/) ){
&error("追加場所と追加数は半角数字で記入して下さい");
}
if(!$in{'ad_num'} && !$in{'rst1_submit'}){&error("アイコン追加数が設定されてません");}
if($in{'ad_num'} > $ico_rv_num){&error("一度に登録できるアイコンは$ico_rv_numコまでです");}
$add_num = $in{'ad_num'};

	if($in{'rst1_submit'}){
	$ti_ex = "名編集";
	$ic_md="rst2_submit";
	$rt_ic="<th align=left>アイコン</th>";
	}else{
	$ad_cm ="アイコン１個あたりのファイルサイズは $max_sz kまで<br>jpg,gif,pngが登録できます";
	$ti_ex = "追加";
	$ic_md="icon_reg";
	$rt_ic2="<th align=left>アイコン画像追加</th>";
	}

&header;

print <<"EOM";
<br>
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>アイコン$ti_exも〜ど</SPAN></b></font></center><br>
<form method="POST" action="$iconCGI" enctype=multipart/form-data>
<center>
<table bgcolor=white cellspacing=0 border=1 bordercolor=black><tr><td>
<input type=hidden name=$ic_md value=on>
<input type=hidden name=ad_pos value=\"$in{ad_pos}\">
<input type=hidden name=bg_img value="$bg_img">
<input type=hidden name=name value=\"$in{name}\">
<input type=hidden name=pwd value=\"$in{pwd}\">
<table>
<tr><td colspan=2>$ad_cm<br>
<br></td></tr>
<tr>$rt_ic<th align=left>アイコン名</th>$rt_ic2</tr>
EOM

if($in{'rst1_submit'}){
	foreach (@rst_img){
	($num,$file,$name) = split(/\t/,$_);

	if($icon_dir2){$icon_dir = $icon_dir2;}
	$img = "$icon_dir$file";

	print"<tr><td><img src=\"$img\"><input type=hidden name=del value=$num></td>";
	print"<td><input type=text name=\"icon_name$num\" value=\"$name\"></td>";
	}
}else{
	foreach (1 .. $add_num){
	print"<tr><td><input type=text name=\"icon_name$_\"></td>";
	print"<td><input type=file name=\"icon_file$_\"></td></tr>";
	}
}

print "</table><br>";
print"<center><input type=submit value=OK></center>";
print "</form></td></tr></table>";
&footer;
exit;
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
<!doctype html>
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
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
if($nobanner){print "";}
}

## --- パスワード暗号処理
sub pwd_en{
	$now = time;
	($p1, $p2) = unpack("C2", $now);
	$wk = $now / (60*60*24*7) + $p1 + $p2 - 8;
	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	$nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
	$ango = crypt($_[0], $nsalt);
	return $ango;
}

## --- パスワード照合処理
sub pwd_de{
	if ($_[0] =~ /^\$1\$/) { $key = 3; }
	else { $key = 0; }

	$check = "";
	if (crypt($in{'pwd'}, substr($_[0],$key,2)) eq "$_[0]") {
		$check = "ok";
	}
	return $check;
}

## デコード等
sub form_decode {

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

		$in{$name} = $value;

		}
	}
}


sub up_icon{

	&date;

	foreach (@in) {

	$_ =~ s/\s//g;

	if($_ =~ /(.*)name=\"icon_file(\d*)\"(.*)filename=\"(.*)\"Content-Type:(.*)\/(.*)/){
	$ic_nm = $2;
	$f_name = $4;
	$f_type = $6;
	$upf_name="icon_name$ic_nm";
	$upf_bin="icon_file$ic_nm";

	if(!$in{$upf_name}){&error("アイコン名が未記入のものがあります");}
	if(!$in{$upf_bin}){&error("$in{$upf_name}のアイコンファイルが選択されていません");}
	if(length($in{$upf_bin}) > $ico_max){&error("$in{$upf_name}のアイコンファイルサイズが$max_sz\kを超えています");}
	$all_len = $all_len + length($in{$upf_bin});
	$tail="";

	if ($_ =~ /application\/x-macbinary/i) { $macbin = 1; }

	if ($f_type =~ /gif/i) { $tail=".gif"; }
	if ($f_type =~ /jpeg/i) { $tail=".jpg"; }
	if ($f_type =~ /x-png/i) { $tail=".png"; }
	if ($f_type =~ /png/i) { $tail=".png"; }

	if (!$tail && $macbin) {
		if ($f_name =~ /.gif/i) { $tail=".gif"; }
		if (($f_name =~ /.jpg/i) || ($f_name =~ /.jpeg/i)){ $tail=".jpg"; }
		if ($f_name =~ /.png/i) { $tail=".png"; }
	}
	
	if (!$tail) { &error("$in{$upf_name}のアイコンはアップロードできないファイル形式です"); }

	$tmp_reg = "$ic_nm<>$tail<>$macbin<>";
	push(@reg_num,$tmp_reg);
	}
	}

if(!$in{'rst2_submit'}){
	#open (LEN,"rw_ck.chk");
	sysopen(LEN,"rw_ck.chk",O_RDONLY);
	$len_ck = <LEN>;
	close(LEN);
	if ($len_ck == $all_len) { &error("同アイコンの連続追加はできません"); }
}
	foreach(@reg_num){
	($ic_nm,$tail,$mac) = split(/<>/,$_);

	$ImgFile = "$icon_dir\ico$date$ic_nm$tail";
	$upf_bin="icon_file$ic_nm";
	$upfile = $in{$upf_bin};

	# マックバイナリ対策
	if ($mac) {
		$length = substr($upfile,83,4);
		$length = unpack("%N",$length);
		$upfile = substr($upfile,128,$length);
	}

	#open(OUT,"> $ImgFile") || &error("アイコンのアップロードに失敗しました");
	sysopen(OUT,"$ImgFile",O_WRONLY |O_TRUNC |O_CREAT ) || &error("アイコンのアップロードに失敗しました");
	binmode(OUT);
	binmode(STDOUT);
	print OUT $upfile;
	close(OUT);

	chmod (0606,$ImgFile);
	}

}

# エラー処理
sub error{
&header;
print"<center><font color=red><B>$_[0]</B></font></center>";
print"</body></html>";
&footer;
exit;
}

## --- クッキーの発行
sub set_cookie {
	# クッキーは60日間有効
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$dmy,$dmy)
					 	= gmtime(time + 60*24*60*60);
	$yearg += 1900;
	if ($secg  < 10) { $secg  = "0$secg";  }
	if ($ming  < 10) { $ming  = "0$ming";  }
	if ($hourg < 10) { $hourg = "0$hourg"; }
	if ($mdayg < 10) { $mdayg = "0$mdayg"; }

	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul',
				'Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday',
				'Thursday','Friday','Saturday')[$wdayg];

	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";
	$c_name = $in{name};
	$c_pwd = $in{pwd};
	$cook="name\:$c_name\,email\:$c_email\,url\:$c_url\,pwd\:$c_pwd\,icon\:$c_icon\,color\:$c_color\,mail_ex\:$c_m_ex";
	print "Set-Cookie: $COOKIE_name=$cook; expires=$date_gmt\n";
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

		# 文字コードをEUC変換 #
		#&jcode'convert(*value,'euc');
                #Jcode::convert(*value,'euc');

		$COOKIE{$name} = $value;
	}
	$c_name  = $COOKIE{'name'};
	$c_email = $COOKIE{'email'};
	$c_url   = $COOKIE{'url'};
	$c_pwd   = $COOKIE{'pwd'};
	$c_icon  = $COOKIE{'icon'};
	$c_color = $COOKIE{'color'};
	$c_m_ex = $COOKIE{'mail_ex'};
}

## 日時の取得
sub date{
# 日時の取得
$ENV{'TZ'} = "JST-9";
$times = time;
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);

$year = $year+1900;$mon = $mon+1;

$date = sprintf("%04d%02d%02d%02d%02d%02d",$year,$mon,$mday,$hour,$min,$sec);
}

sub fll{
	$tmpfile = shift(@_);
	$log_f = shift(@_);
	foreach (1 .. 10) {
		unless (-e $tmpfile) {last;}
		sleep(1);
	}
	$tmp_1 = "$$\.tmp";

	#open(TMP,">$tmp_1") || &error("TMPファイル書きこみ失敗ヽ(´ー｀)ノ");
	sysopen(TMP,"$tmp_1", O_WRONLY|O_TRUNC|O_CREAT ) || &error("TMPファイル書きこみ失敗ヽ(´ー｀)ノ");
	print TMP @_;
	close(TMP);

	foreach (1 .. 10) {
		if (link($tmp_1,$tmpfile)) {
			rename($tmpfile,$log_f); 
			chmod(oct($vt_pm),$log_f);
			last;
		}
		sleep(1);
	}
	unlink $tmp_1;
}
