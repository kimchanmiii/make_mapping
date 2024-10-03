import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import csv
import datetime
import pandas as pd
import json

form_class = uic.loadUiType("untitled.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fName = tuple()
        self.setWindowTitle("Carrot Data Converter 2.0.5")

        # 버튼에 기능을 연결하는 코드
        self.pushBtn_setTargetAddr.clicked.connect(self.setTargetAddr)
        self.pushBtn_startConverting.clicked.connect(self.startConverting)
        self.pushBtn_startConverting_old.clicked.connect(self.startConvertingOld)

    # btn_1이 눌리면 작동할 함수
    def setTargetAddr(self):
        self.fName = QFileDialog.getOpenFileNames(self, 'Select File', filter='*.csv')
        self.label_targetAddr.setText(self.fName[0][0])

    def startConverting(self):
        if len(self.fName) == 0:
            return

        for f_name in self.fName[0]:
            dataIndex = 0
            idx = 0
            try:
                fw = open(f_name[0:-4] + '_cv.csv', 'w')

            except:
                self.label_result.setText("Make sure the file is open")
                return

            try:
                rawData = pd.read_csv(f_name)
            except:
                self.label_result.setText("Invalid CSV File1")
                return

            for rows in rawData.iterrows():
                line = rows[1]
                idx = idx + 1
                if len(line) < 3:
                    continue
                else:
                    jsonStartIdx = line[2].find('{')
                    splitLine = line[2].split()
                    if len(splitLine) < 3:
                        continue

                if idx is 1:
                    fw.write('type,TripCode,sts,ts,rc(lag),tp(cht),fg(ver),rs(rr),pc,ct,lt,ln,ac,al,gx,gy,gz,ax,trip_num,dId\n')
                    dId = splitLine[2]

                if splitLine[4] == "ON":
                    fw.write("dtag/m/on" + ',')  # write "type"
                    fw.write(splitLine[3] + ',')  # write "tripCode"
                    fw.write(splitLine[0] + ' ' + splitLine[1] + ',')  # write "sts"
                    fw.write(str(datetime.datetime.utcfromtimestamp(
                        int(splitLine[5][3:]) / 1000 + 3600 * 9)) + ',')  # write "ts"
                    fw.write(splitLine[6][4:] + ',')  # write "lag"
                    fw.write(splitLine[10][4:] + ',')  # write "cht"
                    fw.write(splitLine[9][4:] + ',')  # write "version"
                    fw.write(splitLine[8][3:] + '\n')  # write "rr"

                elif splitLine[4] == "EC":
                    fw.write("dtag/m/ec" + ',')  # write "type"
                    fw.write(splitLine[3] + ',')  # write "mId"
                    fw.write(splitLine[0] + ' ' + splitLine[1] + ',')  # write "sts"
                    fw.write(str(datetime.datetime.utcfromtimestamp(
                        int(splitLine[5][3:]) / 1000 + 3600 * 9)) + ',')  # write "ts"
                    fw.write(splitLine[6][3:] + ',')  # write "st"
                    fw.write(splitLine[7][3:] + ',')  # write "lt"
                    fw.write(splitLine[8][3:] + '\n')  # write "ln"

                elif splitLine[4] == "GS":
                    fw.write("dtag/m/gs" + ',')  # write "type"
                    fw.write(splitLine[3] + ',')  # write "mId"
                    fw.write(splitLine[0] + ' ' + splitLine[1] + ',')  # write "sts"
                    fw.write(str(datetime.datetime.utcfromtimestamp(
                        int(splitLine[5][3:]) / 1000 + 3600 * 9)) + ',')  # write "ts"
                    fw.write(splitLine[6][3:] + ',')  # write "gv"
                    fw.write(splitLine[7][3:] + ',')  # write "lt"
                    fw.write(splitLine[8][3:] + '\n')  # write "ln"

                elif splitLine[4] == "TR":
                    numOfPayload = line[2].count('lt:')

                    if numOfPayload == -1:
                        continue

                    for i in range(numOfPayload):
                        dataIndex = dataIndex + 1
                        fw.write("dtag/m/tr/x" + ',')
                        fw.write(splitLine[3] + ',')  # write "mId"
                        fw.write(splitLine[0] + ' ' + splitLine[1] + ',')  # write "sts"
                        fw.write(str(datetime.datetime.utcfromtimestamp(int(splitLine[5][3:]) / 1000 + 3600 * 9)) + ',')  # write "ts"
                        fw.write(splitLine[6][3:] + ',')  # write "rc"
                        fw.write(splitLine[11][3:] + ',')  # write "tp"
                        fw.write(splitLine[12][3:] + ',')  # write "fg"
                        fw.write(splitLine[9][3:] + ',')  # write "rs"
                        fw.write(splitLine[8][3:] + ',')  # write "pc"

                        ct = splitLine[i*13+13]
                        ctStatrIdx = ct.find("ct:") + 3
                        fw.write(str(datetime.datetime.utcfromtimestamp(int(ct[ctStatrIdx:]) / 1000 + 3600 * 9)) + ',')  # write "ct"
                        fw.write(splitLine[i*13+14][3:] + ',')  # write "lt"
                        fw.write(splitLine[i*13+15][3:] + ',')  # write "ln"
                        fw.write(splitLine[i*13+16][3:] + ',')  # write "ac"
                        fw.write(splitLine[i*13+22][3:] + ',')  # write "al"

                        splitGvalue = splitLine[i*13+24].split(',')
                        fw.write(splitGvalue[0][2:] + ',')  # write "gx"
                        fw.write(splitGvalue[1] + ',')  # write "gy"
                        fw.write(splitGvalue[2] + ',')  # write "gz"
                        fw.write(splitLine[i*13+25].split(',')[0][2:] + ',')  # write "ax"
                        fw.write('\n')
            fw.close()

            if dataIndex >= 1:
                df = pd.read_csv(f_name[0:-4] + '_cv.csv')
                df = df.sort_values(by=['ts', 'ct']).reset_index(drop=True)
                df.loc[0, 'dId'] = str(dId)
                preTripCode = str('')
                trip_num = 0
                idx2 = 0
                for rows in df.iterrows():
                    line = rows[1]
                    if preTripCode != line['TripCode']:
                        trip_num = trip_num + 1
                    df.loc[idx2, 'trip_num'] = trip_num
                    preTripCode = line['TripCode']
                    idx2 = idx2 + 1

                try:
                    df.to_csv(f_name[0:-4] + '_cv.csv', index=False)
                    self.label_result.setText("Complete Converting")
                except:
                    self.label_result.setText("Make sure the file is open")

            else:
                self.label_result.setText("No Valid Data")

    def startConvertingOld(self):
        if len(self.fName) == 0:
            return

        for f_name in self.fName[0]:
            dataIndex = 0
            idx = 0

            try:
                fw = open(f_name[0:-4] + '_cv.csv', 'w')

            except:
                self.label_result.setText("Make sure the file is open")
                return

            try:
                rawData = pd.read_csv(f_name)
            except:
                self.label_result.setText("Invalid CSV File1")
                return

            for rows in rawData.iterrows():
                line = rows[1]
                idx = idx + 1
                if len(line) < 3:
                    continue
                else:
                    jsonStartIdx = line[2].find('{')

                if idx is 1:
                    fw.write('type,TripCode,sts,ts,rc(lag),tp(cht),fg(ver),rs(rr),pc,ct,lt,ln,ac,al,gx,gy,gz,ax,trip_num,dId\n')
                    dId = line[2].split()[2]

                if line[2].find("dtag/m/on") > 0:
                    onData = json.loads(line[2][jsonStartIdx:])
                    if onData.get("dup") is not None:
                        continue

                    fw.write("dtag/m/on" + ',')  # write "type"
                    fw.write(line[2].split(maxsplit=5)[3] + ',')  # write "TripCode"
                    fw.write(line[2].split(maxsplit=5)[0] + ' ' + line[2].split(maxsplit=5)[1] + ',')  # write "sts"
                    fw.write(
                        str(datetime.datetime.utcfromtimestamp(onData.get("ts") / 1000 + 3600 * 9)) + ',')  # write "ts"
                    fw.write(str(onData.get('lag')) + ',')  # write "lag"
                    fw.write(str(onData.get('cht')) + ',')  # write "cht"
                    fw.write(str(onData.get('ver')) + ',')  # write "version"
                    fw.write(str(onData.get('rr')) + "\n")  # write "version"

                # elif line[2].find("dtag/m/ec") > 0:
                #     ecData = json.loads(line[2][jsonStartIdx:])
                #     if ecData.get("dup") is not None:
                #         continue
                #
                #     fw.write("dtag/m/ec" + ',')  # write "type"
                #     fw.write(line[2].split(maxsplit=5)[3] + ',')  # write "TripCode"
                #     fw.write(line[2].split(maxsplit=5)[0] + ' ' + line[2].split(maxsplit=5)[1] + ',')  # write "sts"
                #     fw.write(str(datetime.datetime.utcfromtimestamp(ecData.get("ts") / 1000 + 3600 * 9)) + ',')  # write "ts"
                #     fw.write(str(ecData.get('st')) + ',')  # write "st"
                #     fw.write(str(ecData.get('lt')) + ',')  # write "lt"
                #     fw.write(str(ecData.get('ln')) + ',')  # write "ln"
                #     fw.write(str(ecData) + '\n')

                # elif line[2].find("dtag/m/gs") > 0:
                #     gsData = json.loads(line[2][jsonStartIdx:])
                #     if gsData.get("dup") is not None:
                #         continue
                #
                #     fw.write("dtag/m/gs" + ',')  # write "type"
                #     fw.write(line[2].split(maxsplit=5)[3] + ',')  # write "TripCode"
                #     fw.write(line[2].split(maxsplit=5)[0] + ' ' + line[2].split(maxsplit=5)[1] + ',')  # write "sts"
                #     fw.write(str(datetime.datetime.utcfromtimestamp(gsData.get("ts") / 1000 + 3600 * 9)) + ',')  # write "ts"
                #     fw.write(str(gsData.get('gv')) + ',')  # write "gv"
                #     fw.write(str(gsData.get('lt')) + ',')  # write "lt"
                #     fw.write(str(gsData.get('ln')) + ',')  # write "ln"
                #     fw.write(str(gsData) + '\n')  # write

                elif line[2].find("dtag/m/tr") > 0:
                    trData = json.loads(line[2][jsonStartIdx:])
                    tr = trData.get('tr')

                    if tr is None:
                        continue

                    for payload in tr:
                        dataIndex = dataIndex + 1
                        fw.write("dtag/m/tr/x" + ',')
                        fw.write(line[2].split(maxsplit=5)[3] + ',')  # write "TripCode"
                        fw.write(line[2].split(maxsplit=5)[0] + ' ' + line[2].split(maxsplit=5)[1] + ',')  # write "sts"
                        fw.write(
                            str(datetime.datetime.utcfromtimestamp(trData.get("ts") / 1000 + 3600 * 9)) + ',')  # write "ts"
                        fw.write(str(trData.get("rc")) + ',')
                        fw.write(str(trData.get("tp")) + ',')
                        fw.write(str(trData.get("fg")) + ',')
                        fw.write(str(trData.get("rs")) + ',')
                        fw.write(str(trData.get("pc")) + ',')
                        fw.write(str(datetime.datetime.utcfromtimestamp(payload.get("ct") / 1000 + 3600 * 9)) + ',')
                        lt = payload.get("lt")
                        if lt is None:
                            fw.write('0' + ',')
                        else:
                            fw.write(str(lt) + ',')

                        ln = payload.get("ln")
                        if ln is None:
                            fw.write('0' + ',')
                        else:
                            fw.write(str(ln) + ',')
                        fw.write(str(payload.get("ac")) + ',')
                        fw.write(str(payload.get("al")) + ',')
                        fw.write(str(payload.get("gx")) + ',')
                        fw.write(str(payload.get("gy")) + ',')
                        fw.write(str(payload.get("gz")) + ',')
                        fw.write(str(payload.get("ax")))
                        fw.write('\n')
            fw.close()
            if dataIndex >= 1:
                df = pd.read_csv(f_name[0:-4] + '_cv.csv')
                df = df.sort_values(by=['ts', 'ct']).reset_index(drop=True)
                df.loc[0, 'dId'] = str(dId)
                preTripCode = str('')
                trip_num = 0
                idx2 = 0
                for rows in df.iterrows():
                    line = rows[1]
                    if preTripCode != line['TripCode']:
                        trip_num = trip_num + 1
                    df.loc[idx2, 'trip_num'] = trip_num
                    preTripCode = line['TripCode']
                    idx2 = idx2 + 1

                try:
                    df.to_csv(f_name[0:-4] + '_cv.csv', index=False)
                    self.label_result.setText("Complete Converting")
                except:
                    self.label_result.setText("Make sure the file is open")

            else:
                self.label_result.setText("No Valid Data")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()