from pyqt5_material import apply_stylesheet
import sys
import PyQt5
from PyQt5.QtWidgets import * # QApplication, QWidgets, QTableView
from PyQt5.QtGui import *
from PyQt5.QtCore import * #QAbstractTableModel, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtWidgets
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GraphData import GraphData1, GraphData2, GraphData3, GraphData4, ResultData

#크기 지정
screenSize = (1200, 930) # 창 크기
mainBtnSize = (300, 176) # 메인버튼 크기
prevBtnSize = (60, 40, 150, 50) #뒤로가기 버튼
gMenuSize = (300, 176) #분석메뉴 버튼사이즈

#메인화면 구성 클래스
class MainWindow(QDialog):
    #메인 로드
    def __init__(self):
        self.clickCheck = [0,0,0] #버튼 1, 2, 3 각각 누른 횟수
        super(MainWindow, self).__init__()
        uic.loadUi("mainScreen.ui",self)
        self.setStyleSheet("background-image:url(./newImg/newMainImg.jpg);")
        self.setFixedSize(screenSize[0],screenSize[1])

        #메인버튼 1 (영화조회)

        ## 버튼에 이미지 입히기 : Pixmap() -> .load(imagePath) -> QIcon(Pixmap객체) -> 버튼객체.setIcon(QIcon객체)
        self.mainbtn1.setIcon(QIcon(QPixmap("./newImg/newBtn1.png")))

        self.mainbtn1.setIconSize(QSize(mainBtnSize[0],mainBtnSize[1]))
        self.mainbtn1.setGeometry(100, 160, mainBtnSize[0], mainBtnSize[1])
        self.mainbtn1.clicked.connect(self.gotoTableScreen) #테이블 조회 페이지로

        #메인버튼 2 (영화분석)
        self.mainbtn2.setIcon(QIcon(QPixmap("./newImg/newBtn2.png")))
        self.mainbtn2.setIconSize(QSize(mainBtnSize[0], mainBtnSize[1]))
        self.mainbtn2.setGeometry(100, 360, mainBtnSize[0], mainBtnSize[1])
        self.mainbtn2.clicked.connect(self.gotoAnalysisScreen) #분석그래프 조회 페이지로

        #메인버튼 3 (흥행도구하기)
        self.mainbtn3.setIcon(QIcon(QPixmap("./newImg/newBtn3.png")))
        self.mainbtn3.setIconSize(QSize(mainBtnSize[0], mainBtnSize[1]))
        self.mainbtn3.setGeometry(100, 560, mainBtnSize[0], mainBtnSize[1])
        self.mainbtn3.clicked.connect(self.gotoCheckBoardScreen) # 흥행도 구하기 페이지로

#스크린 진입 메소드
    #테이블 조회 화면
    def gotoTableScreen(self):
        # 버튼을 처음 누를때 처리하는 조건문
        # 위젯에 스크린을 새로 추가
        if(self.clickCheck[0] == 0):
            self.screen2 = TableScreen()
            widget.addWidget(self.screen2)
            self.clickCheck[0] = 1
            widget.setCurrentWidget(self.screen2)
        # 이미 한번 눌렀던 경우에 위젯을 새로 추가하지않고 선택된 위젯 인덱스만 변경하여 화면 출력
        else:
            widget.setCurrentWidget(self.screen2)
    #분석 화면
    def gotoAnalysisScreen(self):
        if(self.clickCheck[1] == 0):
            self.screen3 = AnalysisScreen()
            widget.addWidget(self.screen3)

            self.clickCheck[1] = 1
            widget.setCurrentWidget(self.screen3)
        else:
            widget.setCurrentWidget(self.screen3)

    def gotoCheckBoardScreen(self):
        if (self.clickCheck[2] == 0):
            self.screen4 = CheckBoardScreen()
            widget.addWidget(self.screen4)
            self.clickCheck[2] = 1
            widget.setCurrentWidget(self.screen4)
        else:
            widget.setCurrentWidget(self.screen4)

    def gotoMain(self):
        widget.setCurrentIndex(0) #메인으로

