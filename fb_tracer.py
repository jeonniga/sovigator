
import os
import json
import pymysql.cursors

import requests
from bs4 import BeautifulSoup

from urllib.parse import unquote

#Jason 형태의 설정파일을 읽어온다.
def readKEYWORDS(filename) :
    d = os.path.dirname(__file__) +'\\'
    with open(d+filename, encoding='utf8') as json_file:  
        data = json.load(json_file)
    return data

def getTrained_Data(kind, keyword):
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
    
    dic = {}
    try:
        sql = 'select content, category '
        sql += ' from '
        sql += 'ml_tour_filterkey'
        sql += ' where content like "%'
        sql += keyword
        sql += '%" and social_kind="'
        sql += kind
        sql += '" limit 100'
            
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
        for i in range(cursor.rowcount):
            content = cursor.fetchone()
            dic[content[0]] = content[1]
            i += 1
                
    finally:
        conn.close()
    return dic
   
def getFacebook_Data():
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
    ary_dic = []
    
    try:
        sql = 'select keyword, content, url'
        sql += ' from '
        sql += 'facebook'
            
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
            for i in range(cursor.rowcount):
                dic = {}
                content = cursor.fetchone()
                dic['keyword'] = content[0]
                dic['content'] = content[1]
                dic['url'] = content[2]
                ary_dic.append(dic)
#               print(dic)
                i += 1
#        print(ary_dic)   
    finally:
        conn.close()
    return ary_dic

def Scrapping(url):
    req  = requests.get(url)
    doc = BeautifulSoup(req.text, "html.parser")


    # 포스팅 게시글 추적
    lst = doc.findAll("div", {"class":"_5pbx userContent _3576"} )
    for s in lst:
        print('DOC: ', s.text)

    # 첨부 사진의 추적
    lst = doc.findAll('img')
    for s in lst:
        orig = str(s)
        start_idx = orig.find('src="') + len('src="')
        end_idx = orig.find('\"', start_idx)
        msg = orig[start_idx:end_idx]
        if msg.find('scontent-')>0:
            print( 'IMG: ', msg.replace('&amp;','&') )

    # 원본 인스타 그램 글 추적, href="이후가 진짜 경로임
    # lst = doc.findAll('a', {"data-render-location":"homepage_stream"})
    # for s in lst:
    #     orig = str(s)
    #     start_idx = orig.find('href="') + len('href="')
    #     end_idx = orig.find('\"',start_idx)
    #     msg = orig[start_idx:end_idx]
    #     print( 'INS: ', msg.replace('&amp;','&') )


if __name__ == "__main__":
    SETTINGS = readKEYWORDS("config.json")
    # print(SETTINGS)
    for k, v in SETTINGS.items(): 
        maria_host = v['maria.host']
        maria_port = v['maria.port']
        maria_id = v['maria.id']
        maria_pw = v['maria.pw']
        maria_dbname = v['maria.dbname']
        maria_charset = v['maria.charset']

    lstburl = getFacebook_Data()

    for i in range(len(lstburl)):
        for k, v in lstburl[i].items():
            if k=='url':
                
                Scrapping(v)
                print('↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ : ', v)

    
