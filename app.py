# coding: utf-8
from flask import Flask, render_template, request, Markup
import sqlite3
import datetime
from operator import itemgetter
import MeCab
import urllib.parse
import math

app = Flask(__name__)

@app.route('/')
def hello():
    dbname = "Nogizaka_matome_ar.db"

    # db接続
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    #記事のデータを取得
    select_sql = "select ar_tbl.title, ar_tbl.hour, ar_tbl.minute, ar_tbl.url, ar_tbl.site, site_tbl.site_url from ar_tbl inner join site_tbl on ar_tbl.site=site_tbl.site order by ar_tbl.time desc limit 30"
    c.execute(select_sql)
    ar_list = c.fetchall()

    # 注目メンバー上位10名を取得
    date = datetime.date.today() #カウントする日にちを取得(今日)
    select_sql="select * from count_tbl where count_time=? order by count3 desc limit 10"
    ranking_list=[]
    ranking=1
    for ranking_data in c.execute(select_sql,[date]):
        ranking_list.append([ranking,ranking_data[0],ranking_data[1],ranking_data[2]])
        ranking=ranking+1

    #注目メンバー上位5名のポイントの動きを取得
    count_list=[] #[["西野七瀬","2019-09-09","10"],[],,,]
    i=1
    for count_name in ranking_list:
        if i==6:
            break
        select_sql="select * from count_tbl where member_name like '%'||?||'%' and datetime('now', '-5 days','9 hours') < count_time order by count_time"
        for count_data in c.execute(select_sql, [count_name[1]]):
            count_list.append([count_data[0],count_data[1],count_data[2]])
        i=i+1

    # グラフ用の日付を取得
    date_list = [] #["2019-09-05","2019-09-06",,,]
    select_sql = "select count_time from count_tbl where member_name like '%西野七瀬%' and datetime('now', '-5 days','9 hours') < count_time order by count_time"
    for date in c.execute(select_sql):
        date_list.append(date[0])

    #注目ワードを取得
    stop_words = ["乃木坂46","乃木坂", "46", "与田", "祐希", "中元", "日芽香", "中村", "麗乃", "中田", "花奈", "久保", "史緒里", "井上", "小百合", "伊藤", "かりん",
                  "伊藤", "万理華", "伊藤", "寧々", "伊藤", "理々杏",
                  "伊藤", "純奈", "佐々木", "琴子", "佐藤", "楓", "北川", "悠理", "北野", "日奈子", "吉本", "彩華", "吉田", "綾乃", "クリスティー", "向井",
                  "葉月", "和田", "まあや", "堀", "未央奈", "大和", "里菜",
                  "大園", "桃子", "安藤", "美雲", "宮澤", "成良", "寺田", "蘭世", "山下", "美月", "山崎", "怜奈","山本", "穂乃香", "岩本", "蓮加", "岩瀬",
                  "佑美子", "川後", "陽菜", "川村", "真洋", "市來", "玲奈",
                  "掛橋", "沙耶香", "斉藤", "優里", "斎藤", "ちはる", "新内", "眞衣", "早川", "聖来", "星野", "みなみ", "松井", "玲奈", "松村", "沙友理",
                  "柏", "幸奈", "柴田", "柚菜", "桜井", "玲香", "梅澤", "美波",
                  "樋口", "日奈", "橋本", "奈々未", "永島", "聖羅", "深川", "麻衣", "清宮", "レイ", "渡辺", "みり愛", "生田", "絵梨花", "生駒", "里奈",
                  "田村", "真佑", "畠中", "清羅", "白石", "麻衣", "相楽", "伊織",
                  "矢久保", "美緒", "矢田", "里沙子", "秋元", "真夏", "筒井", "あやめ", "米徳", "京花", "能條", "愛未", "若月", "佑美", "衛藤", "美彩",
                  "西川", "七海", "西野", "七瀬", "賀喜", "遥香", "遠藤", "さくら",
                  "金川", "紗耶", "鈴木", "絢音", "阪口", "珠美", "高山", "一実", "齋藤", "飛鳥","ちゃん","さん","wwwwww","ｗｗｗｗｗｗ","中","∀","ﾟ",
                  "与田祐希","中元日芽香","中村麗乃","中田花奈","久保史緒里","井上小百合","伊藤かりん","伊藤万理華","伊藤寧々","伊藤理々杏","伊藤純奈",
                  "佐々木琴子","佐藤楓","北川悠理","北野日奈子","吉本彩華","吉田綾乃クリスティー","向井葉月","和田まあや","堀未央奈","大和里菜","大園桃子",
                  "安藤美雲","宮澤成良","寺田蘭世","山下美月","山崎怜奈","山本穂乃香","岩本蓮加","岩瀬佑美子","川後陽菜","川村真洋","市來玲奈","掛橋沙耶香",
                  "斉藤優里","斎藤ちはる","新内眞衣","早川聖来","星野みなみ","松井玲奈","松村沙友理","柏幸奈","柴田柚菜","桜井玲香","梅澤美波","樋口日奈",
                  "橋本奈々未","永島聖羅","深川麻衣","清宮レイ","渡辺みり愛","生田絵梨花","生駒里奈","田村真佑","畠中清羅","白石麻衣","相楽伊織","矢久保美緒",
                  "矢田里沙子","秋元真夏","筒井あやめ","米徳京花","能條愛未","若月佑美","衛藤美彩","西川七海","西野七瀬","賀喜遥香","遠藤さくら","金川紗耶",
                  "鈴木絢音","阪口珠美","高山一実","齋藤飛鳥",] #ストップワード

    tagger = MeCab.Tagger(r" -d C:\Users\Hideki\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20180723")

    # 記事を取得→固有名詞取得
    select_sql = "select title from ar_tbl where datetime('now', '-3 days','9 hours') < time"
    word_list = []  # ["乃木坂","ライブ",,,]
    for row in c.execute(select_sql):
        node = tagger.parseToNode(row[0])  # 形態素解析
        target_parts_of_speech = ('固有名詞')
        while node:
            if node.feature.split(',')[1] in target_parts_of_speech:  # 固有名詞の時
                word_list.append(node.surface)
            node = node.next

    # ストップワードを削除
    for stop_word in stop_words:
        while stop_word in word_list:
            word_list.remove(stop_word)

    #カウントリストを作成
    word_count_list = []  # [["乃木坂",2],["ライブ",3],,,]
    for word in word_list:
        count = word_list.count(word)
        word_count_list.append([word, count])

    # 重複を削除
    seen = []
    word_count_list = [x for x in word_count_list if x not in seen and not seen.append(x)]
    word_count_list.sort(key=itemgetter(1), reverse=True)

    # 接続を閉じる
    conn.close()

    return render_template('main.html', ar_list = ar_list, ranking_list = ranking_list, date_list = date_list, count_list = count_list, word_count_list = word_count_list[0:100])