#ui 클래스 정의
class TableScreen(QDialog):
    def __init__(self):
        super(TableScreen, self).__init__()
        uic.loadUi("tablescreen.ui",self) #테이블 스크린 ui 로드

        self.lbl_bg.setPixmap(QPixmap("./newImg/mainbtn1bg.jpg"))
        self.lbl_bg.setGeometry(0, 0, screenSize[0], screenSize[1])
        # self.setStyleSheet("background-image:url(./newImg/mainbtn1bg.jpg);")

        self.btnPrev1.clicked.connect(mainwindow.gotoMain)
        self.btnPrev1.setStyleSheet("background-color: rgb(249,235,235);")
        #콤보박스 처리
        self.viewList = ['전체', '1000만 이상', '1000만~900만', '900만~800만', '800만~700만',
                    '700만~600만', '600만~500만']
        # for item in self.viewList:
        #     self.cmb.addItem(item)
        self.cmb.setStyleSheet("background-color: rgb(249,235,235);")
        self.cmb.addItems(self.viewList)

        #데이터 전처리
        self.df = pd.read_csv("./movie_new.csv", index_col=0) #인덱스 지우고 출력
        df2 = pd.read_csv("./movie4.csv")
        self.df['관객수'] = df2['관객수']

        list = np.array(self.df['관객수'].tolist())  # 총 관객수를 리스트로 읽기
        for i in range(len(list)):  # 전체 영화 데이터에 대하여
            list[i] = list[i].replace(',', '')  # 전처리(관객수에서 ,값 삭제)
        people = np.array(list, dtype=np.int64)  # string값을 정수 값으로 변환

        self.df_people1 = self.df[people >= 10000000]
        self.df_people2 = self.df[(people < 10000000) & (people >= 9000000)]
        self.df_people3 = self.df[(people < 9000000) & (people >= 8000000)]
        self.df_people4 = self.df[(people < 8000000) & (people >= 7000000)]
        self.df_people5 = self.df[(people < 7000000) & (people >= 6000000)]
        self.df_people6 = self.df[(people < 6000000) & (people >= 5000000)]

        self.viewTable(self.df)

        self.cmb.view().pressed.connect(self.handleItemPressed)

    def handleItemPressed(self, index):
        item = self.cmb.model().itemFromIndex(index)
        value = item.text()

        if(value == self.viewList[1]):
            self.viewTable(self.df_people1)
        elif(value == self.viewList[2]):
            self.viewTable(self.df_people2)
        elif (value == self.viewList[3]):
            self.viewTable(self.df_people3)
        elif (value == self.viewList[4]):
            self.viewTable(self.df_people4)
        elif (value == self.viewList[5]):
            self.viewTable(self.df_people5)
        elif (value == self.viewList[6]):
            self.viewTable(self.df_people6)
        else:
            self.viewTable(self.df)

    # 판다스 불러오기
    def viewTable(self, df):
        self.model = pandasModel(df)
        self.tableView.setModel(self.model)

        self.tableView.show()

