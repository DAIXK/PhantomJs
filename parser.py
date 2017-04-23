#coding:utf-8
from PIL import Image
import pytesseract
import sys
import requests
import os
import pickle
import time
from selenium import webdriver
from lxml import etree
import urllib
import xlrd
import json

# '13632918420'
def get_cookies():
    url = 'https://aso100.com/account/signin'
    drive = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
    drive.get(url)
    drive.find_element_by_id('username').send_keys('yourname')
    drive.find_element_by_id('password').send_keys('yourpwd')
    drive.save_screenshot('aso100.png')
    code = input('请输入验证码>>>>')
    drive.find_element_by_id('code').send_keys(code)
    drive.find_element_by_id('submit').click()
    time.sleep(5)
    cookie_list = drive.get_cookies()
    cookie_dict = {}
    for cookie in cookie_list:
        cookie_dict[cookie['name']] = cookie['value']

    drive.quit()
    # print(cookie_dict)
    return cookie_dict





def aso100(cookies,string):
    hotnumber_dict = {}
    data = urllib.parse.urlencode({'keyword': string})
    # url = 'https://aso100.com/trend/keywordExtend'
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res = requests.get(url=url, cookies=cookies, headers=header,params=data,)
    # print(res.url)
    # print(res.text)
    tree = etree.HTML(res.text)
    try:
        account = tree.xpath('//li/a/span[@class="account-email"]')[0].text
    except Exception:
        account = 0
    if account:
        print('登录成功'+account)
    else:
        print('登录失败')
    try:
        hotnumber_dict['name'] = tree.xpath("//tbody/tr[1]/td[2]/a")[0].text
        hotnumber_dict['num'] = tree.xpath("//tbody/tr[1]/td[3]/a")[0].text
        return hotnumber_dict

    except Exception:
        hotnumber_dict['name'],hotnumber_dict['num'] = '不匹配',''
        return hotnumber_dict

def aso100(filename):
    aso100_table = xlrd.open_workbook(filename)
    aso100_table = aso100_table.sheet_by_index(0)
    nrows = aso100_table.nrows
    aso100_dict = {}
    for row in range(8,nrows):
        aso100_dict[aso100_table.row_values(row)[1]] = {
            '排名': aso100_table.row_values(row)[2],
            '指数': aso100_table.row_values(row)[4],
            '结果数':aso100_table.row_values(row)[5],
        }
    return aso100_dict

def cqaso(string):
    url = 'http://backend.cqaso.com/search/mining'
    data = urllib.parse.urlencode({'word': string,'country':'CN'})
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        'Connection':'close'}

    res = requests.get(url=url, headers=header, params=data)
    # print(res.headers)
    res = json.loads(res.text)
    # print(res)
    return res['contents']
