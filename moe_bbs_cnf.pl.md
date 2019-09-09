# 設定項目
## タイトル名を指定
$title = '';

## タイトルの色
$t_color = '#FF99CC';

## タイトルの大きさ（ポイント数:スタイルシート）
$t_point = '18';

## タイトル文字のフォントタイプ
$t_face = 'HGP創英角ﾎﾟｯﾌﾟ体';

## 本文の文字大きさ（ポイント数:スタイルシート）
$pt = '10';

### 壁紙を指定する場合（http://から指定）<br> 設定しない場合最後に貼られた画像が背景になります(貼りモードONのとき)
$backgif = '';

### Flashが貼られたときの待機画面（500×500以内が妥当）
$fwall = './Icon/loading.gif';

# 背景画像設定(スタイルシート):配置パターン,固定,開始位置
## スタイルシートを使用しないで背景画像を表示したい場合は0に
$css = '0';

## repeat,repeat-x,repeat-y,no-repeat で指定
$bgrep = 'no-repeat';

## fixed,scroll で指定
$bgatc = 'fixed';

## 水平位置 垂直位置 で指定<br>値はpt,pxや相対位置(top,center,bottom,left,right)などで指定
$bg_pos = 'center 50px';

# 色を指定
## 背景色を指定
$bgcolor = '#ffffff';

## 文字色を指定
$text = '#000000';

## 文字色を指定(隠し？)
$text2 = '#ffffff';

## コメント中に「<」がある行の色を変える場合、色を指定
$inyou = '#999999';

#### リンク色を指定
## 未訪問
$link = '#0099FF';

## 訪問済
$vlink = '#0099FF';

## 訪問中
$alink = '#FF66FF';

# 管理設定
## 親記事最大記事数 (あまり多くすると危険)<br>レス記事の数は最大記事数には含まれません
$max = '100000';

## 管理者の名前（アイコン追加CGIで使用）<br>アイコンモードログイン時にこの名前と管理passで入るとアイコン管理モードになります。
$ad_name = '管理人';

## パスワード記録ファイル
$passfile = './moelog/pass.cgi';

## 返信がつくと親記事をトップへ移動(強制的に最終更新日順にする) (0=no 1=yes)
$res_sort = '1';

## ホスト名取得モード<br>0 : $ENV{'REMOTE_HOST'} で取得できる場合<br>1 : gethostbyaddr で取得できる場合
$get_remotehost = '1';

## タイトルにGIF画像を使用する時 (http://から記述) 
$title_gif = '';
## GIF画像の幅 (ピクセル)
$tg_w = '150';
##    〃    高さ (ピクセル)
$tg_h = '50';

# ファイルロック

## ファイルロック形式<br>0=no 3=flock関数 4=カウンタロックのみ
$lockkey = '4';

## ハードリンク＆リネームによるカウンタファイルロック(する:1 しない:0) winプラットフォームでは不可
$fll = '0';

## ログのパーミッション
$vt_pm = '0606';

## ロックファイル名
$lockfile = './moelog/yybbs.lock';

## カウンタのロックファイル
$cntlock = './moelog/yycnt.lock';

## 投票ロックファイル
$vtlock = './vt.lock';

## ランキングロックファイル
$rklock = './moelog/rank.lock';

## アイコンロックファイル
$icolock = './moelog/ico.lock';

## アイコンランキングロックファイル
$irklock = './moelog/irank.lock';

## ミニカウンタの設置<br>0=no 1=テキスト 2=GIF画像
$counter = '1';

## ミニカウンタの桁数
$mini_fig = '5';

## テキストのとき：ミニカウンタの色
$cnt_color = '#4169e1';

## ＧＩＦのとき：画像までのディレクトリ
$gif_path = '.';

## 画像の横サイズ
$mini_w = '8';

## 画像の縦サイズ
$mini_h = '12';

## カウンタファイル
$cntfile = './moelog/count.dat';

## カウンタのミラーリングする(0=no 1=yes)
$cnt_ml = '0';

## カウンタミラーファイル
$cntfile2 = './moelog/count2.dat';

## タグの許可 (0=no 1=yes)
$tagkey = '1';

# マクロ
## マクロ使用 (0=no 1=yes)
$tg_mc = '1';


## マクロの種類（font以外）<br>マクロ名。大文字のほうが無難。
@tgs1 = ('B','I','U','S','H','Q','T','R','C','CN','RT','M','M2','MR','MR2','MA','MA2','BL');
## 上記マクロに対応するタグ
@tgs2 = ('b','i','u','s','span style="cursor:hand"','span style=";cursor:help"','textarea rows=1 cols=25 name=moe_vt','input type=radio name=moe_vt value=moe_vt','input type=checkbox name=moe_vt value=moe_vt','div align=center','div align=right','marquee','marquee scrollamount=12','marquee direction=right','marquee direction=right scrollamount=12','marquee behavior=alternate','marquee behavior=alternate scrollamount=12','blink');