#판다스 처리 모듈
class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
    def rowCount(self,  parent=None):
        return self._data.shape[0]
    def columnCount(self, parent=None):
        return self._data.shape[1]
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class AnalysisScreen(QDialog):
    def __init__(self):
        #그래프 페이지 위젯 추가
        self.clickCheck2 = [0,0,0,0,0]

        super(AnalysisScreen, self).__init__()
        uic.loadUi("graphmenuscreen.ui", self) #분석 버튼나열 스크린 ui 로드

        self.lblbg2.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lblbg2.setGeometry(0, 0, screenSize[0], screenSize[1])
        self.btnPrev2.clicked.connect(mainwindow.gotoMain)
        self.btnPrev2.setStyleSheet("background-color: rgb(249,235,235);")

        #분석메뉴 버튼 5개 디자인
        self.btnGraph1.setIcon(QIcon(QPixmap("./gMenuImg/rtime.jpg")))
        self.btnGraph1.setIconSize(QSize(gMenuSize[0], gMenuSize[1]))
        # self.btnGraph1.setStyleSheet('image:url(../gMenuImg/rtime.jpg);')
        self.btnGraph1.clicked.connect(self.gotoGraph1) #러닝시간 분석 ui로

        self.btnGraph2.setIcon(QIcon(QPixmap("./gMenuImg/date.jpg")))
        self.btnGraph2.setIconSize(QSize(gMenuSize[0], gMenuSize[1]))
        self.btnGraph2.clicked.connect(self.gotoGraph2)

        self.btnGraph3.setIcon(QIcon(QPixmap("./gMenuImg/age.jpg")))
        self.btnGraph3.setIconSize(QSize(gMenuSize[0], gMenuSize[1]))
        self.btnGraph3.clicked.connect(self.gotoGraph3)

        self.btnGraph4.setIcon(QIcon(QPixmap("./gMenuImg/word.jpg")))
        self.btnGraph4.setIconSize(QSize(gMenuSize[0], gMenuSize[1]))
        self.btnGraph4.clicked.connect(self.gotoGraph4)

        self.btnGraph5.setIcon(QIcon(QPixmap("./gMenuImg/genre.jpg")))
        self.btnGraph5.setIconSize(QSize(gMenuSize[0], gMenuSize[1]))
        self.btnGraph5.clicked.connect(self.gotoGraph5)


    def gotoGraph1(self):
        #러닝시간에 해당하는 그래프 처리 메소드
        if (self.clickCheck2[0] == 0):
            self.screen5 = Graph1Screen()
            widget.addWidget(self.screen5)
            self.clickCheck2[0] = 1
            widget.setCurrentWidget(self.screen5)
        else:
            widget.setCurrentWidget(self.screen5)

    #개봉시기 버튼
    def gotoGraph2(self):
        #러닝시간에 해당하는 그래프 처리 메소드
        if (self.clickCheck2[1] == 0):
            self.screen6 = Graph2Screen()
            widget.addWidget(self.screen6)
            self.clickCheck2[1] = 1
            widget.setCurrentWidget(self.screen6)
        else:
            widget.setCurrentWidget(self.screen6)
    #3번버튼
    def gotoGraph3(self):
        #러닝시간에 해당하는 그래프 처리 메소드
        if (self.clickCheck2[2] == 0):
            self.screen7 = Graph3Screen()
            widget.addWidget(self.screen7)
            self.clickCheck2[2] = 1
            widget.setCurrentWidget(self.screen7)
        else:
            widget.setCurrentWidget(self.screen7)
    # #4번버튼
    def gotoGraph4(self):
        #러닝시간에 해당하는 그래프 처리 메소드
        if (self.clickCheck2[3] == 0):
            self.screen8 = Graph4Screen()
            widget.addWidget(self.screen8)
            self.clickCheck2[3] = 1
            widget.setCurrentWidget(self.screen8)
        else:
            widget.setCurrentWidget(self.screen8)
    # #5번버튼
    def gotoGraph5(self):
        #러닝시간에 해당하는 그래프 처리 메소드
        if (self.clickCheck2[4] == 0):
            self.screen9 = Graph5Screen()
            widget.addWidget(self.screen9)
            self.clickCheck2[4] = 1
            widget.setCurrentWidget(self.screen9)
        else:
            widget.setCurrentWidget(self.screen9)

    def gotoGraphMenu(self):
        widget.setCurrentWidget(MainWindow.screen3)


