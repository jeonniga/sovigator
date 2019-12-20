# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:12:42 2018

pip install qrcode

@author: seedp
"""

import json
import qrcode
from urllib import parse

def mkQR(qr, url, fname):
    qr.add_data(url)
    print(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(fname)
    
def readKEYWORDS(filename) :
    f = open(filename, 'rt', encoding='UTF8')
    js = json.loads(f.read() ,encoding='utf-8')
    f.close()
    return js
    
# Create qr code instance
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)

if __name__ == "__main__":
    SETTING = readKEYWORDS("config.json")
        
    for k, v in SETTING.items():
        service_url = v['service_url']
        app_path = v['app_path']
        banner_img_path = v['banner_img_path']
    
   
    KEYWORDS = readKEYWORDS("twitter.json")
    for k, v in KEYWORDS.items():
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        ) 
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=twitter&keyword="+parse.quote(v['keyword']),
             banner_img_path + "twitter_"+v['keyword']+".jpg")
    
      
    KEYWORDS = readKEYWORDS("wiki.json")
    for k, v in KEYWORDS.items():   
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        ) 
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=wikipedia&keyword="+parse.quote(v['keyword']),
             banner_img_path + "wikipedia_"+v['keyword']+".jpg")
    
    KEYWORDS = readKEYWORDS("instagram.json")
    for k, v in KEYWORDS.items():  
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        )         
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=instagram&keyword="+parse.quote(v['keyword']),
             banner_img_path + "instagram_"+v['keyword']+".jpg")
        
 
    KEYWORDS = readKEYWORDS("facebook.json")
    for k, v in KEYWORDS.items():   
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        )  
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=facebook&keyword="+parse.quote(v['keyword']),
             banner_img_path + "facebook_"+v['keyword']+".jpg")

    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        )  
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=naver_blog&keyword="+parse.quote(v['keyword']),
             banner_img_path + "naverblog_"+v['keyword']+".jpg")

    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        )  
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=naver_news&keyword="+parse.quote(v['keyword']),
             banner_img_path + "navernews_"+v['keyword']+".jpg")
        
    KEYWORDS = readKEYWORDS("naver.json")
    for k, v in KEYWORDS.items():   
        qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
        )  
        mkQR(qr, 
             service_url + "/users/maria_get_html?id=total_info&keyword="+parse.quote(v['keyword']),
             banner_img_path + "totalinfo_"+v['keyword']+".jpg")


