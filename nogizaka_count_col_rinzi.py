# カウントリストを取得
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
            select_sql = "select title,tags from ar_tbl where tags like '%'||?||'%' and datetime('now', '-4 days','9 hours') < time and datetime('now', '-1 days','9 hours') > time"
            c.execute(select_sql, [member])
            ar_list = c.fetchall()
            count3=len(ar_list)
            count_time="2019-03-25"
            count_list.append([member,count_time,count3])
        upsert_sql = 'replace into count_tbl values (?,?,?)'
        c.executemany(upsert_sql, count_list)
        conn.commit()
        print('集計データを更新しました' + str(datetime.datetime.now()))

calculate()