class CheckBoardScreen(QDialog):
    def __init__(self):
        super(CheckBoardScreen, self).__init__()
        uic.loadUi("checkboardscreen.ui", self) #흥행도 구하기
        self.lblBoardbg.setPixmap(QPixmap("./newImg/mainbtn3bg.jpg"))
        self.lblBoardbg.setGeometry(0, 0, screenSize[0], screenSize[1])

        self.btnPrev2.clicked.connect(self.getbgInit)
        self.btnPrev2.setStyleSheet("background-color: rgb(249,235,235);")

        # 라디오버튼 초기체크 설정
        self.rbLetter1.setChecked(True)
        self.rbRuntime1.setChecked(True)
        self.rbMonth1.setChecked(True)
        self.rbAge1.setChecked(True)
        self.rbGenre1.setChecked(True)

        #결과출력 버튼 이벤트 발동
        self.btnResult.clicked.connect(self.getResult)

    def getbgInit(self):
        mainwindow.gotoMain()
        self.lblResult.setText('')
        self.lblBoardbg.setPixmap(QPixmap("./newImg/mainbtn3bg.jpg"))
    #흥행도 결과 이벤트 메소드
    def getResult(self):
        # data1, data2, data3, data4, data5 = ResultData.getAttrData() # 아래 로직에 매핑

        labelRadio = {'1글자': 3, '2글자': 14, '3글자': 17, '4글자': 20, '5글자': 17, '6글자': 11, '7글자': 9,
                        '8글자': 7, '9글자': 3, '10글자': 5}
        runningRadio = {'100이하': 3, '100~110': 9,'110~120': 14,'120~130': 20, '130~140': 17,  '140~150': 11,
                      '150~160': 5,'160~': 7}
        monthRadio = {'1월': 10, '2월': 8, '3월': 4, '4월': 10, '5월': 10, '6월': 14, '7월': 20,
                      '8월': 16, '9월': 10, '10월': 12, '11월': 6, '12월': 18}
        ageRadio = {'전체이용가': 10, '12세': 20, '15세': 17, '청불': 10 }
        genreRadio = {'드라마': 18,'미스터리': 5,'멜로': 9,'범죄': 15, '사극': 15,'스릴러': 5, '어드벤쳐': 9,
                    '애니메이션': 9,'액션': 20, '전쟁': 12, '코미디': 15,'판타지': 9, 'SF': 15}

        ## groupBox.setFont("글꼴", 글씨크기)
        totalScore = 0

        # 딕셔너리는 그냥 values로 접근하면 인덱싱이 안먹힌다.
        # list()로 컨버트 해주면 인덱싱 가능
        # 위젯이 상속된 순서에따라 인덱싱이 달라짐
        for i, btn in enumerate(self.groupBox1.children()):
            if(btn.isChecked()):
                totalScore += list(labelRadio.values())[i]
                # labelscore = list(labelRadio.values())[i]
                # print("선택된 글자 수 반영점수 : ", labelscore)
        for i, btn in enumerate(self.groupBox2.children()):
            # print(btn)
            if(btn.isChecked()):
                totalScore += list(runningRadio.values())[i]

        for i, btn in enumerate(self.groupBox3.children()):
            if(btn.isChecked()):
                totalScore += list(monthRadio.values())[i]

        for i, btn in enumerate(self.groupBox4.children()):
            if(btn.isChecked()):
                totalScore += list(ageRadio.values())[i]

        for i, btn in enumerate(self.groupBox5.children()):
            if(btn.isChecked()):
                totalScore += list(genreRadio.values())[i]

        self.printResult(totalScore)
    #흥행도 조회 결과 출력
    def printResult(self, score):
        self.lblBoardbg.setPixmap(QPixmap("./newImg/resultbg.png"))

        if score >= 85:
            self.lblResult.setText('매우 높습니다!!')
            self.lblResult.setGeometry(805,500,300,141)
            self.lblResult.setStyleSheet('color: rgb(255,0,0);') #ff0000
        elif score >= 60:
            self.lblResult.setText('높습니다!')
            self.lblResult.setGeometry(840, 500, 300, 141)
            self.lblResult.setStyleSheet('color:#FFD700;')
        elif score >= 40:
            self.lblResult.setText('보통입니다')
            self.lblResult.setGeometry(835, 500, 300, 141)
            self.lblResult.setStyleSheet('color:#DCEDC1;')
        else:
            self.lblResult.setText('저조합니다..')
            self.lblResult.setGeometry(825, 500, 300, 141)
            self.lblResult.setStyleSheet('color:#C0C0C0;')

