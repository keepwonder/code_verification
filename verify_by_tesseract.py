# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2018/11/22 17:25
# @File  : verify_by_tesseract

import os
import random
import pytesseract

random_pic = 'pic{}_{}.png'.format(random.randint(0, 100), random.randint(0, 100))
img_path = os.path.join(os.path.dirname(__file__), 'images/src_img/{}'.format(random_pic))
code = pytesseract.image_to_string(img_path)
print(random_pic, code)