## 短縮フォント名
@sfont1 = ('PO','ME','W1','W2');
## 上記対応実体
@sfont2 = ('HGP創英角ﾎﾟｯﾌﾟ体','MS P明朝','webdings','wingdings');

## イメージ用マクロの種類
@itgs1 = ('DS','SD','GR','GG','GB','BL','XR','GY','IN','FH','FV');
## 上記対応実体
@itgs2 = ('style="filter:dropshadow()"','','style="filter:shadow()"','','style="filter:glow(color=red)"','','style="filter:glow(color=green)"','','style="filter:glow(color=blue)"','','style="filter:blur()"','','style="filter:xray()"','','style="filter:gray()"','','style="filter:invert()"','','style="filter:fliph()"','','style="filter:flipv()"');

## 投票ボタン（投票システムを使いたくない場合は未記入で $vt_btn = '';）
$vt_btn = '<input type=submit value="投票・見る">';

## 投票ログディレクトリ
$vt_dir = './vt_dir/';

# 動作系設定
## HTML出力をする (0=no 1=yes)
$html_on = '0';

## HTML出力時の外部カウンタソース指定（SSIやレンタルカウンタなどで別途用意）<br> &lt;!--#exec cmd="./aaa.pl"&gt; などと指定。詳しくは使用するカウンタの説明参照。
$count_src = '';

## HTML出力時のページ作成ディレクトリ
$html_dir = '';

## スクリプトのファイル名
$script = 'Hirame_LE.cgi';

## 「ホームへ戻る」のURL (相対パスやフルパスで)
$homepage_back = '';

## 掲示板のTOPのURL (通常は $script か ./page1.html で)
$homepage = "$script";

## フレーム定義HTML 新規投稿時の飛び先にも使用
$top_page = 'moemoe.html';

## ログファイルを指定<br> フルパスで指定する場合は / から記述
$logfile = './moelog/moemoe.log';

## 記事の [タイトル] 部の色
$sub_color = '#FF33CC';

## 記事の [タイトル] 部の色(隠し？)
$sub_color2 = '#9eb6f0';

## 記事表示部の下地の色
$tbl_color = '#FFFFFF';

## 記事表示部の下地の色(隠し？)
$tbl_color2 = '#000000';

## 家アイコンの使用 (0=no 1=yes)
$home_icon = '1';
## ファイル名
$home_gif = 'home.gif';
## 画像の横サイズ
$home_wid = '25';
##   〃  縦サイズ
$home_hei = '22';

## methodの形式 (POST/GET)
$method = 'POST';

## １ページ当たりの記事表示数 (親記事)
$pagelog = '10';

## メールフォーム機能を使う (0=no 1=yes)<br>sendmail必須
$mlfm = '0';

## 投稿があるとメール通知する (0=no 1=yes)<br>sendmail必須
$mailing = '0';

## 管理人メールアドレス
$mailto = '';

## sendmailパス（メールフォームで必要）
$sendmail = '/usr/sbin/sendmail';

## 自分の投稿記事はメール通知する (0=no 1=yes)
$mail_me = '0';

## 他サイトから投稿排除時に指定 (http://から書く)
$base_url = '';

## 文字色の設定。
@COLORS = ('800000','DF0000','008040','0000FF','C100C1','FF80C0','FF8040','000080','e9e2a2','9feabb','f6a091','c150d5','637ac0','b1b36e','917da4','d44d6f','8a9e83','ffffff','9400D3','0000CD','FF0099','FF00FF','DF0000','20B2AA','6495ED','FF80C0','FF9900','000000','B22222','008B8B','FFD700','6A5ACD','D2691E','c1642E');

## 投稿フォーム改行形式 (soft=手動 hard=強制)
$wrap = 'soft';

## URLの自動リンク (0=no 1=yes)<br>タグ許可の場合は no とすること。
$auto_link = '0';

## クッキー名、クッキーの処理に必要
$COOKIE_name = 'MOE_BBS';

## タグ広告挿入オプション上部 (FreeWebなど）
$banner1 = '<!--上部-->';

## タグ広告挿入オプション下部 (FreeWebなど）
$banner2 = '<!--下部-->';

## 過去ログ生成 (0=no 1=yes)
$pastkey = '0';

## 過去ログ用NOファイル
$nofile = './moelog/pastno.dat';

## 過去ログのディレクトリ
$past_dir = './past_log/';

## 過去ログ行数
$log_line = '1500';

## 過去ログ管理ファイル
$past_log = './past_log.cgi';

