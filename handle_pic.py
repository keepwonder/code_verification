# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2018/11/23 15:34
# @File  : handle_pic

import os
import random
from PIL import Image
import pytesseract

random_pic = 'pic{}_{}.png'.format(random.randint(0, 100), random.randint(0, 100))
img_path = os.path.join(os.path.dirname(__file__), 'images/src_img/{}'.format(random_pic))
# img_path = './images/src_img/pic22_66.png'
test_img_path = os.path.join(os.path.dirname(__file__), 'images/test_img')


def load_pic(img_path, is_gray=True):
    if is_gray:
        im = Image.open(img_path).convert('L')
    else:
        im = Image.open(img_path)
    return im


def read_captcha(path):
    image_array = []
    image_label = []
    file_list = os.listdir(path)    # 获取captcha文件
    for file in file_list:
        image = Image.open(path + '/' + file)   # 打开图片
        file_name = file.split(".")[0]  # 获取文件名，此为图片标签
        image_array.append(image)
        image_label.append(file_name)
    return image_array, image_label


def image_transfer(image_arry):
    """
    :param image_arry:图像list，每个元素为一副图像
    :return: image_clean:清理过后的图像list
    """
    threshold_grey = 120
    image_clean = []
    for i, image in enumerate(image_arry):
        image = image.convert('L')  # 转换为灰度图像，即RGB通道从3变为1
        im2 = Image.new("L", image.size, 255)
        for y in range(image.size[1]):  # 遍历所有像素，将灰度超过阈值的像素转变为255（白）
            for x in range(image.size[0]):
                pix = image.getpixel((x, y))
                if int(pix) > threshold_grey:  # 灰度阈值
                    im2.putpixel((x, y), pix)
                else:
                    im2.putpixel((x, y), 255)
        im2.show()
        image_clean.append(im2)

    return image_clean


def img_2_bin(img, threshold=120):
    """
    图片二值化
    :param img:
    :param threshold:
    :return:
    """
    img = img.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return img.point(table, '1')


def img_by_ocr(img):
    code = pytesseract.image_to_string(img)
    print(code)


if __name__ == '__main__':
    # img_2_bin(load_pic(img_path)).show()
    image_array, image_label = read_captcha(test_img_path)
    print(image_array)
    print(image_label)

    image_clean = image_transfer(image_array)
    print(image_clean)
    print('over')