#그래프 분석 버튼 5개 각각에 대한 스크린 클래스
class Graph1Screen(QDialog):
    def __init__(self):
        super(Graph1Screen, self).__init__()
        uic.loadUi("graph1screen.ui", self)

        #배경지정
        self.lbl_bg.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lbl_bg.setGeometry(0, 0, screenSize[0], screenSize[1])

        #뒤로가기
        self.btnPrev2_1.clicked.connect(mainwindow.gotoAnalysisScreen)
        self.btnPrev2_1.setStyleSheet("background-color: rgb(249,235,235);")
        # self.canvas = Canvas(self)
        self.graph1 = GraphData1() #그래프 객체 생성

        self.value1 = self.graph1.getDataValue()[0] #액션 러닝타임 리스트
        self.value2 = self.graph1.getDataValue()[1] #사극 ~
        self.value3 = self.graph1.getDataValue()[2] #드라마 ~
        self.value4 = self.graph1.getDataValue()[3]

        self.canvas1 = FigureCanvas(self.graph1.JWRuntimeByGenreGraph("액션 흥행작의 러닝타임 비율(분)", self.value1))
        self.canvas2 = FigureCanvas(self.graph1.JWRuntimeByGenreGraph("사극 흥행작의 러닝타임 비율(분)", self.value2))
        self.canvas3 = FigureCanvas(self.graph1.JWRuntimeByGenreGraph("드라마 흥행작의 러닝타임 비율(분)", self.value3))
        self.canvas4 = FigureCanvas(self.graph1.JWRuntimeByGenreGraph("코미디 흥행작의 러닝타임 비율(분)", self.value4))
        self.canvaslist = [self.canvas1, self.canvas2, self.canvas3, self.canvas4]

        # 콤보박스
        self.genreList = ['선택하세요','액션장르 러닝타임 비율', '사극장르 러닝타임 비율 ', '드라마장르 러닝타임 비율', '코미디장르 러닝타임 비율']
        for item in self.genreList:
            self.cmbGraph1.addItem(item)
        # QComboBox.currentText()
        #lambda x : (값1) if (조건1) else 값2 (조건2) else 값3 else
        self.cmbGraph1.setStyleSheet("background-color: rgb(249,235,235);")
        self.cmbGraph1.currentIndexChanged.connect(self.printGraph1)

    #CanvasFigure위젯 상속 -> 레이아웃에 출력/비출력 관리
    def printGraph1(self):
        if(self.cmbGraph1.currentText() == self.genreList[1]):
            if(self.vLay1.count() >= 1): #이미 하나 띄워논 상태면
                for canvas in self.canvaslist:
                    canvas.setParent(None) #위젯을 레이아웃에서 떼어낸다.
            self.vLay1.addWidget(self.canvas1)
        elif (self.cmbGraph1.currentText() == self.genreList[2]):
            if (self.vLay1.count() >= 1):
                for canvas in self.canvaslist:
                    canvas.setParent(None)
            self.vLay1.addWidget(self.canvas2)
        elif (self.cmbGraph1.currentText() == self.genreList[3]):
            if (self.vLay1.count() >= 1):
                for canvas in self.canvaslist:
                    canvas.setParent(None)
            self.vLay1.addWidget(self.canvas3)
        elif (self.cmbGraph1.currentText() == self.genreList[4]):
            if (self.vLay1.count() >= 1):
                for canvas in self.canvaslist:
                    canvas.setParent(None)
            self.vLay1.addWidget(self.canvas4)

