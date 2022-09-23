import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from process import Process
from webcam import Webcam
import serial
from POLY_CSV import send_mail
from PyQt5 import uic
from tensorflow.keras.models import load_model
import pandas as pd
import time
import tensorflow as tf
import threading

with tf.device("/device:GPU:0"):
    BPM = 9999
    model = load_model('./model/emotion_model')
    count =0
    main_ui = './UI/main.ui'
    sub_ui = './UI/sub.ui'
    classes = ['negative','positive']

    class NewWindow(QMainWindow):
        def __init__(self, parent=None):
            super(NewWindow, self).__init__(parent)
            uic.loadUi(sub_ui, self)
            global BPM
            self.send_button.clicked.connect(self.make_sheet)
            self.check_list = []
            self.shift = 0

            self.IMG_LABEL.setStyleSheet('image:url(./image/poly4.jpg);')

            self.email = ""
            self.B0.clicked.connect(lambda: self.clicked_0(text='0'))
            self.B1.clicked.connect(lambda: self.clicked_0(text='1'))
            self.B2.clicked.connect(lambda: self.clicked_0(text='2'))
            self.B3.clicked.connect(lambda: self.clicked_0(text='3'))
            self.B4.clicked.connect(lambda: self.clicked_0(text='4'))
            self.B5.clicked.connect(lambda: self.clicked_0(text='5'))
            self.B6.clicked.connect(lambda: self.clicked_0(text='6'))
            self.B7.clicked.connect(lambda: self.clicked_0(text='7'))
            self.B8.clicked.connect(lambda: self.clicked_0(text='8'))
            self.B9.clicked.connect(lambda: self.clicked_0(text='9'))
            self.BQ.clicked.connect(lambda: self.clicked_1(text='q'))
            self.BW.clicked.connect(lambda: self.clicked_1(text='w'))
            self.BE.clicked.connect(lambda: self.clicked_1(text='e'))
            self.BR.clicked.connect(lambda: self.clicked_1(text='r'))
            self.BT.clicked.connect(lambda: self.clicked_1(text='t'))
            self.BY.clicked.connect(lambda: self.clicked_1(text='y'))
            self.BU.clicked.connect(lambda: self.clicked_1(text='u'))
            self.BI.clicked.connect(lambda: self.clicked_1(text='i'))
            self.BO.clicked.connect(lambda: self.clicked_1(text='o'))
            self.BP.clicked.connect(lambda: self.clicked_1(text='p'))
            self.BA.clicked.connect(lambda: self.clicked_1(text='a'))
            self.BS.clicked.connect(lambda: self.clicked_1(text='s'))
            self.BD.clicked.connect(lambda: self.clicked_1(text='d'))
            self.BF.clicked.connect(lambda: self.clicked_1(text='f'))
            self.BG.clicked.connect(lambda: self.clicked_1(text='g'))
            self.BH.clicked.connect(lambda: self.clicked_1(text='h'))
            self.BJ.clicked.connect(lambda: self.clicked_1(text='j'))
            self.BK.clicked.connect(lambda: self.clicked_1(text='k'))
            self.BL.clicked.connect(lambda: self.clicked_1(text='l'))
            self.BZ.clicked.connect(lambda: self.clicked_1(text='z'))
            self.BX.clicked.connect(lambda: self.clicked_1(text='x'))
            self.BC.clicked.connect(lambda: self.clicked_1(text='c'))
            self.BV.clicked.connect(lambda: self.clicked_1(text='v'))
            self.BB.clicked.connect(lambda: self.clicked_1(text='b'))
            self.BN.clicked.connect(lambda: self.clicked_1(text='n'))
            self.BM.clicked.connect(lambda: self.clicked_1(text='m'))
            self.BDOT.clicked.connect(lambda: self.clicked_1(text='.'))
            self.BAT.clicked.connect(lambda: self.clicked_1(text='@'))
            self.BSHIFT.clicked.connect(self.clicked_shift)
            self.BBACK.clicked.connect(self.clicked_back)
            self.BCLEAR.clicked.connect(self.clear_box)
            self.BNAVER.clicked.connect(lambda: self.clicked_0(text="naver.com"))
            self.BGOOGLE.clicked.connect(lambda: self.clicked_0(text="gmail.com"))
            self.BDAUM.clicked.connect(lambda: self.clicked_0(text="daum.net"))
            self.BKAKAO.clicked.connect(lambda: self.clicked_0(text="kakao.com"))
            self.BKOPO.clicked.connect(lambda: self.clicked_0(text="kopo.ac.kr"))
            self.BHANMAIL.clicked.connect(lambda: self.clicked_0(text="hanmail.net"))
            self.BNATE.clicked.connect(lambda: self.clicked_0(text="nate.com"))
            self.BYAHOO.clicked.connect(lambda: self.clicked_0(text="yahoo.com"))
            self.STATUS_BUTTON.clicked.connect(self.reset_button)

        def reset_button(self):
            self.STATUS_BUTTON.setText("...")

        def clear_box(self):
            self.email = ""
            self.e_mail_box.setText(self.email)

        def clicked_back(self):
            text_len = len(self.email)
            self.email = self.email[:text_len-1]
            self.e_mail_box.setText(self.email)

        def clicked_shift(self):
            if self.shift == 1:
                self.shift = 0
            else:
                self.shift = 1

        def clicked_0(self, text):
            self.email = self.email + text
            self.e_mail_box.setText(self.email)

        def clicked_1(self, text):
            if self.shift == 1:
                text = text.upper()
            self.email = self.email + text
            self.e_mail_box.setText(self.email)

        def make_sheet(self):
            global BPM
            self.check_list.append(self.my_ck1.isChecked())
            self.check_list.append(self.my_ck2.isChecked())
            self.check_list.append(self.my_ck3.isChecked())
            self.check_list.append(self.my_ck4.isChecked())
            self.check_list.append(self.my_ck5.isChecked())
            self.check_list.append(self.my_ck6.isChecked())
            self.check_list.append(self.my_ck7.isChecked())
            self.check_list.append(self.fam_ck1.isChecked())
            self.check_list.append(self.fam_ck2.isChecked())
            self.check_list.append(self.fam_ck3.isChecked())
            self.check_list.append(self.fam_ck4.isChecked())
            self.check_list.append(self.fam_ck5.isChecked())
            self.check_list.append(self.fam_ck6.isChecked())
            self.check_list.append(self.fam_ck7.isChecked())

            for i in range(0,14):
                if self.check_list[i] == 0:
                    self.check_list[i] = 'No'
                elif self.check_list[i] == 1:
                    self.check_list[i] = 'Yes'

            if BPM == 9999:
                BPM = "측정 전"

            data_sheet = pd.DataFrame(
                {
                    '병명' : ['뇌졸증(중풍)','심근경색/협심증','고혈압','당뇨병','이상지질혈증','폐결핵','기타(암포함)'],
                    '본인병력' : self.check_list[:7],
                    '가족병력' : self.check_list[7:],
                    '심박수(BPM)' : [BPM, " ", " "," "," "," "," "]
                }
            )
            self.check_list = []
            data_sheet.to_csv("save_data.csv",index=1,encoding='cp949')

            e_mail = self.e_mail_box.toPlainText()
            if len(e_mail) < 3:
                print("unstable email")
                self.STATUS_BUTTON.setText("FAIL")
            else:
                send_mail(e_mail)
                BPM = 0
                self.STATUS_BUTTON.setText("CLEAR")
            self.email = ""
            self.e_mail_box.setText(" ")

    class Communicate(QObject):
        closeApp = pyqtSignal()


    # main window
    class GUI(QMainWindow, QThread):
        """메인 윈도우"""
        qss = """   
            QWidget#windowTitle QLabel {
                color: #FFFFFF;
                background: #333;
            }
        """
        def __init__(self):
            super(GUI, self).__init__()
            uic.loadUi(main_ui, self)
            self.show()

            # self.initUI()
            self.webcam = Webcam()
            self.input = self.webcam
            print("Input: webcam")
            self.reset_button.setEnabled(False)
            self.process = Process()
            self.status = False
            self.frame = np.zeros((10,10,3),np.uint8)
            self.bpm = 0
            self.new_window = NewWindow(self)
            self.score = 0
            self.chart_button.clicked.connect(self.MJP)

            self.start_button.clicked.connect(self.run)
            self.loading_bar.setMinimum(0)
            self.loading_bar.setMaximum(50)
            self.loading_bar.setValue(0)

            self.action_score = 50
            self.emotion_img = 0
            self.available = 1
            self.pred_status = 0
            # self.arduino_ser1 = serial.Serial('/dev/ttyACM1', 9600)  #sudo chmod 666 /dev/ttyACM0
            # self.arduino_ser2 = serial.Serial('/dev/ttyACM0', 9600)  #sudo chmod 666 /dev/ttyACM1

            self.camera_label.setStyleSheet("image:url('./image/new_camera.png');")
            self.state_label.setText("심박수 : ")
            self.state2avg_label.setText("상태 : ")

            self.reset_button.clicked.connect(self.reset_main_window)
            self.reset_label.setStyleSheet("image:url('./image/gauge_0.png');border:0px;")

            self.pred = threading.Thread(target=self.model_predict)
            self.pred.start()

        def reset_main_window(self):
            self.camera_label.setPixmap(QPixmap('./image/new_camera.png'))
            self.state_label.setText("심박수 : ")
            self.state2avg_label.setText("상태 : ")
            self.reset_label.setStyleSheet("image:url('./image/gauge_0.png');")
            self.loading_bar.setValue(0)
            # self.Serial_Action()
            self.pred_status = 0
            self.emotion_img = 0

        def Serial_Action(self):
            motor_data = '1'
            motor_data = motor_data.encode('utf-8')
            if self.score > self.action_score * 0.7:
                val = '1'
                val = val.encode('utf-8')
                self.arduino_ser1.write(val)
                self.arduino_ser2.write(motor_data)
            elif self.score > 10 and self.score < self.action_score * 0.7:
                val = '0'
                val = val.encode('utf-8')
                self.arduino_ser1.write(val)
            else:
                val = '2'
                val = val.encode('utf-8')
                self.arduino_ser1.write(val)
                self.arduino_ser2.write(motor_data)

        def MJP(self):
            self.new_window.show()

        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

        def selectInput(self):
            self.reset()
            self.input = self.webcam
            print("Input: webcam")

        def key_handler(self):
            """
            cv2 window must be focused for keypresses to be detected.
            """
            self.pressed = waitKey(1) & 255  # wait for keypress for 10 ms
            if self.pressed == 27:  # exit program on 'esc'
                print("[INFO] Exiting")
                self.webcam.stop()
                sys.exit()

        def openFileDialog(self):
            self.dirname = QFileDialog.getOpenFileName(self, 'OpenFile',r"C:\Users\uidh2238\Desktop\test videos")

        def reset(self):
            self.process.reset()

        @QtCore.pyqtSlot()
        def getBPMtoProcess(self):
            self.pred_status = 0
            frame = self.input.get_frame()
            x, y, c = frame.shape
            frame = cv2.resize(frame, dsize=(int(y / 3.1), int(x / 3.1)))  # 양호 * 0.5
            self.process.frame_in = frame
            self.process.run()
            self.f_fr = self.process.frame_ROI #get the face to show in GUI
            self.f_fr = cv2.cvtColor(self.f_fr, cv2.COLOR_RGB2BGR)
            self.emotion_img = np.copy(self.f_fr) # tensorflow emotion model image
            self.pred_status = 1
            self.f_fr = cv2.resize(self.f_fr, (700, 700),interpolation=cv2.INTER_LINEAR)

            f_img = QImage(self.f_fr, self.f_fr.shape[1], self.f_fr.shape[0],
                           self.f_fr.strides[0], QImage.Format_RGB888)

            self.camera_label.setPixmap(QPixmap.fromImage(f_img))
            self.print_bpm_result()
            self.print_model_result()  # 점수 값에 따라 GUI 결과 표현 2022_04_02

        def model_predict(self):
            while 1:
                try:
                    if self.pred_status == 1 and self.emotion_img.shape[1] != 10:
                        cutting_image1 = 40
                        cutting_image2 = 200
                        self.emotion_img = self.emotion_img[cutting_image1:cutting_image2, cutting_image1:cutting_image2]
                        self.emotion_img = cv2.resize(self.emotion_img, (100, 100))
                        self.emotion_img = self.emotion_img[np.newaxis, :]
                        pred = model.predict(self.emotion_img)
                        pred = np.argmax(pred, axis=1)
                        if pred[0] == 1:
                            self.score += 1
                except AttributeError:
                    pass

        def print_model_result(self):
            if self.score < 5:
                return
            elif self.score < (self.action_score * 0.1):
                self.reset_label.setStyleSheet("image:url('./image/gauge_1.png'); border:0px;")
            elif self.score < (self.action_score * 0.2):
                self.reset_label.setStyleSheet("image:url('./image/gauge_2.png'); border:0px;")
            elif self.score < (self.action_score * 0.3):
                self.reset_label.setStyleSheet("image:url('./image/gauge_3.png'); border:0px;")
            elif self.score < (self.action_score * 0.4) :
                self.reset_label.setStyleSheet("image:url('./image/gauge_4.png'); border:0px;")
            elif self.score < (self.action_score * 0.6) :
                self.reset_label.setStyleSheet("image:url('./image/gauge_5.png'); border:0px;")
            elif self.score < (self.action_score * 0.7) :
                self.reset_label.setStyleSheet("image:url('./image/gauge_6.png'); border:0px;")
            elif self.score < (self.action_score * 0.8) :
                self.reset_label.setStyleSheet("image:url('./image/gauge_7.png'); border:0px;")
            elif self.score > self.action_score :
                self.reset_label.setStyleSheet("image:url('./image/gauge_8.png'); border:0px;")

        def print_bpm_result(self):
            global BPM
            lens = self.process.bpms.__len__()
            self.loading_bar.setValue(lens)
            if lens > 50:
                bpm_mean = np.mean(self.process.bpms)
                if max(self.process.bpms - bpm_mean) < 4:
                    self.state_label.setText("심박수 : " + str(float("{:.1f}".format(bpm_mean))) + "bpm")
                    BPM = int(bpm_mean)
                    if bpm_mean <= 69:
                        self.state2avg_label.setText("상태 : " + "좋음")
                    elif 70 <= bpm_mean <= 76:
                        self.state2avg_label.setText("상태 : " + "양호")
                    elif 77 <= bpm_mean <= 84:
                        self.state2avg_label.setText("상태 : " + "나쁨")
                    elif 84 < bpm_mean:
                        self.state2avg_label.setText("상태 : " + "매우 나쁨")

        def run(self, input):
            self.reset()
            input = self.input
            if self.status == False:
                self.status = True
                input.start()
                self.start_button.setText("정지")
                self.reset_button.setEnabled(False)
                self.state_label.setText("심박수 : ")
                self.state2avg_label.setText("상태 : ")
                self.score = 0
                while self.status == True:
                    self.getBPMtoProcess()
                    QApplication.processEvents()
            elif self.status == True:
                self.status = False
                self.pred_status = 0
                self.emotion_img = 0
                input.stop()
                self.start_button.setText("시작")
                self.reset_button.setEnabled(True)

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = GUI()

        sys.exit(app.exec_())