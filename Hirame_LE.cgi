#!/usr/bin/perl

# jcode.plが同一ディレクトリにある場合
#require './jcode.pl';
use Encode;

# For sysopen()
use Fcntl;

# しぃじぃあぃぱ〜るぅ〜
require './cgi-lib.pl';
# 設定ファイル読み込み
if ( -f "./moe_bbs_cnf.pl" ){
	require './moe_bbs_cnf.pl';
}else{
	require './moe_bbs_cnf.pl.org';
}

# バージョン情報
$ver = '萌々ぼ〜ど2001 Ver0.54';

#================================================#
#  これ以降は改造したい方だけが変更してください  #
#================================================#


#$cgi_lib'maxdata bug
$cgi_lib'maxdata=$maxdata;


# bgm_mime-type
%ok_ad=("wav","wav","mid","mid","mpeg","mp3","x-ms-asf","asf","x-ms-wma","wma");

if($icon_dir2){$icon_dir = $icon_dir2;}

if ($UP_Pl == 1) {
require './Teikyo.pl';
}

@string_table = split( //, $string_table );

# フォームのデコード
&form_decode;

## 各種制限 ##
if($rf_etc){

	## リファ
	if($ref_rf){
		$ref=$ENV{'HTTP_REFERER'};
		push(@call_bbs,"http://$ENV{'SERVER_NAME'}");
		foreach(@call_bbs){
			if($ref =~/^$_/i){$ref_on = 1;}
		}
	if(!$ref_on){$err_on = "referer ";$err_on2 = "$ref ";&error("@call_bbs");}
	}

	$ip = $ENV{'REMOTE_ADDR'};
	foreach(@rf_ip){
		if($ip =~ /$_/){$err_on = "$err_on\IP ";$err_on2 = "$err_on2$ip ";last;}
	}
	if(@rf_host){
		$host = $ENV{'REMOTE_HOST'};
		if (!$host || $host eq "$ip") {
			$host = gethostbyaddr(pack("C4", split(/\./,$ip)), 2);
		}
		if (!$host) { $host = $ip; }
		foreach(@rf_host){
			if($host =~ /$_/){$err_on = "$err_on\host ";$err_on2 = "$err_on2$host ";last;}
		}
	}

	foreach(@rf_name){
		#&get_cookie;$in{'name'} = $c_name;
		if($in{'name'} =~ /$_/){$err_on = "$err_on\IP ";$err_on2 = "$err_on2$in{'name'} ";last;}
	}

}

if($err_on){
	if($rf_etc == 3 || $rf_etc == 1){
		&get_time;
		$date3 = sprintf("%04d%02d%02d",$year,$mon,$mday);
		$err_log="$log_dir$date3\.log";
		$err_reg = "$date - $ENV{'REMOTE_ADDR'} - $err_on2\r\n";
		if (-e $err_log){
			#open(ERL,"$err_log") or &error("$err_log オープン失敗ヽ(´ー｀)ノ");
			sysopen(ERL,"$err_log",O_RDONLY) or &error("$err_log オープン失敗ヽ(´ー｀)ノ");
			if($flock){flock(ERL,2) or &error("filelock 失敗ヽ(´ー｀)ノ");}
			@err_log = <ERL>;
			close(ERL);
			$erl_ex=1;
		}
		push(@err_log,$err_reg);	
		if($fll){
			&fll("err_log.tmp","$err_log",@err_log);
		}else{
			#open(ERL,">$err_log") or &error("$err_log オープン失敗ヽ(´ー｀)ノ");
			sysopen(ERL,"$err_log", O_WRONLY |O_TRUNC | O_CREAT ) or &error("$err_log オープン失敗ヽ(´ー｀)ノ");
			if($flock){flock(ERL,2) or &error("filelock 失敗ヽ(´ー｀)ノ");}
			print ERL @err_log;
			close(ERL);
			if(!$erl_ex){chmod(oct($vt_pm),$err_log);}
		}

	}
	if($rf_etc >= 2){
		if($err_sort){
			#if ($ENV{PERLXS} eq "PerlIS") {
			#	print "HTTP/1.0 302 Temporary Redirection\r\n";
			#	print "Content-type: text/html\n\n";
			#}
			if(!$redi){
				print "Location: $ex_url\n\n";
			}else{
				&header;
				print "<META HTTP-EQUIV=\"Refresh\" Content=0\;url=$ex_url>";
				&footer;
			}
		}else{
			$no_bk = 1;
			&error("$err_on 制限にひっかかったかもｗヽ(´ー｀)ノ");
		}
	}
}

if($rf_etc >= 2 && $ck_use){		
	$tr_ck = 1;
	&get_cookie;
	if(!$c_name || !$c_pwd){
		if($in{name} && $in{pwd}){
			#if ($ENV{PERLXS} eq "PerlIS") {
			#	print "HTTP/1.0 302 Temporary Redirection\r\n";
			#	print "Content-type: text/html\n\n";
			#}
			if(!$redi){
				&set_cookie;
				print "Location: $script\n";
				print "\n";
			}else{
				&set_cookie;
				&header;
				print "<META HTTP-EQUIV=\"Refresh\" Content=0\;url=$script>";
				&footer;
			}
			exit;
		}
		&header;
		if($in{ck_rf}){
			$ccg = "$icon_dir"."cookie2\.jpg";
			$cmsg = "いいから食いやがれぇ♪ヽ(´ー｀)ノ";
			$csmg2 = "<font color=red><b>クッキーを食べないと先に進めませんｗ</b></font>";
		}else{
			$ccg = "$icon_dir"."cookie1\.jpg";
			$cmsg = "クッキーを食べてね♪ヽ(´ー｀)ノ$c_name$c_pwd";
			$csmg2 = "<a href =\"$script?ck_rf=on\"><b>クッキーを食べないで先に進みたい</b></a>";
		}
print <<EOM;
<center><table><tr><td><img src=$ccg><br><center>$cmsg</center></td></tr>
<tr><td><table border=1 cellspacing=0 width=\"100%\"><tr><th>
<table>
<form action=$script method=POST>
<tr><td>お名前</td><td><input type=text name=name size=15></td></tr>
<tr><td>削除キー</td><td><input type=password name=pwd size=15></td></tr>
<tr><td colspan=2>
<input type=submit value="登録"> <small>（クッキーをONにして登録します。）</small><br><br>
今まで投稿したことがない方は新規で入力して下さい<br>
※ 登録情報はクッキー保存に使用するだけです。<br><br>
$csmg2
</td></tr>
</table>
</th></tr></table></td></tr></table></form>
EOM
		&footer;
		&exit;
	}
}

## ここまで各種制限 ##

# パスワード確認処理[カ〜ル板の真似]
#open(DB,"$passfile") || &error("$passfileが無いです");
sysopen(DB,"$passfile",O_RDONLY | O_CREAT) || &error("$passfileが無いです");
@lines = <DB>;
close(DB);
$password = shift(@lines);
chop($password) if ($password =~ /\n$/);
($header, $password) = split(/:/, $password);
if($password =~ /^\$1\$/) {$salt = 3;} else {$salt = 0;}
if ($header ne 'crypt_password' || $password eq '') {$start2 = 1; &password;}

## --- メイン処理
if ($mode eq "howto") { &howto; }
if ($mode eq "find") { &find; }
if ($mode eq "usr_del") { &usr_del; }
if ($mode eq "msg_del") { &msg_del; }
if ($mode eq "msg") { &regist; }
if ($mode eq "res_msg") {&res_msg; }
if ($mode eq "admin") { &admin; }
if ($mode eq "admin_del") { &admin_del; }
if ($mode eq "image") {&icon_exe; &image; }
if ($mode eq "rest") { &rest; }
if ($mode eq "rank_rest") { &rank_rest; }
if ($mode eq "usr_rest") {&usr_rest; }
if ($mode eq "Reg_usr_rest") { &usr_rest2; }
if ($mode eq "pass_rest") { &pass_rest; }
if ($mode eq "bkup") { &bk_up; }
if ($mode eq "mail"){ &mail;}
if ($mode eq "mc_ex"){ &mc_ex;}
if ($mode eq "swf"){ &swf;}
if ($mode eq "convert"){ &convert;}
if ($in{'papost'} eq 'pcode') { &password; }
if ($new_topic eq "new") {&new_topic;}
if ($new_topic eq "gazou") { &gazou_topic; }
if ($new_topic eq "flash") { &flash_topic; }
if ($in{'rank'}){ &rank;}
if ($in{'vt'}){ &vote;}

	# アイコン設定ファイル読み込み
sub icon_exe{
	#open(IN,"$icofile") || &error("Can't open $icofile",'NOLOCK');
	sysopen(IN,"$icofile",O_RDONLY | O_CREAT ) || &error("Can't open $icofile",'NOLOCK');
	@icons = <IN>;
	close(IN);
$Icon_num = @icons;

	# アイコン名前順並び替え
	if ($nm_st && !$in{sort}){
	foreach(@icons){($d1,$d2,$d3) = split(/\t/,$_);$ico{$d1} = $d3;$icos{$d1} = $_;}
	@sorted = sort {$ico{$a} cmp $ico{$b}} keys %ico;
	$st = 0;	foreach(@sorted){$icons[$st] = $icos{$_} ;++$st;}
	}
    
unshift(@icons,"00\tnone.gif\t無くてﾖｼ♪\t");
unshift(@icons,"01\trand.gif\tらんだむ♪\t");


$i=0;
	foreach $icon (@icons) {

	if ($icon !~ /^#/) {
	($Inum[$i],$icon1[$i],$icon2[$i],$usr_n[$i],$usr_p[$i]) = split(/\t/,$icon);
	if($Inum[$i] =~ /pri_ico/){$icon2[$i] = "$icon2[$i]（$usr_n[$i]専用）";
	$icon = "$Inum[$i]\t$icon1[$i]\t$icon2[$i]\t$usr_n[$i]\t$usr_p[$i]\t";
	if(!$in{sort}){push(@pri_ico,$icon);}else{++$i;}
	}else{++$i;}
	}

	}

	foreach(@pri_ico){($Inum[$i],$icon1[$i],$icon2[$i],$usr_n[$i],$usr_p[$i]) = split(/\t/,$_);++$i;}

	$nm_ico_nm  = $Icon_num - @pri_ico;
}

&html_log;

## --- 記事表示部
sub html_log {
	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_agent;

	# ログを読み込み
	#open(LOG,"$logfile") || &error("Can't open $logfile",'NOLOCK');
	sysopen(LOG,"$logfile",O_RDONLY | O_CREAT) || &error("Can't open $logfile",'NOLOCK');
	@lines = <LOG>;
	close(LOG);

	# 記事番号をカット
	shift(@lines);

	# 更新順に並び替え
	if($in{'dt_sort'}){&dt_sort;}
	
	# 親記事のみの配列データを作成
	@new = ();
	if($in{'rev_sort'}){@lines = reverse(@lines);}
	foreach $line (@lines) {
		local($num,$k,$dt,$na,$em,$sub,$com,
			$url,$host,$pw,$color,$icon,$b,$up_on,$ImgFile,$pixel) = split(/<>/, $line);

		# 親記事を集約
		if ($k eq "") { push(@new,$line); }
	if($ImgFile && ($ImgFile !~ /bgm$/) && ($ImgFile !~ /cgm$/) && ($ImgFile !~ /swf$/) && !$bg_img){$bg_img=$ImgFile;}
	elsif($ImgFile && ($ImgFile =~ /cgm$/) && !$bg_img){$ImgFile =~ s/\.([^.]*)cgm$//;$bg_img=$ImgFile;}
	}

	# レス記事はレス順につけるため配列を逆順にする
	if(!$in{'rev_sort'}){@lines = reverse(@lines);}

	if($in{'vt_all'}){
		opendir (DIR,$vt_dir);
		@dir_list = readdir DIR;
		close(DIR);
		foreach(@dir_list){
			if($_ =~ /(\d+)\.vt/){push(@vt_list,$1);}
		}
		foreach(@vt_list){
			foreach $ln(@new){
				local($num) = split(/<>/, $ln);
				if($_ == $num){push(@vt_lines,$ln);last;}
			}
		}
		@new = reverse(@vt_lines);
	}

	# ヘッダを出力
	&header;

	# カウンタ処理
	if ($counter) { &counter; }

	# タイトル部

	if ($title_gif eq '') {
		$ti_gif="<font color=\"$t_color\" size=6 face=\"$t_face\"><SPAN>$title</SPAN></font>";
	}
	else {
		$ti_gif="<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\">";
	}

if ($mode eq "B") {$ds_on="&ds=on";}

	# 過去ログのリンク部を表示
	if ($pastkey) {
		$past_mode="[<a href=\"$past_log\">過去ログ</a>]";
	}
if($hari_mode){
if($bgm_up){$bgm_tk="・BGM";}
$hari_ex="[<a href=\"$script?new_topic=gazou&bg_img=$bg_img$ds_on\"><B>画像$bgm_tk貼\り付け</B></a>]";
}
if($flash_mode){
$flash_ex="[<a href=\"$script?new_topic=flash&bg_img=$bg_img$ds_on\"><B>Flash貼\り付け</B></a>]";
}
if($icon_mode){$imd="[<a href=\"$iconCGI?bg_img=$bg_img\">アイコンこ〜な〜</a>][<a href=\"$iconCGI?bg_img=$bg_img&rank=on\">アイコンらんきんぐ</a>]";}
if ($UP_Pl) {$up_mode="[<a href='$sum_up_script?bg_img=$bg_img'>DL集計</a>]"; }
if($bgm_up){$bgm_tk="・BGM貼\り付け";}
if($web_mode){$web="[<a href=\"$webedit?bg_img=$bg_img\">設定変更</a>]";}
if($mode eq "all_log"){$all_log = "&mode=all_log";}
if(!$in{'dt_sort'}){
$dt_sort="[<a href='$script?dt_sort=on&bg_img=$bg_img&cnt=no$all_log'>最終レス日順</a>]";
}else{
$dt_sort="[<a href=$script?cnt=no$all_log>新着記事順</a>]";
$hid_dt="<input type=hidden name=dt_sort value=on><input type=hidden name=bg_img value=$bg_img >";
if($homepage eq $script){$homepage="$homepage?dt_sort=on&bg_img=$bg_img&cnt=no";}
$dt_log = "&dt_sort=on";
}

if(!$in{'rev_sort'}){$rev_sort = "[<a href='$script?rev_sort=on&bg_img=$bg_img&cnt=no$all_log'>旧記事順</a>]";}
else{
$rev_sort = "[<a href=$script?cnt=no$all_log>新着記事順</a>]";
$hid_dt="<input type=hidden name=rev_sort value=on><input type=hidden name=bg_img value=$bg_img >";
if($homepage eq $script){$homepage="$homepage?rev_sort=on&bg_img=$bg_img&cnt=no";}
$dt_log = "&rev_sort=on";
}

if($hari_mode || $bgm_up){$hn_db = "[<a href=\"$script?bg_img=$bg_img&rank=on\">貼\り逃げだ〜び〜</a>]";}
if($mode eq "all_log"){$alg = "[<a href=\"$script?cnt=no$dt_log\">通常表\示</a>]";}else{$alg = "[<a href=\"$script?mode=all_log&bg_img=$bg_img&cnt=no$dt_log\">全記事表\示</a>]";}
if($pass_mode){$pm_ex = "[<a href=\"$script?mode=pass_rest&bg_img=$bg_img\">認証pass変更</a>]";}
if($tg_mc){$tg_mc2 = "[<a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank>マクロ説明</a>]";}
if($tg_mc && $vt_btn){
	if(!$in{'vt_all'}){$vt_mc = "[<a href=\"$script?vt_all=on\">投票記事一覧</a>]";}
	else{$vt_mc = "[<a href=\"$script?cnt=no\">通常表\示</a>]";}
}
if($mlfm){$ml_tmn = "[<a href=\"$script?mode=mail&bg_img=$bg_img\">め〜るふぉ〜む</a>]";}
print <<EOM;
<center>$banner1<P>
$ti_gif
<hr width=\"90%\" size=2>
<table border=0 cellpadding=5 bgcolor="#ffffff"><tr><td>
[<a href=\"$homepage_back\">ホームにもどる</a>]
[<a href=\"$homepage\">トップにもどる</a>]
[<a href=\"$script?mode=howto&bg_img=$bg_img\">掲示板の使い方</a>]
[<a href="$script?new_topic=new&bg_img=$bg_img$ds_on"><B>新規$bgm_tk</B></a>]
$hari_ex
$flash_ex
<br>
$tg_mc2
[<a href=\"$script?mode=rest&bg_img=$bg_img$ds_on\">記事編集</a>]
[<a href="$script?mode=msg_del&bg_img=$bg_img">記事削除</a>]
$pm_ex
$imd
$hn_db
$past_mode
[<a href=\"$script?mode=find&bg_img=$bg_img\">ワード検索</a>]
[<a href="$script?mode=admin&bg_img=$bg_img$ds_on">管理用</a>]
$web
<br>
$ml_tmn
$vt_mc
$up_mode
$alg
$dt_sort
$rev_sort
<td><tr></table>
<hr width="90%" size=2></center>
EOM
&kiji_edit;
}

sub kiji_edit {

	if ($in{'page'} eq '') { $page = 0; } 
	else { $page = $in{'page'}; }

	# 記事数を取得
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }
	if ($mode eq "all_log" || $in{'vt_all'}) { $page_end = $end_data; }
	foreach ($page .. $page_end) {
		($number,$k,$date,$name,$email,$sub,
			$comment,$url,$host,$pwd,$color,$icon,$tbl,$up_on,$ImgFile,$pixel) = split(/<>/, $new[$_]);

		$pic_ex="";
        $yoko_hiritu="";
        $tate_hiritu="";
        
        chomp $pixel;
        
		($email,$mail_ex) = split(/>/,$email);

		$sname = $name;
        $sname =~ s/＠.*//;
        $sname =~ s/☆.*//;
	    $sname =~ s/@.*//;
	    $sname =~ s/★.*//;
        
		if(!$mlfm){
			if($email){$name="<a href=\"mailto:$email\">$name</a>"}
		}
        else{
			if ($email && $mail_ex) { $name = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$date\">$name</a>"; }
			elsif ($email) { $name = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$date\">$name</a>"; }
		}

		# URL表示
		if ($url && $home_icon) {
			$url = "<a href=\"http://$url\" target='_blank'><img src=\"$icon_dir$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\" alt='HomePage'></a>";
		}
        elsif ($url && !$home_icon) {
			$url = "&lt;<a href=\"http://$url\" target='_blank'>HOME</a>&gt;";
		}
		$tbl_color1 = $tbl_color;
		$text1 = $text;
		$sub_color1 = $sub_color;
        
		if ($tbl eq 'on') {
		    $tbl_color1 = $tbl_color2;
		    $text1 = $text2;
		    $sub_color1 = $sub_color2;
        }
		if  ($up_on eq 'up_exist'){
        
$up_html= <<EOM;
<td><form action=\"$sum_up_script\" method=\"$method\">
<input type=hidden name=sumu_up value=\"$date\">
<input type=submit value=\"いただく♪\"></td><td>&nbsp;&nbsp;&nbsp;</td></form>
EOM
		}
        else{$up_html="";}

		if ($icon ne "") {$icon_html="<td><img src=\"$icon_dir$icon\"></td>\n"; }
		else{$icon_html="<td width=37>　</td>\n"; }
        
		if($ImgFile =~ /bgm$/){
		    $ImgFile =~ s/bgm$//;if($ImgFile =~ /\.$/){$ImgFile="$ImgFile"."bgm";}	
		    $bgm="<b>BGM</b> <a style=text-decoration:none href=$ImgFile target=_blank>DL
            </a>/<a style=text-decoration:none href=./bgsound.cgi?bgm=$ImgFile target=bgm>演奏
		    </a>/<a style=text-decoration:none href=./bgsound.cgi?mode=no_bgm target=bgm>停止</a>";
		}

		elsif($ImgFile =~ /cgm$/){
		    $ImgFile =~ s/\.([^.]+)\.([^.]*)cgm$//;
		    $pic = "$ImgFile.$1";$bgm = "$ImgFile.$2";if($bgm =~ /\.$/){$bgm="$bgm"."bgm";}
		    $bgm="<b>BGM</b> <a style=text-decoration:none href=$bgm target=_blank>DL
            </a>/<a style=text-decoration:none href=./bgsound.cgi?bgm=$bgm target=bgm>演奏
		    </a>/<a style=text-decoration:none href=./bgsound.cgi?mode=no_bgm target=bgm>停止</a>";

		    $icon_html="<td>　</td>\n";
            
            if ($pixel && $samnail) {
            
                ($yoko,$tate) = split(/×/,$pixel);
                
                if ($yoko > $sam_wid) {
                
                    $yoko_hiritu = $sam_wid / $yoko;
                    $yoko = $sam_wid;
                    $tate = $tate * $yoko_hiritu;
                }
                
                if ($tate > $sam_hei) {
                
                    $tate_hiritu = $sam_hei / $tate;
                    $tate = $sam_hei;
                    $yoko = $yoko * $tate_hiritu;
                }
                if ($pixel ne "$yoko×$tate") { $pic_ex = "<a href=$pic target=_blank><img src=\"$pic\" width=$yoko height=$tate border=0></a><br><br>\n"; }
                else { $pic_ex = "<img src=\"$pic\"><br><br>\n"; }
            }
            else { $pic_ex = "<img src=\"$pic\"><br><br>\n"; }
		}
        
        elsif($ImgFile =~ /swf$/){
		    $bgm="<b>Flash</b> <a style=text-decoration:none href=$ImgFile target=$number>開始
            </a>/<a style=text-decoration:none href=$script?mode=swf target=$number>停止
            </a>/<a style=text-decoration:none href=$ImgFile target=_blank>DL
		    </a>/<a style=text-decoration:none href=./bgsound.cgi?mode=no_bgm target=bgm>音楽停止</a>";

		    $icon_html="<td>　</td>\n";
		    $pic_ex = "<IFRAME src=$script?mode=swf scrolling=no width=600 height=480 marginwidth=0 marginheight=0 name=$number></IFRAME><br><br>\n";
		}
        
		elsif(defined($ImgFile) && ($ImgFile ne "")){
		    $icon_html="<td>　</td>\n";
            
            if ($pixel && $samnail) {
            
                ($yoko,$tate) = split(/×/,$pixel);
                
                if ($yoko > $sam_wid) {
                
                    $yoko_hiritu = $sam_wid / $yoko;
                    $yoko = $sam_wid;
                    $tate = $tate * $yoko_hiritu;
                }
                
                if ($tate > $sam_hei) {
                
                    $tate_hiritu = $sam_hei / $tate;
                    $tate = $sam_hei;
                    $yoko = $yoko * $tate_hiritu;
                }
                if ($pixel ne "$yoko×$tate") { $pic_ex = "<a href=$ImgFile target=_blank><img src=\"$ImgFile\" width=$yoko height=$tate border=0></a><br><br>\n"; }
                else { $pic_ex = "<img src=\"$ImgFile\"><br><br>\n"; }
            }
            else { $pic_ex = "<img src=\"$ImgFile\"><br><br>\n"; }
		}
        
        $inf = "";
        if ($pixel =~ /×/) {
            $inf = "<b>IMG</b> ($pixel)";
        }
        
		# 自動リンク
		if ($auto_link) { 
            $comment =~ s/<br>/\r/g;
            &auto_link($comment);
            $comment =~ s/\r/<br>/g;
		}
        
        if ($inyou) {
            if ($tagkey == 0) {
                $comment =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$inyou\">$2<\/font>/g;
            }
            else {
                $comment =~ s/([>]|^)(>[^<]*)/$1<font color=\"$inyou\">$2<\/font>/g;
            }
        }

$page_html= <<EOM;
<center><TABLE border=1 width='95%' cellpadding=5 cellspacing=2 bordercolor="#000000" bgcolor=\"$tbl_color1\">
<TR><TD>
<table border=0 cellspacing=0 cellpadding=0><tr>
<td valign=top><font color=$text1>[<b>$number</b>] <font color=$sub_color1><b>$sub</b></font>
投稿者：<font color=\"$link\"><b>$name</b></font>
<small>投稿日：$date</small> <small>$inf $bgm</small> <font face=\"Arial,verdana\">&nbsp; $url</font></td>
$up_html
<td><form action=\"$script\" method=\"$method\">
<input type=hidden name=bg_img value=$bg_img>
<input type=hidden name=mode value=\"res_msg\">
<input type=hidden name=resno value=\"$number\">
<input type=submit value=\"返信\"></td></form>
</tr></table>
<table border=0 cellspacing=7><tr>
$icon_html
<td>$pic_ex<font color=\"$color\">$comment</font></td></tr></table>
EOM
        $bgm="";
        print "$page_html\n";

## レスメッセージを表示
		foreach $line (@lines) {
		    ($rnum,$rk,$rd,$rname,$rem,$rsub,
			    $rcom,$rurl,$rho,$rp,$rc,$ri,$rb,$rup,$rimg,$rpixel) = split(/<>/,$line);

			($rem,$mail_ex) = split(/>/,$rem);
            
            $yoko_hiritu="";
            $tate_hiritu="";
        
            chomp $rpixel;
            
			$sname = $rname;
            $sname =~ s/＠.*//;
            $sname =~ s/☆.*//;
	        $sname =~ s/@.*//;
	        $sname =~ s/★.*//;
    
			if(!$mlfm){
				if($rem){$rname="<a href=\"mailto:$rem\">$rname</a>"}
			}
            else{
				if ($rem && $mail_ex) { $rname = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$rd\">$rname</a>"; }

				elsif ($rem) { $rname = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$rd\">$rname</a>"; }
			}
            
		    if ($number eq "$rk") {

			    print "<hr width='85%' size=1 noshade>\n";
			    print "<table cellspacing=0 cellpadding=0 border=0><tr><td width=37>　</td>\n";
            
                if ($rimg) {
                    print "<td colspan=2><font face=\"Arial,verdana\">&nbsp;&nbsp;</font></td>\n";
                }
			    elsif ($ri ne "") {
				    print "<td><img src=\"$icon_dir$ri\"></td><td><font face=\"Arial,verdana\">&nbsp;&nbsp;</font></td>\n";
			    }
                else {
				    print "<td width=35>　</td><td><font face=\"Arial,verdana\">&nbsp;&nbsp;</font></td>\n";
			    }
            
                $inf = "";
                if ($rpixel =~ /×/) {
                    chomp $rpixel;
                    $inf = "<b>IMG</b> ($rpixel)";
                }
            
			    print "<td><font color=$text1><font color=\"$sub_color1\"><b>$rsub</b></font> ";
			    print "投稿者：<font color=\"$link\"><b>$rname</b></font> - ";
			    print "<small>$rd $inf</small> ";

			    # URL表示
			    if ($rurl && !$home_icon) {
				    print "&lt;<a href=\"http://$rurl\" target='_top'>HOME</a>&gt;";
			    }
                elsif ($rurl && $home_icon) {
				    print "<a href=\"http://$rurl\" target='_top'><img src=\"$icon_dir$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\" alt=\"HomePage\"></a>";
			    }
                if ($rimg) {
                
                    if ($rpixel && $samnail) {
            
                        ($yoko,$tate) = split(/×/,$rpixel);
                
                        if ($yoko > $sam_wid) {
                
                            $yoko_hiritu = $sam_wid / $yoko;
                            $yoko = $sam_wid;
                            $tate = $tate * $yoko_hiritu;
                        }
                
                        if ($tate > $sam_hei) {
                
                            $tate_hiritu = $sam_hei / $tate;
                            $tate = $sam_hei;
                            $yoko = $yoko * $tate_hiritu;
                        }
                        if ($rpixel ne "$yoko×$tate") { print "<br><br><a href=$rimg target=_blank><img src=\"$rimg\" width=$yoko height=$tate border=0></a><br><br>\n"; }
                        else { print "<br><br><img src=\"$rimg\"><br><br>\n"; }
                    }
                    else { print "<br><br><img src=\"$rimg\"><br><br>\n"; }
                }

			    # 自動リンク
			    if ($auto_link) { 
                    $rcom =~ s/<br>/\r/g;
                    &auto_link($rcom);
                    $rcom =~ s/\r/<br>/g;
			    }
            
                if ($inyou) {
                    if ($tagkey == 0) {
                        $rcom =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$inyou\">$2<\/font>/g;
                    }
                    else {
                        $rcom =~ s/([>]|^)(>[^<]*)/$1<font color=\"$inyou\">$2<\/font>/g;
                    }
                }
			    print "<br><font color=\"$rc\">$rcom</font></font></td>\n";

		        print"</tr></table>\n";
		    }
	    }
	    print "</TD></TR></TABLE><P>\n";
	}
	print "<table border=0><tr>\n";

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=cnt value=no>\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=submit value=\"前の$pagelog件\">\n";
		print "$hid_dt";
		print "</form></td>\n";	
	}

	# 次頁処理
	if ($page_end ne "$end_data") {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=cnt value=no>\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=submit value=\"次の$pagelog件\">\n";
		print "$hid_dt";
		print "</form></td>\n";
	}

	print "</tr></table><P>\n";
	&footer;
	exit;
}

## --- ログ書き込み処理
sub regist {
	# 他サイトからのアクセスを排除
	if ($base_url) {
		$ref_url = $ENV{'HTTP_REFERER'};
		$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		if ($ref_url !~ /$base_url/) {
			&error("不正なアクセスです",'NOLOCK');
		}
	}

	# 名前とコメントは必須
	if ($name eq "") { &error("名前が入力されていません",'NOLOCK'); }
	if ($comment eq "") { &error("コメントが入力されていません",'NOLOCK'); }
	if(!$mlfm && !$email){$in{mail_ex} = 0;}
	if (($email || $in{mail_ex}) && $email !~ /(.*)\@(.*)\.(.*)/) {
		&error("Ｅメールの入力内容が正しくありません",'NOLOCK');
	}

	# 管理アイコンのチェック
	if ($my_icon && $icon eq "$my_gif") {
		if (crypt($pwd, substr($password, $salt, 2) ) ne $password) { 
		    &error("管理用アイコンは管理者専用です",'NOLOCK');
		}
	}

	# 提供品チェックにチェックが入っているとき
	if ($up_check eq 'on' && $up_comment eq ""){
	    &error("提供品コメントを入力してください",'NOLOCK');
    }
	elsif($up_check eq 'on'){$up_on="up_exist";}
	if($up_title eq ""){$up_title=$sub;}

	# ホスト名を取得
	&get_host;

	# 時間を取得
	&get_time;

	# ログを開く
	if($fll){
		foreach (1 .. 10) {
			unless (-e $lockfile) {last;}
			sleep(1);
		}
	}
	#open(LOG,"$logfile") || &error("Can't open $logfile");
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile");
	if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@lines = <LOG>;
	close(LOG);

	# 記事NO処理
	$oya = $lines[0];
	$oya =~ s/\n//;
	shift(@lines);

	if($tg_mc){$comment = &tg_en("$comment");}

	# 二重投稿の禁止
	srand;
	local($flag) = 0;
	foreach $line (@lines) {
		($knum,$kk,$kd,$kname,$kem,$ksub,$kcom) = split(/<>/,$line);
		if ($name eq "$kname" && $comment eq "$kcom") {
			$flag=1; last;
		}
		if($date eq "$kd"){$und = int(rand(1000));$date = "$date\:$und";}
	}
	if ($flag) { &error("二重投稿は禁止です"); }

	# 親記事の場合、記事Noをカウントアップ
	if ($in{'resno'} eq "") { $oya++; $number=$oya; }
	else { $number = $oya; }

	# 削除キーを暗号化
	if ($in{'pwd'} ne "") { &passwd_encode($in{'pwd'}); }

	if ($up_on eq "up_exist") { 
	    &Teikyo'regist($sum_up_log,$date,$up_title,$up_comment,0,$name,$up_limit,$ango);
	}
    if ($in{'resno'} && $in{'upfile'}) { $in{'hari'} = "on"; }

	## ランキング+認証

	$cut_name = $name;
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;

	if($fll){
		foreach (1 .. 10) {
			unless (-e $rklock) {last;}
			sleep(1);
		}
	}
	#open(RL,"$rank_log") || &error("Can't open $rank_log");
	sysopen(RL,"$rank_log",O_RDONLY | O_CREAT ) || &error("Can't open $rank_log");
	if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@rank = <RL>;
	close(RL);

	foreach(@rank){
	    $_ =~ s/\n//;
	    ($r_name,$r_cnt,$cg_cnt,$bgm_cnt,$flash_cnt,$res_cnt,$r_pass,$last_ac,$rest_cnt,$mcr_cnt) = split(/<>/,$_);

	    if($r_name eq $cut_name){

	        $last_ac = $mon ;
	        if($r_pass && $pass_mode){		
	            $plain_text = $in{'pwd'};
	            $check = &passwd_decode($r_pass);
	            if ($check ne 'yes') { &error("$cut_nameさんのパスワードと一致しません"); }
	            $ps_tr = 1;
	        }
            else{$r_pass=$ango;}

		    if($in{'hari'}){++$cg_cnt;++$r_cnt;$ck_cnt =1;}

            if($in{'upflash'}){++$flash_cnt;++$r_cnt;$ck_cnt =1;}

		    if($in{'upbgm'}){++$bgm_cnt;++$r_cnt;$ck_cnt =1;}
		    if($in{'resno'}){++$res_cnt;}
		    if($mcr_use){++$mcr_cnt;}
	        $r_ck=1;
	    }
	    push(@new_rank,"$r_name<>$r_cnt<>$cg_cnt<>$bgm_cnt<>$flash_cnt<>$res_cnt<>$r_pass<>$last_ac<>$rest_cnt<>$mcr_cnt<>\n");
	}

	if(!$r_ck){
	$cg_cnt = $bgm_cnt = $flash_cnt = 0;
		if($in{'hari'}){$cg_cnt=1;$ck_cnt =1;}
		if($in{'upbgm'}){$bgm_cnt=1;$ck_cnt =1;}
        if($in{'upflash'}){$flash_cnt=1;$ck_cnt =1;}
		if($in{'resno'}){$res_ct = 1;}
        
	    $r_cnt = $cg_cnt + $bgm_cnt + $flash_cnt ;
	    push(@new_rank,"$cut_name<>$r_cnt<>$cg_cnt<>$bgm_cnt<>$flash_cnt<>$res_ct<>$ango<>$last_ac<>$rest_cnt<>$mcr_cnt<>\n");
	}

	# アイコン

	&icon_exe;

	if($in{'icon'} eq "none.gif"){$ico_reg = $in{'icon'};}
	elsif($in{'icon'} eq "rand.gif"){

	    if($rd_pri){$ico_rd = int(rand($Icon_num));}
	    else{$ico_rd = int(rand($nm_ico_nm));}

	    splice(@icon1,0,2);
	    splice(@icon2,0,2);

	    if($icon1[$ico_rd]){$ico_reg = "$icon1[$ico_rd]\" alt=\"$icon2[$ico_rd]";$ic_nm = $ico_rd;}
	    else{$ico_reg = "none.gif";}
	}
	else{

	    foreach(0 .. $#icon1) {
	        if($in{'icon'} eq $icon1[$_]){
	            $ic_nm = $_;
	            if($Inum[$_] =~/pri_ico/){
		            #if($cut_name ne $usr_n[$_]){$ico_err = 1;}
		            $plain_text = $in{'pwd'};
		            $encode_pwd = $usr_p[$_];
		            $check = &passwd_decode($encode_pwd);
		            if ($check ne 'yes') {$ico_err = 1;}
		            if($ps_tr && ($cut_name eq "$usr_n[$_]")) {$ico_err = 0;}
		            if($ico_err){
		                &error("このアイコンは$usr_n[$_]専用です");
		            }
	            }
	            $ico_reg = "$icon1[$_]\" alt=\"$icon2[$_]";last;
	        }
	    }
	}

	if($in{'hari'}){
	    if ($in{'upfile'}) {
            $upf_f=1; &UpFile;$up_cg=1;
	        if($ImgDir2){$ImgFile = "$ImgDir2$imgdata$tail";}
            
            if ($tail eq ".jpg") { ($width,$height) = &GetJpegSize($in{'upfile'}); }
            elsif ($tail eq ".gif") { ($width,$height) = &GetGifSize($in{'upfile'}); }
            elsif ($tail eq ".png") { ($width,$height) = &get_png_size($in{'upfile'}); }
            $pixel = "$width×$height";
	    }
	}

	if ($in{'upflash'}) {
        $upz_f=1; &UpFile;
	    if($ImgDir2){$ImgFile = "$ImgDir2$imgdata$tail";}
	}
    
	if($in{'upbgm'}){
        $upb_f=1;
	    &UpFile;
	    $up_bgm=1;
	    if($up_cg){$b_tail="$b_tail"."cgm";}
        else{$b_tail="$b_tail"."bgm";}

	    if($ImgDir2){$ImgDir = $ImgDir2;}
	    $ImgFile="$ImgDir$imgdata$w_tail.$b_tail";
	}

	# クッキーを定義
	$cook = "name\:$name\,email\:$email\,url\:$url\,pwd\:$pwd\,icon\:$icon\,color\:$color\,mail_ex\:$in{mail_ex}";

	if($in{mail_ex}){$email = "$email\>1";}

	# ログをフォーマット
	$new_msg = "$number<>$in{'resno'}<>$date<>$name<>$email<>$sub<>$comment<>$url<>$host<>$ango<>$color<>$ico_reg<>$in{'Tbl_B'}<>$up_on<>$ImgFile<>$pixel\n";

	## 自動ソート時は、レス記事投稿時は親記事はトップへ移動
	if ($res_sort && $in{'resno'} ne "") {
		@res_data = ();
		@new = ();
		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sb,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # 親記事を抜き出す
		  if ($k eq "" && $in{'resno'} eq "$num") {
			$new_line = "$line";
			$flag = 1;
		  }
		  # 関連のレス記事を抜き出す
		  elsif ($k eq "$in{'resno'}") {
			push(@res_data,$line);
			$flag = 1;
		  }
		  if ($flag == 0) { push(@new,$line); }
		}

		# 関連レス記事をトップへ
		unshift(@new,@res_data);

		# 新規メッセージをトップへ
		unshift(@new,$new_msg);

		# 親記事をトップへ
		unshift(@new,$new_line);


	## 親記事の場合、最大記事数を超える記事をカット
	} elsif ($in{'resno'} eq "") {

		$i = 0;
		$stop = 0;
		foreach $line (@lines) {
		    ($num,$k,$d,$na,$em,$sb,$com,$u,$ho,$p,$c,$ico,$d,$dup,$img,$si)=split(/<>/,$line);

		    if ($k eq "") { 	$i++; }
		    if ($i > $max-1) {
			$stop = 1;

			if(!$k){
				if(-e "$vt_dir$num\.vt"){
					#open(VT,"$vt_dir$num\.vt");
					sysopen(VT,"$vt_dir$num\.vt",O_RDONLY);
					@past_vt = <VT>;
					close(VT);
					unshift(@past_vt,$num);
					push(@past_vt_reg,@past_vt);
					unlink("$vt_dir$num\.vt"); 
				}
			}

			if($ImgDir2){$img =~ s/^$ImgDir2//;$img = "$ImgDir$img";}

			if($img =~ /bgm$/){
			$img =~ s/bgm$//;
			
			#ログ互換
			if($img =~ /\.$/){$img="$img"."bgm";}		
			
#			if(-e "$img"){ unlink("$img"); }
			}

			if($img =~ /cgm$/){
			$img =~ s/\.([^.]+)\.([^.]*)cgm$//;
			$pic = "$img.$1";$bgm = "$img.$2";

			#ログ互換
			if($bgm =~ /\.$/){$bgm="$img.bgm";}

#			if(-e "$pic"){ unlink("$pic"); }
#			if(-e "$bgm"){ unlink("$bgm"); }
			}

#			elsif(($img) && (-e "$img")){ unlink("$img"); }
			if ($pastkey == 0) { last; }
			else {
				if ($k eq "") { $kflag=1; push(@past_data,$line); }
				else { push(@past_res,$line); }
			}
		    }
		    if ($stop == 0) { push(@new,$line); }
		}

		## 過去記事生成
		if ($kflag) {
			@past_res = reverse(@past_res);
			push(@past_data,@past_res);
			&pastlog;
		}

		unshift(@new,$new_msg);

	## レス記事は記事数の調整はしない
	} else {
		@res_data = ();
		@new = ();

		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sb,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # 親記事を抜き出す
		  if ($k eq "" && $in{'resno'} eq "$num") {
			$new_line = "$line";
			$flag = 2;
		  }

		  if ($flag == 0) { push(@new,$line); }
		  elsif ($flag == 2) {
			push(@new,$new_line);
			push(@new,$new_msg);
		  }
		}
	}

	## だ〜び〜書きこみ
	if($fll){
		&fll("$rklock","$rank_log",@new_rank);
	}else{

#open(RL, "+< $rank_log") || &error("Can't open $rank_log");
sysopen(RL, "$rank_log" ,O_RDWR ) || &error("Can't open $rank_log");
if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
truncate(RL, 0);
seek(RL, 0, 0);
print RL @new_rank;
close(RL);

	}


	## アイコンランキング

	$ex_in_nm = defined $ic_nm;

	if(!$ck_cnt && $ex_in_nm){

	if($fll){
		foreach (1 .. 10) {
			unless (-e $irklock) {last;}
			sleep(1);
		}
	}
	#open(IN,"$i_rank_log") || &error("Can't open $i_rank_log");
	sysopen(IN,"$i_rank_log",O_RDONLY) || &error("Can't open $i_rank_log");
	@i_rank = <IN>;
	close(IN);

	foreach(@i_rank){
	($ico,$ic_num) = split(/<>/,$_);
	if($ico eq $icon1[$ic_nm]){++$ic_num;$_ = "$ico<>$ic_num<>\n";$ck_ico = 1;last;}
	}

	if(!$ck_ico){$new_ic = "$icon1[$ic_nm]<>1<>\n";push(@i_rank,$new_ic);}

	if($fll){
		&fll("$irklock","$i_rank_log",@i_rank);
	}else{
		#open(IN,">$i_rank_log") || &error("Can't open $i_rank_log");
		sysopen(IN,"$i_rank_log" , O_WRONLY | O_TRUNC | O_CREAT ) || &error("Can't open $i_rank_log");
		print IN @i_rank;
		close(IN);
	}

	}

	if($vote){
		#open(VT,">$vt_dir$oya\.vt") || &error("Can't open $vt_dir$oya\.vt");
		sysopen(VT,"$vt_dir$oya\.vt" , O_WRONLY | O_TRUNC | O_CREAT ) || &error("Can't open $vt_dir$oya\.vt");
		close(VT);
		chmod(oct($vt_pm),"$vt_dir$oya\.vt");
	}

	# 親記事NOを付加
	unshift (@new,"$oya\n");

	if($fll){
		&fll("$lockfile","$logfile",@new);
	}else{
		#open(LOG, "+< $logfile") || &error("Can't open $logfile");
		sysopen(LOG, "$logfile" , O_RDWR ) || &error("Can't open $logfile");
		if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG @new;
		close(LOG);

	}

	# メール処理
	if ($mailing && $mail_me) { &mail_to; }
	elsif ($mailing && $email ne "$mailto") { &mail_to; }

## HTML作成
if($html_on){
	require './html.pl';
	&html_ex;
	$html_write = 0;
	if($in{'resno'}){
		$top_page = "./page1.html";
	}
}

if($in{'resno'}){
	$top_page = "$script";
}

#if ($ENV{PERLXS} eq "PerlIS") {
#print "HTTP/1.0 302 Temporary Redirection\r\n";
#print "Content-type: text/html\n\n";
#}

if(!$redi){
	&set_cookie;
	print "Location: $top_page\n";
	print "\n";
}else{
	&set_cookie;
	&header;
	print "<META HTTP-EQUIV=\"Refresh\" Content=0\;url=$top_page>";
	&footer;
}
exit;

}

## --- 返信フォーム
sub res_msg {
	# ログを読み込み
	#open(LOG,"$logfile") || &error("Can't open $logfile",'NOLOCK');
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile",'NOLOCK');
	@lines = <LOG>;
	close(LOG);

	# 親記事NOをカット
	@lines = splice(@lines,1);

	# フォーム長を定義
	&get_agent;

	# クッキーを取得
	&get_cookie;

	if($c_m_ex){$c_m_ex = " checked";}

	&header;
	print "以下は、記事NO <B>$in{'resno'}</B> に関する返信フォームです<hr>\n";
	print "<center><table border=0 width=\"97%\" cellpadding=10 bgcolor=\"$tbl_color\">\n";
	print "<tr><td>\n";

	$flag=0;
	foreach $line (@lines) {
		local($num,$k,$date,$name,$email,$sub,$com) = split(/<>/, $line);

		# 親記事を出力
		if ($k eq "" && $in{'resno'} eq "$num") {
			$resub = $sub;
			$flag=1;
			print "<B>【親記事】</B><P>\n";
			print "<font color=\"$sub_color\"><B>$sub</B></font>\n";
			print "投稿者：<font color=\"$link\"><B>$name</B></font>\n";
			print "<small>投稿日：$date</small><br>\n";
			print "<blockquote>$com</blockquote><P>\n";

		# レス記事を @res に格納
		} elsif ($k ne "" && $in{'resno'} eq "$k") {

			push(@res,$line);
		}
	}

	# レス記事を表示
	if (@res) {
		# 記事を逆順に
		@res = reverse(@res);

		$flag = 0;
		foreach $line (@res) {
			local($num,$k,$date,$name,$email,$sub,$com) = split(/<>/,$line);

			if ($flag == 0) {
				$flag=1;
				print "<hr size=2><B>【レス記事】</B><br>\n";
			}

			print "<blockquote><font color=\"$sub_color\"><B>$sub</B></font>\n";
			print "投稿者：<font color=\"$link\"><B>$name</B></font> - \n";
			print "<small>$date</small><br>\n";
			print "<blockquote>$com</blockquote></blockquote><br>\n";
		}
	}

	# タイトル名
	if ($resub !=~ /^Re\:/) { $resub = "Re\: $resub"; }

	if($mlfm){
		$mlad_e = "<input type=checkbox name=mail_ex value=on$c_m_ex> <b>メールアドレスを公開する</b>";
	}else{
		$mlad_e = "<input type=hidden name=mail_ex value=1>";
	}
    $max_dat=int($cgi_lib'maxdata/1024);
    $mx_ex="<span>　</span>jpg,gif,png $max_dat KBまで";
	print <<"EOM";
</td></tr></table></center><hr>
<form method="POST" action="$script" enctype=multipart/form-data>
<input type=hidden name=mode value="msg">
<input type=hidden name=resno value="$in{'resno'}">
<blockquote>
<table>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td><input type=text name=name value="$c_name" size=$nam_wid><small>　<b>「＠、@、☆、★」をつけても同一人物として認識されます。</b></small></td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td><input type=text name=email value="$c_email" size=$nam_wid>
<span>　</span>$mlad_e</td>
</tr>
<tr>
  <td nowrap><b>タイトル</b></td>
  <td><input type=text name=sub value="$resub" size=$subj_wid>
  <input type=submit value="返信する"><input type=reset value="リセット"></td>
</tr>

EOM
if ($res_up) {
    print "<tr><td nowrap><b>貼\り画像</b></td>\n";
    print "  <td nowrap>\n";
    print "  <input type=file name=upfile size=\"$nam_wid\">$mx_ex\n";
    print "</td>\n";
    print "</tr>\n";
}
print <<"EOM";

<tr>
  <td colspan=2><b>メッセージ</b><br>
  <textarea cols=$com_wid rows=5 name=comment wrap="$wrap"></textarea></td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td><input type=text name=url value="http://$c_url" size=$url_wid></td>
</tr>
EOM

	if ($icon_mode) {
		&icon_exe;

	# 管理者アイコンを配列に付加
	if ($my_icon) {
		push(@icon1,"$my_gif");
		push(@icon2,"管理者用");
	}

		print "<tr><td nowrap><b>イメージ</b></td><td><select name=icon>\n";
		$inum = 0;
		foreach(0 .. $#icon1) {
			if($_ > 1){++$inum;}
			if ($c_icon eq "$icon1[$_]") {
				print "<option value=\"$icon1[$_]\" selected>$inum:$icon2[$_]\n";
			} else {
				print "<option value=\"$icon1[$_]\">$inum:$icon2[$_]\n";
			}
		}
		print "</select> <small>(あなたの萌えレスイメージ ←謎)</small><INPUT TYPE='button' VALUE='この画像を見る' onClick='upWindow(icon.options[icon.selectedIndex].value); return true'><br>\n";
	print "[<a href=\"$script?mode=image&bg_img=$in{'bg_img'}\" target='_blank'>画像イメージ参照−開けるな！キケン！（ｗ−[現在のアイコン数$Icon_num]</a>]</td></tr>\n";
	}

	print "<tr><td nowrap><b>削除キー</b>";
	print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$c_pwd\">\n";
	print "<small>(自分の記事を削除時に使用。英数字で8文字以内)</small></td></tr>\n";
	print "<tr><td colspan=2><b>※ 最初に投稿をしたときの削除キーと違うと投稿ができません</b></td></tr>";
	print "<tr><td nowrap><b>文字色</b></td><td>\n";

	# クッキーの色情報がない場合
	if ($c_color eq "") { $c_color = $COLORS[0]; }

	foreach (0 .. $#COLORS) {
		if ($c_color eq "$COLORS[$_]") {
			print "<input type=radio name=color value=\"$COLORS[$_]\" checked>";
			print "<font color=\"$COLORS[$_]\">■</font>\n";

		} else {
			print "<input type=radio name=color value=\"$COLORS[$_]\">";
			print "<font color=$COLORS[$_]>■</font>\n";
		}
	}
	print "</td></tr>";
	if($tg_mc){print "<tr><td colspan=2><a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank><b>マクロ説明</b></a></td></tr>";}

	print "</td></tr></table></form>\n";
	print "</blockquote><P><hr><P>\n";
	&footer;
	exit;
}

## --- フォームからのデータ処理
sub form_decode {
	&ReadParse;
	while (($name,$value) = each %in) {

		if (($name ne "upfile") && ($name ne "upbgm") && ($name ne "upflash") && ($name ne "mail_file")) {

		# 文字コードをEUC変換
		#&jcode'convert(*value,'euc');
		#Jcode::convert(*value,'euc');

		# 一括削除用
		if($name eq 'del'){@delete=split(/\0/,$value);}

		# 投票用
		if($name eq 'moe_vt'){@moe_vt=split(/\0/,$value);}

		# メールフォーム用
		if($name eq 'nums'){@nums =split(/\0/,$value);}

		# タグ処理
		if ($tagkey == 0) {
			#$value =~ s/&/&amp;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ s/\"/&quot;/g;
		} else {
			$value =~ s/<!--(.|\n)*-->//g;
			$value =~ s/<>/&lt;&gt;/g;
		}

		# 改行等処理
		if($name eq "com"){
		$s_in{com} = $value;
		$s_in{com} =~ s/\n/<br>/g;
		#&jcode'convert(*value,'sjis');
		#Jcode::convert(*value,'sjis');
		#&jcode'convert(*value,'jis');
		#Jcode::convert(*value,'jis');

		} elsif ($name eq "comment") {
			$value =~ s/\r\n/<br>/g;
			$value =~ s/\r/<br>/g;
			$value =~ s/\n/<br>/g;
		} elsif ($name eq "up_comment") {
			$value =~ s/\r\n/\r/g;
			$value =~ s/[\r\n]/\r/g;
		} else {
			$value =~ s/\r//g;
			$value =~ s/\n//g;
		}

	}
		$in{$name} = $value;
	}

	$name    = $in{'name'};
	$comment = $in{'comment'};
	$email   = $in{'email'};
	$url     = $in{'url'};
	$url     =~ s/^http\:\/\///;
	$mode    = $in{'mode'};
	$sub     = $in{'sub'};
	$len_ck="$name$comment$email$url$sub";
	if(length($len_ck) > 2048){&error("投稿量が大きすぎます",'NOLOCK');}
	if ($sub eq "") { $sub = "無題"; }
	$pwd     = $in{'pwd'};
	$pwd     =~ s/\r//g;
	$pwd     =~ s/\n//g;
	$icon    = $in{'icon'};
	$color   = $in{'color'};
	$up_check = $in{'up_check'};
	$up_title = $in{'up_title'};
    $up_limit = $in{'up_limit'};
	$up_comment = $in{'up_comment'};
	$DL_num = $in{'DL_num'};
	$new_topic = $in{'new_topic'};
	$bg_img=$in{'bg_img'};

	if($mode eq "mail"){
		while (($key,$value) = each %in) {
			if(($key eq "name") || ($key eq "title")){
			#&jcode'convert(*value,'jis');
			#Jcode::convert(*value,'jis');
			$value_a = Encode::encode('iso-2022-jp-1',$value);
			$in{$key} = $value_a;
			#&jcode'convert(*value,'euc');
			#Jcode::convert(*value,'euc');
			$value = Encode::encode('euc-jp',$value);
			$s_in{$key} = $value;
			}
		}
	}

}
## --- 掲示板の使い方メッセージ
sub howto {
	if ($tagkey == 0) { $tag_msg = "投稿内容には、<b>タグは一切使用できません。</b>\n"; }
	else { $tag_msg = "コメント欄には、<b>タグ使用をすることができます。</b>\n"; }

	&header;
	print <<"HTML";
[<a href="$script\?cnt=no">掲示板にもどる</a>]
<table width="100%">
<tr>
  <th bgcolor="#0000A0">
    <font color="#FFFFFF">掲示板の利用上の注意</font>
  </th>
</tr>
</table>
<P><center>
<table width="90%" border=1 cellpadding=10>
<tr><td bgcolor="$tbl_color">
<OL>
<LI>この掲示板は<b>萌え対応</b>また<b>萌え途上な方にも対応</b>さらには<b>萌え以外にも一応対応</b>です。<P>
<LI>この掲示板は<b>クッキーにも対応</b>っぽいです。<P>
<LI>$tag_msg<P>
<LI>記事を投稿する上での必須なことは<b>萌えてること</b>です。<P>
<LI>記事には、<b>半角カナはあまり使用しないで下さい。</b>マックやUNIX互換系OSで文字化けします。でもチャレンジャーやアンチマックユーザーのために一応半角カナ対策もしています。<P>
<LI>記事の投稿時に<b>「削除キー」</b>にパスワード（英数字で8文字以内）を入れておくと、削除・編集ができます。つーか入れてくださいヽ(´ー｀)ノ<P>
<LI>記事の保持件数は<b>最大 $max件</b>です。それを超えると古い順に自動削除されます。貼\り画像も消えるので消える前に死ぬ気で集めてください。<P>
<LI>既存の記事に<b>「返信」</b>をすることができます。<P>
<LI>管理者が著しく萌えではないと判断する記事は\予\告\なく削除することがあります。<P>
<LI>著作権に抵触する恐れのある画像は貼\らないで下さい。というのが一応タテマエっぽいらしいです。<P>
</OL>
</td></tr></table>
</center>
<hr>
<P>
HTML
	&footer;
	exit;
}

## --- ワード検索サブルーチン
sub find {
	&header;
	print <<"HTML";
[<a href="$script\?cnt=no">掲示板にもどる</a>]
<table width="100%">
<tr>
  <th bgcolor="#0000A0">
    <font color="#FFFFFF">ワード検索</font>
  </th>
</tr>
</table>
<P><center>
<table cellpadding=5>
<tr><td bgcolor="$tbl_color" nowrap>
  <UL>
  <LI>検索したい<b>キーワード</b>を入力し、検索領域を選択して「検索ボタン」を押してください。
  <LI>キーワードは「半角スペース」で区切って複数指定することができます。
  </OL>
</td></tr>
</table>
<P><form action="$script" method="$method">
<input type=hidden name=mode value="find">
<input type=hidden name=bg_img value=$in{'bg_img'}>
<table border=1 cellspacing=1>
<tr>
  <th colspan=2>キーワード <input type=text name=word size=30></th>
</tr>
<tr>
  <td>検索条件</td>
  <td>
    <input type=radio name=cond value="and" checked>AND
    <input type=radio name=cond value="or">OR
  </td>
</tr>
<tr>
  <th colspan=2>
    <input type=submit value="検索する"><input type=reset value="リセット">
  </th>
</tr>
</table>
</form></center>
HTML
	# ワード検索の実行と結果表示
	if ($in{'word'} ne ""){

		# 入力内容を整理
		$cond = $in{'cond'};
		$word = $in{'word'};
		$word =~ s/　/ /g;
		$word =~ s/\t/ /g;
		@pairs = split(/ /,$word);

		# ファイルを読み込み
		#open(LOG,"$logfile") || &error("Can't open $logfile",'NOLOCK');
		sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile",'NOLOCK');
		@lines = <LOG>;
		close(LOG);

		# 検索処理
		foreach (1 .. $#lines) {
			$flag = 0;
			foreach $pair (@pairs){
				if (index($lines[$_],$pair) >= 0) {
					$flag = 1;
					if ($cond eq 'or') { last; }
				} else {
					if ($cond eq 'and') { $flag = 0; last; }
				}
			}
			if ($flag == 1) { push(@new,$lines[$_]); }
		}

		# 検索終了
		$count = @new;
		print "<hr><b><font color=\"$t_color\">検索結果：$count件</font></b><P>\n";
		print "<OL>\n";

		foreach $line (@new) {
			($num,$k,$date,$name,$email,$sub,$com,$url) = split(/<>/,$line);

			($email,$m_ex) = split(/>/,$email);

			if ($email && $m_ex) { $name = "<a href=\"mailto:$email\">$name</a>"; }	
			if ($url) { $url = "[<a href=\"http://$url\" target='_top'>HOME</a>]"; }

			if ($k) { $num = "$kへのレス"; }

			# 結果を表示
			print "<LI>[$num] <font color=\"$sub_color\"><b>$sub</b></font>\n";
			print "投稿者：<b>$name</b> <small> $url 投稿日：$date</small>\n";
			print "<P><blockquote>$com</blockquote><hr>\n";
		}

		print "</OL><P>\n";
	}

	&footer;
	exit;
}

## --- ブラウザを判断しフォーム幅を調整
sub get_agent {
	# ブラウザ名を取得
	$agent = $ENV{'HTTP_USER_AGENT'};

	if ($agent =~ /MSIE 3/i) { 
		$nam_wid  = 30;
		$subj_wid = 40;
		$com_wid  = 65;
		$url_wid  = 48;
		$nam_wid2 = 20;
	}
	elsif ($agent =~ /MSIE 4/i || $agent =~ /MSIE 5/i) { 
		$nam_wid  = 30;
		$subj_wid = 40;
		$com_wid  = 65;
		$url_wid  = 78;
		$nam_wid2 = 20;
	}
	else {
		$nam_wid  = 20;
		$subj_wid = 25;
		$com_wid  = 56;
		$url_wid  = 50;
		$nam_wid2 = 10;
	}
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
	if(!$cook){
		$cook="name\:$name\,email\:$email\,url\:$url\,pwd\:$pwd\,icon\:$icon\,color\:$color\,mail_ex\:$in{mail_ex}";
	}
		#&jcode'convert(*cook,'sjis');
	        #Jcode::convert(*cook,'sjis');
                 
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

	if(!$tr_ck){
		if ($in{'name'})  { $c_name  = $in{'name'}; }
		if ($in{'email'}) { $c_email = $in{'email'}; }
		if ($in{'url'})   { $c_url   = $url; }
		if ($in{'pwd'})   { $c_pwd   = $in{'pwd'}; }
		if ($in{'icon'})  { $c_icon  = $in{'icon'}; }
		if ($in{'color'}) { $c_color = $in{'color'}; }
	}
}

## --- エラー処理
sub error {
	if ($_[1] ne '0') { &header; }

	if (-e $lockfile && $_[1] eq "") { unlink($lockfile); }

	print "<center><hr width=\"75%\"><h3>ERROR !</h3>\n";
	print "<P><font color=red><B>$_[0] $_[1] $_[2]</B></font>\n";
	print "<P><hr width=\"75%\"></center>\n";
	&footer;
	exit;
}

## --- 削除画面
sub msg_del {
	if ($in{'action'} eq 'admin' && (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password)) {
		&error("パスワードが違います",'NOLOCK');
	}

	#open(LOG,$logfile) || &error("Can't open $logfile",'NOLOCK');
	sysopen(LOG,$logfile,O_RDONLY) || &error("Can't open $logfile",'NOLOCK');
	@lines = <LOG>;
	close(LOG);

	shift(@lines);

	# 親記事のみの配列データを作成
	@NEW = ();
	foreach (@lines) {
		($number,$k,$date,$name,$email,$subj,
			$comment,$url,$host,$pwd) = split(/<>/, $_);

		# レス記事を外す
		if ($k eq '') { push(@NEW,$_); }
	}

	@lines = reverse(@lines);

	&header;
	print "[<a href=\"$script\?cnt=no\">掲示板へ戻る</a>]\n";
	print "<table width=\"100%\"><tr><th bgcolor=\"#0000A0\">\n";
	print "<font color=\"#FFFFFF\">コメント削除画面</font></th>\n";
	print "</tr></table><P><center>\n";
	print "<table border=0 cellpadding=5><tr>\n";
	print "<td bgcolor=$tbl_color>\n";

	if ($in{'action'} eq '') {
		print "■投稿時に記入した「削除キー」により、記事を削除します。<br>\n";
	}

	print "■削除したい記事のチェックボックスにチェックを入れ、下記フォームに「削除キー」を入力してください。<br>\n";
	print "■親記事を削除する場合、そのレスメッセージも同時に消滅してしまうことになりますので、ご注意ください。<br>\n";
	print "</td></tr></table><P>\n";
	print "<form action=\"$script\" method=$method>\n";

	if ($in{'action'} eq '') {
	&get_cookie;
		print "<input type=hidden name=mode value=\"usr_del\">\n";
		print "<b>削除キー</b> <input type=password name=del_key size=10 value=$c_pwd>\n";
	} else {
		print "<input type=hidden name=mode value=\"admin_del\">\n";
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	}
	print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
	print "<input type=submit value=\"削除する\"><input type=reset value=\"リセット\">\n";
	print "<P><table border=1>\n";
	print "<tr><th>削除</th><th>記事No</th><th>題名</th><th>投稿者</th><th>投稿日</th><th>コメント</th>\n";

	if ($in{'action'} eq 'admin') { print "<th>ホスト名</th>\n"; }

	print "</tr>\n";

	if ($in{'page'} eq '') { $page = 0; }
	else { $page = $in{'page'}; }

	# 記事数を取得
	$end_data = @NEW - 1;
	$page_end = $page + ($pagelog - 1);

	if ($page_end >= $end_data) { $page_end = $end_data; }
	foreach ($page .. $page_end) {
		($num,$k,$date,$name,$email,$sub,
			$com,$url,$host,$pw,$color) = split(/<>/,$NEW[$_]);

		($email,$mail_ex) = split(/>/,$email);
		if ($email && $mail_ex) { $name="<a href=mailto:$email>$name</a>"; }
		$com =~ s/<br>/ /g;
		if ($tagkey || $tg_mc) { $com =~ s/</&lt;/g; $com =~ s/>/&gt;/g; }

		if (length($com) > 60) { $com = substr($com,0,58); $com = $com . '..'; }

		if ($in{'action'} eq 'admin') {
			print "<tr><th><input type=checkbox name=del value=\"$date\"></th>\n";

		} else {
			print "<tr><th><input type=radio name=del value=\"$date\"></th>\n";
		}

		print "<th>$num</th><td>$sub</td><td>$name</td>\n";
		print "<td><small>$date</small></td><td>$com</td>\n";

		if ($in{'action'} eq 'admin') { print "<td>$host</td>\n"; }

		print "</tr>\n";

		## レスメッセージを表示
		foreach (0 .. $#lines) {
			($rnum,$rk,$rd,$rname,$rem,$rsub,
				$rcom,$rurl,$rho,$rp,$rc) = split(/<>/, $lines[$_]);

			$rcom =~ s/<br>/ /g;
			if ($tagkey || $tg_mc) { $rcom =~ s/</\&lt\;/g; $rcom =~ s/>/\&gt\;/g; }
			if (length($rcom) > 60) { $rcom=substr($rcom,0,58); $rcom=$rcom . '..'; }
			if ($num eq "$rk") {

				if ($in{'action'} eq 'admin') {
					print "<tr><th><input type=checkbox name=del value=\"$rd\"></th>\n";
				} else {
					print "<tr><th><input type=radio name=del value=\"$rd\"></th>\n";
				}

				print "<td colspan=2 align=center><b>$num</b>へのレス</td>\n";

				($rem,$mail_ex) = split(/>/,$rem);
				if ($rem && $mail_ex) { $rname="<a href=mailto:$rem>$rname</a>"; }

				print "<td>$rname</td><td><small>$rd</small></td><td>$rcom</td>\n";

				if ($in{'action'} eq 'admin') { print "<td>$rho</td>\n"; }

				print "</tr>\n";
			}
		}
	}
	print "</table></form>\n";
	print "<table border=0 width=\"100%\"><tr>\n";

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
	  print "<td><form method=\"$method\" action=\"$script\">\n";
	  print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
	  print "<input type=hidden name=cnt value=no>\n";
	  print "<input type=hidden name=page value=\"$back_line\">\n";
	  print "<input type=hidden name=mode value=msg_del>\n";
	  print "<input type=submit value=\"前の親記事$pagelog件\">\n";

	  if ($in{'action'} eq 'admin') {
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	  }

	  print "</form></td>\n";
	}

	# 次頁処理
	if ($page_end ne "$end_data") {
	  print "<td><form method=\"$method\" action=\"$script\">\n";
	  print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
	  print "<input type=hidden name=cnt value=no>\n";
	  print "<input type=hidden name=page value=\"$next_line\">\n";
	  print "<input type=hidden name=mode value=msg_del>\n";
	  print "<input type=submit value=\"次の親記事$pagelog件\">\n";

	  if ($in{'action'} eq 'admin') {
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	  }

	  print "</form></td>\n";
	}

	print "</tr></table><P><hr><P>\n";
	&footer;
	exit;
}

## --- rank編集画面
sub rank_rest {
	if (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password) {
		&error("パスワードが違います",'NOLOCK');
	}

if($fll){
	foreach (1 .. 10) {
		unless (-e $rklock) {last;}
		sleep(1);
	}
}
#open (RL,"$rank_log") || &error("Can't open $rank_log");
sysopen(RL,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
@hd_rank = <RL>;
close(RL);

if($in{rw}){

$in{rw_name} =~ s/＠.*//;
$in{rw_name} =~ s/☆.*//;
$in{rw_name} =~ s/@.*//;
$in{rw_name} =~ s/★.*//;
$db_ck =0;

foreach(@hd_rank){
($r_nm,$d2,$d3,$d4,$d5,$d6,$r_pwd,$lt_ac) = split(/<>/,$_);

if($in{bs_name} eq $r_nm){
$_ =~ s/\n//;
	if($in{rw_rps} eq "rs"){$r_pwd = "";}
	elsif($in{rw_rps} eq "ch"){
	if(!$in{rw_ps}){&error("パスワードが設定されていません",'NOLOCK');}
	&passwd_encode($in{rw_ps});
	$r_pwd = $ango;
	}
$all_cnt = $in{rw_pic}+$in{rw_bgm};
$_ = "$in{rw_name}<>$all_cnt<>$in{rw_pic}<>$in{rw_bgm}<>$in{rw_flash}<>$in{rw_res}<>$r_pwd<>$lt_ac<>$in{rw_rest}<>$in{rw_mcr}<>\n";
}

}

foreach(@hd_rank){
($nm) = split(/<>/,$_);
if($in{rw_name} eq $nm){++$db_ck;}
}

if($db_ck > 1){&error("そのお名前は既に登録済みです",'NOLOCK');}

}

if(@delete){

$del_num = @delete;

foreach(@hd_rank){
if(!$del_num){last;}else{$del_ck = 0;}
($dnm) = split(/<>/,$_);
foreach $del_name(@delete){if($del_name eq $dnm){$del_ck =1;}}
if($del_ck){$_ = "";--$del_num;}
}

}

if($in{mon_del}){
	&get_time;
	foreach(@hd_rank){
		$_ =~ s/\n//;
		($r_nm,$d2,$d3,$d4,$d5,$d6,$r_pwd,$lt_ac) = split(/<>/,$_);
		$sub = $mon - $lt_ac;
		if($sub < 0){$sub = $mon +12 - $lt_ac;}
		if($sub > 1 || !$lt_ac){$_ = "";}else{$_ = "$_\n";}
	}

}

if(@delete || $in{rw} || $in{mon_del}){

if($fll){
	&fll("$rklock","$rank_log",@hd_rank);
}else{
	#open(RL, "+< $rank_log") || &error("Can't open $rank_log");
	sysopen(RL, "$rank_log",O_RDWR) || &error("Can't open $rank_log");
	if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	truncate(RL, 0);
	seek(RL, 0, 0);
	print RL @hd_rank;
	close(RL);
}
}

if($name){

foreach(@hd_rank){
($rw_nm,$rw_cnt,$rw_pic,$rw_bgm,$rw_flash,$rw_res,$rw_rps,$la,$rw_rest,$rw_mcr) = split(/<>/,$_);
if($name eq $rw_nm){last;}
}
if($pass_mode){
$pmex = "pass認証兼";
$pmex2 = <<"EOM";
<li>認証でリセットを選択すると認証passがリセットされて、対象者の次の書きこみ時のpassが新たな認証passになります。<br>
<li>認証で変更を選択、新パスワードを入力すると新しい認証passが設定されます。
EOM
$pmex3 = "<th>認証pass</th>";
$pmex4 = <<"EOM";
<td>
<input type=radio name=rw_rps value=\"\" checked> 変更しない
　
<input type=radio name=rw_rps value=\"rs\"> リセット
　
<input type=radio name=rw_rps value=\"ch\"> 変更：<input type=password name=rw_ps size=8 maxlength=8>
</td>
EOM

}
&header;
print <<EOM;
[<a href=$script?cnt=no>掲示板に戻る</a>]
<center>
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">$pmex\ランキングデータ編集画面</font></th>
</tr></table><br>
<table border=0 cellpadding=5><tr>
<td bgcolor="#FFFFFF">
<ul type=square>
<li>編集したい項目を編集後、変更ボタンを押すと変更されます。<br>
$pmex2
</td></tr></table></ul><br>
<form action=$script method=POST>
<input type=hidden name=mode value=rank_rest>
<input type=hidden name=rw value=on>
<input type=hidden name=pass value=$in{pass}>
<input type=hidden name=bg_img value=$bg_img>
<input type=hidden name=bs_name value=$name>
<table border=1 bgcolor=white cellspacing=0><tr><th>お名前</th><th>総合</th><th>画像</th><th>BGM</th><th>Flash</th><th>レス</th><th>編集</th><th>マクロ</th>$pmex3</tr>
<tr>
<td><input type=text name=rw_name value=\"$rw_nm\"></td>
<td><b>$rw_cnt</b></td>
<td><input type=text name=rw_pic value=\"$rw_pic\" size=4></td>
<td><input type=text name=rw_bgm value=\"$rw_bgm\" size=4></td>
<td><input type=text name=rw_flash value=\"$rw_flash\" size=4></td>
<td><input type=text name=rw_res value=\"$rw_res\" size=4></td>
<td><input type=text name=rw_rest value=\"$rw_rest\" size=4></td>
<td><input type=text name=rw_mcr value=\"$rw_mcr\" size=4></td>
$pmex4
</tr>
</table>
<input type=submit value=\"変更\">
</center></form>
EOM
&footer;
exit;

}

foreach $hd_rank(@hd_rank){
if(!$hd_rank){next;}
$hd_rank =~ s/\n//;
($rname,$cnt,$pic,$bgm,$flash,$res,$rps,$la,$rest,$mcr) = split(/<>/,$hd_rank);
$rank{$rname} = $cnt;
$rank_ex{$rname} = "$cnt<>$pic<>$bgm<>$flash<>$res<>$rps<>$la<>$rest<>$mcr<>";
}

@sort_rank = sort {$rank{$b} <=> $rank{$a}} keys(%rank);

if($pass_mode){$pmex = "pass認証兼";}
&header;
print <<EOM;
[<a href=$script?cnt=no>掲示板に戻る</a>]
<center>
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">$pmex\ランキングデータ削除画面</font></th>
</tr></table><br>
<table border=0 cellpadding=5><tr>
<td bgcolor="#FFFFFF">
<ul type=square>
<li>削除したいデータのチェックボックスにチェックを入れて削除ボタンを押すと削除されます。<br>
<li>最終アクセス日で削除のチェックボックスにチェックを入れて削除ボタンを押すと<br>
先月もしくは今月のアクセスがなかったユーザーが削除されます。<br>
<li>編集したいデータの「お名前」をクリックすると編集画面になります。
</td></tr></table></ul><br>
<form action=$script method=POST>
<input type=hidden name=mode value=rank_rest>
<input type=hidden name=pass value=$in{pass}>
<input type=hidden name=bg_img value=$bg_img>
<table border=1 bgcolor=white><tr><th>　</th><th>お名前</th><th>総合</th><th>画像</th><th>BGM</th><th>Flash</th><th>レス</th><th>編集</th><th>マクロ</th></tr>
EOM

foreach(@sort_rank){
($cnt,$pic,$bgm,$flash,$res,$rps,$la,$rest,$mcr) = split(/<>/,$rank_ex{$_});
if(!$cnt){$cnt = "0";}
if(!$pic){$pic = "0";}
if(!$bgm){$bgm = "0";}
if(!$flash){$flash = "0";}
if(!$res){$res = "0";}
if(!$rest){$rest = "0";}
if(!$mcr){$mcr = "0";}

$uenm = $_;
$uenm =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2',$1)/ge;
$uenm =~ s/\s/+/g;

print "<tr><td><input type=checkbox name=del value=\"$_\"></td><td><a href=$script\?mode=rank_rest&pass=$in{pass}&name=$uenm\&bg_img=$bg_img>$_</a></td><td>$cnt</td><td>$pic</td><td>$bgm</td><td>$flash</td><td>$res</td><td>$rest</td><td>$mcr</td></tr>";
}
print "</table>";
print "<br><input type=submit value=\"削除\"><br><br><input type=checkbox name=mon_del> <b>最終アクセス日で削除</b>";
print "</form></center>";

&footer;
exit;
}

## --- 記事削除処理
sub usr_del {
	if ($in{'del_key'} eq "") { &error("削除キーが入力モレです",'NOLOCK'); }
	if ($in{'del'} eq "") { &error("ラジオボタンの選択がありません",'NOLOCK'); }

	# ログを読み込む
	if($fll){
		foreach (1 .. 10) {
			unless (-e $lockfile) {last;}
			sleep(1);
		}
	}
	#open(LOG,"$logfile") || &error("Can't open $logfile");
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile");
	if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@lines = <LOG>;
	close(LOG);

	#open(RL,"$rank_log") || &error("Can't open $rank_log");
	sysopen(RL,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");

	@rank = <RL>;
	close(RL);

	# 親記事NO
	$oya = $lines[0];
	if ($oya =~ /<>/) { &error("ログが正しくありません");	}

	shift(@lines);

	## 削除キーによる記事削除 ##
	@new=();
	foreach $line (@lines) {
		$dflag = 0;
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$pw,$c,$i,$d,$d,$img,$si) = split(/<>/,$line);

		if ($in{'del'} eq "$dt") {
			$dflag = 1;

			$cut_name = $name;
			$cut_name =~ s/＠.*//;
            $cut_name =~ s/☆.*//;
	        $cut_name =~ s/@.*//;
	        $cut_name =~ s/★.*//;

			if($pass_mode){
			    foreach(@rank){
			        ($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
			        if($cut_name eq "$d1"){$d6 =~ s/\n//;$encode_pwd = $d6;last;}
			    }
			}

			if(!$encode_pwd){$encode_pwd = $pw;}
			$del_num = $num;
			if ($k eq '') { $oyaflag=1; }

		}
        elsif ($oyaflag && $del_num eq "$k") {
			$dflag = 1;
		}

		if ($dflag == 0) { push(@new,$line); }
		else{ push(@del,$line); }
	}

	if ($del_num eq '') { &error("$in{'del'}削除対象記事が見つかりません"); }
	else {
		if ($encode_pwd eq '') { &error("削除キーが設定されていません"); }
		$plain_text = $in{'del_key'};
		$check = &passwd_decode($encode_pwd);
		if ($check ne 'yes') { &error("パスワードが違います"); }
	}

		foreach(@del){
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$pw,$c,$i,$d,$d,$img,$si) = split(/<>/,$_);
			if($ImgDir2){$img =~ s/^$ImgDir2//;$img = "$ImgDir$img";}

			if(!$k){
				if(-e "$vt_dir$num\.vt"){ unlink("$vt_dir$num\.vt"); }
			}

			if($img =~ /bgm$/){
			    $img =~ s/bgm$//;
			
			    #ログ互換
			    if($img =~ /\.$/){$img="$img"."bgm";}		

#			    if(-e "$img"){ unlink("$img"); }
			}

			if($img =~ /cgm$/){
			    $img =~ s/\.([^.]+)\.([^.]*)cgm$//;
			    $pic = "$img.$1";$bgm = "$img.$2";

			    #ログ互換
			    if($bgm =~ /\.$/){$bgm="$img.bgm";}

#			    if(-e "$pic"){ unlink("$pic"); }
#			    if(-e "$bgm"){ unlink("$bgm"); }
			}

#			elsif(($img) && (-e "$img")){ unlink("$img"); }
		}

	# 親記事NOを付加
	unshift(@new,$oya);

	## ログを更新 ##
	if($fll){
		&fll("$lockfile","$logfile",@new);
	}else{
		#open(LOG, "+< $logfile") || &error("Can't open $logfile");
		sysopen(LOG, "$logfile", O_RDWR ) || &error("Can't open $logfile");
		if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG @new;
		close(LOG);
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	## HTML作成
	if($html_on){
		require './html.pl';
		&html_ex;
		$html_write = 0;
	}

	# 削除画面にもどる
	&msg_del;
}

## --- 管理者一括記事削除
sub admin_del {
	if  (crypt($in{'pass'}, substr($password, $salt, 2)) ne $password) {
	&error("パスワードが違います",'NOLOCK');
	}

	if ($in{'del'} eq "") { &error("チェックボックスの選択がありません",'NOLOCK'); }

	# ログを読み込む
	if($fll){
		foreach (1 .. 10) {
			unless (-e $lockfile) {last;}
			sleep(1);
		}
	}
	#open(LOG,"$logfile") || &error("Can't open $logfile");
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile");
	if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@lines = <LOG>;
	close(LOG);

	# 親記事NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("ログが正しくありません。<P>
			<small>\(v2.5以前のログの場合は変換の必要があります\)<\/small>");
	}

	shift(@lines);

	## 削除処理
	foreach $line (@lines) {
		$dflag=0;
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$pw,$d,$d,$d,$d,$img,$si) = split(/<>/,$line);

		foreach $del (@delete) {
			if ($del eq "$dt") {

			if(!$k){
				if(-e "$vt_dir$num\.vt"){ unlink("$vt_dir$num\.vt"); }
			}

			if($ImgDir2){$img =~ s/^$ImgDir2//;$img = "$ImgDir$img";}

			if($img =~ /bgm$/){
			$img =~ s/bgm$//;
			
			#ログ互換
			if($img =~ /\.$/){$img="$img"."bgm";}		

#			if(-e "$img"){ unlink("$img"); }
			}

			if($img =~ /cgm$/){
			$img =~ s/\.([^.]+)\.([^.]*)cgm$//;
			$pic = "$img.$1";$bgm = "$img.$2";

			#ログ互換
			if($bgm =~ /\.$/){$bgm="$img.bgm";}

#			if(-e "$pic"){ unlink("$pic"); }
#			if(-e "$bgm"){ unlink("$bgm"); }
			}

#F			elsif(($img) && (-e "$img")){ unlink("$img"); }

				$dflag = 1;
				$del_num = $num;
				if ($k eq '') { $oyaflag=1; }

			} elsif ($oyaflag && $del_num eq "$k") {
				$dflag = 1;
			}
		}
		if ($dflag == 0) { push(@new,$line); }
	}

	# 親記事NOを付加
	unshift(@new,$oya);

	## ログを更新 ##

	if($fll){
		&fll("$lockfile","$logfile",@new);
	}else{
		#open(LOG, "+< $logfile") || &error("Can't open $logfile");
		sysopen(LOG, "$logfile", O_RDWR ) || &error("Can't open $logfile");
		if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG @new;
		close(LOG);
	}

	## HTML作成
	if($html_on){
		require './html.pl';
		&html_ex;
		$html_write = 0;
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	# 削除画面にもどる
	&msg_del;
}

## --- 管理者入室画面
sub admin {
	&header;
	print "<center><h4>パスワードを入力してください</h4>\n";
	print "<form action=\"$script\" method=$method>\n";
	print "記事削除:<input type=radio name=mode value=\"msg_del\">\n";
	print "記事編集:<input type=radio name=mode value=\"rest\">\n";
	if($pass_mode){$pmex = "pass認証";}else{$pmex = "だ〜び〜";}
	print "$pmex:<input type=radio name=mode value=\"rank_rest\">\n";
	print "ログ:<input type=radio name=mode value=\"bkup\">\n";
    print "ランクログ変換:<input type=radio name=mode value=\"convert\"><br><br>\n";
    print "ランクログ変換は従来の萌え板からこの萌え板を初めて使うときに１回だけやってください<br>\n";
    print "それ以外の時は絶対に使用しないでください<br>\n";

	if ($in{'ds'}) {
	print "<input type=hidden name=ds value='on'>\n";
	}
	print "<input type=hidden name=action value=\"admin\">\n";
	print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
	print "<input type=password name=pass size=8><input type=submit value=\" 認証 \">\n";
	print "</form></center><P><hr><P>\n";
	print "<a href='$script?papost=pcode'>PASSの変更</a><br>\n";
	&footer;
	exit;
}

## --- 時間を取得
sub get_time {
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday,$d,$d) = localtime(time);
	$year += 1900;
	$mon++;
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($sec  < 10) { $sec  = "0$sec";  }
	$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];

	# 日時のフォーマット
	$date = "$year\/$mon\/$mday\($week\)/$hour\:$min\:$sec";
	$imgdata="$year$mon$mday$hour$min$sec";
}

## --- カウンタ処理
sub counter {
	# 閲覧時のみカウントアップ
	$match=0;
	if ($in{'mode'} eq '' && !$in{'cnt'}) {
		# カウンタロック
		if ($lockkey && !$fll) { &lock3; }

		$match=1;
	}

	# カウントファイルを読みこみ
	if($fll){
		foreach (1 .. 10) {
			unless (-e $cntlock) {last;}
			sleep(1);
		}
	}
	#open(NO,"$cntfile") || &error("Can't open $cntfile",'0');
	sysopen(NO,"$cntfile",O_RDONLY | O_CREAT ) || error("Can't open $cntfile",'0');
	if($lockkey == 3){flock(NO,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	$cnt = <NO>;
	close(NO);
	chop($cnt);

	if(!$cnt && $cnt_ml){
		#open(NO,"$cntfile2") || &error("Can't open $cntfile2",'0');
		sysopen(NO,"$cntfile2",O_RDONLY) || &error("Can't open $cntfile2",'0');
		$cnt = <NO>;
		close(NO);
		chop($cnt);
	}

	# カウントアップ
	if ($match) {

		$cnt++;
		$cont="$cnt\n";

		# 更新
		if($fll){
			&fll("$cntlock","$cntfile","$cont");
		}else{
			#open(OUT, "+< $cntfile") || &error("Can't open $cntfile");
			sysopen(OUT, "$cntfile", O_RDWR ) || &error("Can't open $cntfile");
			if($lockkey == 3){flock(OUT,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
			truncate(OUT, 0);
			seek(OUT, 0, 0);
			print OUT $cont;
			close(OUT);
		}

		if($cnt_ml){
			#open(OUT, "+< $cntfile2") || &error("Can't open $cntfile2");
			sysopen(OUT, "$cntfile2" , O_RDWR ) || &error("Can't open $cntfile2");
			if($lockkey == 3){flock(OUT,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
			truncate(OUT, 0);
			seek(OUT, 0, 0);
			print OUT $cont;
			close(OUT);
		}

	}

	# カウンタロック解除
	if ($lockkey && !$fll) {
		if (-e $cntlock) { unlink($cntlock); }
	}
	
	# 桁数調整
	while(length($cnt) < $mini_fig) { $cnt = '0' . "$cnt"; }
	@cnts = split(//,$cnt);

	print "<table><tr><td>\n";

	# GIFカウンタ表示
	if ($counter == 2) {
		foreach (0 .. $#cnts) {
			print "<img src=\"$gif_path/$cnts[$_]\.gif\" alt=\"$cnts[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}

	# テキストカウンタ表示
	} else {
		print "<font color=\"$cnt_color\" face=\"verdana,Times New Roman,Arial\">$cnt</font>";
	}

	print "</td></tr></table>\n";
}

## --- カウンタロック
sub lock3 {
	$cnt_flag = 0;
	foreach (1 .. 7) {
		if (-e $cntlock) { sleep(1); }
		else {
			#open(LOCK,">$cntlock");
			sysopen(LOCK,"$cntlock", O_WRONLY | O_TRUNC | O_CREAT );
			close(LOCK);
			$cnt_flag = 1;
			last;
		}
	}
	if (!$cnt_flag) { unlink($cntlock); }
}

## --- メール送信
sub mail_to {
	$mail_sub = "$title に投稿がありました";

    	#&jcode'convert(*mail_sub,'jis');
    	#&jcode'convert(*name,'jis');
    	#&jcode'convert(*sub,'jis');
    	#&jcode'convert(*comment,'jis');
    	#Jcode::convert(*mail_sub,'jis');
    	#Jcode::convert(*name,'jis');
    	#Jcode::convert(*sub,'jis');
    	#Jcode::convert(*comment,'jis');
	$mail_sub = Encode::encode('MIME-HEADER-ISO_2022_JP',$mail_sub);
	$ver = Encode::encode('MIME-HEADER-ISO_2022_JP',$ver);

	$comment =~ s/<br>/\n/g;
	$comment =~ s/&lt;/</g;
	$comment =~ s/&gt;/>/g;

	if (open(MAIL,"| $sendmail $mailto")) {
	print MAIL "To: $mailto\n";

	# メールアドレスがない場合はダミーメールに置き換え
	if ($email eq "") { $email = "nomail\@xxx.xxx"; }

	print MAIL "From: $email\n";
	print MAIL "Subject: $mail_sub\n";
	print MAIL "MIME-Version: 1.0\n";
	#print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	#print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "Content-type: text/plain; charset=utf-8\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "--------------------------------------------------------\n";
	print MAIL "TIME : $date\n";
	print MAIL "HOST : $host\n";
	print MAIL "NAME : $name\n";
	print MAIL "EMAIL: $email\n";

	if ($url) { print MAIL "URL  : http://$url\n"; }

	print MAIL "TITLE: $sub\n\n";
	print MAIL "$comment\n";
	print MAIL "--------------------------------------------------------\n";
	close(MAIL);
	}
}

## --- パスワード暗号処理
sub passwd_encode {
	$now = time;
	($p1, $p2) = unpack("C2", $now);
	$wk = $now / (60*60*24*7) + $p1 + $p2 - 8;
	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	$nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
	$ango = crypt($_[0], $nsalt);
}

## --- パスワード照合処理
sub passwd_decode {
	if ($_[0] =~ /^\$1\$/) { $key = 3; }
	else { $key = 0; }

	$check = "no";
	if (crypt($plain_text, substr($_[0],$key,2)) eq "$_[0]") {
		$check = "yes";
	}
}

## --- HTMLのヘッダー
sub header {
	if(!$pt_ck){
		$pt_b = $pt + 2 . 'pt';
		$pt_s = $pt - 1 . 'pt';
		$pt .= pt;
		$t_point .= pt;
		$pt_ck = 1;
	}

	if($css){
	if ($backgif) { $bgpic = $backgif; }
	elsif ($bg_img) { $bgpic = $bg_img; }
	$bdcss="body{ background:url($bgpic) $bgrep $bgatc $bg_pos}";
	if($ENV{'HTTP_USER_AGENT'} !~ /MSIE/){$css = 0;}
	}

	$header = <<"EOM";
<!doctype html>
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
<SCRIPT language="JavaScript"><!--
 function upWindow(iFILE) {
 	IMG_DATA = "$icon_dir" + iFILE;
 	Winimg=window.open(IMG_DATA, "Charaimg", "scrollbars=1,resizable=1,width=200,height=200");
 	Winimg.opener=self;
 	if(navigator.appVersion.charAt(0)>=3){Winimg.focus();}
 	}
 //--></SCRIPT>
<title>$title</title>
</head>
EOM

	# bodyタグ
	if ($backgif && !$css) { $bgkey = "background=\"$backgif\" bgcolor=$bgcolor"; }
	elsif ($bg_img && !$css) { $bgkey = "background=\"$bg_img\" bgcolor=$bgcolor"; }
	else { $bgkey = "bgcolor=$bgcolor"; }
	$header  .= "<body $bgkey text=$text link=$link vlink=$vlink alink=$alink>\n";

	if(!$html_write){

if(($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/) &&($gzip == 1)){
$|=1;
	print "Content-type: text/html\n";
	print "Content-encoding: gzip\n\n";
	open(STDOUT,"| /bin/gzip -1 -c");
}else{
	print "Content-type: text/html\n\n";
}
		print "$header";
	}elsif(!$page_cnt){
		$header .= "$count_src";
	}
}

## --- HTMLのフッター
sub footer {
	## MakiMakiさんの画像使用の有無に関わらずこの２箇所のリンク部を
	## 削除することはできません。
	$footer = <<"_HTML_";
<center>$banner2<P><small>
<!-- 削除はしてない(笑
KENT &amp; MakiMaki<br>-->

$ver <a href=$script?mode=B style=text-decoration:none;color:black;>b</a></a>y えうのす ＆ R七瀬<BR>
（正式名：被羅目板2001萌え萌えVer 〜了承♪ by 被羅目〜）<br><font size=2>Customized By 月読 Ver 6.0</font>
<br>Customized By <a href=https://github.com/sina2/moe/ target=_blank>しなしな</a>
</small></center>
_HTML_

	$id1 = "$yeart$mont$mdayt$hourt$mint$sect";
	$id2 = rand(1000000000);
	$id2 = sprintf("%.10d",$id2);
	for( $t=0; $t<32; $t++ ){ 
	$id3 .= $st_table[ int( @string_table * rand() ) ]; }
if($in{'rank'}){
$footer .= "<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>";
}

$footer .= "</body></html>";
if($nobanner){$footer .= "";}
if(!$html_write){print "$footer";}
}

## --- 自動リンク
sub auto_link {
	$_[0] =~ s#http://([\x21-\x7e]+)#<a href="http://$1" target='_top'>http://$1</a>#g;
	$_[0] =~ s#https://([\x21-\x7e]+)#<a href="https://$1" target='_top'>https://$1</a>#g;
	$_[0] =~ s#ftp://([\x21-\x7e]+)#<a href="ftp://$1" target='_top'>ftp://$1</a>#g;
	$_[0] =~ s#news://([\x21-\x7e]+)#<a href="news://$1" target='_top'>news://$1</a>#g;
}

## --- イメージ画像表示
sub image {

	$i=0; $j=0;
	splice(@icon1,0,2);
	splice(@icon2,0,2);
	splice(@usr_n,0,2);
	$stop = @icon1;

$ia_num = @icon1;
if($ia_num){

if($in{ife}){$ife_e = "&ife=on";}

if($in{i_pg} eq "self"){
	&get_cookie;

	$t = $s = 0 ;
	
	foreach(@icon1){
		if($c_name eq "$usr_n[$t]"){push(@self_ico,"$Inum[$t]\t$icon1[$t]\t$icon2[$t]\t\n");}
		++$t;
	}

	foreach(@self_ico){
		($Inum[$s],$icon1[$s],$icon2[$s]) = split(/\t/,$_);
		++$s;
	}
	$st_num = 0;$stop = @self_ico - 1;
}
elsif($in{i_pg} eq "all" || $in{i_ser}){$st_num = 0; $stop = $ia_num - 1;}
else{
if(!$in{i_pg}){$in{i_pg} = 1;}
$ict_num_ex = "page :";

$ict_num = int(($ia_num - 1)/100) + 1;

$st_num = ($in{i_pg} - 1) * 100;
$stop = $st_num + 100;
if($stop > $ia_num){$stop = $ia_num;}
--$stop;
foreach(1 .. $ict_num){
if($in{i_pg} eq "$_"){$ict_num_ex = "$ict_num_ex <b>$_</b>";}
else{$ict_num_ex = "$ict_num_ex <a href=\"$script?i_pg=$_&mode=image$ife_e&bg_img=$in{bg_img}\">$_</a>";}
}

$ict_num_ex = "<br>$ict_num_ex <a href=\"$script?i_pg=all&mode=image&bg_img=$in{bg_img}\">all</a>";
$ict_num_ex = "$ict_num_ex <a href=\"$script?i_pg=self&mode=image&bg_img=$in{bg_img}\">self</a>";
}

}

	&header;
	print "<center><hr width=\"75%\">\n";
	print "<h3>イメージ画像サンプル</h3>\n";
	print "<P>現在登録されているイメージ画像は以下のとおりです。開けるなって言ったのにぃ（ｗ\n";
	if($in{ife}){
		print "<P><a href=\"$script?mode=image&i_pg=$in{i_pg}&bg_img=$in{bg_img}\">アイコンファイル名は表示しない</a>\n";
	}else{
		print "<P><a href=\"$script?mode=image&i_pg=$in{i_pg}&ife=on&bg_img=$in{bg_img}\">アイコンファイル名も表示する</a>\n";
	}
	print "<P><hr width=\"75%\">\n";
	print "$ict_num_ex\n";
	if($in{i_ser}){
		if($in{sort}){$srt_ex = "&sort=rgd";}
		print"<br><a href=\"$script?mode=image$srt_ex&bg_img=$in{bg_img}\">通常ページ表示\</a>\n";
	}
	print "<P><form action=\"$script\">\n";
	print "<input type=hidden name=mode value=image>\n";
	print "<input type=hidden name=bg_img value=\"$in{bg_img}\">\n";
	if($in{sort}){print "<input type=hidden name=sort value=rgd>\n";}
	print "<table><tr><th>アイコン名検索：<input type=text name=i_ser value=\"$in{i_ser}\">　<input type=submit value=\"検索\"></th></tr>\n";
	print "<tr><th>検索条件：</b><input type=radio name=ser_sort value=\"0\" checked>AND　<input type=radio name=ser_sort value=\"1\">OR</th></tr>\n";
	print "<tr><th>アイコン名は「半角スペース」で区切って複数指定できます。</th></tr>\n</table></form>\n";
	print "<P><table border=1 cellpadding=5 cellspacing=0><tr>\n";

	$j = $st_num;
	if($in{i_ser}){
		@i_ser = split(/ /,$in{i_ser});
	}
	foreach ($st_num .. $stop) {
		$inum = $j + 1;
		if(@i_ser){
			foreach $is(@i_ser){
				$sc_ck = 0;
				if (index($icon2[$_],$is) >= 0) {
					$sc_ck = 1;
					if($in{ser_sort}){last;}
				}elsif(!$in{ser_sort}){
					last;
				}
			}
			if ($sc_ck) {
				$it = $i + 1;$ic=1;
				if($in{ife}){$ifee = "<br>$icon1[$_]";}
				print "<th><img src=\"$icon_dir$icon1[$_]\" ALIGN=middle><br>$inum:$icon2[$_]$ifee</th>\n";
				$i++; 
			}else{
				$ic=0;
			}
		}else{
			$it = $i + 1;
			if($in{ife}){$ifee = "<br>$icon1[$_]";}
			print "<th><img src=\"$icon_dir$icon1[$_]\" ALIGN=middle><br>$inum:$icon2[$_]$ifee</th>\n";
			$i++; 
		}
		if ($ic && $it % 5 == 0) { print '</tr><tr>';}
		if ($j eq "$stop") {
			$end_num = $i;
			if ($it % 5 == 0) { last; }
			while ($it % 5) { print "<th><br></th>"; $i++; $it = $i + 1;}
		}
		$j++; $ic=1;
	}

	print "</tr></table><br>\n";
	if($in{ser_sort}){$sst = "OR";}else{$sst = "AND";}
	if($in{i_ser}){print "<b>$sst 条件で $in{i_ser} を検索 $end_num 個該当しました。</b>";}
	print "$ict_num_ex<br><br>\n";
	print "<FORM><INPUT TYPE=\"button\" VALUE=\"  CLOSE  \" onClick=\"top.close();\"></FORM></center>\n";
	print "</body></html>\n";
	if($nobanner){print "";}
	exit;
}

## --- ホスト名取得
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($get_remotehost) {
		if ($host eq "" || $host eq "$addr") {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		}
	}
	if ($host eq "") { $host = $addr; }
}

## --- 過去ログ生成
sub pastlog {
	$new_flag = 0;

	# 過去NOを開く
	#open(NO,"$nofile") || &error("Can't open $nofile");
	sysopen(NO,"$nofile",O_RDONLY) || &error("Can't open $nofile");
	$count = <NO>;
	close(NO);

	# 過去ログのファイル名を定義
	$past_dir =~ s/\/$//;
	$pastfile  = "$past_dir\/$count\.html";

	# 過去ログがない場合、新規に自動生成する
	unless(-e $pastfile) { &new_log; }

	# 過去ログを開く
	if ($new_flag == 0) {
		#open (IN,"$pastfile") || &error("Can't open $pastfile");
		sysopen (IN,"$pastfile",O_RDONLY) || &error("Can't open $pastfile");
		@past = <IN>;
		close(IN);
	}

	# 規定の行数をオーバーすると、次ファイルを自動生成する
	if ($#past > $log_line) { &next_log; }

	foreach $pst_line (@past_data) {
		$w_vt = 0;@w_vt=();
		($pnum,$pk,$pdt,$pname,$pemail,
			$psub,$pcom,$purl,$phost,$ppw) = split(/<>/, $pst_line);

		($pemail,$p_m_ex) = split(/>/,$pemail);

		if ($pemail && $p_m_ex) { $pname = "<a href=\"mailto:$pemail\">$pname</a>"; }
		if ($purl) { $purl="<a href=\"http://$purl\" target='_top'>http://$purl</a>"; }
		if ($pk) { $pnum = "$pkへのレス"; }
		elsif(@past_vt){
			foreach(@past_vt){
				if($w_vt){
					if($_ =~ /^\d$/){last;}
					push(@w_vt,$_);
				}
				if($pnum == $_){$w_vt = 1;}
			}
			if(@w_vt){
				$vt_com = "<br><br>";
				$vt_com .= "投票結果<br><table border=1 cellspacing=0 bordercolor=black>\n";
				$vt_com .= "<tr><th>順位</th><th>項目</th><th>人数</th></tr>\n";
				foreach(@w_vt){
					($vt1,$vt2) = split(/\t/,$_);
					$sort_vt{$vt1} = $vt2;
				}
	
				@sort_vt = sort {$sort_vt{$b} <=> $sort_vt{$a}} keys(%sort_vt);

				foreach(@sort_vt){
					++$rk;
					if($nex_jg == $sort_vt{$_}){
						if($next_num){
							$ex_num = $next_num;
						}else{
							$next_num = $rk; $ex_num = --$next_num;
						}
					}else{
						$next_num=0;$ex_num = $rk;
					}

					$nex_jg = $sort_vt{$_};
					$vt_com .= "<tr><td>$ex_num</td><td>$_</td><td>$sort_vt{$_}人</td></tr>\n";
				}
				$vt_com .= "</table>";
				$pcom = "$pcom$vt_com";
			}
		}

		# 自動リンク
		if ($auto_link) {
$pcom =~ s/<br>/\r/g;
&auto_link($pcom);
$pcom =~ s/\r/<br>/g;
		}

		# 保存記事をフォーマット
		$html = <<"HTML";
[$pnum] <font color=\"$sub_color\"><b>$psub</b></font><!--T--> 投稿者：<font color=\"$link\"><b>$pname</b></font> <small>投稿日：$pdt</small><p><blockquote>$pcom<p>$purl</blockquote><hr>
HTML
		push(@htmls,"$html");
	}

	
	@news = ();
	foreach $line (@past) {
		if ($line =~ /<!--OWARI-->/i) { last; }
		push (@news,$line);
		if ($line =~ /<!--HAJIME-->/i) { push (@news,@htmls); }
	}
	if($nobanner){$kbn = "";}
	push (@news,"<!--OWARI-->\n</body></html>$kbn\n");

	# 過去ログを更新
	#open(OUT,">$pastfile") || &error("Can't write $pastfile");
	sysopen(OUT,"$pastfile", O_WRONLY | O_TRUNC | O_CREAT ) || &error("Can't write $pastfile");
	print OUT @news;
	close(OUT);

}

## --- 過去ログ次ファイル生成ルーチン
sub next_log {
	# 次ファイルのためのカウントアップ
	$count++;

	# カウントファイル更新
	#open(NO,">$nofile") || &error("Can't write $nofile");
	sysopen(NO,"$nofile",O_WRONLY|O_TRUNC | O_CREAT ) || &error("Can't write $nofile");
	print NO "$count";
	close(NO);

	$past_dir =~ s/\/$//;
	$pastfile  = "$past_dir\/$count\.html";

	&new_log;
}

## --- 新規過去ログファイル生成ルーチン
sub new_log {
	$new_flag = 1;

	if ($backgif) { $bgkey = "background=\"$backgif\" bgcolor=$bgcolor"; }
	else { $bgkey = "bgcolor=$bgcolor"; }
	if($nobanner){$kbn = "";}
	$past[0] = "<!doctype html><html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html\; charset=utf-8\"><title>過去ログ</title></head>\n";
	$past[1] = "<body $bgkey text=$text link=$link vlink=$vlink alink=$alink><hr size=1>\n";
	$past[2] = "<\!--HAJIME-->\n";
	$past[3] = "<\!--OWARI-->\n";
	$past[4] = "</body></html>$kbn\n";

	# 新規過去ログファイルを生成更新
	#open(OUT,">$pastfile") || &error("Can't write $pastfile");
	sysopen(OUT,"$pastfile",O_WRONLY | O_TRUNC | O_CREAT) || &error("Can't write $pastfile");
	print OUT @past;
	close(OUT);

}

#------------#
#  編集画面  #
#------------#
sub rest {
	if ($in{'action'} eq 'admin' && (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password)) {
		&error("パスワードが違います",'NOLOCK');
	}

	#open(LOG,$logfile) || &error("Can't open $logfile");
	sysopen(LOG,$logfile,O_RDONLY) || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	shift(@lines);

	# 親記事のみの配列データを作成
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$date,$name,
			$email,$sub,$com,$url,$host,$pw) = split(/<>/,$line);

		# RES記事を外す
		if ($k eq "") { push(@new,$line); }
	}

	@lines = reverse(@lines);

	&header;
	print "[<a href=\"$script?cnt=no\">掲示板へ戻る</a>]\n";
	print "<table width=100%><tr><th bgcolor=\"#0000A0\">\n";
	print "<font color=\"#FFFFFF\">コメント編集画面</font></th></tr></table>\n";
	print "<P><center>\n";
	print "<table border=0 cellpadding=5><tr>\n";
	print "<td bgcolor=\"$tbl_color\">\n";

	if ($in{'action'} eq '') {
		print "■投稿時に記入した「削除キー」により、記事を編集します。<br>\n";
	}

	print "■編集したい記事のチェックボックスにチェックを入れ、下記フォームに「削除キー」を入力してください。<br>\n";
	print "</td></tr></table><P>\n";
	print "<form action=\"$script\" method=$method>\n";
	if ($in{'ds'}) {
	print "<input type=hidden name=ds value='on'>\n";
	}

		print "<input type=hidden name=mode value=\"usr_rest\">\n";

if ($in{'action'} eq 'admin') {
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";}

if ($in{'action'} ne 'admin') {
	&get_cookie;
		print "<b>削除キー</b> <input type=password name=del_key size=10 value='$c_pwd'>\n";
}
	print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
	print "<input type=submit value=\"編集する\"><input type=reset value=\"リセット\">\n";
	print "<P><table border=1>\n";
	print "<tr><th>編集</th><th>記事No</th><th>題名</th><th>投稿者</th>";
	print "<th>投稿日</th><th>コメント</th><th>アイコン</th>\n";
	

	if ($in{'action'} eq 'admin') { print "<th>ホスト名</th>\n"; }

	print "</tr>\n";

	if ($in{'page'} eq '') { $page = 0; }
	else { $page = $in{'page'}; }

	# 記事数を取得
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

	foreach ($page .. $page_end) {
		($num,$k,$date,$name,$email,$sub,
			$com,$url,$host,$pw,$color,$icon,$d,$d,$img,$si) = split(/<>/,$new[$_]);

		($email,$mail_ex) = split(/>/,$email);
		if ($email && $mail_ex) { $name="<a href=mailto\:$email>$name</a>"; }
		if (!$sub) { $sub = "Untitled"; }
		if($img){$icon="貼\り";}elsif(!$icon){$icon="なし";}
		elsif($icon =~ /alt=\"(.*)/){$icon = $1;}

		$com =~ s/<br>/ /g;
		if ($tagkey || $tg_mc) { $com =~ s/</&lt;/g; $com =~ s/>/&gt;/g; }
		if (length($com) > 60) { $com=substr($com,0,58); $com=$com . '..'; }

			print "<tr><th><input type=radio name=del value=\"$date\"></th>\n";

		print "<th>$num</th><td>$sub</td><td>$name</td>\n";
		print "<td><small>$date</small></td><td>$com</td><td>$icon</td>\n";

		if ($in{'action'} eq 'admin') { print "<td>$host</td>\n"; }

		print "</tr>\n";

		## レスメッセージを表示
		foreach (@lines) {
			($rnum,$rk,$rd,$rname,$rem,$rsub,
				$rcom,$rurl,$rho,$rp,$rc,$ri,$d,$d,$rimg,$rsi) = split(/<>/, $_);
            if($rimg) {$ri="貼\り";}
			elsif(!$ri){$ri = "なし";}
            elsif($ri =~ /alt=\"(.*)/){$ri = $1;}
			$rcom =~ s/<br>/ /g;
			if ($tagkey || $tg_mc) { $rcom =~ s/</&lt;/g; $rcom =~ s/>/&gt;/g; }
			if (length($rcom) > 60) { $rcom=substr($rcom,0,58); $rcom=$rcom . '..'; }
			if ($num eq "$rk"){

				print "<tr><th><input type=radio name=del value=\"$rd\"></th>\n";

				print "<td colspan=2 align=center><b>$num</b>へのレス</td>\n";

				($rem,$mail_ex) = split(/>/,$rem);
				if ($rem && $mail_ex) { $rname="<a href=mailto:$rem>$rname</a>"; }

				print "<td>$rname</td><td><small>$rd</small></td><td>$rcom</td><td>$ri</td>\n";

				if ($in{'action'} eq 'admin') { print "<td>$rho</td>\n"; }

				print "</tr>\n";
			}
		}
	}
	print "</table></form>\n";
	print "<table border=0 width=100%><tr>\n";

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=hidden name=mode value=rest>\n";
		print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
		print "<input type=submit value=\"前の親記事$pagelog件\">\n";

		if ($in{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		}

		print "</form></td>\n";	
	}

	# 次頁処理
	if ($page_end ne $end_data) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=hidden name=mode value=rest>\n";
		print "<input type=hidden name=bg_img value=$in{'bg_img'}>\n";
		print "<input type=submit value=\"次の親記事$pagelog件\">\n";

		if ($in{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		}

		print "</form></td>\n";
	}

	print "</tr></table><P><hr><P>\n";
	&footer;
	exit;
}

## --- ユーザ記事編集フォーム
sub usr_rest {
	if ($in{'action'} eq 'admin' && (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password)) {
		&error("パスワードが違います",'NOLOCK');
	} else {
	if (($in{'del_key'} eq "") && ($in{'action'} ne 'admin')) { &error("削除キーが入力モレです。"); }
	}

	if ($in{'del'} eq "") { &error("ラジオボタンの選択がありません。"); }

	# ログを読み込む
	#open(LOG,"$logfile") || &error("Can't open $logfile");
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	#open(RL,"$rank_log") || &error("Can't open $rank_log");
	sysopen(RL,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
	@rank = <RL>;
	close(RL);

	foreach $line (@lines) {
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$encode_pwd,$cor,$icon,$ds,$UP,$img,$pixel) = split(/<>/,$line);

$icon =~ s/\" alt=\".*//;
$com =~ s/<br>/\n/g;
if($tg_mc){$com = &tg_de("$com");}

	if ($in{'del'} eq "$dt") {
$del_num = $num;
last;
}
	}

	if ($del_num eq '') { &error("削除対象記事が見つかりません"); }
		if (($encode_pwd eq '') && ($in{'action'} ne 'admin')) {
		&error("削除キーが設定されていません");
		}

			$cut_name = $name;
			$cut_name =~ s/＠.*//;
            $cut_name =~ s/☆.*//;
	        $cut_name =~ s/@.*//;
	        $cut_name =~ s/★.*//;

			if($pass_mode){
			foreach(@rank){
			($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
			if($cut_name eq "$d1"){$d6 =~ s/\n//;if($d6){$encode_pwd = $d6;}last;}
			}
			}

		$plain_text = $in{'del_key'};
		$check = &passwd_decode($encode_pwd);
		if (($check ne 'yes') && ($in{'action'} ne 'admin')) {
		&error("パスワードが違います");
		}

	# フォーム長を調整
	&get_agent;

	# ヘッダを出力
	&header;

	print "<center>$banner1<P>\n";

	# タイトル部
	if ($title_gif eq '') {
		print"<font color=\"$t_color\" size=5 face=\"$t_face\">";
		print "<b>記事編集</b></font>\n";
	} else {
		print "<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\">\n";
	}

($email,$m_ex) = split (/>/,$email);

if($m_ex){$m_ex = " checked";}

	if($mlfm){
		$mlad_e = "<input type=checkbox name=mail_ex value=on$m_ex> <b>メールアドレスを公開する</b>";
	}else{
		$mlad_e = "<input type=hidden name=mail_ex value=1>";
	}

	print <<"EOM";
<form method="$method" action="$script">
<input type=hidden name=mode value="Reg_usr_rest">
<input type=hidden name=del value="$in{'del'}">
<input type=hidden name=del_key value="$in{'del_key'}">
<input type=hidden name=bg_img value=$in{'bg_img'}>
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td>
    <input type=text name=name size="$nam_wid" value="$name">
  </td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td>
    <input type=text name=email size="$nam_wid" value="$email">
<span>　</span>$mlad_e
  </td>
</tr>
<tr>
  <td nowrap><b>題　　名</b></td>


  <td>
    <input type=text name=sub size="$subj_wid" value="$sub">
　  <input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap">$com</textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td>
    <input type=text size="$url_wid" name=url value="http://$url">
  </td>
</tr>
EOM

	if ( $icon_mode && (!$img || ($img =~ /bgm$/))) {
	
	&icon_exe;

	# 管理者アイコンを配列に付加
	if ($my_icon) {
		push(@icon1,"$my_gif");
		push(@icon2,"管理者用");
	}

		print "<tr><td nowrap><b>イメージ</b></td><td><select name=icon>\n";
		$inum = 0;
		foreach(0 .. $#icon1) {
			if($_ > 1){++$inum;}
			if ($icon eq "$icon1[$_]") {
				print "<option value=\"$icon1[$_]\" selected>$inum:$icon2[$_]\n";
			} else {
				print "<option value=\"$icon1[$_]\">$inum:$icon2[$_]\n";
			}
		}
		print "</select> <small>(あなたの萌えイメージ ←謎)</small><INPUT TYPE='button' VALUE='この画像を見る' onClick='upWindow(icon.options[icon.selectedIndex].value); return true'><br>\n";
	print "[<a href=\"$script?mode=image&bg_img=$in{'bg_img'}\" target='_blank'>画像イメージ参照−開けるな！キケン！（ｗ−[現在のアイコン数$Icon_num]</a>]</td></tr>\n";
	}


print<<"EOM";
<tr>
  <td nowrap>
    <b>文字色</b>
  </td>
  <td>
EOM

	if ($cor eq "") { $cor = "$COLORS[0]"; }
	foreach (@COLORS) {
		if ($cor eq "$_") {
			print "<input type=radio name=color value=\"$_\" checked>";
			print "<font color=$_>■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$_\">";
			print "<font color=$_>■</font>\n";
		}
	}
	print "</td></tr>";
	if($tg_mc){print "<tr><td colspan=2><a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank><b>マクロ説明</b></a></td></tr>";}


if ($UP_Pl == 1) {
if (!$k) {
&Teikyo'get_num($sum_up_log,$dt);
$Teikyo'SUM_coment =~ s/<br>/\r/g;
if ($UP eq 'up_exist') {$UP_ck = ' checked';}
print <<"EOM";
<BR><BR>
<tr>
  <td colspan=2>
  <input type=checkbox name=up_check$UP_ck>
  <b>提供品がある場合はここにチェックを</b>(チェックを外せば削除できます)</td><br>
</tr>
<tr>
  <td nowrap><b>提供品名</b></td>
  <td><input type=text size="$subj_wid" name=up_title value="$Teikyo'SUM_title">：空欄の場合は題名が提供品名になります</td>
</tr>
<tr>
  <td nowrap><b>提供数</b></td>
  <td><input type=text size="5" name=up_limit maxlength=3 value="$Teikyo'SUM_limit">：0〜999の間で入力してね。それ以外は無制限になります</td>
</tr>
<tr>
  <td colspan=2>
    <b>提供品ＵＲＬ・コメント等</b><br>
    <textarea cols="$com_wid" rows=2 name=up_comment wrap="$wrap">$Teikyo'SUM_coment</textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>DL数</b></td>
  <td><input type=text size="4" name=DL_num value="$Teikyo'SUM_num"></td>
</tr>
EOM
}
}
if($img =~ /bgm$/){$img =~ s/bgm$//;$bgm=$img;$bgme="　<a href=$bgm target=_blank><b>貼\りBGM</b></a>";$imps=1;}
elsif($img =~ /swf$/){ $bgmz="　<b>貼\りFlash</b></a>";$impz=1;}
elsif($img =~ /cgm$/){
$img =~ s/\.([^.]+)\.([^.]*)cgm$//;
$pic = "$img.$1";$bgm = "$img.$2";
$bgme="　<a href=$bgm target=_blank><b>貼\りBGM</b></a>";
$img = $pic;
}

if($bgm){print"<tr><td nowrap><input type=checkbox name=ch_bgm value=$bgm checked>$bgme
</td><td>（チェックを外せば削除できます)</td></tr>";}

if($impz){print"<tr><td nowrap><input type=checkbox name=ch_img value=$img checked>$bgmz
</td><td>（チェックを外せば削除できます)</td></tr><tr><td colspan=2><embed src=$img width=600 height=480></td></tr>";}

if(!$imps && $img &&!$impz){print"<tr><td nowrap><input type=checkbox name=ch_img value=$img checked>　<B>貼\り画像</B>
</td><td>（チェックを外せば削除できます)</td></tr><tr><td colspan=2><img src=$img></td></tr>";}

&d_mode;
		if ($in{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		}

	print "</td></tr></table></form></blockquote><hr>\n";

	&footer;
	exit;

}

## --- ユーザ記事編集処理
sub usr_rest2{
	if ($in{'action'} eq 'admin' && (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password)) {
		&error("パスワードが違います",'NOLOCK');
	} else {
	if (($in{'del_key'} eq "") && ($in{'action'} ne 'admin')) { &error("削除キーが入力モレです。"); }
	}

	if ($in{'del'} eq "") { &error("ラジオボタンの選択がありません。"); }

	# ログを読み込む
	if($fll){
		foreach (1 .. 10) {
			unless (-e $lockfile) {last;}
			sleep(1);
		}
	}
	#open(LOG,"$logfile") || &error("Can't open $logfile");
	sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile");
	if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@lines = <LOG>;
	close(LOG);

	if($fll){
		foreach (1 .. 10) {
			unless (-e $rklock) {last;}
			sleep(1);
		}
	}
	#open(RL,"$rank_log") || &error("Can't open $rank_log");
	sysopen(RL,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
	if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@rank = <RL>;
	close(RL);

	# 親記事NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("ログが正しくありません。<P><small>\(Petit v2.5以前のログの場合は変換の必要があります\)<\/small>");
	}

	shift(@lines);

	## 削除キーによる記事編集 ##
	@new=();
	foreach $line (@lines) {
		$dflag = 0;
		($num,$k,$dt,$dn,$d,$d,$d,$d,$d,$ango,$d,$d,$d,$UP,$dimg,$pixel) = split(/<>/,$line);

		if ($in{'del'} eq "$dt") {

		if (($ango eq '') && ($in{'action'} ne 'admin')) {
		&error("削除キーが設定されていません");
		}

			$cut_dn = $dn;
			$cut_dn =~ s/＠.*//;
            $cut_dn =~ s/☆.*//;
	        $cut_dn =~ s/@.*//;
	        $cut_dn =~ s/★.*//;

			if($pass_mode){
			foreach(@rank){
			($d1,$d2,$d3,$d4,$d5,$d6) = split(/<>/,$_);
			if($cut_dn eq "$d1"){$d6 =~ s/\n//;if($d6){$ango = $d6;}last;}
			}
			}

		$plain_text = $in{'del_key'};
		$check = &passwd_decode($ango);
		if (($check ne 'yes') && ($in{'action'} ne 'admin')) {
		&error("パスワードが違います");
		}

	# 名前とコメントは必須
	if ($name eq "") { &error("名前が入力されていません"); }
	if ($comment eq "") { &error("コメントが入力されていません"); }
	if(!$mlfm && !$email){$in{mail_ex} = 0;}
	if (($email || $in{mail_ex}) && $email !~ /(.*)\@(.*)\.(.*)/) {
		&error("Ｅメールの入力内容が正しくありません",'NOLOCK');
	}

	# 提供品チェックにチェックが入っているとき
	if ($up_check eq 'on' && $up_comment eq ""){
	&error("提供品コメントを入力してください",'NOLOCK');}
	elsif($up_check eq 'on'){$up_on="up_exist";}
	if($up_title eq ""){$up_title=$sub;}

	# ホスト名を取得
	&get_host;

	$del_num = $num;

	$cut_name = $name;
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;


	## 認証&編集rank

	foreach(@rank){
	$_ =~ s/\n//;
	($r_name,$r_cnt,$cg_cnt,$bgm_cnt,$flash_cnt,$res_cnt,$r_pass,$lac,$rest_cnt,$mcr_cnt) = split(/<>/,$_);

	if($r_name eq $cut_name){

	if($pass_mode){
	if($r_pass){		
	$plain_text = $in{'del_key'};
	$check = &passwd_decode($r_pass);
	if ($check ne 'yes') { &error("$cut_nameさんのパスワードと一致しません"); }
	$ps_tr = 1;
	}
	}

	++$rest_cnt;
	$new_rank = "$r_name<>$r_cnt<>$cg_cnt<>$bgm_cnt<>$flash_cnt<>$res_cnt<>$r_pass<>$lac<>$rest_cnt<>$mcr_cnt<>\n";
	push(@new_rank,$new_rank);

	}else{
	push(@new_rank,"$_\n");
	}

	}

	&icon_exe;

	if($icon eq "none.gif"){$icon_reg = $icon;}
	elsif($icon eq "rand.gif"){

	srand;

	if($rd_pri){$ico_rd = int(rand($Icon_num));}
	else{$ico_rd = int(rand($nm_ico_nm));}

	splice(@icon1,0,2);
	splice(@icon2,0,2);

	$icon_reg = "$icon1[$ico_rd]\" alt=\"$icon2[$ico_rd]";
	}
	else{

	foreach(0 .. $#icon1) {

	if($icon eq $icon1[$_]){
		if($Inum[$_] =~/pri_ico/){
		#if($cut_name ne $usr_n[$_]){$ico_err = 1;}
		$plain_text = $in{'del_key'};
		$encode_pwd = $usr_p[$_];
		$check = &passwd_decode($encode_pwd);
		if ($check ne 'yes') {$ico_err = 1;}
		if ($in{'action'} eq 'admin' && (crypt($in{'pass'}, substr($password, $salt, 2) ) eq $password)) {$ico_err=0;}
		if($ps_tr && ($cut_name eq "$usr_n[$_]")) {$ico_err = 0;}
		if($ico_err){&error("このアイコンは$usr_n[$_]専用です");}
		}

	$icon_reg = "$icon1[$_]\" alt=\"$icon2[$_]";last;
	}

	}

	}

	# 時間を取得
	&get_time;

	if($ImgDir2){$dimg =~ s/^$ImgDir2//;$dimg = "$ImgDir$dimg";}

	# .cgm処理
	if($dimg =~ /cgm$/){
	$t_dimg=$dimg;
	$t_dimg =~ s/\.([^.]+)\.([^.]*)cgm$//;
	$pic = "$t_dimg.$1";$bgm = "$t_dimg.$2";

	#ログ互換
	if($bgm =~ /\.$/){$bgm="$t_dimg.bgm";}

#	if(!$in{'ch_img'} && (-e "$pic")){ unlink("$pic");$img_del=1; }
#	if(!$in{'ch_bgm'} && (-e "$bgm")){ unlink("$bgm");$bgm_del=1; }
	if($img_del && $bgm_del){$dimg="";}
	elsif($img_del){$dimg="$bgm"."bgm";}
	elsif($bgm_del){$dimg=$pic;}

	}

	# 貼り画像削除
	elsif(($dimg !~ /bgm$/) && !$in{'ch_img'} && ($dimg) && (-e "$dimg")){
#       unlink("$dimg");
        $dimg="";
        $pixel = "";
    }

	# 貼りBGM削除
	elsif(($dimg =~ /bgm$/) && !$in{'ch_bgm'}){

	$t_dimg=$dimg;
	$t_dimg =~ s/bgm$//;		
	#ログ互換
	if($t_dimg =~ /\.$/){$t_dimg="$t_dimg"."bgm";}		
	if(-e "$t_dimg"){ unlink("$t_dimg");$dimg="";}

	}

	if($dimg && $ImgDir2){$dimg =~ s/^$ImgDir//;$dimg = "$ImgDir2$dimg";}

	if($in{mail_ex}){$email = "$email\>1";}

	if($tg_mc){$comment = &tg_en("$comment");}
	if($vote){
		unless(-e "$vt_dir$num\.vt"){
			#open(VT,">$vt_dir$num\.vt") || &error("Can't open $vt_dir$num\.vt");
			sysopen(VT,"$vt_dir$num\.vt" , O_WRONLY | O_TRUNC | O_CREAT) || &error("Can't open $vt_dir$num\.vt");
			close(VT);
			chmod(oct($vt_pm),"$vt_dir$num\.vt");
		}
	}
	# ログをフォーマット
	$line = "$num<>$k<>$date(編集)<>$name<>$email<>$sub<>$comment<>$url<>$host<>$ango<>$color<>$icon_reg<>$in{'Tbl_B'}<>$up_on<>$dimg<>$pixel";

	if (($UP eq 'up_exist') && ($up_check eq 'on')) {
	# 提供品ログの修正
	&Teikyo'rest($sum_up_log,$dt,$up_title,$up_comment,$DL_num,"$date(編集)",$name,$up_limit,$ango);
	} elsif ($up_check eq 'on') {
	# 提供品ログに書き込み
	&Teikyo'regist($sum_up_log,"$date(編集)",$up_title,$up_comment,0,$name,$up_limit,$ango);
	} elsif (($UP eq 'up_exist') && ($up_check ne 'on')) {
	# 提供品ログより削除
	&Teikyo'del($sum_up_log,$dt);
	}

	last;	}

	}

	$dbl = 0;srand;
	foreach(@lines){
	($num,$k,$dt,$name,$email,$sub,$comment,$url,$host,$ango,$color,$icon_reg,$in{'Tbl_B'},$up_on,$dimg,$pixel) = split(/<>/,$_);
	if($dt eq "$date(編集)"){++$dbl;if($dbl > 1){$und = int(rand(1000));$_ = "$num<>$k<>$date\:$und\(編集)<>$name<>$email<>$sub<>$comment<>$url<>$host<>$ango<>$color<>$icon_reg<>$in{'Tbl_B'}<>$up_on<>$dimg<>$pixel";}}
	}

	# 親記事NOを付加
	unshift(@lines,$oya);
	if ($del_num eq '') { &error("編集対象記事が見つかりません"); }

	## だ〜び〜書きこみ
	if($fll){
		&fll("$rklock","$rank_log",@new_rank);
	}else{
		#open(RL, "+< $rank_log") || &error("Can't open $rank_log");
		sysopen(RL, "$rank_log" , O_RDWR ) || &error("Can't open $rank_log");
		if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(RL, 0);
		seek(RL, 0, 0);
		print RL @new_rank;
		close(RL);
	}

	## ログを更新 ##
	if($fll){
		&fll("$lockfile","$logfile",@lines);
	}else{
		#open(LOG, "+< $logfile") || &error("Can't open $logfile");
		sysopen(LOG, "$logfile" , O_RDWR ) || &error("Can't open $logfile");
		if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG @lines;
		close(LOG);
	}

	## HTML作成
	if($html_on){
		require './html.pl';
		&html_ex;
		$html_write = 0;
	}

$in{'ds'} = $in{'Tbl_B'};

	# 編集画面にもどる
	&rest;
}

## pass認証変更
sub pass_rest{

if($in{rest_sel}){

	## 認証
	if($fll){
		foreach (1 .. 10) {
			unless (-e $rklock) {last;}
			sleep(1);
		}
	}
	#open(RL,"$rank_log") || &error("Can't open $rank_log");
	sysopen(RL,"$rank_log",O_RDONLY) || &error("Can't open $rank_log");
	if($lockkey == 3){flock(RL,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
	@rank = <RL>;
	close(RL);

	$cut_name = $name;
	$cut_name =~ s/＠.*//;
    $cut_name =~ s/☆.*//;
	$cut_name =~ s/@.*//;
	$cut_name =~ s/★.*//;

	foreach(@rank){
	$tmp = $_;
	$tmp =~ s/\n//;
	($r_name,$r_cnt,$cg_cnt,$bgm_cnt,$flash_cnt,$res_cnt,$r_pass,$la,$rest_cnt,$mcr_cnt) = split(/<>/,$tmp);

	if($r_name eq $cut_name){
	$usr_ck = 1;

	if($r_pass){		
	$plain_text = $in{'pwd'};
	$check = &passwd_decode($r_pass);
	if ($check ne 'yes') { &error("$cut_nameさんのパスワードと一致しません"); }
	}

		if($in{rest_sel} eq "pass_del"){
		$ex_msg = "貼\り逃げだ〜び〜のお名前・認証passが削除されました";$_ = "";last;
		}else{
		if(!$in{ch_pwd}){&error("パスワードが記入されてません");}
		elsif($in{ch_pwd} ne $in{ch_pwd2}){&error("パスワードの入力ミスです");}

			else{
			&passwd_encode($in{ch_pwd});
			$_ = "$r_name<>$r_cnt<>$cg_cnt<>$bgm_cnt<>$flash_cnt<>$res_cnt<>$ango<>$la<>$rest_cnt<>$mcr_cnt<>\n";
			}

		$ex_msg = "認証passは変更されました";last;
		}

	}

	}

if(!$usr_ck){&error("対象となるお名前がありません");}
if($fll){
	&fll("$rklock","$rank_log",@rank);
}else{
	#open(RL, "+< $rank_log") || &error("Can't open $rank_log");
	sysopen(RL, "$rank_log" , O_RDWR ) || &error("Can't open $rank_log");
	if($lockkey == 3){flock(RL,2) |unlink| &error("filelock 失ヽ(´ー｀)ノ敗");}
	truncate(RL, 0);
	seek(RL, 0, 0);
	print RL @rank;
	close(RL);
}

&get_cookie;

$name = $c_name;
$email = $c_email;
$url = $c_url;
$pwd = $in{ch_pwd};
$icon = $c_icon;
$color = $c_color;
$in{mail_ex} = $c_m_ex;

&set_cookie;

&header;
print <<"EOM";
[<a href=\"$script?cnt=no\">掲示板へ戻る</a>]<br><br><br>
<center><b><font color=blue face=\"$t_face\" size=+2>$ex_msg</font></b></font></center><br><br><br>
EOM
&footer;
exit;
}

&get_cookie;
&header;
print <<"EOM";
[<a href=\"$script?cnt=no\">掲示板へ戻る</a>]<br>
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>認証pass変更・だ〜び〜削除</SPAN></b></font></center><br>
<form method="POST" action="$script">
<center>
<table bgcolor=white cellspacing=0 border=1 bordercolor=black><tr><td>
<input type=hidden name=mode value=pass_rest>
<input type=hidden name=bg_img value="$bg_img">
<table>
<tr><td>お名前</td><td><input type=text name=name size=12 value=\"$c_name\"></td></tr>
<tr><td>削除キー</td><td><input type=password name=pwd size=12 maxlength=8 value=$c_pwd></td></tr>
<tr><td colspan=2><br></td></tr>
<tr><td colspan=2><input type=radio name=rest_sel value=pass_ch checked>　認証pass変更</td></tr>
<tr><td>新削除キー</td><td><input type=password name=ch_pwd size=12 maxlength=8></td></tr>
<tr><td>新削除キー</td><td><input type=password name=ch_pwd2 size=12 maxlength=8>（もう一度）</td></tr>
<tr><td colspan=2><br></td></tr>
<tr><td colspan=2><input type=radio name=rest_sel value=pass_del>　らんきんぐ削除</td></tr>
<tr><td colspan=2>※貼\り逃げだ〜び〜からお名前を削除します<br>※認証passも削除されます</td></tr>
</table>

<br>
<center><input type=submit name=pre_ch value=OK></center>
</td></tr></table>
EOM
&footer;
exit;
}

#--- 管理者パスワード登録＆暗号化 --------------------------------#
sub password {
  $psold = $in{'password_old'};
  $pas1 = $in{'password'};
  $pas2 = $in{'password2'};
  
  print <<"_HTML_";
Content-type: text/html

<!doctype html>
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<TITLE>$title</TITLE>
</HEAD>
$body
<H1>管理者パスワードの設定\／変更画面</H1>
_HTML_
  if ($start2 == 1 && $pas1 eq '') {
    print "管理者パスワードをこのページで設定\します。<P>\n";
  } elsif ($pas1 =~ /\W/) {
    print "<FONT COLOR=red>新パスワードに英数字以外の文字が含まれています。</FONT><P>\n";
  } elsif ( $pas1 ne '' && $pas1 ne $pas2 ){
    print "<FONT COLOR=red>確認のために入力された新パスワードが一致しません。</FONT><P>\n";
  } elsif ( $start2 != 1 && $psold eq '' ) {
    print "<FONT COLOR=red>旧パスワードも入力して下さい。</FONT><P>\n";
  } elsif ( $start2 != 1 && (crypt($psold, substr($password, $salt, 2) ) ne $password) ){
    print "<FONT COLOR=red>旧パスワードが認証されませんでした。</FONT><P>\n";
  } else {
    $now = time;
    ($p1, $p2) = unpack("C2", $now);
    $wk = $now / (60 * 60 * 24 * 7) + $p1 + $p2 - 8;
    @saltset = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
    $nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
    $pwd = crypt($in{'password'}, $nsalt);

    #if ( !open(DB,">$passfile") ) { &error(0,__LINE__,__FILE__); }
    sysopen(DB,"$passfile" ,O_WRONLY | O_TRUNC | O_CREAT ) || &error(0,__LINE__,__FILE__);
    print DB "crypt_password:$pwd\n";
    close(DB);
    print "<FONT COLOR=blue SIZE=+3>管理者パスワードが設定\されました。<BR><A HREF='$script'>[ＮＥＸＴ]</A>をクリックして下さい。</FONT><P>再度変更する場合は下記フォームで再入力しなおして下さい。<P><br>従来の萌え板のログを引き継ぐ方はまずは管理画面のランクログ変換をしてください<br>新規で使うかたはこのままで大丈夫です\n";
  }
  print "<FORM method=\"POST\" action=\"$script?pas\">\n";
  print "<INPUT type=\"hidden\" name=\"papost\" value=\"pcode\">\n";
  if ($start2 != 1) {
    print "旧パスワード <INPUT type=\"password\" name=\"password_old\" size=\"8\" maxlength=\"8\"><BR>\n";
  }
  print <<"_HTML_";
新パスワード <INPUT type="password" name="password" size="8" maxlength="8">（半角英数８文字以内）<BR>
新パスワード <INPUT type="password" name="password2" size="8" maxlength="8">（確認のため上と同じパスをもう一度）<P>
<INPUT type="submit" value="     登録     ">
</FORM><P>
</BODY>
</HTML>
_HTML_
  exit;
}

sub d_mode{
if ($in{'ds'} || $ds) {
if ($ds) {$dark_side = ' checked';}
	print <<"_HTML_";
<tr>
  <td nowrap>
    <b>だ〜くさいど</b>
  </td>
  <td>
<input type="checkbox" name="Tbl_B" value="on"$dark_side>
  </td>
</tr>
_HTML_
}
}

## 新規投稿
sub new_topic {

	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_agent;
if($c_m_ex){$c_m_ex = " checked";}
if($bgm_up){
$max_dat=int($cgi_lib'maxdata/1024);
$bgm_ti="・BGM貼\り";
$bgm_form= <<"EOM";
<tr><td nowrap><b>貼\りBGM</b></td>
  <td nowrap>
  <input type=file name=upbgm size="$nam_wid"><span>　</span>wav,mid,mp3,asf,wma $max_dat KBまで（貼りたい人だけ）
</td>
</tr>
EOM
}

	if($mlfm){
		$mlad_e = "<input type=checkbox name=mail_ex value=on$c_m_ex> <b>メールアドレスを公開する</b>";
	}else{
		$mlad_e = "<input type=hidden name=mail_ex value=1>";
	}

&header;
print <<EOM;
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>新規かきこも〜ど♪</SPAN></b></font></center><br>
<form method="POST" action="$script" enctype=multipart/form-data target=_parent>
<input type=hidden name=mode value="msg">
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td><input type=text name=name size="$nam_wid" value="$c_name"><small>　<b>「＠、@、☆、★」をつけても同一人物として認識されます。</b></small></td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td><input type=text name=email size="$nam_wid" value="$c_email">
<span>　</span>$mlad_e
</td>
</tr>
<tr>
  <td nowrap><b>題　　名</b></td>
  <td nowrap>
    <input type=text name=sub size="$subj_wid">
　  <input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
$bgm_form
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap"></textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td><input type=text size="$url_wid" name=url value="http://$c_url"></td>
</tr>
EOM



	if ($icon_mode) {

		&icon_exe;

	# 管理者アイコンを配列に付加
	if ($my_icon) {
		push(@icon1,"$my_gif");
		push(@icon2,"管理者用");
	}

		print "<tr><td nowrap><b>イメージ</b></td><td><select name=icon>\n";
		$inum = 0;
		foreach(0 .. $#icon1) {
			if($_ > 1){++$inum;}
			if ($c_icon eq "$icon1[$_]") {
				print "<option value=\"$icon1[$_]\" selected>$inum:$icon2[$_]\n";			   } else {
				print "<option value=\"$icon1[$_]\">$inum:$icon2[$_]\n";
			}
		}
	print "</select> <small>(あなたの萌えキャラ（笑）を選択して下さい♪)</small><INPUT TYPE='button' VALUE='この画像を見る' onClick='upWindow(icon.options[icon.selectedIndex].value); return true'><br>\n";
	print "[<a href=\"$script?mode=image&bg_img=$in{'bg_img'}\" target='_blank'>画像イメージ参照−開けるな！キケン！（ｗ−[現在のアイコン数$Icon_num]</a>]</td></tr>\n";
	}

	print "<tr><td nowrap><b>削除キー</b></td>\n";
	print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$c_pwd\">\n";
	print "<small>(自分の記事を削除時に使用。英数字で8文字以内)</small></td></tr>\n";
	print "<tr><td colspan=2><b>※ 最初に投稿をしたときの削除キーと違うと投稿ができません</b></td></tr>";
	print "<tr><td nowrap><b>文字色</b></td><td>\n";

	# クッキーの色情報がない場合
	if ($c_color eq "") { $c_color = $COLORS[0]; }

	foreach (0 .. $#COLORS) {
		if ($c_color eq "$COLORS[$_]") {
			print "<input type=radio name=color value=\"$COLORS[$_]\" checked> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$COLORS[$_]\"> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		}
	}
	print "</td></tr>";
	if($tg_mc){print "<tr><td colspan=2><a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank><b>マクロ説明</b></a></td></tr>";}

&d_mode;

if ($UP_Pl == 1) {
## ↓提供品名・提供品ＵＲＬ・コメント等を追加##
print <<"EOM";
<BR><BR>
<tr>
  <td colspan=2>
  <input type=checkbox name=up_check>
  <b>提供品がある場合はここにチェックを</b></td><br>
</tr>
<tr>
  <td nowrap><b>提供品名</b></td>
  <td><input type=text size="$subj_wid" name=up_title>：空欄の場合は題名が提供品名になります</td>
</tr>
<tr>
  <td nowrap><b>提供数</b></td>
  <td><input type=text size="5" name=up_limit maxlength=3>：0〜999の間で入力してね。それ以外は無制限になります</td>
</tr>
<tr>
  <td colspan=2>
    <b>提供品ＵＲＬ・コメント等</b><br>
    <textarea cols="$com_wid" rows=2 name=up_comment wrap="$wrap"></textarea>
  </td>
</tr>
EOM
}
print "</td></tr></table></form></blockquote><hr>\n";
&footer;
exit;}

## 画像はっつけ投稿フォーム
sub gazou_topic {

$max_dat=int($cgi_lib'maxdata/1024);
	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_agent;

if($c_m_ex){$c_m_ex = " checked";}
$mx_ex="<span>　</span>jpg,gif,png $max_dat KBまで";

if($bgm_up){
$mx_ex="<span>　</span>jpg,gif,png";
$bgm_ti="+BGM";
$bgm_form= <<"EOM";
<tr><td nowrap><b>貼\りBGM</b></td>
  <td nowrap>
  <input type=file name=upbgm size="$nam_wid"><span>　</span>wav,mid,mp3,asf,wma 画像と合わせて $max_dat KBまで（貼りたい人だけ）
</td>
</tr>
EOM
}

	if($mlfm){
		$mlad_e = "<input type=checkbox name=mail_ex value=on$c_m_ex> <b>メールアドレスを公開する</b>";
	}else{
		$mlad_e = "<input type=hidden name=mail_ex value=1>";
	}

&header;
print <<EOM;
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>画像$bgm_tiはっつけモード</SPAN></b></font></center><br>
<form method="POST" action="$script" enctype=multipart/form-data target=_parent>
<input type=hidden name=mode value="msg">
<input type=hidden name=hari value="on">
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td><input type=text name=name size="$nam_wid" value="$c_name"><small>　<b>「＠、@、☆、★」をつけても同一人物として認識されます。</b></small></td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td><input type=text name=email size="$nam_wid" value="$c_email">
<span>　</span>$mlad_e
</td>
</tr>
<tr>
  <td nowrap><b>題　　名</b></td>
  <td nowrap>
    <input type=text name=sub size="$subj_wid">
　  <input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
<tr><td nowrap><b>貼\り画像</b></td>
  <td nowrap>
  <input type=file name=upfile size="$nam_wid">$mx_ex
</td>
</tr>
$bgm_form
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap"></textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td><input type=text size="$url_wid" name=url value="http://$c_url"></td>
</tr>
<input type=hidden name=icon value=$c_icon>
EOM
	print "<tr><td nowrap><b>削除キー</b></td>\n";
	print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$c_pwd\">\n";
	print "<small>(自分の記事を削除時に使用。英数字で8文字以内)</small></td></tr>\n";
	print "<tr><td colspan=2><b>※ 最初に投稿をしたときの削除キーと違うと投稿ができません</b></td></tr>";
	print "<tr><td nowrap><b>文字色</b></td><td>\n";

	# クッキーの色情報がない場合
	if ($c_color eq "") { $c_color = $COLORS[0]; }

	foreach (0 .. $#COLORS) {
		if ($c_color eq "$COLORS[$_]") {
			print "<input type=radio name=color value=\"$COLORS[$_]\" checked> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$COLORS[$_]\"> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		}
	}
	print "</td></tr>";
	if($tg_mc){print "<tr><td colspan=2><a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank><b>マクロ説明</b></a></td></tr>";}
&d_mode;

if ($UP_Pl == 1) {
## ↓提供品名・提供品ＵＲＬ・コメント等を追加##
print <<"EOM";
<BR><BR>
<tr>
  <td colspan=2>
  <input type=checkbox name=up_check>
  <b>提供品がある場合はここにチェックを</b></td><br>
</tr>
<tr>
  <td nowrap><b>提供品名</b></td>
  <td><input type=text size="$subj_wid" name=up_title>：空欄の場合は題名が提供品名になります</td>
</tr>
<tr>
  <td nowrap><b>提供数</b></td>
  <td><input type=text size="5" name=up_limit maxlength=3>：0〜999の間で入力してね。それ以外は無制限になります</td>
</tr>
<tr>
  <td colspan=2>
    <b>提供品ＵＲＬ・コメント等</b><br>
    <textarea cols="$com_wid" rows=2 name=up_comment wrap="$wrap"></textarea>
  </td>
</tr>
EOM
}
print "</td></tr></table></form></blockquote><hr>\n";
&footer;
exit;}

## Flash投稿
sub flash_topic {

	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_agent;
if($c_m_ex){$c_m_ex = " checked";}
$max_dat=int($cgi_lib'maxdata/1024);

$bgm_form= <<"EOM";
<tr><td nowrap><b>貼\りFlash</b></td>
  <td nowrap>
  <input type=file name=upflash size="$nam_wid"><span>　</span>swfファイル $max_dat KBまで
</td>
</tr>
EOM


	if($mlfm){
		$mlad_e = "<input type=checkbox name=mail_ex value=on$c_m_ex> <b>メールアドレスを公開する</b>";
	}else{
		$mlad_e = "<input type=hidden name=mail_ex value=1>";
	}

&header;
print <<EOM;
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>Flashはっつけも〜ど♪</SPAN></b></font></center><br>
<form method="POST" action="$script" enctype=multipart/form-data target=_parent>
<input type=hidden name=mode value="msg">
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td><input type=text name=name size="$nam_wid" value="$c_name"><small>　<b>「＠、@、☆、★」をつけても同一人物として認識されます。</b></small></td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td><input type=text name=email size="$nam_wid" value="$c_email">
<span>　</span>$mlad_e
</td>
</tr>
<tr>
  <td nowrap><b>題　　名</b></td>
  <td nowrap>
    <input type=text name=sub size="$subj_wid">
　  <input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
$bgm_form
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap"></textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td><input type=text size="$url_wid" name=url value="http://$c_url"></td>
</tr>
<input type=hidden name=icon value=$c_icon>
EOM
	print "<tr><td nowrap><b>削除キー</b></td>\n";
	print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$c_pwd\">\n";
	print "<small>(自分の記事を削除時に使用。英数字で8文字以内)</small></td></tr>\n";
	print "<tr><td colspan=2><b>※ 最初に投稿をしたときの削除キーと違うと投稿ができません</b></td></tr>";
	print "<tr><td nowrap><b>文字色</b></td><td>\n";

	# クッキーの色情報がない場合
	if ($c_color eq "") { $c_color = $COLORS[0]; }

	foreach (0 .. $#COLORS) {
		if ($c_color eq "$COLORS[$_]") {
			print "<input type=radio name=color value=\"$COLORS[$_]\" checked> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$COLORS[$_]\"> ";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		}
	}
	print "</td></tr>";
	if($tg_mc){print "<tr><td colspan=2><a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank><b>マクロ説明</b></a></td></tr>";}

&d_mode;

if ($UP_Pl == 1) {
## ↓提供品名・提供品ＵＲＬ・コメント等を追加##
print <<"EOM";
<BR><BR>
<tr>
  <td colspan=2>
  <input type=checkbox name=up_check>
  <b>提供品がある場合はここにチェックを</b></td><br>
</tr>
<tr>
  <td nowrap><b>提供品名</b></td>
  <td><input type=text size="$subj_wid" name=up_title>：空欄の場合は題名が提供品名になります</td>
</tr>
<tr>
  <td nowrap><b>提供数</b></td>
  <td><input type=text size="5" name=up_limit maxlength=3>：0〜999の間で入力してね。それ以外は無制限になります</td>
</tr>
<tr>
  <td colspan=2>
    <b>提供品ＵＲＬ・コメント等</b><br>
    <textarea cols="$com_wid" rows=2 name=up_comment wrap="$wrap"></textarea>
  </td>
</tr>
EOM
}
print "</td></tr></table></form></blockquote><hr>\n";
&footer;
exit;}

## 以下KENTさんの ClipBoard から流用

sub UpFile {
	# 画像処理
	$macbin=0;
	foreach (@in) {
		if($upf_f && $t_f){$dm_f=1;}elsif($_ =~ /(.*)Content-type:(.*)\/(.*)/i) { $tail=$3;$t_f=1; }
		if($upf_f && $f_f){$dm_f=1;}elsif($_ =~ /(.*)filename=(.*)/i) { $fname=$2;$f_f=1; }
		if ($_ =~ /application\/x-macbinary/i) { $macbin=1; }
	}
	$upf_f="";$t_f="";$f_f="";
	$tail =~ s/\r//g;
	$tail =~ s/\n//g;
	$fname =~ s/\"//g;

	# ファイル形式を認識
	$flag=0;
	if ($tail =~ /gif/i) { $tail=".gif"; $flag=1; }
	if ($tail =~ /jpeg/i) { $tail=".jpg"; $flag=1; }
	if ($tail =~ /x-png/i) { $tail=".png"; $flag=1; }
	if ($tail =~ /png/i) { $tail=".png"; $flag=1; }
	if (!$flag) {
		#if ($fname =~ /.gif/i) { $tail=".gif"; $flag=1; }
		#if (($fname =~ /.jpg/i) || ($fname =~ /.jpeg/i)){ $tail=".jpg"; $flag=1; }
		#if ($fname =~ /.png/i) { $tail=".png"; $flag=1; }
	}
    
    if($upz_f){
    if ($tail =~ /shockwave\-flash/i) { $tail=".swf"; $msz=1; }
	if (!$msz) { &error("アップロードできないファイル形式です","lock"); }

	$upfile = $in{'upflash'};
    }
    
	if($upb_f){

	@ok_ad= keys(%ok_ad);
	foreach $ck_ad(@ok_ad){
	if ($tail =~ /$ck_ad/i) { $tail=".$ok_ad{$ck_ad}";$b_tail=$ok_ad{$ck_ad};$msc=1;last;}
	}

	if (!$msc) { &error("アップロードできないファイル形式です","lock"); }

	$upfile = $in{'upbgm'};
	}elsif(!$msz){
	if (!$flag) { &error("アップロードできないファイル形式です","lock"); }
	$w_tail=$tail;
	$upfile = $in{'upfile'};
	}

	# マックバイナリ対策
	if ($macbin) {
		$length = substr($upfile,83,4);
		$length = unpack("%N",$length);
		$upfile = substr($upfile,128,$length);
	}

	# 添付データを書き込み
	if($upb_f){
	$ImgFile = "$ImgDir$imgdata$tail";
	$up_err_msg="BGMのアップロードに失敗しました";
	}
    elsif($upz_f){
	$ImgFile = "$ImgDir$imgdata$tail";
	$up_err_msg="Flashのアップロードに失敗しました";
	}
	else{
	$ImgFile = "$ImgDir$imgdata$tail";
	$up_err_msg="画像のアップロードに失敗しました";
	}

	#open(OUT,"> $ImgFile") || &error("$up_err_msg","lock");
	sysopen(OUT,"$ImgFile" , O_WRONLY | O_TRUNC | O_CREAT ) || &error("$up_err_msg","lock");
	binmode(OUT);
	binmode(STDOUT);
	print OUT $upfile;
	close(OUT);

	chmod (0666,$ImgFile);
	$upb_f="";$macbin="";$msc="";
}

# バックアップ
sub bk_up{

	if  (crypt($in{'pass'}, substr($password, $salt, 2)) ne $password) {
	&error("パスワードが違います",'NOLOCK');
	}

if($in{'bk_load'}){&recv;}
if($in{'bk_lock'}){chmod(oct($bk_pm),$bk_dat);}

elsif($in{'bk_save'}){
&get_time;
@bk_up_lines=("$date\n<date>\n");

foreach(@bk_up){
	#open(BKUP,$_);
	sysopen(BKUP,$_,O_RDONLY);
	@bk_lines=<BKUP>;
	close(BKUP);
	push(@bk_lines,"<$_>\n");
	push(@bk_up_lines,@bk_lines);
}

#open(BKUP,">$bk_dat");
sysopen(BKUP,"$bk_dat",O_WRONLY | O_TRUNC | O_CREAT);
print BKUP @bk_up_lines;
close(BKUP);

chmod (0666,$bk_dat);

	#if ($ENV{PERLXS} eq "PerlIS") {
	#print "HTTP/1.0 302 Temporary Redirection\r\n";
	#print "Content-type: text/html\n";
	#}
if(!$redi){
	print "Location: $bk_dat\n\n";
}else{
	&header;
	print "<META HTTP-EQUIV=\"Refresh\" Content=0\;url=$bk_dat>";
	&footer;
}
exit;
}

#open(BKUP,"$bk_dat");
sysopen(BKUP,"$bk_dat",O_RDONLY);
$bk_date=<BKUP>;
close(BKUP);

	if($bk_date){
	chop($bk_date);

$bkex= <<"EOM";
ログ修復：$bk_dateの状態に戻します$a<br>
<form action=$script target=_parent>
<input type=hidden name=mode value=bkup>
<input type=hidden name=bk_load value=on>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=bg_img value=$in{'bg_img'}>
<input type=submit value=修復する>
</form>
EOM

	}

	else{
	$bk_date="不明";
	}
&header;
print <<EOM;
[<a href=\"$homepage\">トップにもどる</a>]<br><br>
<center>
最後にバックアップをとったのは$bk_dateです。<br><br>
<table>
<tr><td>
<a href=$script?mode=bkup&bk_save=on&pass=$in{'pass'}&bg_img=$in{'bg_img'}>ログバックアップ</a>
</td></tr>
<tr><td><br></td></tr>
<tr><td>
<a href=$script?mode=bkup&bk_lock=on&pass=$in{'pass'}&bg_img=$in{'bg_img'}>ログ鍵かけ</a>
(バックアップをとった後に実行して下さい)
</td></tr>
<tr><td><br></td></tr>
<tr><td>
<a href=\"ico_del.cgi?bg_img=$bg_img\">アイコン削除</a>
(アイコンログないアイコンをアイコンディレクトリから削除します)
</td></tr>
<tr><td><br></td></tr>
<tr><td>
$bkex
</td></tr>
</table>
EOM
&footer;
exit;

}
# ログ修復
sub recv{
	#open(BKUP,"$bk_dat");
	sysopen(BKUP,"$bk_dat",O_RDONLY);
	@bkup=<BKUP>;

	splice(@bkup,0,2);
	$num=0;

	foreach $bkp(@bkup){
		if($bkp eq "<$bk_up[$num]>\n"){
		#open(BKUP,">$bk_up[$num]");
		sysopen(BKUP,"$bk_up[$num]",O_WRONLY | O_TRUNC | O_CREAT );
		print BKUP @b_lines;
		close(BKUP);
		@b_lines=();
		$num=$num+1;
		}

		else{push(@b_lines,$bkp);}
	}

#if ($ENV{PERLXS} eq "PerlIS") {
#print "HTTP/1.0 302 Temporary Redirection\r\n";
#print "Content-type: text/html\n\n";}
if(!$redi){
	print "Location: $top_page\n\n";
}else{
	&header;
	print "<META HTTP-EQUIV=\"Refresh\" Content=0\;url=$top_page>";
	&footer;
}
exit;

}

# 最終レス日順並び替え
sub dt_sort{
	foreach(@lines){
	($dt_knum,$dt_num,$dt_date)=split(/<>/,$_);
	if($dt_num){$nxt_key=1;}else{$nxt=0;$nxt_key=0;next;} # next を $dt_num=$dt_knum に変えれば更新順
	if($nxt){next;}
	$dt_date =~ s/\///g; $dt_date =~ s/://g; $dt_date =~ s/\([^)]*\)//g;
	$no_sort{$dt_num}="$dt_date";
	if($nxt_key){$nxt=1;}
	}
	@dt_sort = sort{ "$no_sort{$b}" cmp "$no_sort{$a}"} (keys %no_sort);
	foreach(@dt_sort){
		foreach $ln(@lines){
		($dt_knum,$dt_num)=split(/<>/,$ln);
		if(!$dt_num){$dt_num=$dt_knum;}
		if($_ == $dt_num){push(@newlines,$ln);}
		}
	}

	foreach (@lines){
	($dt_knum,$dt_num)=split(/<>/,$_);
	if(!$dt_num){$dt_num=$dt_knum;}
		foreach $in(@dt_sort){
		if($in == $dt_num){$in_f=1;}
		}
	if(!$in_f){push(@newlines,$_);}
	$in_f=0;
	}
@lines=@newlines;
}

## ランキング表示
sub rank{

#open (RL,"$rank_log") || &error("Can't open $rank_log");
sysopen (RL,"$rank_log",O_RDONLY | O_CREAT) || &error("Can't open $rank_log");
@hd_rank = <RL>;
close(RL);

foreach $hd_rank(@hd_rank){
$hd_rank =~ s/\n//;
($name,$cnt,$cg_cnt,$bgm_cnt,$flash_cnt,$res_cnt,$pass,$la,$rest_cnt,$mcr_cnt) = split(/<>/,$hd_rank);
if($cnt){$rank{$name} = $cnt;}
$cg_rank{$name} = $cg_cnt;
$bgm_rank{$name} = $bgm_cnt;
$flash_rank{$name} = $flash_cnt;
$res_rank{$name} = $res_cnt;
$rest_rank{$name} = $rest_cnt;
$mcr_rank{$name} = $mcr_cnt;

}

@sort_rank = sort {$rank{$b} <=> $rank{$a}} keys(%rank);
foreach(@sort_rank){++$num;$all_num = $all_num + $rank{$_};}

&header;
print <<EOM;
<a name=top>[<a href=$script?cnt=no>掲示板に戻る</a>]</a>
<br>
<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>貼\り逃げだ〜び〜</SPAN></b></font><br><br>
<a name=all><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌え総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングは総合貼\りランキングです（ｗ</b></td><td align=right><a href=#cg>画像</a>　<a href=#bgm>BGM</a>　<a href=#flash>Flash</a>　<a href=#res>レス</a>　<a href=#rest>編集</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

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
$per = int((($rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
$gif_w =int($rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}

print"</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table><br>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$cg_rank{$b} <=> $cg_rank{$a}} keys(%cg_rank);
foreach(@sort_rank){if($cg_rank{$_}){++$num;$all_num = $all_num + $cg_rank{$_};}}

print <<EOM;
<a name=cg><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌え画像総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングは貼\り画像ランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#bgm>BGM</a>　<a href=#flash>Flash</a>　<a href=#res>レス</a>　<a href=#rest>編集</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $cg_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $cg_rank{$_};
$per = int((($cg_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($cg_rank{$_}){
$gif_w =int($cg_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$cg_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}

print"</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table><br>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$bgm_rank{$b} <=> $bgm_rank{$a}} keys(%bgm_rank);
foreach(@sort_rank){if($bgm_rank{$_}){++$num;$all_num = $all_num + $bgm_rank{$_};}}

print <<EOM;
<a name=bgm><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌えBGM総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングは貼\りBGMランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#cg>画像</a>　<a href=#flash>Flash</a>　<a href=#res>レス</a>　<a href=#rest>編集</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $bgm_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $bgm_rank{$_};
$per = int((($bgm_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($bgm_rank{$_}){
$gif_w =int($bgm_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$bgm_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}

print "</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table><br>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$flash_rank{$b} <=> $flash_rank{$a}} keys(%flash_rank);
foreach(@sort_rank){if($flash_rank{$_}){++$num;$all_num = $all_num + $flash_rank{$_};}}

print <<EOM;
<a name=flash><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌えFlash総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングは貼\りFlashランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#cg>画像</a>　<a href=#bgm>BGM</a>　<a href=#res>レス</a>　<a href=#rest>編集</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $flash_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $flash_rank{$_};
$per = int((($flash_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($flash_rank{$_}){
$gif_w =int($flash_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$flash_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}

print "</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table><br>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$res_rank{$b} <=> $res_rank{$a}} keys(%res_rank);
foreach(@sort_rank){if($res_rank{$_}){++$num;$all_num = $all_num + $res_rank{$_};}}

print <<EOM;
<a name=res><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌えレス総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングはレスランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#cg>画像</a>　<a href=#bgm>BGM</a>　<a href=#flash>Flash</a>　<a href=#rest>編集</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $res_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $res_rank{$_};
$per = int((($res_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($res_rank{$_}){
$gif_w =int($res_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$res_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}
print "</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$rest_rank{$b} <=> $rest_rank{$a}} keys(%rest_rank);
foreach(@sort_rank){if($rest_rank{$_}){++$num;$all_num = $all_num + $rest_rank{$_};}}

print <<EOM;
<a name=rest><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌え編集総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングは編集ランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#cg>画像</a>　<a href=#bgm>BGM</a>　<a href=#flash>Flash</a>　<a href=#res>レス</a>　<a href=#mcr>マクロ</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $res_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $rest_rank{$_};
$per = int((($rest_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($rest_rank{$_}){
$gif_w =int($rest_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$rest_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}
print "</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table>";

$ex_num = $rk = $nex_jg = $next_num = $num = $all_num = 0;

@sort_rank = sort {$mcr_rank{$b} <=> $mcr_rank{$a}} keys(%mcr_rank);
foreach(@sort_rank){if($mcr_rank{$_}){++$num;$all_num = $all_num + $mcr_rank{$_};}}

print <<EOM;
<a name=mcr><br></a>
<table width=\"80%\"><tr><td>
<font color=blue size=+1 face=\"$t_face\">現在の萌えマクロ総数 $all_num だ〜び〜参加人数 $num人</font><br><br>
<table width="100%"><tr><td><b>※このランキングはマクロ使用ランキングです（ｗ</b></td><td align=right><a href=#all>総合</a>　<a href=#cg>画像</a>　<a href=#bgm>BGM</a>　<a href=#flash>Flash</a>　<a href=#res>レス</a>　<a href=#rest>編集</a>　<a href=#top>TOPに戻る</a></td></tr></table></td></tr></table>
<table width="80%" border=1 cellspacing=0>
<tr><th>順位</th><th>お名前</th><th nowrap>萌え度</th><th>萌えぱ〜せんて〜じ</th></tr>
EOM

foreach(@sort_rank){
++$rk;
	if($nex_jg == $mcr_rank{$_}){
		if($next_num){
		$ex_num = $next_num;
		}else{
		$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
	$next_num=0;$ex_num = $rk;
	}

$nex_jg = $mcr_rank{$_};
$per = int((($mcr_rank{$_}/$all_num)*100)+0.5);
if(!$per){$per=1;}
if($mcr_rank{$_}){
$gif_w =int($mcr_rank{$_}*$g_width);if(!$gif_w){$gif_w=1;}
print"<tr><td>$ex_num</td><td><b>$_</b></td><td><b>$mcr_rank{$_}</b></td><td nowrap><img src=$icon_dir\graph.gif height=\"12\" width=\"$gif_w\"> $per\%</td></tr>";
}
}
print "</table>";
print "<table width=\"80%\"><tr><td>お名前の＠、@、☆、★以下は省略されます</td></tr></table>";
&footer;
exit;
}


# メールフォーム
sub mail{

if($in{'mail_reg'}){&mail_send;}
else{&mail_form;}

sub mail_send{
if(!$in{'name'}){$err1="お名前";}
if(!$in{'email'}){$err2="e-mail";}
if(!$in{'com'}){$err3="コメント";}
if($err1 || $err2 || $err3){&error("$err1 $err2 $err3 が未記入です");}

if($in{'email'} !~ /(\w|[\.\-\~])+@(\w|[\.\-\~])+/){&error("e-mailが不正です");}

if(!@nums && !$in{ml_ad}){&error("チェックBOXにチェックが入っていません");}

if(@nums){

#open (LOG,"$logfile");
sysopen(LOG,"$logfile",O_RDONLY);
if($lockkey == 3){flock(LOG,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
@log = <LOG>;
close(LOG);

shift(@log);

$mail_to = "";

OUT : foreach $nms(@nums){
($m_dt,$m_nm) = split (/p/,$nms);
$ck_num = 0;

	foreach(@log){
	($d1,$d2,$d3,$d4,$d5) = split (/<>/,$_);

		if($d3 eq $m_dt){
		($d5) = split(/>/,$d5);
		if(!$d5){push(@ml_err,$m_nm);next OUT;}
		if($mail_to){$mail_to = "$mail_to".","."$d5";}else{$mail_to = $d5;}
		$ck_num = 1;last;
		}

	}

if(!$ck_num){push(@ml_rtr,$m_nm);}

}

OUT2 : foreach $rtr(@ml_rtr){
$ck_num = 0;

	foreach(@log){
	($d1,$d2,$d3,$d4,$d5) = split (/<>/,$_);
	$d4 =~ s/＠.*//;
    $d4 =~ s/☆.*//;
	$d4 =~ s/@.*//;
	$d4 =~ s/★.*//;
    
		if($d4 eq $rtr){
		($d5) = split(/>/,$d5);
		if(!$d5){push(@ml_err,$rtr);next OUT2;}
		if($mail_to){$mail_to = "$mail_to".","."$d5";}else{$mail_to = $d5;}
		$ck_num = 1;last;
		}

	}

if(!$ck_num){push(@ml_err,$rtr);}

}

}

if($in{ml_ad}){if($mail_to){$mail_to = "$mail_to".","."$mailto";}else{$mail_to = $mailto;}}

if(!$mail_to){&error("対象記事が編集もしくは削除されたため送信できませんでした");}

if($in{self}){$mail_to = "$mail_to".","."$in{email}";}

if($in{mail_file}){
$fi = $in[6];
$fi =~ s/\s//g;$_ =~ s/\n//g;

if($fi =~ /(.*)name=\"mail_file\"(.*)filename=\"(.*)\"Content-Type:(.*)/){
$f_name_tmp = $3;
$c_type = $4;
}
if($f_name_tmp =~ /\\([^\\]+)$/){$f_name = $1;}

$pre_file = &base64encode($in{mail_file});

while($pre_file){
$pic_file = substr($pre_file,0,76);
$pre_file = substr($pre_file,76);
$new_file .= "$pic_file\n";
}

$file_up = "--_kugiri_\n";
$file_up .="Content-Type: $c_type;\n";
$file_up .="\tname=\"$f_name\"\n";
$file_up .="Content-Transfer-Encoding: base64\n";
$file_up .="Content-Disposition: attachment\;\n";
$file_up .="\tfilename=\"$f_name\"\n\n";
$file_up .="$new_file\n";
$file_up .="--_kugiri_--";

$mix = "Mime-Version: 1.0\n";
$mix .="Content-Type: multipart/mixed; boundary=\"_kugiri_\"\n";
$mix .="X-Mailer: Moe_Moe_Board-Mailer\n\n";
$mix .="This is a multi-part message in MIME format.\n\n";
$mix .="--_kugiri_";

}

&st_ck;

$in{'name'} = &mail64encode($in{'name'});
if($in{'title'}){$in{'title'} = &mail64encode($in{'title'});}

open(ML,"| $sendmail $mailto") || &error("sendmail失敗〜");
print ML "From: $in{'name'}<$in{email}>\n";
print ML "Bcc: $mail_to\n";
print ML "Subject: $in{'title'}\n";
	if($mix){print ML "$mix\n";
	}else{
	print ML "X-Mailer: Moe_Moe_Board-Mailer\n";
	print ML "Mime-Version: 1.0\n";
	}
print ML "Content-type:text/plain; charset=iso-2022-jp\n";
print ML "Content-Transfer-Encoding: 7bit\n\n";
print ML "$in{'com'}\n\n";
if($file_up){print ML "$file_up\n";}
close (ML);

&header;
if($f_name){$f_name = "<tr><td><b>添付ファイル：$f_name</b></td></tr>";}

if(@ml_err){
foreach(@ml_err){if($mler){$mler = "$mler".","."$_";}else{$mler = $_;}}
$mler = "<tr><td><br></td></tr><tr><td><b><font color=red>注！</font>：$mler\さんへのメー\ル送信は、対象記事が編集もしくは削除されたため送信できませんでした</b></td></tr>";
}

print <<EOM;
<font size=-2>[<a href=\"$script?cnt=no\">掲示板に戻る</a>]</font>
<center><font color=blue><B>たぶん送信されました（ｗ</B></font><br><br>
<table width="80%" bgcolor="white" border=1 cellspacing=0 bordercolor=black>
<tr><td>
<center><table width="80%">
<tr><td align=left><b>送信者：$s_in{name}&lt;$in{email}&gt;<br>
件名：$s_in{title}</b>
<hr>
$s_in{com}
</td></tr>
$f_name
$mler
</table>
</center>
</td></tr>
</table>
</center>
EOM
&footer;
exit;

}

sub mail_form{
$max_dat=int($cgi_lib'maxdata/1024);

#open(LOG,"$logfile") || &error("Can't open $logfile",'NOLOCK');
sysopen(LOG,"$logfile",O_RDONLY) || &error("Can't open $logfile",'NOLOCK');
@log = <LOG>;
close(LOG);
shift(@log);
reverse(@log);

if($in{num}){
	foreach(@log){
		($d1,$d2,$m_date,$m_name,$m_mail) = split(/<>/,$_);
		if($in{num} eq "$m_date"){
			$m_name =~ s/＠.*//;
            $m_name =~ s/☆.*//;
	        $m_name =~ s/@.*//;
	        $m_name =~ s/★.*//;
	        if($m_mail){($mail_a,$mail_e) = split(/>/,$m_mail);}
			last;
		}
	}
	if(!$mail_a){&error("対象記事がありません");}
}

if($mail_e){$in_sname = "<a href =\"mailto:$mail_a\">$m_name</a>";}else{$in_sname = "$m_name";}
if($mail_a){
$s_name = "<blockquote><b>$in_snameさんへメールを送ります</b></blockquote>";
$s_names = "<input type=hidden name=nums value=\"$in{num}\p$m_name\">";
}else{

	foreach(@log){
	($d1,$d2,$m_date,$m_name,$m_mail) = split(/<>/,$_);
	$m_name =~ s/＠.*//;
    $m_name =~ s/☆.*//;
	$m_name =~ s/@.*//;
	$m_name =~ s/★.*//;
	if($m_mail){$mail_es{$m_name} = "$m_date";}
	}

$s_names = "<b>メールを送りたい方にチェック（複数OK）をつけてください。</b><br><table><tr>";$rt = 0;

	foreach(sort keys %mail_es){
	if($rt){$rtg = $rt % 5;}
	if(!$rtg && $rt){$s_names = "$s_names"."</tr><tr>";}
	++$rt;
	$s_names = "$s_names"."<td><input type=checkbox name=nums value=\"$mail_es{$_}\p$_\">$_\さん</td>";
	}

if($rt){$rtg = $rt % 5;}
if(!$rtg){$s_names = "$s_names"."</tr><tr>";}
$s_names = "$s_names"."<td><input type=checkbox name=ml_ad value=on>管理人</td>";
$s_names = "$s_names"."</tr></table><br>";
}

&gt_ck;
&header;
print <<EOM;
<center><h3><font color=blue face="HGP創英角ﾎﾟｯﾌﾟ体">め〜るふぉ〜む</font></h3></center>
<br>
<blockquote>
<form action=$script method=POST enctype=multipart/form-data>
<input type=hidden name=mode value=mail>
<input type=hidden name=mail_reg value=on>
<input type=hidden name=bg_img value=$bg_img>
$s_name
<table>
<tr><th align=left>お名前</th><td><input type=text name=name value=\"$ck_in{'name'}\"></td><tr>
<tr><th align=left>e-mail</th><td><input type=text name=email value=\"$ck_in{'email'}\"></td><tr>
<tr><th align=left>件名</th><td><input type=text size=30 name=title></td><tr>
<tr><th align=left>添付ファイル</th><td><input type=file name=mail_file><span>　</span>なんでも $max_dat KBまで</td><tr>
<tr><th align=left colspan=2><input type=checkbox name=self value=on checked> 自分にもメールを送信する</th></tr>
</table>
<b>コメント</b><br>
<textarea name=com cols=60 rows=10></textarea>
<br><br>
$s_names
<input type=submit value="ぽちっとね（ｗ">
</form>
EOM
&footer;
exit;
}

# メール用クッキーの発行
sub st_ck{

($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$dmy) = gmtime(time + 60*24*60*60);

@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
@mons = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
$date_g = sprintf("%s, %02d\-%s\-%04d %02d:%02d:%02d GMT",$week[$wdayg],$mdayg,$mons[$mong],$yearg+1900,$hourg,$ming,$secg);

$cook="name\:$s_in{'name'}\,email\:$in{'email'}";
print "Set-Cookie: MAIL=$cook; expires=$date_g\n";

}

# メール用クッキーを取得
sub gt_ck{

@pairs = split(/;/,$ENV{'HTTP_COOKIE'});

	foreach $pair (@pairs) {
	local($name, $value) = split(/=/, $pair);
	$name =~ s/ //g;
	$ck_name{$name} = $value;
	}

@pairs = split(/,/,$ck_name{'MAIL'});

	foreach $pair (@pairs) {
	local($name, $value) = split(/:/, $pair);

	# 文字コードをEUC変換 #
	#&jcode'convert(*value,'euc');
        #Jcode::convert(*value,'euc');

	$ck_in{$name} = $value;
	}

}

# MIMEエンコード とほほさんのページから引用

sub mail64encode {
  local($xx) = $_[0];
  #&jcode'convert(*xx, "jis");
  #Jcode::convert(*xx, "jis");
  $xx = Encode::encode('iso-2022-jp-1',$xx);

  $xx =~ s/\x1b\x28\x42/\x1b\x28\x4a/g; # 不要かも
  $xx = &base64encode($xx);
  return("=?iso-2022-jp?B?$xx?=");
}

sub base64encode {
  local($base) = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               . "abcdefghijklmnopqrstuvwxyz"
               . "0123456789+/";
  local($xx, $yy, $zz, $i);
  $xx = unpack("B*", $_[0]);
  for ($i = 0; $yy = substr($xx, $i, 6); $i += 6) {
    $zz .= substr($base, ord(pack("B*", "00" . $yy)), 1);
    if (length($yy) == 2) {
      $zz .= "==";
    } elsif (length($yy) == 4) {
      $zz .= "=";
    }
  }
  return($zz);
}
}

# タグマクロ説明
sub mc_ex{
if($in{ft_ex}){
@wrs1 = ('0'..'9');
@wrs2 = ('a'..'z');
@wrs3 = ('A'..'Z');
@wrs4 = ('!','"','#','$','%','&','\'','(',')','-','=','^','~','\\','|','@','`','[','{',';','+',':','*',']','}',',','<','.','>','/','?','_');

@fs = ("webdings","wingdings");

&header;
print <<EOM;
<center>
<br><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>特殊フォント</SPAN></b></font></center><br><br>
<blockquote>
EOM

foreach $fs(@fs){
print "<center><font size=4><b>$fsフォント一覧</b></font></center>";
foreach $fsn(1 .. 4){

	if($fsn == 1){@wrs = @wrs1;}
	elsif($fsn == 2){@wrs = @wrs2;}
	elsif($fsn == 3){@wrs = @wrs3;}
	elsif($fsn == 4){@wrs = @wrs4;}

	$wrss = "<table border=1 bgcolor=\"white\"><tr style=\"font-family:$fs\" align=center>";
	foreach(@wrs){
		$wrss .= "<td><font size=+2>$_</font></td>";
	}
	$wrss .= "</tr><tr align=center>";
	foreach(@wrs){
		$wrss .= "<td>$_</td>";
	}
	$wrss .= "</tr></table>";

	print "$wrss<br><br>";
}
print "<br><br>";
}
print "</blockquote>";
&footer;
exit;
}
@tc_nm =( "うぐぅ","そんなこと言う人キライです","了承","あははー","あぅ〜","くぅ。。。","かなりキライじゃない");
srand;

$tgs=0;
foreach(@tgs1){
$tgtb = "$tgtb<tr><td nowrap>$_：<$tgs2[$tgs]>$tc_nm[int(rand(7))]</$tgs2[$tgs]></td></tr>\n";
++$tgs;
}

$tgs=0;
foreach(@itgs1){
$itgtb = "$itgtb<tr><td nowrap>$_：<img $itgs2[$tgs] src=$icon_dir\home.gif></td></tr>\n";
++$tgs;
}

if($vt_btn){
$vtex1 = "<tr><td>VT：投票ボタンです。ラジオボタン、チェックボックス等と組み合わせると簡易投票システムとなります</td></tr>";
$vtex2 = "<br>・<b>VTは親記事でのみ使用可能、書式は[VT]となります</b><br><br>";
}

$ftad=0;
foreach(@sfont1){
	$fts .= "$_（$sfont2[$ftad]） ";
	++$ftad;
}

$nog = "none.gif";

&header;
print <<EOM;
<center>
<br><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>マクロ説明</SPAN></b></font><br><br>
<table bgcolor=white><tr><td>
<pre>
投稿コメントにマクロが使用できます

・使えるタグマクロ一覧
<table width="100%">
$tgtb
$vtex1
<tr><td>F：font（s:size,c:color,f:face と併用します。<font color=red>s,c,fは小文字です</font>）</td></tr>
<tr><td>RB：文にルビが振れます</td></tr>
</table><br>
・Fの書式は
<b>Fs(サイズ1〜7)c(色名か色コード)f(ポップ体などのフォント名)</b>
フォント名は正式名の他、$ftsの短縮名で指定することもできます
<a href=\"$script?mode=mc_ex&ft_ex=on&bg_img=$bg_img\" target=_blank>webdings,wingdingsフォント一覧（Win系フォントです）</a>

・使用方法(書式)はマクロをM1,M2,M3,M4,…とすると
<b>[M1,M2,M3,M4,…:コメント]</b>

・RBの書式は
<b>[RB,M1,M2,…:コメント(色指定:ふりがな)] ( 色指定をしない場合は (ふりがな) でOK)</b>

$vtex2
・<b>/アイコンファイル名/ でアイコン表示可能です。</b><a href=\"$script?mode=image&ife=on&bg_img=$in{'bg_img'}\" target='_blank'>画像イメージ参照</a>

・使えるアイコン用マクロ一覧
<table width="100%">
$itgtb
<tr><td nowrap>IN(アイコンファイル名)：アイコンの上にマウスが来た時にINで指定したアイコンに変える</td></tr>
<tr><td nowrap>OUT(アイコンファイル名)：アイコンからマウスが離れた時にOUTで指定したアイコンに変える</td></tr>
</table><br>
・アイコン用マクロの書式は
<b>/アイコン用マクロ:アイコンファイル名/</b>（<font color=red>アイコンマクロは複数使用不可です</font>）
（アイコン用マクロのほとんどはIE用です。また、透過GIF以外だとあまり効果がないかもしれません）
<b>・使用例１</b>
[Fs(4)c(blue)f(HGP創英角ﾎﾟｯﾌﾟ体),B,I,U:うぐぅ] 

　↓
</pre>
<font size=4 color=blue face=HGP創英角ﾎﾟｯﾌﾟ体><b><i><u>うぐぅ</u></i></b></font>

<pre>
<b>・使用例２</b>
[Fs(4)c(blue)f(HGP創英角ﾎﾟｯﾌﾟ体),B,I,U:秋子さん]の[Fs(6)c(#e2de83),B,S:じゃむ]は[Fs(4)c(blue),RB:おいしい(red:命がけ)]

　↓
</pre>
<font size=4 color=blue face=HGP創英角ﾎﾟｯﾌﾟ体><b><i><u>秋子さん</u></i></b></font>の<font size=6 color=#e2de83><b><s>じゃむ</s></b></font>は<font size=4 color=blue><ruby>おいしい<rt style="color:red">命がけ</rt></ruby></font>

<pre>
<b>・使用例３</b>
/home.gif/だと動きませんが[MR:/home.gif/]だと動きます。
また/IN(none.gif),OUT(home.gif):home.gif/だとマウスの接触で画像が変化します。

　↓
</pre>
<img src=$icon_dir\home.gif>だと動きませんが<marquee direction=right><img src=$icon_dir\home.gif></marquee>だと動きます。
また<img onmouseover="this.src='$icon_dir$nog'" onmouseout="this.src='$icon_dir\home.gif'" src="$icon_dir\home.gif">だとマウスの接触で画像が変化します。

<pre>
<b>・使用例４</b>
/home.gif/ を /FH:home.gif/左右反転 /FV:home.gif/上下反転 [MR:/GR:home.gif/]赤く発光させて動かします

　↓
</pre>
<img src=$icon_dir\home.gif> を <img style="filter:fliph()" src=$icon_dir\home.gif>左右反転 <img style="filter:flipv()" src=$icon_dir\home.gif>上下反転 <marquee direction=right><img style="filter:glow(color=red)" src=$icon_dir\home.gif></marquee>赤く発光させて動かします

EOM

if($vt_btn){
print <<EOM;
<pre>
<b>・使用例５(簡易投票システム)</b>
KANONでのあなたの萌えキャラは？
[R:あゆあゆ]
[R,B:名雪]
[R,I:しおりん]
[R,U:まこぴー]
[R:舞]
[R,B:秋子さん]
その他[T:]
[VT]

　↓
</pre>
<input type=hidden name=vt value="6213">
KANONでのあなたの萌えキャラは？<br>
<com0><input type=radio name=moe_vt value="あゆあゆ">あゆあゆ</input type=radio name=moe_vt value=moe_vt></com0><br>
<com1><b><input type=radio name=moe_vt value="名雪">名雪</input type=radio name=moe_vt value=moe_vt></b></com1><br>
<com2><i><input type=radio name=moe_vt value="しおりん">しおりん</input type=radio name=moe_vt value=moe_vt></i></com2><br>
<com3><u><input type=radio name=moe_vt value="まこぴー">まこぴー</input type=radio name=moe_vt value=moe_vt></u></com3><br>
<com4><input type=radio name=moe_vt value="舞">舞</input type=radio name=moe_vt value=moe_vt></com4><br>
<com5><b><input type=radio name=moe_vt value="秋子さん">秋子さん</input type=radio name=moe_vt value=moe_vt></b></com5><br>
その他<com6><textarea rows=1 cols=25 name=moe_vt></textarea rows=1 cols=25 name=moe_vt></com6><br>
<input type=submit value="投票・見る">（サンプルなので押せません）
EOM
}

print "</td></tr></table></center>";

&footer;
exit;
}

# タグマクロ
sub tg_en{

	local($size,$color,$face);

	$tgrp = 0;
	@pcom = ();

	if($_[0] =~ /\/([^\/:]+):([\w\d]*\.\w{3})\//){

		if(!$op_ico){
			#open(IN,"$icofile") || &error("Can't open $icofile",'NOLOCK');
			sysopen(IN,"$icofile",O_RDONLY) || &error("Can't open $icofile",'NOLOCK');
			@icons = <IN>;
			close(IN);
			$op_ico = 1;
		}

		while($_[0] =~ /\/([^\/:]+):([\w\d]*\.\w{3})\//){
			$ch_css = $imcd = "";
			$imc = "$1";
			@imcs = split(/,/,$imc);
			foreach(@imcs){
				if($_ =~ /IN\((.+)\)/){$ch_css .=" onmouseover=\"this.src=\'$icon_dir$1\'\"";}

				elsif($_ =~ /OUT\((.+)\)/){$ch_css .=" onmouseout=\"this.src=\'$icon_dir$1\'\"";}
				else{$imcd = "$_";}
			}

			$cs_rp = 0;
			foreach(@itgs1){
				if($_ eq "$imcd"){$ch_css .= " $itgs2[$cs_rp]";$css_ck = 1;last;}
				++$cs_rp;
			}
			if($imcd && !$css_ck){&error("$imcdはマクロ登録されていません");}

			$_[0] =~ s/\/([^\/:]+):([\w\d]*\.\w{3})\//<img$ch_css src="$icon_dir$2">/;
			$ic_ck = 0;
			foreach(@icons){
				($d1,$d2) = split(/\t/,$_);
				if($d2 eq "$2"){$ic_ck = 1;last;}
			}
			if(!$ic_ck){&error("$2はアイコン登録されていません");}

			$mcr_use = 1;
		}

	}

	if($_[0] =~ /\/([\w\d]*\.\w{3})\//){

		if(!$op_ico){
			#open(IN,"$icofile") || &error("Can't open $icofile",'NOLOCK');
			sysopen(IN,"$icofile",O_RDONLY) || &error("Can't open $icofile",'NOLOCK');
			@icons = <IN>;
			close(IN);
			$op_ico = 1;
		}

		while($_[0] =~ s/\/([\w\d]*\.\w{3})\//<img src="$icon_dir$1">/){
			$ic_ck = 0;
			foreach(@icons){
				($d1,$d2) = split(/\t/,$_);
				if($d2 eq "$1"){$ic_ck = 1;last;}
			}
			if(!$ic_ck){&error("$1はアイコン登録されていません");}

			$mcr_use = 1;
		}

	}

	if($vt_btn){
		if($_[0] =~ s/\[VT]/$vt_btn<\/form>/){
			if($mode eq "msg" && !$in{'resno'}){$vt_num = $oya+1;}
			elsif($mode eq "Reg_usr_rest" && !$k) {$vt_num = $num;}
			else{&error("投票システムを使えるのは親記事のみです",'NOLOCK');}
			$vote = 1;
		}
	}
	
	push(@tgs1,"RB");
	push(@tgs2,"ruby");

	while($_[0] =~ s/\[([^:\]]+):([^\]]*)]/<com$tgrp>/){
		$rb_ck = $rb_cl = "";
		++$tgrp;
		@base_tgs = @tg_ex = @tg_ed = ();

		$tg_ex = $ft_ex = $size = $color = $face = "";

		$base_tgs = $1;
		$com1 = $com2 = $2;

		@base_tgs = split(/,/,$base_tgs);

		foreach(@base_tgs){
			$tgs_cn = 0;
			if($_ =~ /^F/){
				if($_ =~ /s\(([^)]+)\)/){$size = $1;}
				if($_ =~ /c\(([^)]+)\)/){$color = $1;}
				if($_ =~ /f\(([^)]+)\)/){$face = $1;}
				$sf_ad = 0;
				foreach(@sfont1){
					if($face eq "$_"){$face = "$sfont2[$sf_ad]";}
					++$sf_ad;
				}
				$ft_ex = 1;
			}
			if($_ eq "RB"){$rb_ck = 1;}
			foreach $tg(@tgs1){
				if($_ eq "$tg"){push(@tg_ex,$tgs2[$tgs_cn]);}
				++$tgs_cn;
			}
		}
		if($rb_ck){
			if($com1 =~ s/\(([^:\)]+):([^)]+)\)$/\($2\)/){$rb_cl = $1;}
			if($rb_cl){$rb_cl = " style=\"color:$rb_cl\"";}
			$com1 =~ s/\(([^)]+)\)$/<rt$rb_cl>$1<\/rt>/;
		}
		foreach(@tg_ex){
			$tg_ed = "</$_>";
			push(@tg_ed,$tg_ed);
			$_ = "<$_>";
		}

		if($ft_ex){
			if($size){$size =" size=\"$size\"";}
			if($color){$color =" color=\"$color\"";}
			if($face){$face =" face=\"$face\"";}
			unshift(@tg_ex,"<font$size$color$face>");
			unshift(@tg_ed,"</font>");
		}

		foreach(@tg_ex){
		$com1 = "$_"."$com1"."$tg_ed[$tg_ex]";
		++$tg_ex;
		}
		$com1 =~ s/value=moe_vt/value="$com2"/;
		push(@pcom,$com1);

		$mcr_use = 1;

	}

	$tgrp = 0;

	foreach(@pcom){
		$_[0] =~ s/<com$tgrp>/<com$tgrp>$_<\/com$tgrp>/;
		++$tgrp;
	}

	if($vote){$_[0] = "<form action=\"$script\" method=\"POST\" target=_blank><input type=hidden name=vt value=\"$vt_num\">$_[0]";}
	return($_[0]);

}

sub tg_de{

	local($size,$color,$face);

	$tgrp = 0;
	@pcom = ();

	$_[0] =~ s/<img src="$icon_dir([^"]+)">/\/$1\//g;

	while($_[0] =~ /<img ([^>]+) src="$icon_dir([^"]+)">/){

		$imcd = $ch_css = "";@ch_css =();
		$imcs = "$1";
		@imcs = split(/ /,$imcs);

		foreach(@imcs){
			if($_ =~ /onmouseover.+'$icon_dir(.+)'/){push(@ch_css,"IN($1)");}
			elsif($_ =~ /onmouseout.+'$icon_dir(.+)'/){push(@ch_css,"OUT($1)");}
			else{$imcd = "$_";}
		}

		$cs_rp = 0;
		foreach(@itgs2){
			if($_ eq "$imcd"){$ch_css = "$itgs1[$cs_rp]";push(@ch_css,"$ch_css");last;}
			++$cs_rp;
		}

		foreach(@ch_css){
			if(!$ch_csss){$ch_csss = "$_";}
			else{$ch_csss .= ",$_";}
		}

		$_[0] =~ s/<img ([^>]+) src="$icon_dir([^"]+)">/\/$ch_csss:$2\//;
	}

	if($_[0] =~ s/<input type=submit value="[^"]+"><\/form>/\[VT]/){
		$_[0] =~ s/<input type=hidden name=vt value="[^"]+">//;
		$_[0] =~ s/value="[^"]+"/value=moe_vt/g;
		$_[0] =~ s/<form action.+target=_blank>//;
	}else{
		$_[0] =~ s/value="[^"]+"/value=moe_vt/g;
	}

	push(@tgs1,"RB");
	push(@tgs2,"ruby");

	while($_[0] =~ s/<com$tgrp>(.+)<\/com$tgrp>/<com$tgrp>/){

		$base_aftg = $1;

		++$tgrp;

		@us_ft = ();

		$us_ft = $size = $color = $face = "";

		$base_aftg =~ s/<rt style="color:([^"]+)">(.+)<\/rt>/\($1:$2\)/;
		$base_aftg =~ s/<rt>(.+)<\/rt>/\($1\)/;

		if($base_aftg =~ s/<font([^>]+)>//){
			$tg_ck = $1;
			if($tg_ck =~ /size="([^"]+)"/){$size = $1;}
			if($tg_ck =~ /color="([^"]+)"/){$color = $1;}
			if($tg_ck =~ /face="([^"]+)"/){$face = $1;}
			if($size){$size="s($size)";}
			if($color){$color="c($color)";}
			if($face){$face="f($face)";}
			push(@us_ft,"F$size$color$face");
			$base_aftg =~ s/<\/font>//;
		}

		$tgs_cn = 0;
		foreach(@tgs2){
			if($base_aftg =~ s/<$_>//){
				$base_aftg =~ s/<\/$_>//;
				push(@us_ft,"$tgs1[$tgs_cn]");
			}
			++$tgs_cn;
		}

		foreach(@us_ft){
			if(!$us_ft){
				$us_ft = "$_";
			}else{
				$us_ft = "$us_ft,$_";
			}
		}
		$base_aftg = "[$us_ft:$base_aftg]";
		push(@pcom,$base_aftg);
	}

	$tgrp = 0;

	foreach(@pcom){
		$_[0] =~ s/<com$tgrp>/$_/;
		++$tgrp;
	}

	return($_[0]);
}

sub vote{

if($fll){
	foreach (1 .. 10) {
		unless (-e $vtlock) {last;}
		sleep(1);
	}
}
#open(VT,"$vt_dir$in{vt}\.vt");
sysopen(VT,"$vt_dir$in{vt}\.vt",O_RDONLY);
if($lockkey == 3){flock(VT,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
@vt = <VT>;
close(VT);

if(@moe_vt){
$addr = $ENV{'REMOTE_ADDR'};
	foreach(@moe_vt){
		$_ =~ s/\n//g;
		$vtc = 0;
		foreach $vt(@vt){
			($vt1,$vt2,$vt3) = split(/\t/,$vt);
			if($vt1 eq "$_"){
				$vtc = 1;
				if($vt3 ne "$addr"){
					++$vt2;
					$vt = "$vt1\t$vt2\t$addr\t\n";
				}
				last;
			}
		}
		if(!$vtc){push(@vt,"$_\t1\t$addr\t\n");}
	}

	if($fll){
		&fll("$vtlock","$vt_dir$in{vt}\.vt",@vt);
	}else{
		#open(VT, "+< $vt_dir$in{vt}\.vt") || &error("Can't open $vt_dir$in{vt}\.vt");
		sysopen(VT, "$vt_dir$in{vt}\.vt" , O_RDWR ) || &error("Can't open $vt_dir$in{vt}\.vt");
		if($lockkey == 3){flock(VT,2) || &error("filelock 失ヽ(´ー｀)ノ敗");}
		truncate(VT, 0);
		seek(VT, 0, 0);
		print VT @vt;
		close(VT);
	}
}

&header;

print "<center><font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>記事No$in{vt}の投票結果</SPAN></b></font></center><br>";
print "<center><table border=1 cellspacing=0 bordercolor=black>\n";
print "<tr><th>順位</th><th>項目</th><th>人数</th></tr>\n";
foreach(@vt){
	($vt1,$vt2) = split(/\t/,$_);
	$sort_vt{$vt1} = $vt2;
}
	
@sort_vt = sort {$sort_vt{$b} <=> $sort_vt{$a}} keys(%sort_vt);

foreach(@sort_vt){
	++$rk;
	if($nex_jg == $sort_vt{$_}){
		if($next_num){
			$ex_num = $next_num;
		}else{
			$next_num = $rk; $ex_num = --$next_num;
		}
	}else{
		$next_num=0;$ex_num = $rk;
	}

	$nex_jg = $sort_vt{$_};
print "<tr><td>$ex_num</td><td>$_</td><td>$sort_vt{$_}人</td></tr>\n";
}
print "</table></center>";
&footer;
exit;
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
	sysopen(TMP,"$tmp_1",O_WRONLY | O_TRUNC | O_CREAT ) || &error("TMPファイル書きこみ失敗ヽ(´ー｀)ノ");
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

sub swf {

&header;

print <<EOM;
<STYLE>
<!--
BODY{
  margin-top : 0px;
  margin-left : 0px;
  margin-right : 0px;
  margin-bottom : 0px;
}
-->
</STYLE>

EOM

print "<img src=$fwall></body></html>";
exit;
}

sub convert {

if (crypt($in{'pass'}, substr($password, $salt, 2) ) ne $password) {
	&error("パスワードが違います",'NOLOCK');
}

#if (!open(DATA,"$rank_log")) {	return ;	}
if (!sysopen(DATA,"$rank_log",O_RDONLY)) {	return ;	}
@LOG = <DATA>;	close(DATA);
foreach ( @LOG )	{
	chop $_ ;
	($name,$all,$cg,$bgm,$res,$pass,$la,$rest,$mcr) = split(/<>/,$_);
	push(@new,"$name<>$all<>$cg<>$bgm<>0<>$res<>$pass<>$la<>$rest<>$mcr<>\n");
}
#if ( !(open(OUT,">$rank_log")))	{	return;	}
if ( !(sysopen(OUT,"$rank_log",O_WRONLY | O_TRUNC | O_CREAT )))	{	return;	}
print OUT @new;	close(OUT);

&header;
print "<div align=center>変換終了〜</div><P><hr><P>\n";
&footer;
exit;
}

sub GetGifSize {
	local($buf) = $_[0];

	local($GIFWidth) = ord(substr($buf,6,1)) + ord(substr($buf,7,1)) * 256;
	local($GIFHeight) = ord(substr($buf,8,1)) + ord(substr($buf,9,1)) * 256;
	return $GIFWidth,$GIFHeight;
}

sub GetJpegSize {
	local($buffer) = $_[0];

	local($SOFnIdx) = 2;
	local(%SOFn) = ("\xC0", 1, "\xC1", 1, "\xC2", 1, "\xC3", 1, "\xC5", 1, 
					"\xC6", 1, "\xC7", 1, "\xC8", 1, "\xC9", 1, "\xCA", 1, 
					"\xCB", 1, "\xCD", 1, "\xCE", 1, "\xCF", 1);

	local($BufLen) = length($buffer);
	while($SOFnIdx < $BufLen){
		$c = substr($buffer, $SOFnIdx, 1); $SOFnIdx++;
		if($c eq "\xFF"){
			$c = substr($buffer, $SOFnIdx, 1); $SOFnIdx++;
			if($SOFn{$c}){
				@SIZE = unpack("CCCC", substr($buffer, $SOFnIdx + 3, 4));
				return $SIZE[2] * 256 + $SIZE[3],$SIZE[0] * 256 + $SIZE[1];
			}else{
				$c = substr($buffer, $SOFnIdx, 2);
				@JMP = unpack("CC", $c);
				$SOFnIdx += $JMP[0] * 256 + $JMP[1];
			}
		}
	}
}

sub get_png_size {
	local($buffer) = $_[0];

	local($pos, $chunk_len, $chunk_type, @w, @h, $width, $height);
	$chunk_len = 8;
	while($chunk_type ne "IHDR"){
		$pos = $chunk_len;
		$chunk_len = substr($buffer, $pos, 4);
		$pos += 4;
		$chunk_type = substr($buffer, $pos, 4);
	}

	@w = unpack("CCCC", substr($buffer, $pos + 4, 4));
	@h = unpack("CCCC", substr($buffer, $pos + 8, 4));
	$width = 0;
	$height = 0;
	$k = 3;
	foreach(0..3){
		$width += $w[$_] * (256 ** $k);
		$height += $h[$_] * (256 ** $k);
		$k--;
	}
	return $width,$height;
}