class Graph2Screen(QDialog):
    def __init__(self):
        super(Graph2Screen, self).__init__()
        uic.loadUi("graph2screen.ui", self)

        self.lbl_bg2.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lbl_bg2.setGeometry(0, 0, screenSize[0], screenSize[1])

        self.btnPrev2_2.clicked.connect(mainwindow.gotoAnalysisScreen)
        self.btnPrev2_2.setStyleSheet("background-color: rgb(249,235,235);")

        self.graph2 = GraphData2()
        self.canvas2_1 = FigureCanvas(self.graph2.JHSortedByYearGraph(self.graph2.getDataValue(0)))
        self.canvas2_2 = FigureCanvas(self.graph2.JHSortedByMonthGraph(self.graph2.getDataValue(1)))

        self.canvas2list = [self.canvas2_1, self.canvas2_2]

        # 콤보박스
        self.dateList = ['선택하세요','연도별 흥행영화 추이', '월별 흥행영화 추이']
        for item in self.dateList:
            self.cmbGraph2.addItem(item)

        self.cmbGraph2.currentIndexChanged.connect(self.printGraph2)
        self.cmbGraph2.setStyleSheet("background-color: rgb(249,235,235);")

    def printGraph2(self):
        if (self.cmbGraph2.currentText() == self.dateList[1]):  # [0] 여백
            if (self.vLay2.count() >= 1):
                for canvas in self.canvas2list:
                    canvas.setParent(None)
            self.vLay2.addWidget(self.canvas2_1)
        elif (self.cmbGraph2.currentText() == self.dateList[2]):
            if (self.vLay2.count() >= 1):
                for canvas in self.canvas2list:
                    canvas.setParent(None)
            self.vLay2.addWidget(self.canvas2_2)

class Graph3Screen(QDialog):
    def __init__(self):
        super(Graph3Screen, self).__init__()
        uic.loadUi("graph3screen.ui", self)

        self.lbl_bg3.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lbl_bg3.setGeometry(0, 0, screenSize[0], screenSize[1])

        self.btnPrev2_3.clicked.connect(mainwindow.gotoAnalysisScreen)
        self.btnPrev2_3.setStyleSheet("background-color: rgb(249,235,235);")

        self.graph3 = GraphData3()

        self.canvas3_1 = FigureCanvas(self.graph3.YJMeanAgesPerDayGraph())
        self.canvas3_2 = FigureCanvas(self.graph3.YJRatingByAgesGraph())

        self.canvas3list = [self.canvas3_1, self.canvas3_2]

        # 콤보박스
        self.ratingList = ['선택하세요','연령등급별 첫날 평균 관객 빈도', '연령 등급별 흥행영화 빈도']
        for item in self.ratingList:
            self.cmbGraph3.addItem(item)

        self.cmbGraph3.currentIndexChanged.connect(self.printGraph3)
        self.cmbGraph3.setStyleSheet("background-color: rgb(249,235,235);")

    #위젯 상속 -> 레이아웃에 출력/비출력 관리
    def printGraph3(self):

        if(self.cmbGraph3.currentText() == self.ratingList[1]): #[0] 여백
            if(self.vLay3.count() >= 1):
                for canvas in self.canvas3list:
                    canvas.setParent(None)
            self.vLay3.addWidget(self.canvas3_1)
        elif (self.cmbGraph3.currentText() == self.ratingList[2]):
            if (self.vLay3.count() >= 1):
                for canvas in self.canvas3list:
                    canvas.setParent(None)
            self.vLay3.addWidget(self.canvas3_2)

class Graph4Screen(QDialog):
    def __init__(self):
        super(Graph4Screen, self).__init__()
        uic.loadUi("graph4screen.ui", self)

        self.lbl_bg4.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lbl_bg4.setGeometry(0, 0, screenSize[0], screenSize[1])

        self.btnPrev2_4.clicked.connect(mainwindow.gotoAnalysisScreen)
        self.btnPrev2_4.setStyleSheet("background-color: rgb(249,235,235);")

        self.graph4 = GraphData4()

        self.canvas4_1 = FigureCanvas(self.graph4.lettersbyPopRatioGraph(self.graph4.getDataValue(0)))
        self.canvas4_2 = FigureCanvas(self.graph4.PopularGenrelettersGraph(self.graph4.getDataValue(1)))

        self.canvas4list = [self.canvas4_1, self.canvas4_2]

        # 콤보박스
        self.lettersList = ['선택하세요','관객수 비중에 대한 글자수 분포', '상위 4개 장르에 대한 영화 글자수 분포']
        for item in self.lettersList:
            self.cmbGraph4.addItem(item)

        self.cmbGraph4.currentIndexChanged.connect(self.printGraph4)
        self.cmbGraph4.setStyleSheet("background-color: rgb(249,235,235);")

    #위젯 상속 -> 레이아웃에 출력/비출력 관리
    def printGraph4(self):
        if(self.cmbGraph4.currentText() == self.lettersList[1]): #[0] 여백
            if(self.vLay4.count() >= 1):
                for canvas in self.canvas4list:
                    canvas.setParent(None)
            self.vLay4.addWidget(self.canvas4_1)
        elif (self.cmbGraph4.currentText() == self.lettersList[2]):
            if (self.vLay4.count() >= 1):
                for canvas in self.canvas4list:
                    canvas.setParent(None)
            self.vLay4.addWidget(self.canvas4_2)

