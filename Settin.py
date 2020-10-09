# -*- coding: utf-8 -*-

import json
import webbrowser
from os import startfile

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from API import MessageBox, get_Access_Token
from ScreenRate import get_screen_rate


class SettinInterface(QWidget):

    def __init__(self, screen_scale_rate):

        super(SettinInterface, self).__init__()

        if 1.01 <= screen_scale_rate <= 1.49:
            self.rate = 1.25
            self.px = 80
            self.image_sign = 2
        else:
            self.rate = 1
            self.px = 75
            self.image_sign = 1

        self.get_settin()
        self.setupUi()

    def setupUi(self):

        # 窗口尺寸及不可拉伸
        self.resize(404*self.rate, 576*self.rate)
        self.setMinimumSize(QtCore.QSize(404*self.rate, 576*self.rate))
        self.setMaximumSize(QtCore.QSize(404*self.rate, 576*self.rate))
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        # 窗口标题
        self.setWindowTitle("团子翻译器")

        # 窗口图标
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("./config/图标.ico"),
                            QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(self.icon)

        # 顶部工具栏
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(
            QtCore.QRect(-2, 0, 410*self.rate, 580*self.rate))
        self.tabWidget.setCurrentIndex(0)

        # 工具栏样式
        self.tabWidget.setStyleSheet(
            "QTabBar::tab {""min-width:%dpx;"
            "background: rgba(255, 255, 255, 1);"
            "}"
            "QTabBar::tab:selected {""border-bottom: 2px solid #4796f0;""}"
            "QLabel{""background: transparent;""}"
            "QCheckBox{""background: transparent;""}" % (self.px)
        )

        # 工具栏1
        self.tab_1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_1, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), "API设定")

        # 此Label用于雾化工具栏1的背景图
        self.bgImage1 = QLabel(self.tab_1)
        self.bgImage1.setGeometry(QRect(0, 0, 408*self.rate, 578*self.rate))
        self.bgImage1.setStyleSheet("background: rgba(255, 255, 255, 0.3);")

        # OCR API标签
        self.OCR_label_1 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_1.setGeometry(QtCore.QRect(
            20*self.rate, 20*self.rate, 340*self.rate, 16*self.rate))
        self.OCR_label_1.setText(
            "<font color=red>（必填）</font><font >OCR API：用于识别要翻译的文字</font>")

        # OCR API Key输入框
        self.OCR_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Key_Text.setGeometry(QtCore.QRect(
            30*self.rate, 45*self.rate, 330*self.rate, 22*self.rate))
        self.OCR_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                        "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.OCR_Key_Text.setPlaceholderText("OCR API Key")
        self.OCR_Key_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setPlainText(self.OCR_Key)

        # OCR API Key输入框右侧红点标签
        self.OCR_label_4 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_4.setGeometry(QtCore.QRect(
            370*self.rate, 50*self.rate, 16*self.rate, 16*self.rate))
        self.OCR_label_4.setStyleSheet("color: #f00000")
        self.OCR_label_4.setText("*")

        # OCR API Secret输入框
        self.OCR_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Secret_Text.setGeometry(QtCore.QRect(
            30*self.rate, 70*self.rate, 330*self.rate, 22*self.rate))
        self.OCR_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                           "border-width:0; border-style:outset;"
                                           "border-bottom: 2px solid #92a8d1;""}"
                                           "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.OCR_Secret_Text.setPlaceholderText("OCR API Secret")
        self.OCR_Secret_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setPlainText(self.OCR_Secret)

        # OCR API Secret输入框右侧红点标签
        self.OCR_label_5 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_5.setGeometry(QtCore.QRect(
            370*self.rate, 75*self.rate, 16*self.rate, 16*self.rate))
        self.OCR_label_5.setStyleSheet("color: #f00000")
        self.OCR_label_5.setText("*")

        # 百度翻译API标签
        self.baiduAPI_label_1 = QtWidgets.QLabel(self.tab_1)
        self.baiduAPI_label_1.setGeometry(QtCore.QRect(
            20*self.rate, 140*self.rate, 281*self.rate, 16*self.rate))
        self.baiduAPI_label_1.setText("（选填）百度翻译 API：每月额度200万字符")

        # 百度翻译API APP ID输入框
        self.baidu_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Key_Text.setGeometry(QtCore.QRect(
            30*self.rate, 165*self.rate, 330*self.rate, 22*self.rate))
        self.baidu_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                          "border-width:0; border-style:outset;"
                                          "border-bottom: 2px solid #92a8d1;""}"
                                          "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.baidu_Key_Text.setPlaceholderText("百度翻译API APP ID")
        self.baidu_Key_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setPlainText(self.baidu_Key)

        # 百度翻译API 密钥输入框
        self.baidu_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Secret_Text.setGeometry(QtCore.QRect(
            30*self.rate, 190*self.rate, 330*self.rate, 22*self.rate))
        self.baidu_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                             "border-width:0; border-style:outset;"
                                             "border-bottom: 2px solid #92a8d1;""}"
                                             "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.baidu_Secret_Text.setPlaceholderText("百度翻译API 密钥")
        self.baidu_Secret_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setPlainText(self.baidu_Secret)

        # 腾讯翻译API标签
        self.TencentAPI_laber_1 = QtWidgets.QLabel(self.tab_1)
        self.TencentAPI_laber_1.setGeometry(QtCore.QRect(
            20*self.rate, 260*self.rate, 281*self.rate, 16*self.rate))
        self.TencentAPI_laber_1.setText("（选填）腾讯翻译 API：每月额度500万字符")

        # 腾讯翻译API Secretld输入框
        self.tencent_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Key_Text.setGeometry(QtCore.QRect(
            30*self.rate, 285*self.rate, 330*self.rate, 22*self.rate))
        self.tencent_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                            "border-width:0; border-style:outset;"
                                            "border-bottom: 2px solid #92a8d1;""}"
                                            "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.tencent_Key_Text.setPlaceholderText("腾讯翻译API Secretld")
        self.tencent_Key_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setPlainText(self.tencent_Key)

        # 腾讯翻译API SecretKey输入框
        self.tencent_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Secret_Text.setGeometry(QtCore.QRect(
            30*self.rate, 310*self.rate, 330*self.rate, 22*self.rate))
        self.tencent_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                               "border-width:0; border-style:outset;"
                                               "border-bottom: 2px solid #92a8d1;""}"
                                               "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.tencent_Secret_Text.setPlaceholderText("腾讯翻译API SecretKey")
        self.tencent_Secret_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setPlainText(self.tencent_Secret)

        # 彩云翻译API标签
        self.caiyunAPI_laber_1 = QtWidgets.QLabel(self.tab_1)
        self.caiyunAPI_laber_1.setGeometry(QtCore.QRect(
            20*self.rate, 380*self.rate, 281*self.rate, 16*self.rate))
        self.caiyunAPI_laber_1.setText("（选填）彩云翻译 API：每月额度100万字符")

        # 彩云翻译API token输入框
        self.caiyun_token_Text = QtWidgets.QTextEdit(self.tab_1)
        self.caiyun_token_Text.setGeometry(QtCore.QRect(
            30*self.rate, 405*self.rate, 330*self.rate, 22*self.rate))
        self.caiyun_token_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                             "border-width:0; border-style:outset;"
                                             "border-bottom: 2px solid #92a8d1;""}"
                                             "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.caiyun_token_Text.setPlaceholderText("彩云小泽API token")
        self.caiyun_token_Text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.caiyun_token_Text.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.caiyun_token_Text.setPlainText(self.caiyun_token)

        # 工具栏2
        self.tab_2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "翻译源设定")

        # 此Label用于雾化工具栏2的背景图
        self.bgImage2 = QLabel(self.tab_2)
        self.bgImage2.setGeometry(QRect(0, 0, 408*self.rate, 578*self.rate))
        self.bgImage2.setStyleSheet("background: rgba(255, 255, 255, 0.3);")

        # 公共翻译接口标签
        self.translateSource_label_2 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_2.setGeometry(QtCore.QRect(
            30*self.rate, 85*self.rate, 340*self.rate, 16*self.rate))
        self.translateSource_label_2.setText("公共接口：可直接使用，但可能会抽风")

        # 有道翻译checkBox
        self.youdao_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.youdao_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 120*self.rate, 80*self.rate, 16*self.rate))
        self.youdao_checkBox.setChecked(self.youdaoUse)
        self.youdao_checkBox.setText("有道翻译")

        # 彩云翻译checkBox
        self.caiyun_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.caiyun_checkBox.setGeometry(QtCore.QRect(
            160*self.rate, 120*self.rate, 80*self.rate, 16*self.rate))
        self.caiyun_checkBox.setChecked(self.caiyunUse)
        self.caiyun_checkBox.setText("公共彩云")

        # 金山翻译checkBox
        self.jinshan_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.jinshan_checkBox.setGeometry(QtCore.QRect(
            290*self.rate, 120*self.rate, 80*self.rate, 16*self.rate))
        self.jinshan_checkBox.setChecked(self.jinshanUse)
        self.jinshan_checkBox.setText("金山词霸")

        # yeekit翻译checkBox
        self.yeekit_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.yeekit_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 155*self.rate, 91*self.rate, 16*self.rate))
        self.yeekit_checkBox.setChecked(self.yeekitUse)
        self.yeekit_checkBox.setText("yeekit")

        # ALAPI翻译checkBox
        self.ALAPI_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.ALAPI_checkBox.setGeometry(QtCore.QRect(
            160*self.rate, 155*self.rate, 80*self.rate, 16*self.rate))
        self.ALAPI_checkBox.setChecked(self.alapiUse)
        self.ALAPI_checkBox.setText("ALAPI")

        # 私人翻译接口标签
        self.translateSource_label_3 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_3.setGeometry(QtCore.QRect(
            30*self.rate, 315*self.rate, 271*self.rate, 16*self.rate))
        self.translateSource_label_3.setText("私人API：使用稳定，但需注册后才可使用")

        # 百度翻译私人版checkBox
        self.baidu_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.baidu_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 350*self.rate, 80*self.rate, 16*self.rate))
        self.baidu_checkBox.setChecked(self.baiduUse)
        self.baidu_checkBox.setText("私人百度")

        # 腾讯翻译私人版checkBox
        self.tencent_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.tencent_checkBox.setGeometry(QtCore.QRect(
            160*self.rate, 350*self.rate, 80*self.rate, 16*self.rate))
        self.tencent_checkBox.setChecked(self.tencentUse)
        self.tencent_checkBox.setText("私人腾讯")

        # 彩云翻译私人版checkBox
        self.caiyunPrivate_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.caiyunPrivate_checkBox.setGeometry(QtCore.QRect(
            290*self.rate, 350*self.rate, 80*self.rate, 16*self.rate))
        self.caiyunPrivate_checkBox.setChecked(self.caiyunPrivateUse)
        self.caiyunPrivate_checkBox.setText("私人彩云")

        # 翻译语种标签
        self.translateSource_label_6 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_6.setGeometry(QtCore.QRect(
            30*self.rate, 395*self.rate, 151*self.rate, 16*self.rate))
        self.translateSource_label_6.setText("选择你要翻译的原语言：")

        # 翻译语种comboBox
        self.language_comboBox = QtWidgets.QComboBox(self.tab_2)
        self.language_comboBox.setGeometry(QtCore.QRect(
            195*self.rate, 393*self.rate, 131*self.rate, 22*self.rate))
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.setItemText(0, "日语（Japanese）")
        self.language_comboBox.setItemText(1, "英语（English）")
        self.language_comboBox.setItemText(2, "韩语（Korean）")
        self.language_comboBox.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4);")
        self.language_comboBox.setCurrentIndex(self.language)

        # 自动模式速率标签1
        self.translateMode_label_1 = QtWidgets.QLabel(self.tab_2)
        self.translateMode_label_1.setGeometry(QtCore.QRect(
            30*self.rate, 440*self.rate, 111*self.rate, 16*self.rate))
        self.translateMode_label_1.setText("设定自动翻译时每")

        # 自动模式速率设定
        self.autoSpeed_spinBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.autoSpeed_spinBox.setGeometry(QtCore.QRect(
            155*self.rate, 435*self.rate, 45*self.rate, 25*self.rate))
        self.autoSpeed_spinBox.setDecimals(1)
        self.autoSpeed_spinBox.setMinimum(1.0)
        self.autoSpeed_spinBox.setMaximum(15.0)
        self.autoSpeed_spinBox.setSingleStep(0.1)
        self.autoSpeed_spinBox.setStyleSheet("background: transparent;")
        self.autoSpeed_spinBox.setValue(self.translateSpeed)

        # 自动模式速率标签2
        self.translateMode_label_2 = QtWidgets.QLabel(self.tab_2)
        self.translateMode_label_2.setGeometry(QtCore.QRect(
            215*self.rate, 440*self.rate, 101*self.rate, 16*self.rate))
        self.translateMode_label_2.setText("秒刷新一次翻译")

        # 工具栏3
        self.tab_3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "翻译样式")

        # 此Label用于雾化工具栏3的背景图
        self.bgImage3 = QLabel(self.tab_3)
        self.bgImage3.setGeometry(QRect(0, 0, 408*self.rate, 578*self.rate))
        self.bgImage3.setStyleSheet("background: rgba(255, 255, 255, 0.3);")

        # 翻译字体颜色设定标签
        self.colour_label = QtWidgets.QLabel(self.tab_3)
        self.colour_label.setGeometry(QtCore.QRect(
            30*self.rate, 20*self.rate, 340*self.rate, 16*self.rate))
        self.colour_label.setText("设定不同翻译源翻译时的文字颜色：")

        # 有道翻译颜色按钮
        self.youdaoColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.youdaoColour_toolButton.setGeometry(QtCore.QRect(
            30*self.rate, 55*self.rate, 71*self.rate, 25*self.rate))
        self.youdaoColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.youdaoColor))
        self.youdaoColour_toolButton.clicked.connect(
            lambda: self.get_font_color(1))
        self.youdaoColour_toolButton.setText("有道翻译")

        # 公共彩云翻译颜色按钮
        self.caiyunColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.caiyunColour_toolButton.setGeometry(QtCore.QRect(
            160*self.rate, 55*self.rate, 71*self.rate, 25*self.rate))
        self.caiyunColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.caiyunColor))
        self.caiyunColour_toolButton.clicked.connect(
            lambda: self.get_font_color(2))
        self.caiyunColour_toolButton.setText("公共彩云")

        # 金山翻译颜色按钮
        self.jinshanColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.jinshanColour_toolButton.setGeometry(QtCore.QRect(
            290*self.rate, 55*self.rate, 71*self.rate, 25*self.rate))
        self.jinshanColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.jinshanColor))
        self.jinshanColour_toolButton.clicked.connect(
            lambda: self.get_font_color(3))
        self.jinshanColour_toolButton.setText("金山词霸")

        # yeekit翻译颜色按钮
        self.yeekitColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.yeekitColour_toolButton.setGeometry(QtCore.QRect(
            30*self.rate, 95*self.rate, 71*self.rate, 25*self.rate))
        self.yeekitColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.yeekitColor))
        self.yeekitColour_toolButton.clicked.connect(
            lambda: self.get_font_color(4))
        self.yeekitColour_toolButton.setText("yeekit")

        # alapi翻译颜色按钮
        self.alapiColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.alapiColour_toolButton.setGeometry(QtCore.QRect(
            160*self.rate, 95*self.rate, 71*self.rate, 25*self.rate))
        self.alapiColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.ALAPIColor))
        self.alapiColour_toolButton.clicked.connect(
            lambda: self.get_font_color(5))
        self.alapiColour_toolButton.setText("ALAPI")

        # 百度翻译私人版颜色按钮
        self.baiduColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.baiduColour_toolButton.setGeometry(QtCore.QRect(
            30*self.rate, 175*self.rate, 71*self.rate, 25*self.rate))
        self.baiduColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.baiduColor))
        self.baiduColour_toolButton.clicked.connect(
            lambda: self.get_font_color(10))
        self.baiduColour_toolButton.setText("私人百度")

        # 腾讯翻译私人版颜色按钮
        self.tencentColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.tencentColour_toolButton.setGeometry(QtCore.QRect(
            160*self.rate, 175*self.rate, 71*self.rate, 25*self.rate))
        self.tencentColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.tencentColor))
        self.tencentColour_toolButton.clicked.connect(
            lambda: self.get_font_color(11))
        self.tencentColour_toolButton.setText("私人腾讯")

        # 彩云翻译私人版颜色按钮
        self.caiyunPrivateColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.caiyunPrivateColour_toolButton.setGeometry(QtCore.QRect(
            290*self.rate, 175*self.rate, 71*self.rate, 25*self.rate))
        self.caiyunPrivateColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.caiyunPrivateColor))
        self.caiyunPrivateColour_toolButton.clicked.connect(
            lambda: self.get_font_color(12))
        self.caiyunPrivateColour_toolButton.setText("私人彩云")

        # 原文颜色按钮
        self.originalColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.originalColour_toolButton.setGeometry(QtCore.QRect(
            30*self.rate, 215*self.rate, 71*self.rate, 25*self.rate))
        self.originalColour_toolButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4); color: {};".format(self.originalColor))
        self.originalColour_toolButton.clicked.connect(
            lambda: self.get_font_color(13))
        self.originalColour_toolButton.setText("原  文")

        # 翻译字体大小设定标签
        self.fontSize_label = QtWidgets.QLabel(self.tab_3)
        self.fontSize_label.setGeometry(QtCore.QRect(
            30*self.rate, 265*self.rate, 145*self.rate, 16*self.rate))
        self.fontSize_label.setText("设定翻译时的文字大小：")

        # 翻译字体大小设定
        self.fontSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.fontSize_spinBox.setGeometry(QtCore.QRect(
            190*self.rate, 260*self.rate, 50*self.rate, 25*self.rate))
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(30)
        self.fontSize_spinBox.setStyleSheet(
            "background: rgba(255, 255, 255, 0)")
        self.fontSize_spinBox.setValue(self.fontSize)

        # 翻译字体样式设定标签
        self.translate_label = QtWidgets.QLabel(self.tab_3)
        self.translate_label.setGeometry(QtCore.QRect(
            30*self.rate, 305*self.rate, 145*self.rate, 20*self.rate))
        self.translate_label.setText("设定翻译时的字体样式：")

        # 翻译字体样式设定
        self.fontComboBox = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox.setGeometry(QtCore.QRect(
            190*self.rate, 305*self.rate, 151*self.rate, 25*self.rate))
        self.fontComboBox.setStyleSheet("background: rgba(255, 255, 255, 0.4)")
        self.fontComboBox.activated[str].connect(self.get_fontType)
        self.ComboBoxFont = QtGui.QFont(self.fontType)
        self.fontComboBox.setCurrentFont(self.ComboBoxFont)

        # 显示颜色样式checkBox
        self.showColorType_checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.showColorType_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 350*self.rate, 340*self.rate, 20*self.rate))
        self.showColorType_checkBox.setChecked(self.showColorType)
        self.showColorType_checkBox.setText("使用实心字体样式（不勾选则显示描边字体样式）")

        # 显示原文checkBox
        self.showOriginal_checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.showOriginal_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 390*self.rate, 340*self.rate, 20*self.rate))
        self.showOriginal_checkBox.setChecked(self.showOriginal)
        self.showOriginal_checkBox.setText("翻译时是否显示识别到的原文")

        # 原文自动复制到剪贴板checkBox
        self.Clipboard_checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.Clipboard_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 430*self.rate, 231*self.rate, 16*self.rate))
        self.Clipboard_checkBox.setChecked(self.showClipboard)
        self.Clipboard_checkBox.setText("启用将原文自动复制到剪贴板")

        # 工具栏4
        self.tab_4 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_4, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), "其他设定")

        # 此Label用于雾化工具栏4的背景图
        self.bgImage4 = QLabel(self.tab_4)
        self.bgImage4.setGeometry(QRect(0, 0, 408*self.rate, 578*self.rate))
        self.bgImage4.setStyleSheet("background: rgba(255, 255, 255, 0.3);")

        # 翻译框透明度设定标签1
        self.tab4_label_1 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_1.setGeometry(QtCore.QRect(
            30*self.rate, 60*self.rate, 211*self.rate, 16*self.rate))
        self.tab4_label_1.setText("调节翻译界面的背景透明度")

        # 翻译框透明度设定
        self.horizontalSlider = QtWidgets.QSlider(self.tab_4)
        self.horizontalSlider.setGeometry(QtCore.QRect(
            30*self.rate, 90*self.rate, 347*self.rate, 22*self.rate))
        self.horizontalSlider.setStyleSheet("background: transparent;")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setValue(self.horizontal)
        self.horizontalSlider.valueChanged.connect(self.get_horizontal)

        # 翻译框透明度设定标签2
        self.tab4_label_2 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_2.setGeometry(QtCore.QRect(
            30*self.rate, 120*self.rate, 61*self.rate, 20*self.rate))
        self.tab4_label_2.setObjectName("tab4_label_2")
        self.tab4_label_2.setText("完全透明")

        # 翻译框透明度设定标签3
        self.tab4_label_3 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_3.setGeometry(QtCore.QRect(
            310*self.rate, 120*self.rate, 71*self.rate, 20*self.rate))
        self.tab4_label_3.setText("完全不透明")

        # 竖排文字翻译模式checkBox
        self.TranslateRow_checkBox = QtWidgets.QCheckBox(self.tab_4)
        self.TranslateRow_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 165*self.rate, 340*self.rate, 16*self.rate))
        self.TranslateRow_checkBox.setChecked(self.showTranslateRow)
        self.TranslateRow_checkBox.setText("启用竖排文字翻译模式（额度为每天500次）")

        # 竖排高精度翻译模式checkBox
        self.highPrecision_checkBox = QtWidgets.QCheckBox(self.tab_4)
        self.highPrecision_checkBox.setGeometry(QtCore.QRect(
            30*self.rate, 200*self.rate, 340*self.rate, 16*self.rate))
        self.highPrecision_checkBox.setChecked(self.highPrecision)
        self.highPrecision_checkBox.setText("启用高精度翻译模式（额度为每天500次）")

        # 高精度模式额度说明标签
        self.highPrecisionlabel = QtWidgets.QLabel(self.tab_4)
        self.highPrecisionlabel.setGeometry(QtCore.QRect(
            30*self.rate, 225*self.rate, 340*self.rate, 20*self.rate))
        self.highPrecisionlabel.setStyleSheet("color: #f00000")
        self.highPrecisionlabel.setText("* 高精度和竖排文字翻译模式共享每天500次的额度")

        # 设置保存按钮
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setGeometry(QtCore.QRect(
            85*self.rate, 515*self.rate, 90*self.rate, 30*self.rate))
        self.SaveButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4);font: 12pt;")
        self.SaveButton.setText("保存设置")

        # 设置返回按钮
        self.CancelButton = QtWidgets.QPushButton(self)
        self.CancelButton.setGeometry(QtCore.QRect(
            232*self.rate, 515*self.rate, 90*self.rate, 30*self.rate))
        self.CancelButton.setStyleSheet(
            "background: rgba(255, 255, 255, 0.4);font: 12pt")
        self.CancelButton.setText("退出")

    def get_settin(self):  # 获取所有预设值

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 获取各翻译源颜色预设值
        self.youdaoColor = self.data["fontColor"]["youdao"]
        self.caiyunColor = self.data["fontColor"]["caiyun"]
        self.jinshanColor = self.data["fontColor"]["jinshan"]
        self.yeekitColor = self.data["fontColor"]["yeekit"]
        self.ALAPIColor = self.data["fontColor"]["ALAPI"]
        self.baiduwebColor = self.data["fontColor"]["baiduweb"]
        self.tencentwebColor = self.data["fontColor"]["tencentweb"]
        self.googleColor = self.data["fontColor"]["google"]
        self.BingColor = self.data["fontColor"]["Bing"]
        self.baiduColor = self.data["fontColor"]["baidu"]
        self.tencentColor = self.data["fontColor"]["tencent"]
        self.caiyunPrivateColor = self.data["fontColor"]["caiyunPrivate"]
        self.originalColor = self.data["fontColor"]["original"]

        # 获取翻译字体大小预设值
        self.fontSize = self.data["fontSize"]

        # 获取翻译字体样式预设值
        self.fontType = self.data["fontType"]

        # 获取颜色样式预设值
        self.showColorType = self.data["showColorType"]
        if self.showColorType == "True":
            self.showColorType = True
        else:
            self.showColorType = False

        # 获取是否显示原文预设值
        self.showOriginal = self.data["showOriginal"]
        if self.showOriginal == "True":
            self.showOriginal = True
        else:
            self.showOriginal = False

        # 获取是否将原文复制到剪贴板预设值
        self.showClipboard = self.data["showClipboard"]
        if self.showClipboard == "True":
            self.showClipboard = True
        else:
            self.showClipboard = False

        # 获取是否启用竖排文本翻译模式预设值
        self.showTranslateRow = self.data["showTranslateRow"]
        if self.showTranslateRow == "True":
            self.showTranslateRow = True
        else:
            self.showTranslateRow = False

        # 获取是否启用高精度翻译模式预设值
        self.highPrecision = self.data["highPrecision"]
        if self.highPrecision == "True":
            self.highPrecision = True
        else:
            self.highPrecision = False

        # 获取文本框透明度预设值
        self.horizontal = self.data["horizontal"]

        # 获取是否使用有道翻译预设值
        self.youdaoUse = self.data["youdaoUse"]
        if self.youdaoUse == "True":
            self.youdaoUse = True
        else:
            self.youdaoUse = False

        # 获取是否使用彩云翻译预设值
        self.caiyunUse = self.data["caiyunUse"]
        if self.caiyunUse == "True":
            self.caiyunUse = True
        else:
            self.caiyunUse = False

        # 获取是否使用金山翻译预设值
        self.jinshanUse = self.data["jinshanUse"]
        if self.jinshanUse == "True":
            self.jinshanUse = True
        else:
            self.jinshanUse = False

        # 获取是否使用yeekit翻译预设值
        self.yeekitUse = self.data["yeekitUse"]
        if self.yeekitUse == "True":
            self.yeekitUse = True
        else:
            self.yeekitUse = False

        # 获取是否使用alapi翻译预设值
        self.alapiUse = self.data["alapiUse"]
        if self.alapiUse == "True":
            self.alapiUse = True
        else:
            self.alapiUse = False

        # 获取是否使用百度翻译预设值
        self.baiduUse = self.data["baiduUse"]
        if self.baiduUse == "True":
            self.baiduUse = True
        else:
            self.baiduUse = False

        # 获取是否使用腾讯翻译预设值
        self.tencentUse = self.data["tencentUse"]
        if self.tencentUse == "True":
            self.tencentUse = True
        else:
            self.tencentUse = False

        # 获取是否使用私人彩云翻译预设值
        self.caiyunPrivateUse = self.data["caiyunPrivateUse"]
        if self.caiyunPrivateUse == "True":
            self.caiyunPrivateUse = True
        else:
            self.caiyunPrivateUse = False

        # 获取自动翻译时的刷新间隔预设值
        self.translateSpeed = self.data["translateSpeed"]

        # 获取各API预设值
        self.OCR_Key = self.data["OCR"]["Key"]
        self.OCR_Secret = self.data["OCR"]["Secret"]
        self.baidu_Key = self.data["baiduAPI"]["Key"]
        self.baidu_Secret = self.data["baiduAPI"]["Secret"]
        self.tencent_Key = self.data["tencentAPI"]["Key"]
        self.tencent_Secret = self.data["tencentAPI"]["Secret"]
        self.caiyun_token = self.data["caiyunAPI"]

        # 获取翻译语言预设值
        self.language = self.data["language"]
        if self.language == 'ENG':
            self.language = 1
        elif self.language == 'KOR':
            self.language = 2
        else:
            self.language = 0

    def Select_background(self):  # 将背景图片路径打印在显示框

        self.image_path = QFileDialog.getOpenFileName(
            self, '选择要作为背景的图片文件', '', 'image files(*.jpg , *.png)')[0]
        if self.image_path:
            self.openfileText.setText(self.image_path)

    def get_font_color(self, sign):  # 各翻译源字体颜色

        color = QColorDialog.getColor()
        if sign == 1:
            self.youdaoColor = color.name()
            self.youdaoColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["youdao"] = self.youdaoColor
        elif sign == 2:
            self.caiyunColor = color.name()
            self.caiyunColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["caiyun"] = self.caiyunColor
        elif sign == 3:
            self.jinshanColor = color.name()
            self.jinshanColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["jinshan"] = self.jinshanColor
        elif sign == 4:
            self.yeekitColor = color.name()
            self.yeekitColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["yeekit"] = self.yeekitColor
        elif sign == 5:
            self.ALAPIColor = color.name()
            self.alapiColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["ALAPI"] = self.ALAPIColor
        elif sign == 6:
            self.baiduwebColor = color.name()
            self.baiduwebColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["baiduweb"] = self.baiduwebColor
        elif sign == 7:
            self.tencentwebColor = color.name()
            self.tencentwebColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["tencentweb"] = self.tencentwebColor
        elif sign == 8:
            self.googleColor = color.name()
            self.googleColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["google"] = self.googleColor
        elif sign == 9:
            self.BingColor = color.name()
            self.BingColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["Bing"] = self.BingColor
        elif sign == 10:
            self.baiduColor = color.name()
            self.baiduColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["baidu"] = self.baiduColor
        elif sign == 11:
            self.tencentColor = color.name()
            self.tencentColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["tencent"] = self.tencentColor
        elif sign == 12:
            self.caiyunPrivateColor = color.name()
            self.caiyunPrivateColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["caiyunPrivate"] = self.caiyunPrivateColor
        elif sign == 13:
            self.originalColor = color.name()
            self.originalColour_toolButton.setStyleSheet(
                "background: rgba(255, 255, 255, 0.4);color: {};".format(color.name()))
            self.data["fontColor"]["original"] = self.originalColor

    def get_fontType(self, text):  # 字体样式

        self.fontType = text
        self.data["fontType"] = self.fontType

    def showOriginal_state(self):  # 颜色样式

        if self.showColorType_checkBox.isChecked():
            self.showColorType = "True"
        else:
            self.showColorType = "False"
        self.data["showColorType"] = self.showColorType

    def showColorType_state(self):  # 是否显示原文

        if self.showOriginal_checkBox.isChecked():
            self.showOriginal = "True"
        else:
            self.showOriginal = "False"
        self.data["showOriginal"] = self.showOriginal

    def showClipboard_state(self):  # 是否将原文自动复制到剪贴板

        if self.Clipboard_checkBox.isChecked():
            self.showClipboard = "True"
        else:
            self.showClipboard = "False"
        self.data["showClipboard"] = self.showClipboard

    def showTranslateRow_state(self):  # 是否启用竖排文字翻译模式

        if self.TranslateRow_checkBox.isChecked():
            self.showTranslateRow = "True"
        else:
            self.showTranslateRow = "False"
        self.data["showTranslateRow"] = self.showTranslateRow

    def highPrecision_state(self):  # 是否启用高精度翻译模式

        if self.highPrecision_checkBox.isChecked():
            self.highPrecision = "True"
        else:
            self.highPrecision = "False"
        self.data["highPrecision"] = self.highPrecision

    def get_horizontal(self):  # 文本框透明度

        self.horizontal = self.horizontalSlider.value()
        self.data["horizontal"] = self.horizontal

    def save_fontSize(self):  # 翻译源字体大小

        self.data["fontSize"] = self.fontSize_spinBox.value()

    def youdaoUse_state(self):  # 是否使用有道翻译

        if self.youdao_checkBox.isChecked():
            self.youdaoUse = "True"
        else:
            self.youdaoUse = "False"
        self.data["youdaoUse"] = self.youdaoUse

    def caiyunUse_state(self):  # 是否使用彩云翻译

        if self.caiyun_checkBox.isChecked():
            self.caiyunUse = "True"
        else:
            self.caiyunUse = "False"
        self.data["caiyunUse"] = self.caiyunUse

    def jinshanUse_state(self):  # 是否使用金山翻译

        if self.jinshan_checkBox.isChecked():
            self.jinshanUse = "True"
        else:
            self.jinshanUse = "False"
        self.data["jinshanUse"] = self.jinshanUse

    def yeekitUse_state(self):  # 是否使用yeekit翻译

        if self.yeekit_checkBox.isChecked():
            self.yeekitUse = "True"
        else:
            self.yeekitUse = "False"
        self.data["yeekitUse"] = self.yeekitUse

    def alapiUse_state(self):  # 是否使用ALAPI翻译

        if self.ALAPI_checkBox.isChecked():
            self.alapiUse = "True"
        else:
            self.alapiUse = "False"
        self.data["alapiUse"] = self.alapiUse

    def baiduUse_state(self):  # 是否使用百度翻译
        if self.baidu_checkBox.isChecked():
            self.baiduUse = "True"
        else:
            self.baiduUse = "False"
        self.data["baiduUse"] = self.baiduUse

    def tencentUse_state(self):  # 是否使用腾讯翻译
        if self.tencent_checkBox.isChecked():
            self.tencentUse = "True"
        else:
            self.tencentUse = "False"
        self.data["tencentUse"] = self.tencentUse

    def caiyunPrivateUse_state(self):  # 是否使用私人彩云翻译
        if self.caiyunPrivate_checkBox.isChecked():
            self.caiyunPrivateUse = "True"
        else:
            self.caiyunPrivateUse = "False"
        self.data["caiyunPrivateUse"] = self.caiyunPrivateUse

    def saveAPI(self):

        self.OCR_Key = self.OCR_Key_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.OCR_Secret = self.OCR_Secret_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.baidu_Key = self.baidu_Key_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.baidu_Secret = self.baidu_Secret_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.tencent_Key = self.tencent_Key_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.tencent_Secret = self.tencent_Secret_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')
        self.caiyun_token = self.caiyun_token_Text.toPlainText().replace(
            ' ', '').replace('\n', '').replace('\t', '')

        self.data["OCR"]["Key"] = self.OCR_Key
        self.data["OCR"]["Secret"] = self.OCR_Secret
        self.data["baiduAPI"]["Key"] = self.baidu_Key
        self.data["baiduAPI"]["Secret"] = self.baidu_Secret
        self.data["tencentAPI"]["Key"] = self.tencent_Key
        self.data["tencentAPI"]["Secret"] = self.tencent_Secret
        self.data["caiyunAPI"] = self.caiyun_token

    def range(self):

        with open('.\\config\\settin.json') as file:
            data1 = json.load(file)

            self.data["range"]["X1"] = data1["range"]["X1"]
            self.data["range"]["Y1"] = data1["range"]["Y1"]
            self.data["range"]["X2"] = data1["range"]["X2"]
            self.data["range"]["Y2"] = data1["range"]["Y2"]

    def save_language(self):  # 保存翻译语种

        if self.language_comboBox.currentIndex() == 1:
            self.data["language"] = 'ENG'
            self.data["yeekitLanguage"] = "nen"
            self.data["BingLanguage"] = "en"
        elif self.language_comboBox.currentIndex() == 2:
            self.data["language"] = 'KOR'
            self.data["yeekitLanguage"] = "nko"
            self.data["BingLanguage"] = "ko"
        else:
            self.data["language"] = 'JAP'
            self.data["yeekitLanguage"] = "nja"
            self.data["BingLanguage"] = "ja"

    def save_settin(self):

        self.range()
        self.get_horizontal()
        self.save_fontSize()

        self.showColorType_state()
        self.showOriginal_state()
        self.showClipboard_state()
        self.showTranslateRow_state()
        self.highPrecision_state()

        self.youdaoUse_state()
        self.caiyunUse_state()
        self.jinshanUse_state()
        self.yeekitUse_state()
        self.alapiUse_state()
        self.baiduUse_state()
        self.tencentUse_state()
        self.caiyunPrivateUse_state()

        self.save_language()

        self.data["translateSpeed"] = self.autoSpeed_spinBox.value()
        self.saveAPI()

        with open('.\\config\\settin.json', 'w') as file:
            json.dump(self.data, file)

        sign = get_Access_Token()
        if sign == 1:
            MessageBox('保存设置', '保存成功啦 ヾ(๑╹◡╹)ﾉ"')


if __name__ == "__main__":

    import sys
    screen_scale_rate = get_screen_rate()
    APP = QApplication(sys.argv)
    Settin = SettinInterface(screen_scale_rate)
    Settin.show()
    sys.exit(APP.exec_())
