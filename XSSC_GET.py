# -*- coding: UTF-8 -*-
import requests
import XSSC
import time
imga = []
imgb = []
opta = []
optb = []
s = requests.session()
XSSC.exam_login(s)
for i in range(0,50):
    time.sleep(5)
    tmp_exam_url = XSSC.exam_open(s)
    tmpimga, tmpimgb = XSSC.image_url_get(s, tmp_exam_url)
    imga.extend(tmpimga)
    imgb.extend(tmpimgb)
    tmpopta,tmpoptb=XSSC.options_get(s,tmp_exam_url)
    opta.extend(tmpopta)
    optb.extend(tmpoptb)
    XSSC.exam_close(s,tmp_exam_url)
XSSC.image_save(imga,0,imgb,0)
XSSC.option_save(opta,0,optb,0)
