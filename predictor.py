# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 12:32:40 2018
설치 :
    BayesianFilter.py need on same Folder
    
기능 : 지정한 필터 규칙에 입각해 학습해 정보의 판독하는 기능

@author: seedp
"""
import os
import json
import pymysql.cursors
from BayesianFilter import BayesianFilter
   
#Jason 형태의 설정파일을 읽어온다.
def readKEYWORDS(filename) :
    d = os.path.dirname(__file__) +'\\'
    with open(d+filename, encoding='utf8') as json_file:  
        data = json.load(json_file)
    return data

# 텍스트 학습 함수
def study(bf, content,category):
    bf.fit(content, category)
    return bf

# 예측
def predict(bf, msg):
    pre, scorelist = bf.predict(msg)
    # scorelist
    print(msg, "->결과 =", pre, ":", scorelist)
    return pre

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
   
def getInstagram_Data():
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
    ary_dic = []
    
    try:
        sql = 'select id, display_url, thumbnail_src, edge_media_to_caption, taken_at_timestamp, is_video'
        sql += ' from '
        sql += 'instagram'
            
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
            for i in range(cursor.rowcount):
                dic = {}
                content = cursor.fetchone()
                dic['id'] = content[0]
                dic['display_url'] = content[1]
                dic['thumbnail_src'] = content[2]
                dic['edge_media_to_caption'] = content[3]
                dic['taken_at_timestamp'] = content[4]
                dic['is_video'] = content[5]
                dic['flag'] = '정보'
                ary_dic.append(dic)
#               print(dic)
                i += 1
#        print(ary_dic)   
    finally:
        conn.close()
    return ary_dic

def getTwitter_Data():
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
    ary_dic = []
    
    try:
        sql = 'select uId, screen, txtId, date, text, urls'
        sql += ' from '
        sql += 'twitter'
            
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
            for i in range(cursor.rowcount):
                dic = {}
                content = cursor.fetchone()
                dic['uId'] = content[0]
                dic['screen'] = content[1]
                dic['txtId'] = content[2]
                dic['date'] = content[3]
                dic['text'] = content[4]
                dic['urls'] = content[5]
                dic['flag'] = '정보'
                ary_dic.append(dic)
#                print(dic)
                i += 1
#        print(ary_dic)   
    finally:
        conn.close()
    return ary_dic


def doInstagram(dic):
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
     
    try:
        tid = dic['id']
        display_url = dic['display_url']
        thumbnail_src = dic['thumbnail_src']
        edge_media_to_caption = dic['edge_media_to_caption']
        taken_at_timestamp = dic['taken_at_timestamp']
        is_video = dic['is_video']
        flag = dic['flag']

        if tid == None:
            tid = ''
        elif display_url == None:
            display_url = '#'
        elif thumbnail_src == None:
            thumbnail_src = '#'
        elif edge_media_to_caption == None:
            edge_media_to_caption = ''
        elif taken_at_timestamp == None:
            taken_at_timestamp = '0'
        elif is_video == None:
            is_video = ''
        elif flag == None:
            flag = '정보'

#        print(dic)
            
        with conn.cursor() as cursor:
            sql = 'INSERT INTO instagram '
            sql += '(id, display_url, thumbnail_src, edge_media_to_caption, taken_at_timestamp, is_video, flag) '
            sql += 'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            sql += 'ON DUPLICATE  KEY '
            sql += 'UPDATE id=%s, display_url=%s, thumbnail_src=%s, edge_media_to_caption=%s, '
            sql += 'taken_at_timestamp=%s, is_video=%s, flag=%s'
            cursor.execute(sql, (tid, display_url, thumbnail_src, edge_media_to_caption, taken_at_timestamp, is_video, flag,
                                 tid, display_url, thumbnail_src, edge_media_to_caption, taken_at_timestamp, is_video, flag))
            # print(cursor.description)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def doTwitter(dic):
    conn = pymysql.connect(host=maria_host,
            user=maria_id,
            password=maria_pw,
            db=maria_dbname,
            charset=maria_charset)
     
    try:
        uId = dic['uId']
        screen = dic['screen']
        txtId = dic['txtId']
        date = dic['date']
        text = dic['text']
        urls = dic['urls']
        flag = dic['flag']

        if uId == None:
            uId = ''
        elif screen == None:
            screen = '#'
        elif txtId == None:
            txtId = '#'
        elif date == None:
            date = '0'
        elif text == None:
            text = ''
        elif urls == None:
            urls = ''
        elif flag == None:
            flag = '정보'

#        print(dic)
            
        with conn.cursor() as cursor:
            sql = 'INSERT INTO twitter '
            sql += '(uId, screen, txtId, date, text, urls, flag) '
            sql += 'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            sql += 'ON DUPLICATE  KEY '
            sql += 'UPDATE uId=%s, screen=%s, txtId=%s, date=%s, '
            sql += 'text=%s, urls=%s, flag=%s'
            cursor.execute(sql, (uId, screen, txtId, date, text, urls, flag,
                                 uId, screen, txtId, date, text, urls, flag))
            # print(cursor.description)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


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

    dic = getTrained_Data('wiki','계룡산')
    # print(dic)

    # 필터 생성    
    bf = BayesianFilter()

    #필터의 규칙을 학습    
    for k, v in dic.items():
        study(bf, k, v)

    lst_insta = getInstagram_Data()
#    print(lst_insta)
    
    for i in range(len(lst_insta)):
        insta_dic = lst_insta[i]
        for k, v in insta_dic.items():
            if k=='edge_media_to_caption':
                insta_dic['flag']  = predict(bf, v)
        doInstagram(insta_dic)
#        print(insta_dic['id'],":", insta_dic['flag'])
            
    lst_twitt = getTwitter_Data()
    for i in range(len(lst_twitt)):
        twitt_dic = lst_twitt[i]
        for k, v in twitt_dic.items():
            if k=='text':
                twitt_dic['flag']  = predict(bf, v)
        doTwitter(twitt_dic)

    # # 예측
    # predict(bf, "계룡산 정도령")
    # predict(bf, "동학사 정상에서 고라니를 봤다")
    # predict(bf, "계룡산의 정상에서 고라니를 봤다")
    # predict(bf, "갑사의 정상에서 한나씨를 봤다")
    # predict(bf, "구봉산 전망대서 막걸리 먹지마라. 박아지다.")
    # predict(bf, "계룡산의 명소 선녀보살")


    # # 예측
    # predict(bf, "계룡산의 선녀보살")
    # predict(bf, "장태산 정상의 매점은 박아지가 너무 심하다.")
    # predict(bf, "계룡산노래방 아가씨 존나 못생김")
    # predict(bf, "만개한 계룡산 벚꽃축제 2018년 4월6-15 http://dlvr.it/QNZMvG")
    # predict(bf, "마 그카다가 천운으로 덕 많고 공이 깊으신 계룡산 도양보살님을 만나가, 지금은 마 육천전안 신령님들 모시면서 무해무탈 잘 지내고 있습니다.")