@app.route('/member/<name>/<page>')
def member(name,page):
    dbname = "Nogizaka_matome_ar.db"

    # pageの記事番号を取得
    page_number_start = (int(page) - 1) * 15
    page_number_end = int(page) * 15

    # db接続
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # 記事のデータを取得
    select_sql = "select ar_tbl.title, ar_tbl.hour, ar_tbl.minute, ar_tbl.url, ar_tbl.site, site_tbl.site_url, ar_tbl.month, ar_tbl.day from ar_tbl inner join site_tbl on ar_tbl.site=site_tbl.site where ar_tbl.tags like '%'||?||'%' order by ar_tbl.time desc"
    c.execute(select_sql,[name])
    ar_list = c.fetchall()

    # 注目ワードを取得
    stop_words = ["乃木坂46", "乃木坂", "46", "与田", "祐希", "中元", "日芽香", "中村", "麗乃", "中田", "花奈", "久保", "史緒里", "井上", "小百合", "伊藤",
                  "かりん",
                  "伊藤", "万理華", "伊藤", "寧々", "伊藤", "理々杏",
                  "伊藤", "純奈", "佐々木", "琴子", "佐藤", "楓", "北川", "悠理", "北野", "日奈子", "吉本", "彩華", "吉田", "綾乃", "クリスティー", "向井",
                  "葉月", "和田", "まあや", "堀", "未央奈", "大和", "里菜",
                  "大園", "桃子", "安藤", "美雲", "宮澤", "成良", "寺田", "蘭世", "山下", "美月", "山崎", "怜奈", "山本", "穂乃香", "岩本", "蓮加", "岩瀬",
                  "佑美子", "川後", "陽菜", "川村", "真洋", "市來", "玲奈",
                  "掛橋", "沙耶香", "斉藤", "優里", "斎藤", "ちはる", "新内", "眞衣", "早川", "聖来", "星野", "みなみ", "松井", "玲奈", "松村", "沙友理",
                  "柏", "幸奈", "柴田", "柚菜", "桜井", "玲香", "梅澤", "美波",
                  "樋口", "日奈", "橋本", "奈々未", "永島", "聖羅", "深川", "麻衣", "清宮", "レイ", "渡辺", "みり愛", "生田", "絵梨花", "生駒", "里奈",
                  "田村", "真佑", "畠中", "清羅", "白石", "麻衣", "相楽", "伊織",
                  "矢久保", "美緒", "矢田", "里沙子", "秋元", "真夏", "筒井", "あやめ", "米徳", "京花", "能條", "愛未", "若月", "佑美", "衛藤", "美彩",
                  "西川", "七海", "西野", "七瀬", "賀喜", "遥香", "遠藤", "さくら",
                  "金川", "紗耶", "鈴木", "絢音", "阪口", "珠美", "高山", "一実", "齋藤", "飛鳥", "ちゃん", "さん", "wwwwww", "ｗｗｗｗｗｗ", "中", "∀",
                  "ﾟ",
                  "与田祐希", "中元日芽香", "中村麗乃", "中田花奈", "久保史緒里", "井上小百合", "伊藤かりん", "伊藤万理華", "伊藤寧々", "伊藤理々杏", "伊藤純奈",
                  "佐々木琴子", "佐藤楓", "北川悠理", "北野日奈子", "吉本彩華", "吉田綾乃クリスティー", "向井葉月", "和田まあや", "堀未央奈", "大和里菜", "大園桃子",
                  "安藤美雲", "宮澤成良", "寺田蘭世", "山下美月", "山崎怜奈", "山本穂乃香", "岩本蓮加", "岩瀬佑美子", "川後陽菜", "川村真洋", "市來玲奈", "掛橋沙耶香",
                  "斉藤優里", "斎藤ちはる", "新内眞衣", "早川聖来", "星野みなみ", "松井玲奈", "松村沙友理", "柏幸奈", "柴田柚菜", "桜井玲香", "梅澤美波", "樋口日奈",
                  "橋本奈々未", "永島聖羅", "深川麻衣", "清宮レイ", "渡辺みり愛", "生田絵梨花", "生駒里奈", "田村真佑", "畠中清羅", "白石麻衣", "相楽伊織", "矢久保美緒",
                  "矢田里沙子", "秋元真夏", "筒井あやめ", "米徳京花", "能條愛未", "若月佑美", "衛藤美彩", "西川七海", "西野七瀬", "賀喜遥香", "遠藤さくら", "金川紗耶",
                  "鈴木絢音", "阪口珠美", "高山一実", "齋藤飛鳥" ]  # ストップワード

    tagger = MeCab.Tagger(
        r" -d C:\Users\Hideki\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20180723")

    # 記事を取得→名詞取得
    word_list = []  # ["乃木坂","ライブ",,,]
    for row in ar_list:
        node = tagger.parseToNode(row[0])  # 形態素解析
        target_parts_of_speech = ('固有名詞')
        while node:
            if node.feature.split(',')[1] in target_parts_of_speech:  # 固有名詞の時
                word_list.append(node.surface)
            node = node.next

    # ストップワードを削除
    for stop_word in stop_words:
        while stop_word in word_list:
            word_list.remove(stop_word)

    # カウントリストを作成
    word_count_list = []  # [["乃木坂",2],["ライブ",3],,,]
    for word in word_list:
        count = word_list.count(word)
        word_count_list.append([word, count])

    # 重複を削除
    seen = []
    word_count_list = [x for x in word_count_list if x not in seen and not seen.append(x)]
    word_count_list.sort(key=itemgetter(1), reverse=True)

    i = 1
    word_count_rank_list = []
    for word_count in word_count_list[0:5]:
        word_count_rank_list.append([i, word_count[0], word_count[1]])
        i = i + 1

    # ページ数を取得
    page_count = math.ceil(len(ar_list) / 15)

    print(page_count)

    # 接続を閉じる
    conn.close()

    return render_template('detail.html', ar_list = ar_list[page_number_start:page_number_end], name = name,
                           word_count_list = word_count_list[0:50], word_count_rank_list = word_count_rank_list,
                           cate = 'member', page = int(page), page_prev = int(page)-1, page_next = int(page)+1, page_count = page_count)

