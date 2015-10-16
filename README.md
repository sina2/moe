
はるか昔，CGIがPerl全盛期のころ，萌え板というCGIが流行っていました。

時代は流れ，すでに作者のえうのすさん，R七瀬さん，月読さんのサイトは電子の塵になってしまい，
このまま無くなってしまうのも心残りなので，手元のソースを github に登録してみました。


動作環境

・Centos6.7 + perl5.10.1 + Encode.pm で動作しています。

・Perl のパスは /usr/bin/perl に統一しています。

・cgi-lib.plは一緒に配布してます。


主な変更点

・UTF-8に対応させてみました。

  と言ってもjcode.pl →　Jode.pm → Encode.pm と機械的に置換しただけです。


インストール

  $ cd public_html
  
  $ git clone https://(ユーザー名)@github.com/sina2/moe.git
  
  $ cd moe
  
  $ mv moe_bbs_cnf.pl.org moe_bbs_cnf.pl
  
  $ chmod 755 *.cgi
  
  このあとアクセスすると初期画面になります（多分）


今後

・不明

