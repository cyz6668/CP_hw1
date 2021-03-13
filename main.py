import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PIL import Image as img,ImageTk
import  time
import math
import numpy as np
from tkinter import *
import cv2 as cv


images=[]

def init():
    for i in range(16):
        images_temp=[]
        for j in range(16):
            name=dealwithnum(i,j)
            image = img.open("D:\\courses_postgrad1\\CP\\toyLF\\lowtoys" + name + ".bmp");
            image_arr = np.array(image)
            images_temp.append(image_arr)
        images.append(images_temp)


def dealwithnum(x,y):
    #if(x==math.floor(x)|y==math.floor(y)): return '*';
    #if(x<0|x>15|y<0|y>15|x==0|y==0|x==15|y==15):return "#"
    if (x < 0 | x > 15 | y < 0 | y > 15): return "#"
    i = str(x*16+y+1);
    length = len(i)
    if (length < 3):
        len_0 = 3 - length
        for j in range(len_0):
            i = '0' + i;
    return i



class EventsSignals(QWidget):

    def __init__(self):
        super(EventsSignals,self).__init__()
        self.x = 3.4
        self.y = 5.6
        self.sz=0.0
        self.d=0.0
        self.z=1.0
        self.initUI()

    def initUI(self):
        #lcd = QLCDNumber(self)  # 显示一个LCD数字。
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Signal & slot')
        self.show()
        self.sld_x = QSlider(Qt.Horizontal, self)  # 提供了一个水平滑动条# 。
        self.sld_y = QSlider(Qt.Horizontal, self)
        self.sld_dis=QSlider(Qt.Horizontal,self)
        self.sld_sz=QSlider(Qt.Horizontal,self)
        self.sld_z=QSlider(Qt.Horizontal,self)

        self.label_x=QLabel(self)
        self.label_x.setText('X')

        self.label_y=QLabel(self)
        self.label_y.setText('Y')

        self.label_z=QLabel(self)
        self.label_z.setText('Z')

        self.label_dis=QLabel(self)
        self.label_dis.setText('disparity')

        self.label_len=QLabel(self)
        self.label_len.setText('aperture')
        #self.label_len.setGeometry()

        self.sld_x.setMinimum(0)
        self.sld_x.setMaximum(150)
        #self.sld_x.setSingleStep(10)
        self.sld_x.setTickPosition(QSlider.TicksBelow)
        #sld_x.setTickInterval(10)

        self.sld_y.setMinimum(0)
        self.sld_y.setMaximum(150)
        #self.sld_y.setSingleStep(10)
        self.sld_y.setTickPosition(QSlider.TicksBelow)
        #sld_y.setTickInterval(10)

        self.sld_sz.setMinimum(100)
        self.sld_sz.setMaximum(200)
        # self.sld_y.setSingleStep(10)
        self.sld_sz.setTickPosition(QSlider.TicksBelow)
        # sld_y.setTickInterval(10)

        self.sld_dis.setMinimum(0)
        self.sld_dis.setMaximum(10)
        self.sld_dis.setSingleStep(1)
        self.sld_dis.setTickPosition(QSlider.TicksBelow)

        self.sld_z.setMinimum(1)
        self.sld_z.setMaximum(10)
        self.sld_z.setSingleStep(0.1)
        self.sld_z.setTickPosition(QSlider.TicksBelow)

        self.label_pic=QLabel(self)
        self.label_pic.setFixedSize(320,320)
        #label_pic.move(160,160)

        self.vbox = QVBoxLayout()
        #vbox.addWidget(lcd)
        self.vbox.addWidget(self.label_x)
        self.vbox.addWidget(self.sld_x)
        self.vbox.addWidget(self.label_y)
        self.vbox.addWidget(self.sld_y)
        self.vbox.addWidget(self.label_len)
        self.vbox.addWidget(self.sld_sz)
        self.vbox.addWidget(self.label_dis)
        self.vbox.addWidget(self.sld_dis)
        self.vbox.addWidget(self.label_z)
        self.vbox.addWidget(self.sld_z)
        self.vbox.addWidget(self.label_pic)

        self.setLayout(self.vbox)
        self.sld_x.valueChanged['int'].connect(self.set_X)
        self.sld_y.valueChanged['int'].connect(self.set_Y)
        self.sld_sz.valueChanged['int'].connect(self.set_SZ)
        self.sld_dis.valueChanged['int'].connect(self.set_dis)
        self.sld_z.valueChanged['int'].connect(self.set_Z)
        ##  滑块条的valueChanged信号和lcd数字显示的display槽连接在一起。
        # 发送者是一个发送了信号的对象。接受者是一个接受了信号的对象。槽是对信号做出反应的方法。


    def openimage(image_post):
            pic=QtGui.QPixmap(image_post)
            label_pic.setPixmap(pic)


    def getapic_quadralinear(self):
        # double x,double y
        x1 = math.floor(self.x)
        y1 = math.floor(self.y)
        x2 = x1 + 1
        y2 = y1 + 1
        pics = [[x1, y1], [x1, y2], [x2, y1], [x2, y2]]
        image_touse = []
        for i in pics:
            if (i[0] < 0 | i[0] > 15 | i[1] < 0 | i[1] > 15): continue;
            image_touse.append(images[i[0]][i[1]])
        image_post = image_touse[0]
        w = image_post.shape[0];
        h = image_post.shape[1];

        a = self.x - x1;
        b = x2 - self.x;
        c = self.y - y1;
        d = y2 - self.y;
        if (len(image_touse) == 4):
            #image_post = int(image_touse[0]* b * d + image_touse[1]* b * c + image_touse[2]* a * d + image_touse[3] * a * c);
            image_post[:][:] = image_touse[0][:][:] * b * d + image_touse[1][:][:] * b * c + image_touse[2][:][:] * a * d + image_touse[3][:][:] * a * c;

            # for i in range(w):
            #     for j in range(h):
            #         image_post[i][j] = image_touse[0][i][j] * b * d + image_touse[1][i][j] * b * c + image_touse[2][i][j] * a * d + image_touse[3][i][j] * a * c;

        elif (len(image_touse) == 2):
            if (x < 0 | x > 15 | x == 0 | x == 15): c = float(y - y1);d = float(y2 - y);
            if (y < 0 | y > 15 | y == 0 | y == 15): c =float( x - x1);d = float(x2 - x);
            image_post[:][:] = image_touse[0][:][:] * d + image_touse[1][:][:] * c;

        else:
            image_post = image_touse[0]

        #print(image_post.dtype)
        #image_post = img.fromarray(image_post)
        #image_post = ImageTk.PhotoImage(image=image_post)
        image_post=QImage(image_post.data, image_post.shape[1], image_post.shape[0],QImage.Format_RGB888)
        #image_post=QImage(image_post)
        #pic = QtGui.QPixmap(image_post)
        #print(type(image_post))
        self.label_pic.setPixmap(QPixmap(image_post))

    def getapic_disparity(self):

        dis=self.d;
        x1 = math.floor(self.x)
        y1 = math.floor(self.y)

        x2 = x1 + 1
        y2 = y1 + 1
        pics = [[x1, y1], [x1, y2], [x2, y1], [x2, y2]]
        image_touse = []
        for i in pics:
            if (i[0] < 0 | i[0] > 15 | i[1] < 0 | i[1] > 15): continue;
            image = images[i[0]][i[1]];
            image_arr = np.array(image)
            image_touse.append(image_arr)
        image_post = image_touse[0]
        w = image_post.shape[0];
        h = image_post.shape[1];

        #image_post = np.zeros((w,h,3))
        image_post[:][:] = [0, 0, 0]
        # for i in range(w):
        #     for j in range(h):
        #         image_post[i][j]=[0,0,0]
        a = self.x - x1;
        b = x2 - self.x;
        c = self.y - y1;
        e = y2 - self.y;
        if (len(image_touse) == 4):
            image_post[0:w - dis, 0:h - dis, :] = image_touse[0][dis:w, dis:h, :] * b * e
            image_post[0:w - dis, dis:h, :] = image_post[0:w - dis, dis:h, :] + image_touse[1][dis:w, 0:h - dis, :] * b * c
            image_post[dis:w, 0:h - dis, :] = image_post[dis:w, 0:h - dis, :] + ( image_touse[2][0:w - dis, dis:h, :] * a * e)
            image_post[dis:w, dis:h, :] = ((image_post[dis:w, dis:h, :]) + (image_touse[3][0:w - dis, 0:h - dis, :] * a * c))



        elif (len(image_touse) == 2):
            if (x < 0 | x > 15 | x == 0 | x == 15):
                c = y - y1;
                d = y2 - y;
                image_post[dis:w][0:h - dis] = image_post[dis:w][0:h - dis] + (image_touse[0][0:w - dis][dis:h]) * d;
                image_post[dis:w][dis:h] = image_post[dis:w][dis:h] + (image_touse[1][0:w - dis][0:h - dis]) * c;

                image_post[0:w-int(dis*c)][int(dis*d):h]=image_touse[0][int(dis)*c:w][0:h-int(dis*d)]


                # for i in range(w - dis):
                #     for j in range(h - dis):
                #         image_post[i+dis][j]= ((image_post[i + dis][j]) + (image_touse[0][i][j+dis]) * d);
                #         image_post[i + dis][j + dis]= ((image_post[i + dis][j + dis]) + (image_touse[1][i][j]) * c);

            if (y < 0 | y > 15 | y == 0 | y == 15):
                c = x - x1;
                d = x2 - x;
                image_post[0:w - dis][dis:h] = image_post[0:w - dis][dis:h] + (image_touse[0][dis:w][0:h - dis]) * d;
                image_post[dis:w][dis:h] = image_post[dis:w][dis:h] + (image_touse[1][0:w - dis][0:h - dis]) * c;

                # for i in range(w - dis):
                #     for j in range(h - dis):
                #         image_post[i][j+dis]= ((image_post[i][j+dis]) + (image_touse[0][i+dis][j]) * d);
                #         image_post[i + dis][j + dis] = ((image_post[i + dis][j + dis]) + (image_touse[1][i][j]) * c);
        else:
            image_post = image_touse[0]
        image_post = QImage(image_post.data, image_post.shape[1], image_post.shape[0], QImage.Format_RGB888)
        self.label_pic.setPixmap(QPixmap(image_post))

    def getapic_setlen(self):
        sz = self.sz
        x1 = math.floor(self.x)
        y1 = math.floor(self.y)
        x2 = x1 + 1
        y2 = y1 + 1
        pics = [[x1, y1], [x1, y2], [x2, y1], [x2, y2]]
        image_touse = []
        for i in pics:
            if (i[0] < 0 | i[0] > 15 | i[1] < 0 | i[1] > 15): continue;
            image_touse.append(images[i[0]][i[1]])
        image_post = image_touse[0]
        w = image_post.shape[0];
        h = image_post.shape[1];

        a = self.x - x1;
        b = x2 - self.x;
        c = self.y - y1;
        d = y2 - self.y;
        if (len(image_touse) == 4):
            # image_post = image_touse[0]* b * d + image_touse[1]* b * c + image_touse[2]* a * d + image_touse[3] * a * c;
            image_post[:][:] = image_touse[0][:][:] * b * d + image_touse[1][:][:] * b * c + image_touse[2][:][:] * a * d + image_touse[3][:][:] * a * c;


        elif (len(image_touse) == 2):
            if (x < 0 | x > 15 | x == 0 | x == 15): c = self.y - y1;d = y2 - self.y;
            if (y < 0 | y > 15 | y == 0 | y == 15): c = self.x - x1;d = x2 - self.x;
            image_post[:][:] = image_touse[0][:][:] * d + image_touse[1][:][:] * c;


        image_pre = image_post

        kernel_size = (5, 5);
        sigma = 1.5;
        image_post = cv.GaussianBlur(image_post, kernel_size, sigma)
        limit_lx = int(100 - self.sz / 2);
        limit_rx = int(100 + self.sz / 2);
        limit_uy = int(150 + self.sz / 2);
        limit_dy = int(150- self.sz / 2);
        image_post[limit_lx:limit_rx][limit_dy:limit_uy] = image_pre[limit_lx:limit_rx][limit_dy:limit_uy]
        image_post = QImage(image_post.data, image_post.shape[1], image_post.shape[0], QImage.Format_RGB888)
        self.label_pic.setPixmap(QPixmap(image_post))

    def getapic_z(self):

        x1 = math.floor(self.x)
        y1 = math.floor(self.y)
        x2 = x1 + 1
        y2 = y1 + 1
        pics = [[x1, y1], [x1, y2], [x2, y1], [x2, y2]]
        image_touse = []
        for i in pics:
            if (i[0] < 0 | i[0] > 15 | i[1] < 0 | i[1] > 15): continue;
            image_touse.append(images[i[0]][i[1]])
        image_post = image_touse[0]
        w = image_post.shape[0];
        h = image_post.shape[1];

        a = self.x - x1;
        b = x2 - self.x;
        c = self.y - y1;
        d = y2 - self.y;
        if (len(image_touse) == 4):
            # image_post = int(image_touse[0]* b * d + image_touse[1]* b * c + image_touse[2]* a * d + image_touse[3] * a * c);
            image_post[:][:] = image_touse[0][:][:] * b * d + image_touse[1][:][:] * b * c + image_touse[2][:][
                                                                                             :] * a * d + image_touse[
                                                                                                              3][:][
                                                                                                          :] * a * c;

            # for i in range(w):
            #     for j in range(h):
            #         image_post[i][j] = image_touse[0][i][j] * b * d + image_touse[1][i][j] * b * c + image_touse[2][i][j] * a * d + image_touse[3][i][j] * a * c;

        elif (len(image_touse) == 2):
            if (x < 0 | x > 15 | x == 0 | x == 15): c = float(y - y1);d = float(y2 - y);
            if (y < 0 | y > 15 | y == 0 | y == 15): c = float(x - x1);d = float(x2 - x);
            image_post[:][:] = image_touse[0][:][:] * d + image_touse[1][:][:] * c;

        else:
            image_post = image_touse[0]

        image_post=cv.resize(image_post, None,fx=self.z,fy=self.z, interpolation=cv.INTER_CUBIC)
        image_post=image_post[0:w][0:h]
        image_post = QImage(image_post.data, image_post.shape[1], image_post.shape[0], QImage.Format_RGB888)
        self.label_pic.setPixmap(QPixmap(image_post))


    def set_X(self,value):
        #x = float(m)
        self.x=float(value/10)
        self.getapic_quadralinear()

    def set_Y(self,value):
        #y = float(n)
        self.y=float(value/10)
        self.getapic_quadralinear()

    def set_SZ(self,value):
        self.sz=value
        self.getapic_setlen()

    def set_dis(self,value):
        self.d=value;
        self.getapic_disparity()

    def set_Z(self,value):
        self.z=value
        self.getapic_z()

if __name__ == '__main__':
    init()
    app = QApplication(sys.argv)
    ex = EventsSignals()
    sys.exit(app.exec_())