## ランダム文字列精製用ストリングテーブル
$st_table = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890';

# バックアップ関連
## バックアップファイル名
$bk_dat = './moelog/moe_bk_up.zip';

## バックアップログパーミッション(鍵かけ時に使用)<br>(調子が悪かったら 0606 or 0666 で)
$bk_pm = '0606';

## バックアップしたいログ
@bk_up = ('./moelog/count.dat','./moelog/icon.lst','./moelog/rank.log','./moelog/icon_rank.log','./moelog/moemoe.log','./moelog/sum_up.log');

# おぷしょんこ〜な〜

## レス時にも画像を貼りつけをする
$res_up = '0';

## 揚げ板機能 (0=no 1=yes)
$UP_Pl = '0';

## ダウンロード集計CGI
$sum_up_script = './sum_up.cgi';

## 集計ログ
$sum_up_log = "./moelog/sum_up.log";

## WEB上設定更新モード (0=no 1=yes)
$web_mode = '1';

## WEB上設定CGI
$webedit = './moe_bbs_adm.cgi';

## アイコンモード (0=no 1=yes)
$icon_mode = '1';

## アイコン管理CGI
$iconCGI = './Icons_Edit.cgi';

## アイコン画像をアップするディレクトリ
$icon_dir = './Icon/';

## 画像がうまく表示されない場合に表示用ディレクトリをフルパス記入。
$icon_dir2 = '';

## アイコン設定ファイル
$icofile = './moelog/icon.lst';

## アイコンひとつあたりの登録受理最大サイズ (bytes)<br> 1KB=1024B
$ico_max = "204800";

## 一度に登録可能なアイコン数
$ico_rv_num = '50';

## 管理者専用アイコン機能 (0=no 1=yes)
$my_icon = '0';

## 管理者専用アイコンの「ファイル名」を指定
$my_gif = '';

## アイコン五十音順並び替え (0=no 1=yes)
$nm_st = '0';

## ランダム時の専用アイコン使用許可 (0=no 1=yes)
$rd_pri = '1';

## 画像貼りモード (0=no 1=yes)
$hari_mode = '1';

## BGM貼りモード (0=no 1=yes)
$bgm_up = '1';

## デフォルトでBGM再生する(0=no 1=yes)
$bgm_play = '0';

## Flash貼りモード (0=no 1=yes)
$flash_mode = '1';

## 貼り画像・BGMをアップするディレクトリ
$ImgDir = './img/';

## 画像がうまく表示されない場合に表示用貼り画像・BGMディレクトリをフルパスで
$ImgDir2 = '';

## 貼り投稿受理最大サイズ (bytes)<br>1KB=1024B
$maxdata = '102400000';

## 貼りランキングファイル
$rank_log = './moelog/rank.log';

## アイコン使用ランキングファイル
$i_rank_log = './moelog/icon_rank.log';

## 指定したサイズ以上の画像を貼った場合にサムネイルを表示する
$samnail = '0';

## その時の横幅
$sam_wid = '640';

## その時の縦幅
$sam_hei = '480';

## ランキンググラフの1萌えあたりの長さ(ピクセルで指定)
$g_width = '0.5';

## ポップアップ広告消し (0=no 1=yes)
$nobanner = '1';

## pass認証機能 (0=no 1=yes)
$pass_mode = '0';

## Locationがうまく行かない場合（新規投稿時に自動的にTOPに戻らない）<br>HTMLのリダイレクションでTOPに飛ばします。(0=no 1=yes)
$redi = '0';

# 各種制限設定

### 各種制限の使用方法(3:エラー実行・ログ保存 2:エラー実行・ログ未保存 1:エラー未実行・ログ保存 0:使わない)
$rf_etc = '3';

## エラーログ保存ディレクトリ（エラーログを保存する場合）
$log_dir = './err_log/';

## エラー種類 メッセージ表示:0 他URL飛ばし:1
$err_sort = '0';

## 他URL飛ばしの場合の飛ばし先URL
$ex_url = "_not_found";

## リファはじきを(1:使う 0:使わない)
$ref_rf = '0';

### 呼び出し許可URL
@call_bbs = ();

### 呼び出し不可IP、ホスト名、名前は条件に一部でもマッチしたら呼び出せません。
@rf_ip = ();

### 呼び出し不可ホスト名 
@rf_host = ();

### 書きこみ不可名前
@rf_name = ();

### 要クッキー(yes:1 no:0) クッキーをONにしていないと板に入れなくします<br>これはエラーログには保存されません
$ck_use = '0';

### 表示をGZIP圧縮 (yes:1)
$gzip = '0';

#### SYSTEM
$adminPass = '';
$reload = 'moemoe.hcgi';
