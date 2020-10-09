# -*- coding: utf-8 -*-

from traceback import print_exc

from cv2 import COLOR_BGR2GRAY, cvtColor, imread
from pyperclip import copy
from PyQt5.QtWidgets import QApplication
from skimage.measure import compare_ssim

from API import (ALAPI, baidu, baidu_orc, caiyun, caiyunAPI, jinshan, tencent,
                 yeekit, youdao)


# 截图
def image_cut(window, data):

    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    try:
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(
            QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save('.\\config\\image.jpg')

    except Exception:
        print_exc()


# 判断图片相似度
def compare_image(imageA, imageB):

    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)

    return score


# 翻译主函数
def translate(window, data):

    text = window.translateText.toPlainText()
    if text[:5] == "团子翻译器" or (not text[:1]):
        score = 0.97
        image_cut(window, data)
    else:
        imageA = imread('.\\config\\image.jpg')
        image_cut(window, data)
        imageB = imread('.\\config\\image.jpg')
        try:
            score = compare_image(imageA, imageB)
        except Exception:
            score = 0.97

    if score < 0.98:

        sign, original = baidu_orc(data)

        if sign and original and (original != window.original):

            # 过滤不需要加入翻译的字符
            try:
                with open(".\\config\\filter.txt") as file:
                    char = file.read()
                char.split('''&''')
                for ch in char:
                    original = original.replace(ch, '')
            except Exception:
                print_exc()

            # 是否复制到剪贴板
            if data["showClipboard"] == 'True':
                copy(original)

            youdaoUse = data["youdaoUse"]  # 有道
            caiyunUse = data["caiyunUse"]  # 公共彩云
            jinshanUse = data["jinshanUse"]  # 金山
            yeekitUse = data["yeekitUse"]  # yeekit
            alapiUse = data["alapiUse"]  # alapi

            baiduUse = data["baiduUse"]  # 百度私人版
            tencentUse = data["tencentUse"]  # 腾讯私人版
            caiyunPrivateUse = data["caiyunPrivateUse"]  # 私人彩云

            yeekitLanguage = data["yeekitLanguage"]  # yeekit翻译语种

            # 有道
            if youdaoUse == "True":
                result_youdao = youdao(original)
            else:
                result_youdao = ''
            # 公共彩云
            if caiyunUse == "True":
                result_caiyun = caiyun(original)
            else:
                result_caiyun = ''
            # 金山
            if jinshanUse == "True":
                result_jinshan = jinshan(original)
            else:
                result_jinshan = ''
            # yeekit
            if yeekitUse == "True":
                result_yeekit = yeekit(original, yeekitLanguage)
            else:
                result_yeekit = ''
            # alapi
            if alapiUse == "True":
                result_alapi = ALAPI(original)
            else:
                result_alapi = ''

            # 百度私人版
            if baiduUse == "True":
                result_baidu = baidu(original, data)
            else:
                result_baidu = ''
            # 腾讯私人版
            if tencentUse == "True":
                result_tencent = tencent(original, data)
            else:
                result_tencent = ''
            # 彩云私人版
            if caiyunPrivateUse == "True":
                result_caiyunPrivate = caiyunAPI(original, data)
            else:
                result_caiyunPrivate = ''

        else:
            result_youdao = ''
            result_caiyun = ''
            result_jinshan = ''
            result_yeekit = ''
            result_alapi = ''
            result_baidu = ''
            result_tencent = ''
            result_caiyunPrivate = ''

    else:
        result_youdao = ''
        result_caiyun = ''
        result_jinshan = ''
        result_yeekit = ''
        result_alapi = ''
        result_baidu = ''
        result_tencent = ''
        result_caiyunPrivate = ''
        original = ''
        sign = True

    result = dict()
    result["youdao"] = result_youdao
    result["caiyun"] = result_caiyun
    result["jinshan"] = result_jinshan
    result["yeekit"] = result_yeekit
    result["alapi"] = result_alapi
    result["baidu"] = result_baidu
    result["tencent"] = result_tencent
    result["caiyunPrivate"] = result_caiyunPrivate
    result["original"] = original
    result["sign"] = sign

    return result