class Graph5Screen(QDialog):
    def __init__(self):
        super(Graph5Screen, self).__init__()
        uic.loadUi("graph5screen.ui", self)

        self.lbl_bg5.setPixmap(QPixmap("./newImg/mainbtn2bg.jpg"))
        self.lbl_bg5.setGeometry(0, 0, screenSize[0], screenSize[1])

        self.btnPrev2_5.clicked.connect(mainwindow.gotoAnalysisScreen)
        self.btnPrev2_5.setStyleSheet("background-color: rgb(249,235,235);")

        self.graph5 = GraphData3()

        self.canvas5_1 = FigureCanvas(self.graph5.YJMeanThemesGraph())
        self.canvas5_2 = FigureCanvas(self.graph5.YJMinMaxThemes1dayGraph())

        self.canvas5list = [self.canvas5_1, self.canvas5_2]

        # 콤보박스
        self.genreList = ['선택하세요','장르별 개봉 1일차 평균 관객 수', '장르별 첫날 관객 평균,최대,최소']
        for item in self.genreList:
            self.cmbGraph5.addItem(item)

        self.cmbGraph5.currentIndexChanged.connect(self.printGraph5)
        self.cmbGraph5.setStyleSheet("background-color: rgb(249,235,235);")

    #위젯 상속 -> 레이아웃에 출력/비출력 관리
    def printGraph5(self):
        if(self.cmbGraph5.currentText() == self.genreList[1]): #[0] 여백
            if(self.vLay5.count() >= 1):
                for canvas in self.canvas5list:
                    canvas.setParent(None)
            self.vLay5.addWidget(self.canvas5_1)
        elif (self.cmbGraph5.currentText() == self.genreList[2]):
            if (self.vLay5.count() >= 1):
                for canvas in self.canvas5list:
                    canvas.setParent(None)
            self.vLay5.addWidget(self.canvas5_2)

# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
widget.addWidget(mainwindow)
# widget.setAcceptDrops(True)

widget.setFixedSize(screenSize[0],screenSize[1])
# widget.setGeometry()
widget.show()
widget.setWindowTitle("MovieAnalysisProgram")
widget.setWindowIcon(QIcon('./bhhj.ico'))
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

