$html_write = 1;
## ---HTML作成
sub html_ex {

	# フォーム長を調整
	&get_agent;

	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile",'NOLOCK');
	@lines = <LOG>;
	close(LOG);

	# 記事番号をカット
	shift(@lines);
	
	# 親記事のみの配列データを作成
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$dt,$na,$em,$sub,$com,
			$url,$host,$pw,$color,$icon,$b,$up_on,$ImgFile) = split(/<>/, $line);

		# 親記事を集約
		if ($k eq "") { push(@new,$line); }
	if($ImgFile && ($ImgFile !~ /bgm$/) && ($ImgFile !~ /cgm$/) && !$bg_img){$bg_img=$ImgFile;}
	elsif($ImgFile && ($ImgFile =~ /cgm$/) && !$bg_img){$ImgFile =~ s/\.([^.]*)cgm$//;$bg_img=$ImgFile;}

	}

	# レス記事はレス順につけるため配列を逆順にする
	@lines = reverse(@lines);

	# カウンタ処理
	#if ($counter) { &counter; }

	# タイトル部

	if ($title_gif eq '') {
		$ti_gif="<font color=\"$t_color\" size=6 face=\"$t_face\"><b><SPAN>$title</SPAN></b></font>";
	}
	else {
		$ti_gif="<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\">";
	}

	# 過去ログのリンク部を表示
	if ($pastkey) {
		$past_mode="[<a href=\"$past_log\">過去ログ</a>]";
	}
if($hari_mode){
if($bgm_up){$bgm_tk="・BGM";}
$hari_ex="[<a href=\"$script?new_topic=gazou&bg_img=$bg_img$ds_on\"><B>画像$bgm_tk貼\り付け記事投稿</B></a>]";
}
if($icon_mode){$imd="[<a href=\"$iconCGI?bg_img=$bg_img\">アイコンこ〜な〜</a>][<a href=\"$iconCGI?bg_img=$bg_img&rank=on\">アイコンらんきんぐ</a>]";}
if ($UP_Pl) {$up_mode="[<a href='$sum_up_script' target=_blank>ＤＬ集計</a>]"; }
if($bgm_up){$bgm_tk="・BGM貼\り付け";}
if($mode eq "all_log"){$all_log = "&mode=all_log";}

$dt_sort="[<a href='$script?dt_sort=on&bg_img=$bg_img&cnt=no$all_log'>最終レス日順</a>]";

$rev_sort = "[<a href='$script?rev_sort=on&bg_img=$bg_img&cnt=no$all_log'>旧記事順</a>]";

