# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 17:04:16 2018

pip install facepy
pip install redis

python -m pip install --upgrade pip
pip install PyMySQL

pip install InstagramApi
pip install python-twitter
pip install WikiApi

conda install -c conda-forge wordcloud

pip install tensorflow
pip install qrcode
@author: seedp
"""

import sys
sys.setrecursionlimit(5000)


import json
import time

import datetime
from dateutil.parser import parse

import bs4
import requests
import re
import threading
import pymysql.cursors

from wikiapi import WikiApi
import twitter
from facepy import GraphAPI

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

KEYWORDS={}
SETTINGS={}

CONSUMER_KEY='my3faDiZqgxeXnwJ5URBcfHPW'
CONSUMER_SECRET='orPOOiu76MkkVRiuGZpqdnxXOL7Opu1p0JnFJFkSXMh5KBCzpY'
ACCESS_TOKEN='929809559832559616-665xDVjAZ9uM9ReDDsnnzcaFMEnWSuW'
ACCESS_TOKEN_SECRET='HjqU9HslBI1qThqPa0fbd0E9xOpEa7fkHWF5pEu45XY1y'

MAKE_LOGO = 0

naver_client_id = "Gb_Lj2js5gquq33B1Guj"
naver_client_secret = "sPszanmgLx"

headers = {
    'Host' : 'openapi.naver.com',
    'User-Agent' : 'curl/7.43.0',
    'Accept' : '*/*',
    'Content-Type' : 'application/xml',
    'X-Naver-Client-Id' : 'Gb_Lj2js5gquq33B1Guj',
    'X-Naver-Client-Secret' : 'sPszanmgLx'
}

def extractTag(content):
    return content.replace('&apos;','`').replace('<b>','').replace('</b>','').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&nbsp;',' ').replace('</br>','').replace('<br>','\n').replace('&amp;','&')

def makeReqURL_NEWS(sort, start, display, keyword):
    defaultURL = 'https://openapi.naver.com/v1/search/news.xml?'
    query = '&query=' + urllib.parse.quote_plus(keyword)  # 사용자에게 검색어를 입력받아 quote_plus 함수로 UTF-8 타입에 맞도록 변환시켜 줍니다.
    return defaultURL + sort + start + display + query

def Parse_NEWS(fullURL):
    # HTTP 요청을 하기 전에 헤더 정보를 이용해 request 객체를 생성합니다. urllib 모듈에서 헤더 정보를 서버에 전달할 때 사용하는 대표적인 방법입니다.
    req = urllib.request.Request(fullURL, headers=headers)
    # 생성된 request객체를 uplopen함수의 인수로 전달합니다. 이렇게 되면 헤더 정보를 포함하여 서버에게 HTTP 요청을 하게 됩니다.
    f = urllib.request.urlopen(req)
    resultXML = f.read()
    xmlsoup = BeautifulSoup(resultXML, 'html.parser')
    items = xmlsoup.find_all('item')
    ary = []
    for item in items:
        dic = {}
        title = extractTag( item.title.get_text(strip=True) )
        desc = extractTag( item.description.get_text(strip=True) )
        link = extractTag( item.originallink.get_text(strip=True) )
        dic = {'title':title, 'desc':desc, 'link':link}
        ary.append(dic)
        # print(  'TITLE:',  dic['title'] )
        # print(  'DESC:',   dic['desc'])
        # print(  'LINK:',  dic['link'])
        # print('-------------------------------------------')
        insertMaria('naver_news', dic)

    return ary

def makeReqURL_BLOG(sort, start, display, keyword):
    defaultURL = 'https://openapi.naver.com/v1/search/blog?'
    query = '&query=' + urllib.parse.quote_plus(keyword) 
    return defaultURL + sort + start + display + query


def Parse_BLOG(fullURL):
    request = urllib.request.Request(fullURL)
    request.add_header("X-Naver-Client-Id",naver_client_id)
    request.add_header("X-Naver-Client-Secret",naver_client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        
        # json처리
        result = response_body.decode('utf-8')
        js = json.loads(result)
        ary = []
        for k, v in js.items():
            #lastBuildDate, total, start, display, items
            if k=='items':
                for i in range(len(v)):
                    dict = v[i]
                    for k2, v2 in dict.items():
                        if k2=='title' :
                            title = extractTag(v2)
                        elif k2=='link':
                            link = extractTag(v2)
                        elif k2 == 'description':
                            desc = extractTag(v2)
                    dic = {'title':title, 'link':link, 'desc':desc}
                    # print('TITLE:', dic['title'])
                    # print('LINK:', dic['link'])
                    # print('DESC:', dic['desc'])
                    insertMaria('naver_blog', dic)
                    ary.append(dic)
    else:
        print("Error Code:" + rescode)

    return ary


#Jason 형태의 설정파일을 읽어온다
def readKEYWORDS(filename) :
    f = open(filename, 'rt', encoding='UTF8')
    js = json.loads(f.read() ,encoding='utf-8')
    f.close()
    return js

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)  
    result = file.json()['access_token']
    return result

#Redis 접속정보를 생성해 ResultSet으로 리턴
#def connRedis(host='localhost', port=6379, db=0):
#    r = redis.StrictRedis(host=redis_host, port=int(redis_port), db=0)
#    return r

#def generateWordCloud(text, template, output_filename, use_color_pickup):
#    
#    cloud_coloring = np.array(Image.open(template))
#    stopwords = set(STOPWORDS)
#    stopwords.add("said")
#    
#    wc = WordCloud(font_path=path.join(app_path, 'fonts/NanumGothic.ttf'), 
#                   background_color="rgba(255, 255, 255, 0)", mode="RGBA", 
#                   max_words=2000, mask=cloud_coloring, stopwords=stopwords, 
#                   max_font_size=20, random_state=42)
#
#    wc.generate(text)
#
#    if use_color_pickup==1:
#        image_colors = ImageColorGenerator(cloud_coloring)
#        wc.recolor(color_func=image_colors)
#
#    plt.imshow(wc)
#    plt.axis("off")
#    plt.show() 
#            
#    wc.to_file(output_filename) 
    
def getKeyWord(col, table, keyword):
    conn = pymysql.connect(host='localhost',
            user='root',
            password='dh2026!@#$A',
            db='test',
            charset='utf8mb4')
    
    msg = keyword
    try:
        sql = 'select '
        sql += col
        sql += ' from '
        sql += table
        if keyword !=None and table=='facebook':
            sql+= ' where keyword="'
            sql+= keyword
            sql+= '" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '
                i += 1
        elif keyword !=None and table=='twitter':
            sql+= ' where text like "%'
            sql+= keyword
            sql+= '%" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '
        elif keyword !=None and table=='instagram':
            sql+= ' where edge_media_to_caption like "%'
            sql+= keyword
            sql+= '%" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '
        elif keyword !=None and table=='wikipedia':
            sql+= ' where keyword = "'
            sql+= keyword
            sql+= '" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '
                
    finally:
        conn.close()
    return msg

    
def insertMaria(table, dic):
        
    conn = pymysql.connect(host=maria_host,
        user=maria_id,
        password=maria_pw,
        db=maria_dbname,
        charset=maria_charset)
     
    try:
        with conn.cursor() as cursor:
            if table=='wikipedia':
                sql = 'INSERT INTO wikipedia (keyword, heading, content) VALUES (%s, %s, %s)'
                sql += 'ON DUPLICATE KEY UPDATE keyword=%s, heading=%s, content=%s'
                cursor.execute(sql, (dic['keyword'], dic['heading'], dic['content'],
                                     dic['keyword'], dic['heading'], dic['content']))
            elif table=='facebook':
                sql = 'INSERT INTO facebook (keyword, content, url) VALUES (%s, %s, %s)'
                sql += 'ON DUPLICATE KEY UPDATE keyword=%s, content=%s, url=%s'
                cursor.execute(sql, (dic['keyword'], dic['content'], dic['url'], 
                                     dic['keyword'], dic['content'], dic['url']))
            elif table=='instagram':
                sql = 'INSERT INTO instagram (	id, display_url, thumbnail_src, edge_media_to_caption, taken_at_timestamp, is_video) VALUES (%s, %s, %s, %s, %s, %s)'
                sql += 'ON DUPLICATE  KEY UPDATE id=%s, display_url=%s, thumbnail_src=%s, edge_media_to_caption=%s, taken_at_timestamp=%s, is_video=%s'
                cursor.execute(sql, (dic['tid'], dic['display_url'], dic['thumbnail_src'], dic['edge_media_to_caption'], dic['taken_at_timestamp'], dic['is_video'],
                     dic['tid'], dic['display_url'], dic['thumbnail_src'], dic['edge_media_to_caption'], dic['taken_at_timestamp'], dic['is_video']))
            elif table=='twitter':
                sql = 'INSERT INTO twitter (uId, screen, txtId, date, text, urls) VALUES (%s, %s, %s, %s, %s, %s)'
                sql += 'ON DUPLICATE KEY UPDATE uId=%s, screen=%s, txtId=%s, date=%s, text=%s, urls=%s'
                cursor.execute(sql, (dic['uId'], dic['screen'], dic['txtId'], dic['date'], dic['text'], dic['urls'],
                                     dic['uId'], dic['screen'], dic['txtId'], dic['date'], dic['text'], dic['urls']))
            elif table=='naver_blog':
                sql = 'INSERT INTO naver_blog (title, link, description) VALUES (%s, %s, %s)'
                sql += 'ON DUPLICATE KEY UPDATE title=%s, link=%s, description=%s'
                cursor.execute(sql, (dic['title'], dic['link'], dic['desc'], 
                                     dic['title'], dic['link'], dic['desc']))
            elif table=='naver_news':
                sql = 'INSERT INTO naver_news (title, link, description) VALUES (%s, %s, %s)'
                sql += 'ON DUPLICATE KEY UPDATE title=%s, link=%s, description=%s'
                cursor.execute(sql, (dic['title'], dic['link'], dic['desc'], 
                                     dic['title'], dic['link'], dic['desc']))                                                 
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
def wiki():
#    redisR = connRedis(redis_host, int(redis_port), 0)   
    while(1):
        KEYWORDS = readKEYWORDS("wiki.json")
     
        wiki = WikiApi({ 'locale' : 'ko'})
            
        for k, v in KEYWORDS.items():  
            k 
            results = wiki.find(v['keyword'])
            article = wiki.get_article(results[0])
     
            jsonstring = "{'"+article.heading
            jsonstring += "':'" + article.content
            jsonstring += "'}"
    
#            redisR.set(article.heading, jsonstring)
            
            try:
                dic = {'keyword': v['keyword'], 'heading':article.heading, 'content':article.content }
                insertMaria('wikipedia', dic)
#                if MAKE_LOGO==1:
#                    makeLogo('wikipedia', v['keyword'])
            except Exception as e:
                print(e)        
           
        time.sleep(60)

def makeQry(keyword, since, count):
    qrystring = 'q='
    qrystring += keyword
    qrystring += '%20&result_type=recent&since='
    qrystring += since
    qrystring += '&count='
    qrystring += count
    return qrystring
        
def twitt():
    addr = None

#    redisR = connRedis(redis_host, int(redis_port), 0)
        
    api = twitter.Api(tw_consumer_key,
                          tw_consumer_secret,
                          tw_access_token,
                          tw_access_token_secret)
       
    while(1):
        KEYWORDS = readKEYWORDS("twitter.json")
        
        for k, v in KEYWORDS.items():
            k
            results = api.GetSearch( raw_query=makeQry(v['keyword'], v['since'], v['count']) )
           
            for status in results:
                uId = str(status.user.id)
                screen =  status.user.screen_name
                txtId = status.id_str
                date = time.strftime( str(parse(status.created_at)) )
                text = status.text
                urls = str(status.urls)
                
#                redisR.set(status.id_str, status.text)

                try:
                    try:
                        addr = urls.split(',')[1]
                        addr = addr.split('=')[1][:-2]
                    except Exception as ea:
                        print(ea)
                        addr = '#'
                   
                    dic = {'uId':uId, 'screen':screen, 'txtId':txtId, 'date':date, 'text':text, 'urls':addr}
                    insertMaria('twitter', dic)
#                    if MAKE_LOGO==1:
#                        makeLogo('twitt', v['keyword'])
                except Exception as e:
                    print(e)
            
        time.sleep(60)

def extract_shared_data(doc):
    for script_tag in doc.find_all("script"):
        if script_tag.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\\._sharedData = ", "", script_tag.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
            return shared_data
        
def extract_recent_tag(tag):
    KEYWORDS = readKEYWORDS("instagram.json")    
    for k, v in KEYWORDS.items():  
        url_string = "https://www.instagram.com/explore/tags/%s/" % tag
        response = bs4.BeautifulSoup(requests.get(url_string).text, "html.parser")
        shared_data = extract_shared_data(response)
    
        try:
            context_lst = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']
        
            for i in range(len(context_lst)):
                media = context_lst[i]['node']
                
                for k,v in media.items():
                    if k=='id':
                        tid = v
                    elif k=='display_url':
                        display_url = v
                    elif k=='thumbnail_src':
                        thumbnail_src = v
                    elif k=='edge_media_to_caption':
                        for k1, v1 in v.items():
                            k1
                            edge_media_to_caption = v1[0]['node']['text']
                    elif k=='taken_at_timestamp':
                        t = datetime.datetime.fromtimestamp(float(v))
                        taken_at_timestamp = t.strftime('%Y-%m-%d %H:%M:%S')
                    elif k=='is_video':
                        is_video = v
                        
                try:
                    dic = {"tid":tid, "display_url":display_url, "thumbnail_src":thumbnail_src,                     "edge_media_to_caption":edge_media_to_caption, "taken_at_timestamp":taken_at_timestamp, "is_video":is_video}
                    insertMaria('instagram', dic)
#                    if MAKE_LOGO==1:
#                        makeLogo('instagram', tag)
                except Exception as e:
                    print(e)
        except Exception as ee:
            print(ee)
            continue
 
def instagram():    
    while(1):
        KEYWORDS = readKEYWORDS("instagram.json")
        
        for k, v in KEYWORDS.items(): 
            k
            qry = v['keyword']
            try:
                extract_recent_tag(qry)
            except Exception as e:
                print(e)
                continue
            
        time.sleep(60) 

def search(graph, key, stype):
    #GET graph.facebook.com/search?q=coffee&type=place&center=37.76,-122.427&distance=1000
    response = graph.search(key, stype)     
    print(response)
    return response

def facebook():
#    redisR = connRedis(redis_host, int(redis_port), 0)  
    KEYWORDS = readKEYWORDS("facebook.json")
    token = get_fb_token(fb_user_id, fb_user_secret)
    
    graph = GraphAPI(token)
    
    while(True):
        for k, v in KEYWORDS.items(): 
            k
            qry = v['keyword']
            place = v['type']

            res = search(graph, qry, place)  

            for k1, v1 in res.items():
                k1
                if type(v1)==list:
                    for i in range(len(v1)):
                        urlstring = 'https://www.facebook.com/profile.php?id=%s' % v1[i]['id']
#                        redisR.set(v1[i]['name'], urlstring)
                        try:
                            dic = {"keyword":v['keyword'], "content":v1[i]['name'], "url":urlstring}
                            print(dic)
                            insertMaria('facebook', dic)
#                            if MAKE_LOGO==1:
#                                makeLogo('facebook', v['keyword'])
    #                        print (dic)
                        except Exception as e:
                            print(e)
    time.sleep(60)
    
#def makeLogo(type, keyword):   
#    if type=='facebook':
#        msg = getKeyWord('content', 'facebook', keyword)  
#        generateWordCloud(msg, app_path+"template/fb.jpg", banner_img_path + "facebook_"+keyword+".png", 0)
#    elif type=='twitter':
#        msg = getKeyWord('text', 'twitter', keyword)  
#        generateWordCloud(msg, app_path+"template/tw.jpg", banner_img_path + "twitter_"+keyword+".png", 0)
#    elif type=='instagram':
#        msg = getKeyWord('edge_media_to_caption', 'instagram', keyword)  
#        generateWordCloud(msg, app_path+"template/in.jpg", banner_img_path + "instagram_"+keyword+".png", 0)
#    elif type=='wikipedia':
#        msg = getKeyWord('content', 'wikipedia', keyword)  
#        generateWordCloud(msg, app_path+"template/wiki.jpg", banner_img_path + "wikipedia_"+keyword+".png", 0)
#        
#    return
         
def Naver_Blog():
    while (True):
        KEYWORDS = readKEYWORDS("naver.json")
        
        for k, v in KEYWORDS.items(): 
            k
            qry = v['keyword']
        
            fullURL = makeReqURL_BLOG('sort=sim','&start=1', '&display=100', qry)
            # print(fullURL)
            Parse_BLOG(fullURL)

        time.sleep(50)

    return
    
def Naver_News():
    while(True):
        KEYWORDS = readKEYWORDS("naver.json")
        
        for k, v in KEYWORDS.items(): 
            k
            qry = v['keyword']
        
            fullURL = makeReqURL_NEWS('sort=sim', '&start=1', "&display=100", qry) 
            # print(fullURL)
            Parse_NEWS(fullURL)

        time.sleep(50)

    return 


# generateWordCloud(text, template, output_filename)        
if __name__ == "__main__":
    SETTINGS = readKEYWORDS("config.json")
    for k, v in SETTINGS.items(): 
        redis_host = v['redis.host']
        redis_port = v['redis.port']
        maria_host = v['maria.host']
        maria_port = v['maria.port']
        maria_id = v['maria.id']
        maria_pw = v['maria.pw']
        maria_dbname = v['maria.dbname']
        maria_charset = v['maria.charset']
        fb_user_id = v['face_id']
        fb_user_secret = v['face_secret']
        tw_consumer_key = v['TW_CONSUMER_KEY']
        tw_consumer_secret = v['TW_CONSUMER_SECRET']
        tw_access_token = v['TW_ACCESS_TOKEN']
        tw_access_token_secret = v['TW_ACCESS_TOKEN_SECRET']
        banner_img_path = v['banner_img_path']
        app_path = v['app_path']

    # 데몬 쓰레드
    face = threading.Thread(target=facebook)
    face.daemon = True 
    face.start()
     
    insta = threading.Thread(target=instagram)
    insta.daemon = True 
    insta.start()

    twitt = threading.Thread(target=twitt)
    twitt.daemon = True 
    twitt.start()
    
    wiki = threading.Thread(target=wiki)
    wiki.daemon = True 
    wiki.start()
    
    nBlog = threading.Thread(target=Naver_Blog)
    nBlog.daemon = True
    nBlog.start()

    nNews = threading.Thread(target=Naver_News)
    nNews.daemon = True
    nNews.start()
    
    print("### If you press return key, it will be exited ###")
    
    input('')

