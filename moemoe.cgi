#!/usr/bin/perl -T

# BBSスクリプト名
$bbs_script="./Hirame_LE.cgi";

# BGM再生スクリプト名
$bgm_script="./bgsound.cgi";

## 設定ここまで ##

print "Content-type: text/html\n\n";
print <<EOM;
<html>
<head><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<title>萌え板〜</title></head>
<FRAMESET rows="*,100%" border=0 frameborder=0 framespacing=0 framecolor="#000000">
<FRAME src="$bgm_script" name="bgm">
<FRAME src="$bbs_script" name="moe_bbs">
<noframes>
<body>
フレーム未対応。。。
</body>
</noframes>
</frameset>
</html>
<noembed>
EOM
