#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Py40 PyQt5 tutorial

In this example, we position two push
buttons in the bottom-right corner
of the window.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""
import cv2
import read_config,read_frame,frame_background,frame_detection,frame_tracker

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal,pyqtSlot,Qt)

class A(QThread):
    changePixmap = pyqtSignal(QImage)
    detected = pyqtSignal(QImage)
    tracked = pyqtSignal(QImage)
    def run(self):
        # 计数器初始化
        count = 0
        # 读取配置
        data = read_config.read()
        cap, ok, frame, length = read_frame.cam_init(self.address)
        # 背景减除器初始化
        fgbg = frame_background.background_init()
        tracker_list = []
        detect_list = []
        result_list = []
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if self.method:
                # https://stackoverflow.com/a/55468544/6622587
                    step = 10
                    diff = frame_background.process(fgbg, frame, count, step)
                    if diff is not 0:
                        # 当前帧的目标检测
                        detect_list, detected_img, contour = frame_detection.detectobj(diff, frame)
                        new_detect_list = frame_tracker.list_compare(detect_list, result_list)
                        Added_tracker_list = frame_tracker.init_tracker(frame, new_detect_list)
                        tracker_list += Added_tracker_list
                        tracked_img, result_list = frame_tracker.update_tracker(frame, tracker_list)

                        frame = detected_img
                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                        self.detected.emit(p)

                        frame = tracked_img
                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                        self.tracked.emit(p)
    def setting(self,add,method=0):
        self.address = add
        self.method=method

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # 放入四个按钮
        self.pushButton1 = QPushButton()
        self.pushButton1.setText("导入摄像机")
        self.pushButton2 = QPushButton()
        self.pushButton2.setText("导入视频")
        self.pushButton3 = QPushButton()
        self.pushButton3.setText("识别")
        self.pushButton4 = QPushButton()
        self.pushButton4.setText("识别")
        self.pushButton5 = QPushButton()
        self.pushButton5.setText("航道管理")

        self.Stack = QStackedWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox =QHBoxLayout()
        hbox.addWidget(self.pushButton1)
        hbox.addWidget(self.pushButton2)
        hbox.addWidget(self.pushButton3)
        hbox.addWidget(self.pushButton4)

        hbox.setContentsMargins(0, 0, 0, 0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.pushButton5)
        vbox.addLayout(hbox)
        vbox.addWidget(self.Stack)

        vbox.setContentsMargins(0, 0, 0, 0)

        self.Stack.setCurrentIndex(0)

        self.pushButton1.clicked.connect(self.on_pushButton1_clicked)
        self.pushButton2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton4.clicked.connect(self.on_pushButton4_clicked)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    @pyqtSlot(QImage)
    def setImage1(self, image):
        self.label1.setPixmap(QPixmap.fromImage(image))
    def stack1UI(self):
        self.formLayout1 = QHBoxLayout(self.stack1)
        self.label1 = QLabel(self)
        # self.label1.move(280, 120)
        # self.label1.resize(640, 480)
        self.formLayout1.addWidget(self.label1)
        th = A(self)
        th.setting(0)
        th.changePixmap.connect(self.setImage1)
        th.start()

    @pyqtSlot(QImage)
    def setImage2(self, image):
        self.label2.setPixmap(QPixmap.fromImage(image))
    def stack2UI(self):
        self.formLayout2 = QHBoxLayout(self.stack2)
        self.label2 = QLabel(self)
        # self.label1.move(280, 120)
        # self.label1.resize(640, 480)
        self.formLayout2.addWidget(self.label2)
        self.th = A(self)
        self.th.setting('MOT16-03.mp4', 1)
        self.th.changePixmap.connect(self.setImage2)
        self.th.start()
    #
    # def stack2UI(self):
    #     self.formLayout2 = QHBoxLayout(self.stack2)
    #     # self.label2 = QLabel()
    #     # self.label2.setText("第二个面板，哼哼哼！")
    #     # # self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    #     # #self.label2.setAlignment(Qt.AlignCenter)
    #     # self.label2.setFont(QFont("Roman times", 50, QFont.Bold))
    #     # self.formLayout2.addWidget(self.label2)
    #     self.pictureLabel = QLabel()
    #     init_image = QPixmap("cat.jpeg").scaled(self.width(), self.height())
    #     self.pictureLabel.setPixmap(init_image)
    #
    #     self.playButton = QPushButton()
    #     self.playButton.setEnabled(True)
    #     self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    #     # self.playButton.clicked.connect(self.switch_video)
    #
    #     control_box = QHBoxLayout()
    #     control_box.setContentsMargins(0, 0, 0, 0)
    #     control_box.addWidget(self.playButton)
    #
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.pictureLabel)
    #     layout.addLayout(control_box)
    #     self.formLayout2.addLayout(layout)

    @pyqtSlot(QImage)
    def setImage3(self, image):
        self.label3.setPixmap(QPixmap.fromImage(image))
    def stack3UI(self):
        self.formLayout3 = QHBoxLayout(self.stack3)
        self.label3 = QLabel()
        # self.label3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.label3.setAlignment(Qt.AlignCenter)
        self.th.detected.connect(self.setImage3)
        self.formLayout3.addWidget(self.label3)


    @pyqtSlot(QImage)
    def setImage4(self, image):
        self.label4.setPixmap(QPixmap.fromImage(image))
    def stack4UI(self):
        self.formLayout4 = QHBoxLayout(self.stack4)
        self.label4 = QLabel()
        # self.label4.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.label4.setAlignment(Qt.AlignCenter)
        self.th.tracked.connect(self.setImage4)
        self.formLayout4.addWidget(self.label4)




    def on_pushButton1_clicked(self):
        self.Stack.setCurrentIndex(0)
    def on_pushButton2_clicked(self):
        self.Stack.setCurrentIndex(1)
    def on_pushButton3_clicked(self):
        self.Stack.setCurrentIndex(2)
    def on_pushButton4_clicked(self):
        self.Stack.setCurrentIndex(3)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())