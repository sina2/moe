#!/usr/bin/perl

# ログファイル読み込み
$logfile = "./moelog/moemoe.log";

if($ENV{'QUERY_STRING'}){
	($name, $value) = split(/=/,$ENV{'QUERY_STRING'});
	$bgm = $value;
}else{
	open(IN,"$logfile");
	@lines = <IN>;
	close(IN);
	shift(@lines);
	
	foreach $line (@lines) {
		local($num,$k,$dt,$na,$em,$sub,$com,
		$url,$host,$pw,$color,$icon,$b,$up_on,$img) = split(/<>/, $line);

		if($img =~ /bgm$/){
			$img =~ s/bgm$//;
			if($img =~ /\.$/){
				$img="$img"."bgm";
			}
			$bgm=$img;
		}elsif($img =~ /cgm$/){
			$img =~ s/\.([^.]+)\.([^.]*)cgm$//;
			$bgm = "$img.$2";
			if($bgm =~ /\.$/){$bgm="$bgm"."bgm";}
		}

		if($bgm){last;}
	}
}

if($ENV{'HTTP_USER_AGENT'} =~ /MSIE/){
	$bgm_ex="<bgsound src=$bgm loop=infinite>";
}else{
	$bgm_ex="<EMBED SRC=$bgm WIDTH=150 HEIGHT=40 AUTOSTART=true REPEAT=true LOOP=true PANEL=0>";
}



sub no_bgm{

print "Content-type: text/html\n\n";
print <<EOD;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<TITLE>NO_BGM</TITLE>
</HEAD>
<BODY>
EOD
}



print "Content-type: text/html\n\n";
print <<EOM;
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
</head>
<body>
$bgm_ex
</body></html>
<noembed>
EOM
