#coding:utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
from contextlib import closing
import schedule
import time
import datetime
import re

# 乃木坂まとめらんだむのスクレイピング
def matomemorandam(bs):
    cates = bs.select('.right a')
    tag = ''
    for cate_text in cates:
        cate = cate_text.text
        cate = re.sub(' ', "", cate)  # スペースの削除
        cate = re.sub('\n', "", cate)  # 改行の削除
        tag = tag + cate + '\n'
    date = bs.select_one('.left').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date)
    year = date[0] + date[1] + date[2] + date[3]
    month = date[5] + date[6]
    day = date[8] + date[9]

    return year,month,day,tag

# 乃木坂まとめんばーのスクレイピング
def matomember(bs):
    cate_box = bs.select_one('.attr')
    cates = cate_box.select('strong')
    tag = ''
    for cate in cates:
        cate = re.sub('\n', "", cate.text)  # 改行の削除
        tag = tag + '\n' + cate
    date = bs.select_one('.date').text
    year = date[1] + date[2] + date[3] + date[4]
    if date[7]=='.':
        month=date[6]
        day = date[8] + date[9]
    else:
        month=date[6] + date[7]
        day = date[9] + date[10]

    return year, month, day, tag


# 乃木坂まとめ1/46のスクレイピング
def matome1_46(bs):
    cates = bs.select('.article-tags dd')
    tag = ''
    for cate in cates:
        tag = tag + '\n' + cate.text
    date = bs.select_one('time').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date)  # 改行の削除
    year = date[0] + date[1] + date[2] + date[3]
    month = date[5] + date[6]
    day = date[8] + date[9]

    return year, month, day, tag

# 乃木坂まとめの「ま」のスクレイピング
def matomenoma(bs):
    cate = bs.select_one('.related-articles h3').text
    tag = cate.strip("「」カテゴリの最新記事")
    date = bs.select_one('time').text
    date = re.sub(' ', "", date)  # スペースの削除
    date = re.sub('\n', "", date)  # 改行の削除
    year = date[1] + date[2] + date[3] + date[4]
    month = date[6] + date[7]
    day = date[9] + date[10]

    return year, month, day, tag

# 乃木坂めんばー
def nogizakamember(bs):
    cates = bs.find_all('a', {"rel": 'tag'})
    tag = ''
    for cate in cates:
        tag = tag + '\n' + cate.text
    tag = re.sub(' ', "", tag)
    date = bs.select_one('time').text
    year = date[0] + date[1] + date[2] + date[3]
    if date[6] == '/':
        month = date[5]
        day = date[7] + date[8]
    else:
        month = date[5] + date[6]
        day = date[8] + date[9]

    return year, month, day, tag

def scraping():
    dbname = 'Nogizaka_matome_ar.db'

    # 乃木坂まとめのまとめ
    matome_url = "http://nogizaka46matome.antenam.jp/categories/all/page:"

    # まとめのまとめサイトに遷移
    response = requests.get(matome_url)
    response.status_code
    session = requests.session()
    bs = BeautifulSoup(response.content, "html.parser")

    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        infos=bs.select('#main tr')
        infos.pop(0) #記事の一行目がブログ名を持たずうまくいかないため削除
        upsert_list=[]
        for info in infos:
            site = info.select_one('.blog_title a').text  # まとめサイトの名前を取得
            if site=='欅坂46速報(欅坂46乃木坂46まとめ)': #欅坂46速報(欅坂46乃木坂46まとめ)の時はパス
                pass
            else:
                title=info.select_one('.blog_post').text #タイトル取得
                time_text=info.select_one('.item_title_list').text #記事投稿の時間を取得
                if time_text[5]==':':
                    hour=int(time_text[4]) #記事投稿の時を取得
                    minute=int(time_text[6]+time_text[7]) #記事投稿の分を取得
                else:
                    hour = int(time_text[4] + time_text[5])  # 記事投稿の時を取得
                    minute = int(time_text[7] + time_text[8])  # 記事投稿の分を取得
                url="http://nogizaka46matome.antenam.jp"+info.select_one('a').attrs['href'] #掲載先のurlを取得

                # 掲載先のサイトに遷移
                response = requests.get(url)
                response.status_code
                session = requests.session()
                bs = BeautifulSoup(response.content, "html.parser")
                site_url = bs.find('link', {"rel": 'canonical'})
                url=site_url['href']

                #サイトごとにタグの取得
                if site=='乃木坂46まとめもらんだむ|乃木坂4':
                    tags=matomemorandam(bs)
                elif site=='乃木坂46まとめんばー':
                    tags=matomember(bs)
                elif site=='乃木坂46まとめ　乃木仮めんばー':
                    tags=nogizakamember(bs)
                elif site=='乃木坂46まとめの「ま」':
                    tags=matomenoma(bs)
                elif site=='乃木坂46まとめ 1/46':
                    tags=matome1_46(bs)
                else:
                    print("エラー")
                #データをリストに追加
                time = datetime.datetime(int(tags[0]), int(tags[1]), int(tags[2]), hour, minute, 0)  # 投稿時間をまとめて保存
                upsert_list.append([title,time,int(tags[0]), int(tags[1]), int(tags[2]),hour,minute,url,site,tags[3]])

        #データが無ければ追加、あればそのまま
        upsert_sql = 'replace into ar_tbl values (?,?,?,?,?,?,?,?,?,?)'
        c.executemany(upsert_sql, upsert_list)
        conn.commit()
        print('記事データを更新しました'+str(datetime.datetime.now()))

def calculate():
    dbname = 'Nogizaka_matome_ar.db'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql='select name from member_tbl'
        member_list=[] #['秋元真夏','生田絵梨花'...]
        #メンバーの名前を取得
        for member_name in c.execute(select_sql):
            member_list.append(member_name[0])
        count_list=[]
        for member in member_list:
            select_sql = "select title,tags from ar_tbl where tags like '%'||?||'%' and datetime('now', '-3 days','9 hours') < time"
            c.execute(select_sql, [member])
            ar_list = c.fetchall()
            count3=len(ar_list)
            count_time=datetime.date.today()
            count_list.append([member,count_time,count3])
        upsert_sql = 'replace into count_tbl values (?,?,?)'
        c.executemany(upsert_sql, count_list)
        conn.commit()
        print('集計データを更新しました' + str(datetime.datetime.now()))


#scraping()
#calculate()

# 10分毎にjobを実行
schedule.every(30).minutes.do(scraping)
schedule.every(30).minutes.do(calculate)
while True:
    schedule.run_pending()
    time.sleep(1)
