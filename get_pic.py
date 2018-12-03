# -*- coding:utf-8 -*-
# @Author: Jone Chiang
# @Date  : 2018/11/22 16:07
# @File  : get_pic

import random
import urllib
import threading
import time


class FetchCodePic(threading.Thread):
    def __init__(self, idx):
        super(FetchCodePic, self).__init__()
        self.idx = idx

    def run(self):
        for i in range(100):
            url = 'http://www.gxgs.gov.cn:8103/WSSBSL/do_index_NsrglLogin_yzm.action?wssbtid={}'.format(random.randint(100000, 999999))
            urllib.urlretrieve(url, './images/src_img/pic{}_{}.png'.format(self.idx, i))


if __name__ == '__main__':
    begin_t = time.time()
    thread_list = []
    for i in range(100):
        t = FetchCodePic(i)
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    print("共花费{}s".format(time.time() - begin_t))