@app.route('/word/<name>/<page>')
def word(name,page):
    dbname = "Nogizaka_matome_ar.db"

    #pageの記事番号を取得
    page_number_start=(int(page)-1)*15
    page_number_end=int(page)*15

    #URLデコード
    name=urllib.parse.unquote(name)

    # db接続
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # 記事のデータを取得
    select_sql = "select ar_tbl.title, ar_tbl.hour, ar_tbl.minute, ar_tbl.url, ar_tbl.site, site_tbl.site_url, ar_tbl.month, ar_tbl.day from ar_tbl inner join site_tbl on ar_tbl.site=site_tbl.site where ar_tbl.title like '%'||?||'%' order by ar_tbl.time desc"
    c.execute(select_sql,[name])
    ar_list = c.fetchall()

    # 注目ワードを取得
    stop_words = ["乃木坂46", "乃木坂", "46", "与田", "祐希", "中元", "日芽香", "中村", "麗乃", "中田", "花奈", "久保", "史緒里", "井上", "小百合", "伊藤",
                  "かりん",
                  "伊藤", "万理華", "伊藤", "寧々", "伊藤", "理々杏",
                  "伊藤", "純奈", "佐々木", "琴子", "佐藤", "楓", "北川", "悠理", "北野", "日奈子", "吉本", "彩華", "吉田", "綾乃", "クリスティー", "向井",
                  "葉月", "和田", "まあや", "堀", "未央奈", "大和", "里菜",
                  "大園", "桃子", "安藤", "美雲", "宮澤", "成良", "寺田", "蘭世", "山下", "美月", "山崎", "怜奈", "山本", "穂乃香", "岩本", "蓮加", "岩瀬",
                  "佑美子", "川後", "陽菜", "川村", "真洋", "市來", "玲奈",
                  "掛橋", "沙耶香", "斉藤", "優里", "斎藤", "ちはる", "新内", "眞衣", "早川", "聖来", "星野", "みなみ", "松井", "玲奈", "松村", "沙友理",
                  "柏", "幸奈", "柴田", "柚菜", "桜井", "玲香", "梅澤", "美波",
                  "樋口", "日奈", "橋本", "奈々未", "永島", "聖羅", "深川", "麻衣", "清宮", "レイ", "渡辺", "みり愛", "生田", "絵梨花", "生駒", "里奈",
                  "田村", "真佑", "畠中", "清羅", "白石", "麻衣", "相楽", "伊織",
                  "矢久保", "美緒", "矢田", "里沙子", "秋元", "真夏", "筒井", "あやめ", "米徳", "京花", "能條", "愛未", "若月", "佑美", "衛藤", "美彩",
                  "西川", "七海", "西野", "七瀬", "賀喜", "遥香", "遠藤", "さくら",
                  "金川", "紗耶", "鈴木", "絢音", "阪口", "珠美", "高山", "一実", "齋藤", "飛鳥", "ちゃん", "さん", "wwwwww", "ｗｗｗｗｗｗ", "中", "∀",
                  "ﾟ",
                  "与田祐希", "中元日芽香", "中村麗乃", "中田花奈", "久保史緒里", "井上小百合", "伊藤かりん", "伊藤万理華", "伊藤寧々", "伊藤理々杏", "伊藤純奈",
                  "佐々木琴子", "佐藤楓", "北川悠理", "北野日奈子", "吉本彩華", "吉田綾乃クリスティー", "向井葉月", "和田まあや", "堀未央奈", "大和里菜", "大園桃子",
                  "安藤美雲", "宮澤成良", "寺田蘭世", "山下美月", "山崎怜奈", "山本穂乃香", "岩本蓮加", "岩瀬佑美子", "川後陽菜", "川村真洋", "市來玲奈", "掛橋沙耶香",
                  "斉藤優里", "斎藤ちはる", "新内眞衣", "早川聖来", "星野みなみ", "松井玲奈", "松村沙友理", "柏幸奈", "柴田柚菜", "桜井玲香", "梅澤美波", "樋口日奈",
                  "橋本奈々未", "永島聖羅", "深川麻衣", "清宮レイ", "渡辺みり愛", "生田絵梨花", "生駒里奈", "田村真佑", "畠中清羅", "白石麻衣", "相楽伊織", "矢久保美緒",
                  "矢田里沙子", "秋元真夏", "筒井あやめ", "米徳京花", "能條愛未", "若月佑美", "衛藤美彩", "西川七海", "西野七瀬", "賀喜遥香", "遠藤さくら", "金川紗耶",
                  "鈴木絢音", "阪口珠美", "高山一実", "齋藤飛鳥" ]  # ストップワード

    tagger = MeCab.Tagger(
        r" -d C:\Users\Hideki\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20180723")

    # 記事を取得→名詞取得
    word_list = []  # ["乃木坂","ライブ",,,]
    for row in ar_list:
        node = tagger.parseToNode(row[0])  # 形態素解析
        target_parts_of_speech = ('固有名詞')
        while node:
            if node.feature.split(',')[1] in target_parts_of_speech:  # 固有名詞の時
                word_list.append(node.surface)
            node = node.next

    # ストップワードを削除
    for stop_word in stop_words:
        while stop_word in word_list:
            word_list.remove(stop_word)

    # カウントリストを作成
    word_count_list = []  # [["乃木坂",2],["ライブ",3],,,]
    for word in word_list:
        count = word_list.count(word)
        word_count_list.append([word, count])

    # 重複を削除
    seen = []
    word_count_list = [x for x in word_count_list if x not in seen and not seen.append(x)]
    word_count_list.sort(key=itemgetter(1), reverse=True)

    i=1
    word_count_rank_list=[]
    for word_count in word_count_list[0:5]:
        word_count_rank_list.append([i,word_count[0],word_count[1]])
        i=i+1

    #ページ数を取得
    page_count=math.ceil(len(ar_list)/15)

    # 接続を閉じる
    conn.close()

    return render_template('detail.html',
                           ar_list = ar_list[page_number_start:page_number_end], name = name, word_count_list = word_count_list[0:50]
                           ,word_count_rank_list = word_count_rank_list, cate ='word', page = int(page), page_prev = int(page)-1, page_next = int(page)+1, page_count = page_count)

@app.route('/ar/<page>')
def ar(page):
    dbname = "Nogizaka_matome_ar.db"

    # db接続
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    #記事のデータを取得
    select_sql = "select ar_tbl.title, ar_tbl.hour, ar_tbl.minute, ar_tbl.url, ar_tbl.site, site_tbl.site_url, ar_tbl.month, ar_tbl.day from ar_tbl inner join site_tbl on ar_tbl.site=site_tbl.site order by ar_tbl.time desc"
    c.execute(select_sql)
    ar_list = c.fetchall()

    #取得ページ数の取得
    # pageの記事番号を取得
    page_number_start = int(page) * 30
    page_number_end = (int(page)+1) * 30

    # ページ数を取得
    page_count = math.ceil(len(ar_list) / 30)

    return render_template('ar.html', ar_list = ar_list[page_number_start:page_number_end],page=int(page), page_count = page_count, page_prev = int(page)-1, page_next = int(page)+1)

@app.route('/about')
def about():
    return render_template('about.html')

## おまじない
if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)