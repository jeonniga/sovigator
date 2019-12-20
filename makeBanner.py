# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 17:57:01 2018

@author: seedp
"""

import json
import pymysql.cursors
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def readKEYWORDS(filename) :
    f = open(filename, 'rt', encoding='UTF8')
    js = json.loads(f.read() ,encoding='utf-8')
    f.close()
    return js

def getKeyWord(col, table, keyword):
    conn = pymysql.connect(host='106.246.227.252',
            user='root',
            password='linktree0415!',
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
        elif keyword !=None and table=='naver_blog':
            sql+= ' where title like "%'
            sql+= keyword
            sql+= '%" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '

        elif keyword !=None and table=='naver_news':
            sql+= ' where title like "%'
            sql+= keyword
            sql+= '%" limit 10'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '
        elif keyword !=None and table=='total_info':
            sql+= ' where title like "%'
            sql+= keyword
            sql+= '%" limit 30'
            
            with conn.cursor() as cursor:
                cursor.execute(sql)
                
            for i in range(cursor.rowcount):
                content = cursor.fetchone()
                msg += content[0]
                msg += ' '   
                
    finally:
        conn.close()
    return msg

def generateWordCloud(text, template, output_filename, use_color_pickup):
    
    cloud_coloring = np.array(Image.open(template))
    stopwords = set(STOPWORDS)
    stopwords.add("said")
    font_path=path.join(app_path, 'fonts/gulim.ttc')
    
    wc = WordCloud(font_path, 
                   background_color="rgba(255, 255, 255, 0)", mode="RGBA", 
                   max_words=2000, mask=cloud_coloring, stopwords=stopwords, 
                   max_font_size=20, random_state=42)
    
    print(font_path)

    wc.generate(text)

    if use_color_pickup==1:
        image_colors = ImageColorGenerator(cloud_coloring)
        wc.recolor(color_func=image_colors)

    plt.imshow(wc)
    plt.axis("off")
    plt.show() 
            
    wc.to_file(output_filename)

def makeLogo(type, keyword):   
    if type=='facebook':
        msg = getKeyWord('content', 'facebook', keyword)  
        generateWordCloud(msg, app_path+"template/fb.jpg", banner_img_path + "facebook_"+keyword+".png", 0)
    elif type=='twitter':
        msg = getKeyWord('text', 'twitter', keyword)  
        generateWordCloud(msg, app_path+"template/tw.jpg", banner_img_path + "twitter_"+keyword+".png", 0)
    elif type=='instagram':
        msg = getKeyWord('edge_media_to_caption', 'instagram', keyword)  
        generateWordCloud(msg, app_path+"template/in.jpg", banner_img_path + "instagram_"+keyword+".png", 0)
    elif type=='wikipedia':
        msg = getKeyWord('content', 'wikipedia', keyword)  
        generateWordCloud(msg, app_path+"template/wiki.jpg", banner_img_path + "wikipedia_"+keyword+".png", 0)
    elif type=='naver_blog':
        msg = getKeyWord('title', 'naver_blog', keyword)  
        generateWordCloud(msg, app_path+"template/naver.jpg", banner_img_path + "naverblog_"+keyword+".png", 0)
    elif type=='naver_news':
        msg = getKeyWord('title', 'naver_news', keyword)  
        generateWordCloud(msg, app_path+"template/naver.jpg", banner_img_path + "navernews_"+keyword+".png", 0)
    elif type=='total_info':
        msg = getKeyWord('title', 'total_info', keyword)  
        generateWordCloud(msg, app_path+"template/dime.jpg", banner_img_path + "totalinfo_"+keyword+".png", 0)

    return

if __name__ == "__main__":
    
    SETTINGS = readKEYWORDS("config.json")
    for k, v in SETTINGS.items(): 
        banner_img_path = v['banner_img_path']
        app_path = v['app_path']
        
    
    KEYWORDS = readKEYWORDS("twitter.json")
    for k, v in KEYWORDS.items():
        makeLogo('twitter', v['keyword'])
        
    KEYWORDS = readKEYWORDS("wiki.json")
    for k, v in KEYWORDS.items():   
        makeLogo('wikipedia', v['keyword'])
        
    KEYWORDS = readKEYWORDS("instagram.json")
    for k, v in KEYWORDS.items():   
        makeLogo('instagram', v['keyword'])
        
    KEYWORDS = readKEYWORDS("facebook.json")
    for k, v in KEYWORDS.items():   
        makeLogo('facebook', v['keyword'])

    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        makeLogo('naver_news', v['keyword'])

    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        makeLogo('naver_blog', v['keyword'])

    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        makeLogo('total_info', v['keyword'])