#참고자료
#백그라운드 이미지 관련: https://www.youtube.com/watch?v=uAXm-oFsDuA&list=PLnzqK5HvcpwRd3yoMoUe1H5QFK2I6sGo9&index=24&ab_channel=%D9%85%D8%AD%D9%85%D8%AF%D8%B4%D9%88%D8%B4%D8%A7%D9%86
#UI 파일을 파이썬 코드에서 로드하기 : https://wikidocs.net/5227
#Qt Documentation : https://doc.qt.io/qt-5/qtwidgets-index.html#widgets
#PyQt5 Designer + Python Stacked Widget Walkthrough : https://youtu.be/Vq1laKeSk9M
#실행파일 만들기 (PyInstaller) : https://wikidocs.net/21952
#How to use Pandas, Matplotlib and Seaborn to draw pie charts : https://www.dataforeverybody.com/matplotlib-seaborn-pie-charts/
#Seaborn : User guide and tutorial : https://seaborn.pydata.org/tutorial.html
#아이콘, 버튼 hover 이미지 바꾸기(Qt designer, in code)
#PyQt + PyCharm 계산기 예제 강좌 : https://youtube.com/playlist?list=PLh665u8WZRR1d1hhLuZQThLhZbaOE5Whf
#Multiple Screens in PyQt5: Switch screens without opening a new window : https://youtu.be/82v2ZR-g6wY
#Color Hex Color Codes : https://www.color-hex.com/
#Display pandas DataFrame using PyQt5 | Python PyQt Tutotiral : https://www.youtube.com/watch?v=hJEQEECZSH0&ab_channel=JieJenn
#pyqt: how to remove elements from a QVBoxLayout? : https://stackoverflow.com/questions/5889705/pyqt-how-to-remove-elements-from-a-qvboxlayout/5890555
#How to programmatically change/update data in Python PyQt4 TableView? : https://stackoverflow.com/questions/26965185/how-to-programmatically-change-update-data-in-python-pyqt4-tableview
#QComboBox click event : https://stackoverflow.com/questions/35932660/qcombobox-click-event
#pyqt: how to remove a widget? : https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget




#Garbage

# class Canvas(FigureCanvas):
#     def __init__(self, parent):
#         fig, self.ax = plt.subplots(figsize=(2,2), dpi=100)
#         super().__init__(fig)
#         self.setParent(parent)
#
#         t = np.arange(0.0, 2.0, 0.01)
#         s = 1 + np.sin(2 * np.pi * t )
#
#         self.ax.plot(t, s)
#         self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#                     title='About as simple as it gets, folks')
#         self.ax.grid()

# class pandasModel2(QAbstractTableModel):
#     DtypeRole = Qt.UserRole + 1000
#     ValueRole = Qt.UserRole + 1001
#
#     def __init__(self, df=pd.DataFrame(), parent=None):
#         super(pandasModel2, self).__init__(parent)
#         self._dataframe = df
#
#     def setDataFrame(self, dataframe):
#         self.beginResetModel()
#         self._dataframe = dataframe.copy()
#         self.endResetModel()
#
#     def dataFrame(self):
#         return self._dataframe
#
#     dataFrame = pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)
#
#     @pyqtSlot(int, Qt.Orientation, result=str)
#     def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Horizontal:
#                 return self._dataframe.columns[section]
#             else:
#                 return str(self._dataframe.index[section])
#         return QVariant()
#
#     def rowCount(self, parent=QModelIndex()):
#         if parent.isValid():
#             return 0
#         return len(self._dataframe.index)
#
#     def columnCount(self, parent=QModelIndex()):
#         if parent.isValid():
#             return 0
#         return self._dataframe.columns.size
#
#     def data(self, index, role=Qt.DisplayRole):
#         if not index.isValid() or not (0 <= index.row() < self.rowCount() \
#                                        and 0 <= index.column() < self.columnCount()):
#             return QVariant()
#         row = self._dataframe.index[index.row()]
#         col = self._dataframe.columns[index.column()]
#         dt = self._dataframe[col].dtype
#
#         val = self._dataframe.iloc[row][col]
#         if role == Qt.DisplayRole:
#             return str(val)
#         elif role == pandasModel2.ValueRole:
#             return val
#         if role == pandasModel2.DtypeRole:
#             return dt
#         return QVariant()
#
#     def roleNames(self):
#         roles = {
#             Qt.DisplayRole: b'display',
#             pandasModel2.DtypeRole: b'dtype',
#             pandasModel2.ValueRole: b'value'
#         }
#         return roles
#테이블 콤보 선택시 호출처리
# if (self.cmb.currentText() == self.viewList[0]):
        #     nowTable = df[0]
        #     self.model = pandasModel(nowTable)
        # elif (self.cmb.currentText() == self.viewList[1]):
        #     nowTable = df[1]
        #     self.model = pandasModel(nowTable)