# -*- coding: UTF-8 -*-
import requests
import re
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

def exam_login(s):
    login_url = 'https://xgb.zjuqsc.com/exam/user/login'
    form_data = {
        'stuid': '******',
        'password': '******',
        'submit': 'true'
    }
    response = s.post(login_url, data=form_data, headers=header)


def exam_open(s):
    url = 'https://xgb.zjuqsc.com/exam/'
    response = s.get(url,headers=header)
    # print(response.text)
    bs = BeautifulSoup(response.text, "lxml")
    exam_url = bs.find('table', {'id': "exam_list"}).find('a', {"href": re.compile(".*\/view/go/.*")}).attrs['href']
    exam_url = exam_url.replace('go', 'exam')
    return exam_url


def image_url_get(s,exam_url):
    judge_images_url=[]
    select_images_url=[]
    pagechange = "?p={:}"
    tmp_count = 0
    for i in range(1, 6):
        page = s.get(exam_url + pagechange.format(i), headers=header)
        # print(page.text)
        bs0 = BeautifulSoup(page.text, "lxml")
        tmp = bs0.find_all('img', {'class': 'hidden-sm hidden-xs'})
        for single_url in tmp:
            tmp_count += 1
            if tmp_count <= 15:
                judge_images_url.append(single_url.attrs['src'])
            else:
                select_images_url.append(single_url.attrs['src'])
    return judge_images_url, select_images_url


def options_get(s,exam_url):
    judge_options=[]
    select_options=[]
    pagechange = "?p={:}"
    tmp_count = 0
    for i in range(1, 6):
        page = s.get(exam_url + pagechange.format(i), headers=header)
        # print(page.text)
        bs0 = BeautifulSoup(page.text, "lxml")
        tmp = bs0.find_all('fieldset')
        for single_option_set in tmp:
            tmp_count += 1
            if tmp_count <= 15:
                labels = single_option_set.find_all('label')
                tmp_set = []
                for tt in labels:
                    tmp_set.append(tt.get_text().replace(' ',''))
                judge_options.append(tmp_set)
            else:
                labels = single_option_set.find_all('label')
                tmp_set = []
                for tt in labels:
                    tmp_set.append(tt.get_text().replace(' ',''))
                select_options.append(tmp_set)
    return judge_options, select_options


def image_save(judge_images_url,judge_count,select_images_url,select_count):
    judge_example_address = 'E:/xssc/judge/{:}.png'
    select_example_address = 'E:/xssc/select/{:}.png'
    for tmp in judge_images_url:
        judge_count += 1
        res = requests.get(tmp)
        image = Image.open(BytesIO(res.content))
        image.save(judge_example_address.format(judge_count))
    for tmp in select_images_url:
        select_count += 1
        res = requests.get(tmp)
        image = Image.open(BytesIO(res.content))
        image.save(select_example_address.format(select_count))


def option_save(judge_options,judge_count,select_options,select_count):
    judge_example_address = 'E:/xssc/judge/{:}.txt'
    select_example_address = 'E:/xssc/select/{:}.txt'
    for tmp in judge_options:
        judge_count += 1
        tt = open(judge_example_address.format(judge_count),'w')
        for i in tmp:
            tt.write(i+'\n')
        tt.close()
    for tmp in select_options:
        select_count += 1
        tt = open(select_example_address.format(select_count),'w')
        for i in tmp:
            tt.write(i+'\n')
        tt.close()


def exam_close(s,exam_url):
    close_url = exam_url.replace('view/exam','api/update')+'?submit=yes'
    form_data = {
        'data':'\"{}\"'
    }
    s.post(close_url,data = form_data,headers = header)