if($hari_mode || $bgm_up){$hn_db = "[<a href=\"$script?bg_img=$bg_img&rank=on\">貼\り逃げだ〜び〜</a>]";}
$alg = "[<a href=\"$script?mode=all_log&bg_img=$bg_img&cnt=no$dt_log\">全記事表\示</a>]";
if($pass_mode){$pm_ex = "[<a href=\"$script?mode=pass_rest&bg_img=$bg_img\">認証pass変更</a>]";}
if($tg_mc){$tg_mc2 = "[<a href=\"$script?mode=mc_ex&bg_img=$bg_img\" target=_blank>マクロ説明</a>]";}
if($tg_mc && $vt_btn){
	$vt_mc = "[<a href=\"$script?vt_all=on\">投票記事一覧</a>]";
}
if($mlfm){$ml_tmn = "[<a href=\"$script?mode=mail&bg_img=$bg_img\">め〜るふぉ〜む</a>]";}
$html_top = <<"EOM";
<center>$banner1<P>
$ti_gif
<hr width=\"90%\" size=2>
[<a href=\"$homepage_back\" target=_parent>ホームにもどる</a>]
[<a href=\"$homepage\">トップにもどる</a>]
[<a href=\"$script?mode=howto&bg_img=$bg_img\">掲示板の使い方</a>]
[<a href="$script?new_topic=new&bg_img=$bg_img$ds_on"><B>新規$bgm_tk記事投稿</B></a>]
$hari_ex
$tg_mc2
[<a href=\"$script?mode=rest&bg_img=$bg_img$ds_on\">記事編集</a>]
[<a href="$script?mode=msg_del&bg_img=$bg_img">記事削除</a>]
$pm_ex
$imd
$hn_db
$past_mode
[<a href=\"$script?mode=find&bg_img=$bg_img\">ワード検索</a>]
[<a href="$script?mode=admin&bg_img=$bg_img$ds_on">管理用</a>]
$ml_tmn
$vt_mc
$up_mode
$alg
$dt_sort
$rev_sort
<hr width="90%" size=2></center>
EOM

$page = 0;
$page_cnt = 0;
$html_next = 1;
while($html_next){
	$html_ex = "";
	&kiji_edit;
}

sub kiji_edit {

	# 記事数を取得
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }
	foreach ($page .. $page_end) {
		($number,$k,$date,$name,$email,$sub,
			$comment,$url,$host,$pwd,$color,$icon,$tbl,$up_on,$ImgFile,$pixel) = split(/<>/, $new[$_]);

		$pic_ex="";

		($email,$mail_ex) = split(/>/,$email);

		$sname = $name;$sname =~ s/＠.*//;

		if(!$mlfm){
			if($email){$name="<a href=\"mailto:$email\">$name</a>"}
		}else{

			if ($email && $mail_ex) { $name = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$date\">$name</a>"; }

			elsif ($email) { $name = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$date\">$name</a>"; }
		}

		# URL表示
		if ($url && $home_icon) {
			$url = "<a href=\"http://$url\" target='_top'><img src=\"$icon_dir$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\" alt='HomePage'></a>";
		} elsif ($url && !$home_icon) {
			$url = "&lt;<a href=\"http://$url\" target='_top'>HOME</a>&gt;";
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
<td><form action=\"$sum_up_script\" method=\"$method\" target='_blank'>
<input type=hidden name=sumu_up value=\"$date\">
<input type=submit value=\"いただく♪\"></td></form>
EOM
		}else{$up_html="";}

		if ($icon ne "") {$icon_html="<td><img src=\"$icon_dir$icon\"></td>\n"; }
		else{$icon_html="<td width=37>　</td>\n"; }
		if($ImgFile =~ /bgm$/){
		$ImgFile =~ s/bgm$//;if($ImgFile =~ /\.$/){$ImgFile="$ImgFile"."bgm";}	
		$bgm="<b>BGM</b> <a style=text-decoration:none href=$ImgFile target=_blank>DL
		</a>/<a style=text-decoration:none href=./bgsound.cgi?bgm=$ImgFile target=bgm>変更</a>";
		}

		elsif($ImgFile =~ /cgm$/){
		$ImgFile =~ s/\.([^.]+)\.([^.]*)cgm$//;
		$pic = "$ImgFile.$1";$bgm = "$ImgFile.$2";if($bgm =~ /\.$/){$bgm="$bgm"."bgm";}
		$bgm="<b>BGM</b> <a style=text-decoration:none href=$bgm target=_blank>DL
		</a>/<a style=text-decoration:none href=./bgsound.cgi?bgm=$bgm target=bgm>変更</a>";

		$icon_html="<td>　</td>\n";
		$pic_ex = "<img src=\"$pic\"><br><br>\n";
		}

		elsif(defined($ImgFile) && ($ImgFile ne "")){
		$icon_html="<td>　</td>\n";
		$pic_ex = "<img src=\"$ImgFile\"><br><br>\n";
		}

		# 自動リンク
		if ($auto_link) { 
$comment =~ s/<br>/\r/g;
&auto_link($comment);
$comment =~ s/\r/<br>/g;
		}

$page_html= <<"EOM";
<center><TABLE border=1 width='95%' cellpadding=5 cellspacing=0 bgcolor=\"$tbl_color1\">
<TR><TD>
<table border=0 cellspacing=0 cellpadding=0><tr>
<td valign=top><font color=$text1>[<b>$number</b>] <font color=$sub_color1><b>$sub</b></font>
投稿者：<font color=\"$link\"><b>$name</b></font>
<small>投稿日：$date</small> <small>$bgm</small> <font face=\"Arial,verdana\">&nbsp; $url</font></td>
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

## ここまで$page_html 出力

$res_ex = "";
## レスメッセージを表示
		foreach $line (@lines) {
		  ($rnum,$rk,$rd,$rname,$rem,$rsub,
			$rcom,$rurl,$rho,$rp,$rc,$ri,$rb,$rup) = split(/<>/,$line);

			($rem,$mail_ex) = split(/>/,$rem);

			$sname = $rname;$sname =~ s/＠.*//;

			if(!$mlfm){
				if($rem){$rname="<a href=\"mailto:$rem\">$rname</a>"}
			}else{

				if ($rem && $mail_ex) { $rname = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$rd\">$rname</a>"; }

				elsif ($rem) { $rname = "<a href=\"$script?mode=mail&bg_img=$bg_img&num=$rd\">$rname</a>"; }

			}

		  if ($number eq "$rk") {

			$res_ex .= "<hr width='85%' size=1 noshade>\n";
			$res_ex .= "<table cellspacing=0 cellpadding=0 border=0><tr><td width=37>　</td>\n";

			if ($ri ne "") {
				$res_ex .= "<td><img src=\"$icon_dir$ri\"></td><td><font face=\"Arial,verdana\">&nbsp;&nbsp;</font></td>\n";
			} else {
				$res_ex .= "<td width=35>　</td><td><font face=\"Arial,verdana\">&nbsp;&nbsp;</font></td>\n";
			}

			$res_ex .= "<td><font color=$text1><font color=\"$sub_color1\"><b>$rsub</b></font> ";
			$res_ex .= "投稿者：<font color=\"$link\"><b>$rname</b></font> - ";
			$res_ex .= "<small>$rd</small> ";

			# URL表示
			if ($rurl && !$home_icon) {
				$res_ex .= "&lt;<a href=\"http://$rurl\" target='_top'>HOME</a>&gt;";
			} elsif ($rurl && $home_icon) {
				$res_ex .= "<a href=\"http://$rurl\" target='_top'><img src=\"$icon_dir$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\" alt=\"HomePage\"></a>";
			}

			# 自動リンク
			if ($auto_link) { 
$rcom =~ s/<br>/\r/g;
&auto_link($rcom);
$rcom =~ s/\r/<br>/g;
			}

			$res_ex .= "<br><font color=\"$rc\">$rcom</font></font></td>\n";

		# 提供品表示
		if  ($rup eq 'up_exist'){
		$res_ex .= "<td><form action=\"$sum_up_script\" method=\"$method\" target='_blank'>\n";
		$res_ex .= "<input type=hidden name=sumu_up value=\"$rd\">\n";
		$res_ex .= "<input type=submit value=\"いただく♪\"></td></form>";
		}

		$res_ex .= "</tr></table>\n";
		  }
		}
		$res_ex .= "</TD></TR></TABLE><P>\n";
		$html_ex .="$page_html$res_ex";

	}
	$html_ex .= "<table border=0><tr>\n";


	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
		$html_ex .= "<td><a href=\"./page$page_cnt\.html\"><b>前の$pagelog件</b></a>　</td>\n";
	}

	# 次頁処理
	if ($page_end ne "$end_data") {
		$tmp_pg = $page_cnt + 2;
		$html_ex .= "<td>　<a href=\"./page$tmp_pg\.html\"><b>次の$pagelog件</b></a></td>\n";
	}else{
		$html_next = 0;
	}
	$page += $pagelog;

	$html_ex .= "</tr></table><P>\n";

	# ヘッダ・フッターを出力
	&header;
	&footer;

	++$page_cnt;

	$html_ex = "$header"."$html_top"."$html_ex"."$footer";

	open(HTML,">$html_dir\page$page_cnt\.html");
	print HTML "$html_ex";
	close(HTML);
}

	open(IN,"$logfile");
	@lines = <IN>;
	close(IN);

	shift(@lines);

	foreach $line (@lines) {
	local($num,$k,$dt,$na,$em,$sub,$com,
	$url,$host,$pw,$color,$icon,$b,$up_on,$img) = split(/<>/, $line);

	if($img =~ /bgm$/){$img =~ s/bgm$//;if($img =~ /\.$/){$img="$img"."bgm";}$bgm=$img;}
	elsif($img =~ /cgm$/){
	$img =~ s/\.([^.]+)\.([^.]*)cgm$//;
	$bgm = "$img.$2";
	if($bgm =~ /\.$/){$bgm="$bgm"."bgm";}
	}

	if($bgm){last;}
	}

$bgm_html = <<"EOM";
<html>
<head><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<SCRIPT LANGUAGE="JavaScript">
<!--
function nnbgm(){
	usr=navigator.userAgent;
	if(usr.indexOf("MSIE")<0){
		bgm.innerHTML='<EMBED SRC=$bgm WIDTH=150 HEIGHT=40 AUTOSTART=true REPEAT=true LOOP=true PANEL=0>';
	}
}
//-->
</SCRIPT>
</head>
<body>
<span id="bgm"><bgsound src=$bgm loop=infinite></span>
</body></html>
<noembed>
EOM
	$bgm_write = "$html_dir"."bgm\.html";
	open(BGM,">$bgm_write");
	print BGM "$bgm_html";
	close(BGM);
}

1;
