#coding:UTF-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
from contextlib import closing
import schedule
import time
import datetime
import re
from operator import itemgetter
import MeCab

def scraping():
    dbname = 'Nogizaka_matome_ar.db'

    '''
    # 乃木坂まとめのまとめ
    matome_url = "http://nogizaka46matome.antenam.jp/categories/all/page:1"

    # まとめのまとめサイトに遷移
    response = requests.get(matome_url)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        infos=bs.select('#main tr')
        infos.pop(0) #記事の一行目がブログ名を持たずうまくいかないため削除
        for info in infos:
            site = info.select_one('.blog_title a').text  # まとめサイトの名前を取得
            if site=='欅坂46速報(欅坂46乃木坂46まとめ)': #欅坂46速報(欅坂46乃木坂46まとめ)の時はパス
                pass
            else:
                title=info.select_one('.blog_post').text #タイトル取得
                date=datetime.date.today() #記事投稿の日付を取得
                year=date.year #記事投稿の年を取得
                month=date.month #記事投稿の月を取得
                day=date.day #記事投稿の日を取得
                time_text=info.select_one('.item_title_list').text #記事投稿の時間を取得
                hour=int(time_text[4]+time_text[5]) #記事投稿の時を取得
                minute=int(time_text[7]+time_text[8]) #記事投稿の分を取得
                url="http://nogizaka46matome.antenam.jp"+info.select_one('a').attrs['href'] #掲載先のurlを取得

                # 掲載先のサイトに遷移
                response = requests.get(site)
                response.status_code
                session = requests.session()
                bs = BeautifulSoup(response.content, "html.parser")
                '''

    '''
    # 乃木坂まとめもらんだむ
    site = "http://nogizaka46matome.2chblog.jp/archives/36667653.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    cates=bs.select('.right a')
    tag=''
    for cate_text in cates:
        cate=cate_text.text
        cate = re.sub(' ', "", cate) #スペースの削除
        cate = re.sub('\n', "", cate) #改行の削除
        tag=tag+cate+'\n'
    print(tag)
    date=bs.select_one('.left').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date) #改行の削除
    year=date[0]+date[1]+date[2]+date[3]
    month=date[5] + date[6]
    day=date[8] + date[9]'''

    '''
    # 乃木坂まとめんばー
    site = "http://nogitweet.com/%E3%80%90%E4%B9%83%E6%9C%A8%E5%9D%8246%E3%80%91%E5%B9%95%E5%BC%B5%E5%85%A8%E6%8F%A1%E3%80%81%E3%81%BF%E3%81%95%E5%85%88%E8%BC%A9%E3%83%AC%E3%83%BC%E3%83%B3%E3%81%AB%E3%81%AF%E3%81%82%E3%81%AE%E4%BA%BA/"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    cate_box=bs.select_one('.attr')
    cates=cate_box.select('strong')
    tag=''
    for cate in cates:
        cate= re.sub('\n', "", cate.text)  # 改行の削除
        tag=tag+'\n'+cate
    date=bs.select_one('.date').text
    print(date)
    year=date[1]+date[2]+date[3]+date[4]
    if date[7]=='.':
        month=date[6]
        day = date[8] + date[9]
    else:
        month=date[6] + date[7]
        day = date[9] + date[10]
    print(year)
    print(month)
    print(day)

    return year,month,day,tag'''


    '''# 乃木坂1/46
    site = "http://nogizaka-46bunno1.blog.jp/archives/77569206.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    cates=bs.select('.article-tags dd')
    tag=''
    for cate in cates:
        tag=tag+'\n'+cate.text
    print(tag)
    date=bs.select_one('time').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date)  # 改行の削除
    year = date[0] + date[1] + date[2] + date[3]
    month = date[5] + date[6]
    day = date[8] + date[9]

    return year,month,day,tag'''


    '''# 乃木坂46まとめの「ま」
    site = "http://nogizaka46matomenoma.blog.jp/archives/79266289.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    cate=bs.select_one('.related-articles h3').text
    tag=cate.strip("「」カテゴリの最新記事")
    print(tag)
    date=bs.select_one('time').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date)  # 改行の削除
    year = date[1] + date[2] + date[3] + date[4]
    month = date[6] + date[7]
    day = date[9] + date[10]

    return year, month, day, tag'''

    '''
    site = "http://nogizaka46matomenoma.blog.jp/archives/79278158.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    #print(bs)
    url=bs.find('link',{"rel":'canonical'})
    print(url['href'])
    '''

    '''site = "http://nogizaka46matome.2chblog.jp/archives/36719351.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    # print(bs)
    url = bs.find('link', {"rel": 'canonical'})
    print(url['href'])'''


    '''#乃木仮メンバー
    site = "http://nogizaka46democracy.com/archives/post-24310.html"
    response = requests.get(site)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")
    cates=bs.find_all('a',{"rel":'tag'})
    tag=''
    for cate in cates:
        tag=tag+'\n'+cate.text
    tag = re.sub(' ', "", tag)
    print(tag)
    date = bs.select_one('time').text
    year = date[0] + date[1] + date[2] + date[3]
    if date[6] == '/':
        month = date[5]
        day = date[7] + date[8]
    else:
        month = date[5] + date[6]
        day = date[8] + date[9]
    print(year)
    print(month)
    print(day)'''

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        stop_words = ["乃木坂","46","与田","祐希","中元","日芽香","中村","麗乃","中田","花奈","久保","史緒里","井上","小百合","伊藤","かりん","伊藤","万理華","伊藤","寧々","伊藤","理々杏",
                    "伊藤","純奈","佐々木","琴子","佐藤","楓","北川","悠理","北野","日奈子","吉本","彩華","吉田","綾乃","クリスティー","向井","葉月","和田","まあや","堀","未央奈","大和","里菜",
                    "大園","桃子","安藤","美雲","宮澤","成良","寺田","蘭世","山下","美月","山崎","怜奈""山本","穂乃香","岩本","蓮加","岩瀬","佑美子","川後","陽菜","川村","真洋","市來","玲奈",
                    "掛橋","沙耶香","斉藤","優里","斎藤","ちはる","新内","眞衣","早川","聖来","星野","みなみ","松井","玲奈","松村","沙友理","柏","幸奈","柴田","柚菜","桜井","玲香","梅澤","美波",
                    "樋口","日奈","橋本","奈々未","永島","聖羅","深川","麻衣","清宮","レイ","渡辺","みり愛","生田","絵梨花","生駒","里奈","田村","真佑","畠中","清羅","白石","麻衣","相楽","伊織",
                    "矢久保","美緒","矢田","里沙子","秋元","真夏","筒井","あやめ","米徳","京花","能條","愛未","若月","佑美","衛藤","美彩","西川","七海","西野","七瀬","賀喜","遥香","遠藤","さくら",
                    "金川","紗耶","鈴木","絢音","阪口","珠美","高山","一実","齋藤","飛鳥"]
        tagger = MeCab.Tagger(
            r" -d C:\Users\Hideki\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20180723")

        tagger.parse('')
        text='【乃木坂46】『衛藤美彩 卒業ソロコンサート＠両国国技館』14th〜22nd特製ポスタープレゼント！'
        node = tagger.parseToNode(text)
        word_class = []
        while node:
            word = node.surface
            wclass = node.feature.split(',')
            if wclass[0] != u'BOS/EOS':
                if wclass[6] == None:
                    word_class.append((word, wclass[0], wclass[1], wclass[2], ""))
                else:
                    word_class.append((word, wclass[0], wclass[1], wclass[2], wclass[6]))
            node = node.next
        for i in word_class:
            print(i)

        '''
        select_sql = "select title from ar_tbl where datetime('now', '-3 days','9 hours') < time"
        word_list = []  # ["乃木坂","ライブ",,,]
        for row in c.execute(select_sql):
            node = tagger.parseToNode(row[0])  # 形態素解析
            target_parts_of_speech = ('名詞')
            while node:
                if node.feature.split(',')[0] in target_parts_of_speech:  # 固有名詞の時
                    word_list.append(node.surface)
                node = node.next

        
        # ストップワードを削除
        for stop_word in stop_words:
            while stop_word in word_list:
                word_list.remove(stop_word)

        # ワードの数をカウントしリストに保存
        word_count_list = []  # [["乃木坂",2],["ライブ",3],,,]
        for word in word_list:
            count = word_list.count(word)
            word_count_list.append([word, count])

        # 重複を削除
        seen = []
        word_count_list = [x for x in word_count_list if x not in seen and not seen.append(x)]
        word_count_list.sort(key=itemgetter(1), reverse=True)

        for a in word_count_list:
            print(a)'''


scraping()


