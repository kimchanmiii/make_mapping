# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import io
import math
import sys
import os

import folium
import folium as g
from PyQt5.QtCore import QUrl
from folium import Choropleth, Circle, Marker, CircleMarker
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import time
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic

form_class = uic.loadUiType("mapmapping.ui")[0]
ROOT_DIR = os.path.abspath(os.curdir)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fName = tuple()
        self.tripMaxNum = 0
        self.tripMaxNum_first = 0
        self.filename_start_idx = str()
        self.filename = str()
        self.filename_first = str()
        self.trip_time = dict()

        # WebEngineView 시그널 연결
        self.WEV1.loadStarted.connect(self.printLoadStart)
        self.WEV1.loadProgress.connect(self.printLoading)
        self.WEV1.loadFinished.connect(self.printLoadFinished)
        self.WEV1.urlChanged.connect(self.urlChangedFunction)

        # 기타 위젯 신호 연결
        self.btn_open_file.clicked.connect(self.setTargetAddr)
        self.btn_create_map.clicked.connect(self.createMap)
        self.sb_trip_num.valueChanged.connect(self.loadMap)

        self.setWindowTitle('Map Mapping 1.0.4')

    def printLoadStart(self):
        print("Start Loading")

    def printLoading(self):
        print("Loading")

    def printLoadFinished(self):
        print("Load Finished")

    def urlChangedFunction(self):
        print("Url Changed")

    def setTargetAddr(self):
        tempFName = QFileDialog.getOpenFileNames(self, 'Select File', filter='*.csv')
        if len(tempFName[0]) > 0:
            self.fName = tempFName
            self.label_file_path.setText(self.fName[0][0])

    def createMap(self):
        if len(self.fName) == 0:
            self.label_map_status.setText("파일이 없습니다.")
            return

        for index, f_name in enumerate(self.fName[0]):
            try:
                data_pd = pd.read_csv(f_name, encoding='utf-8')
            except:
                self.label_map_status.setText("파일 오류")
                return

            self.tripMaxNum = int(max(data_pd['trip_num']))

            if math.isnan(self.tripMaxNum):
                self.label_map_status.setText("데이터 없음")
                return

            if self.tripMaxNum <= 0:
                self.label_map_status.setText("파일에 트립이 없습니다.")
                return

            self.pBar.setValue(0.0)
            self.label_map_status.setText("지도생성 중")
            self.filename_start_idx = f_name.rfind('/') + 1
            self.filename = f_name[self.filename_start_idx:-4]
            if index == 0:
                self.label_trip_max_num.setText('트립수: ' + str(self.tripMaxNum))
                self.filename_first = self.filename
                self.tripMaxNum_first = self.tripMaxNum

            for j in range(1, self.tripMaxNum + 1):
                data_trip = data_pd[data_pd.trip_num == j]
                if len(data_trip) < 1:
                    continue
                self.trip_time[str(j)] = dict()
                self.trip_time[str(j)]['start'] = data_trip.iloc[0]['ts']
                self.trip_time[str(j)]['end'] = data_trip.iloc[len(data_trip) - 1]['ts']

                if os.path.isfile(f_name[0:-4] + '/' + self.filename + 'Map' + str(j) + '.html'):
                    self.pBar.setValue(j / self.tripMaxNum * 100)
                    self.label_map_status.setText(f_name[self.filename_start_idx:] + "에서 지도생성 완료!")
                    continue

                isFirstPos = 0
                for i in range(0, len(data_trip)):
                    if math.isnan(data_trip.iloc[i]['lt']) or data_trip.iloc[i]['lt'] < 10.0:
                        continue

                    iframe = folium.IFrame(
                        'ct : ' + data_trip.iloc[i]['ct'] + '<br>' +
                        'lt: ' + str(data_trip.iloc[i]['lt']) + '<br>' +
                        'ln: ' + str(data_trip.iloc[i]['ln']) + '<br>' +
                        'ac: ' + str(data_trip.iloc[i]['ac']) + '<br>' +
                        'al: ' + str(data_trip.iloc[i]['al']) + '<br>' +
                        'ts: ' + data_trip.iloc[i]['ts'] + '<br>' +
                        'sts: ' + data_trip.iloc[i]['sts'] + '<br>' +
                        'ax: ' + str(data_trip.iloc[i]['ax']) + '<br>' +
                        #                        'dis: ' + str(data_trip.iloc[i]['distance']) + '<br>' +
                        'rs: ' + str(data_trip.iloc[i]['rs(rr)']) + '<br>' +
                        'pc: ' + str(data_trip.iloc[i]['pc']), width=300, height=300)
                    popup = folium.Popup(iframe, min_width=300, max_width=300, min_height=300, max_height=300)

                    if isFirstPos == 0:
                        # 첫데이터 위치에서 zoom_start
                        isFirstPos = 1
                        gMap = g.Map(location=[data_trip.iloc[i]['lt'], data_trip.iloc[i]['ln']], zoom_start=12,
                                     control_scale=True, zoom_control=True)
                        # 첫 데이터는 블루 마커로 표시
                        Marker(
                            location=[data_trip.iloc[i]['lt'], data_trip.iloc[i]['ln']],
                            popup=popup,
                            icon=folium.Icon(color='blue')
                        ).add_to(gMap)
                    else:
                        # 일반 데이터는 파란 점으로 표시
                        CircleMarker(
                            location=[data_trip.iloc[i]['lt'], data_trip.iloc[i]['ln']],
                            radius=4,
                            color='blue',
                            fill_color='blue',
                            fill_opacity=0.4,
                            weight=1,
                            stroke=False,
                            popup=popup
                        ).add_to(gMap)
                # 유효한 데이터가 없을 때는 지도 생성 안하고 다음 트립으로
                if isFirstPos == 0:
                    continue

                createFolder(f_name[0:-4])
                gMap.save(f_name[0:-4] + '/' + self.filename + 'Map' + str(j) + '.html')
                self.pBar.setValue(j / self.tripMaxNum * 100)
                self.label_map_status.setText(f_name[self.filename_start_idx:] + "에서 지도생성 완료!")

            if index == 0:
                self.sb_trip_num.setRange(0, self.tripMaxNum)

    def loadMap(self):
        if self.tripMaxNum_first <= 0:
            return

        trip_num = self.sb_trip_num.value()
        if trip_num <= 0 or self.tripMaxNum_first < trip_num:
            return
        # print(self.fName[0][0:-4] + '/' + self.filename + 'Map' + str(trip_num) + '.html')

        self.WEV1.load(QUrl(self.fName[0][0][0:-4] + '/' + self.filename_first + 'Map' + str(trip_num) + '.html'))
        if not str(trip_num) in self.trip_time:
            return
        self.label_trip_time.setText(
            '주행시간: ' + self.trip_time[str(trip_num)]['start'] + " ~ " + self.trip_time[str(trip_num)]['end'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()