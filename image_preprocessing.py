# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2018/11/23 15:34
# @File  : handle_pic

import os
from PIL import Image
import random

test_img_path = os.path.join(os.path.dirname(__file__), 'images/test_img/pic0_0.png')
file_name = random.randint(10000, 99999)

def get_img(pic_path):
    image = Image.open(pic_path)
    image = image.convert('L')
    table = get_bin_table()
    im = image.point(table, '1')
    return im


def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)

    return table


def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


def img_pixel_2_file(im):
    """
    将图片按像素值保存进文本
    :param im:
    :return:
    """
    with open('./images/text_img/{}.txt'.format(file_name), 'w') as f:
        for y in range(im.height):
            for x in range(im.width):
                count = sum_9_region(im, x, y)
                if count < 3:
                    f.write('1')
                else:
                    f.write(str(im.getpixel((x, y))))
            f.write('\n')


def img_2_matric(im):
    """
    将图像转化为二维像素矩阵
    :param im:
    :return:
    """
    out_arr = []
    for x in range(im.width):
        in_arr = []
        for y in range(im.height):
            count = sum_9_region(im, x, y)
            if count < 3:
                in_arr.append(1)
            else:
                in_arr.append(im.getpixel((x, y)))
        out_arr.append(in_arr)

    return out_arr


def max_4_value_pair(arr_2d):
    """
    返回
    :param arr_2d: 二维数组，内层为2个值的列表
    :return: 差值最大的四个
    """
    extremum_list = []
    max_4_pairs = []
    for arr in arr_2d:
        v = arr[1] - arr[0]
        extremum_list.append(v)
    extremum_list.sort(reverse=True)
    max_4_values = extremum_list[:4]
    for arr in arr_2d:
        if arr[1] - arr[0] in max_4_values:
            max_4_pairs.append(arr)

    return max_4_pairs


def get_split_image_coordinate(im):
    """
    纵向切割图片
    :param img:
    :return: 距离最大的四个（起始值，结束值）对
    """
    img_arr = img_2_matric(im)
    # data = pd.DataFrame(img_arr)
    records = []
    record = []
    flag = 0
    flag2 = 0
    for i, line in enumerate(img_arr):
        c = sum(line) / len(line)
        if not record and not c:
            record.append(i)
            # flag = 1
        if record and c:
            record.append(i)
            flag = 1
            flag2 = 1
        if flag:
            records.append(record)
        if flag2:
            record = []
        flag = 0
        flag2 = 0

    if len(records) == 4:
        return records
    else:
        return max_4_value_pair(records)


def crop_image(im, coordinate):
    im_split_arr = []
    im_split = im.crop(coordinate)
    im_split_arr.append(im_split)


def crop_img(im, coordinates):
    pass


def main():

    im = get_img(test_img_path)
    # im.show()
    img_pixel_2_file(im)
    # img_arr = img_2_matric(im)
    coordinates = get_split_image_coordinate(im)
    im_split_arr = []
    for i, coord in enumerate(coordinates):
        co = (coord[0], 0, coord[1], im.size[1])
        im_s = im.crop(co)
        im_s = im_s.resize((10, 25))
        # im_s.show()
        im_s.save('./images/split_img/{}_{}.png'.format(file_name, i))
        im_split_arr.append(im_s)

    print(coordinates)


if __name__ == '__main__':
    main()
