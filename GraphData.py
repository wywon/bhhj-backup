import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
#그래프 가져오기

df = pd.read_csv("./movie_new.csv")
df2 = pd.read_csv("./movie4.csv")

#러닝타임
class GraphData1:
    def __init__(self):
        #한글폰트 설정
        fm.get_fontconfig_fonts()
        font_location = 'C:\\Windows\\Fonts\\malgun.ttf'  # For Windows
        font_name = fm.FontProperties(fname=font_location).get_name()
        mpl.rc('font', family=font_name)

    def getDataValue(self):
        genre_values = df['장르']
        genrelist = genre_values.drop_duplicates()

        df_action = df[genre_values == genrelist[4]]  # 불린추출하기
        df_history = df[genre_values == genrelist[0]]
        df_drama = df[genre_values == genrelist[3]]
        df_comedy = df[genre_values == genrelist[1]]

        # 액션
        runtime = df_action['러닝시간']
        df_action_runtime1 = df_action[runtime > 160]
        df_action_runtime2 = df_action[(runtime <= 160) & (runtime > 130)]
        df_action_runtime3 = df_action[(runtime <= 130) & (runtime > 100)]
        df_action_runtime4 = df_action[(runtime <= 100)]


        rtimeList = []
        rtimeList.append(len(df_action_runtime1))
        rtimeList.append(len(df_action_runtime2))
        rtimeList.append(len(df_action_runtime3))
        rtimeList.append(len(df_action_runtime4))

        # 사극
        runtime = df_history['러닝시간']
        df_history_runtime1 = df_history[runtime > 160]
        df_history_runtime2 = df_history[(runtime <= 160) & (runtime > 130)]
        df_history_runtime3 = df_history[(runtime <= 130) & (runtime > 100)]
        df_history_runtime4 = df_history[(runtime <= 100)]

        rtimeList1 = []
        rtimeList1.append(len(df_history_runtime1))
        rtimeList1.append(len(df_history_runtime2))
        rtimeList1.append(len(df_history_runtime3))
        rtimeList1.append(len(df_history_runtime4))

        # 드라마
        runtime = df_drama['러닝시간']
        df_drama_runtime1 = df_drama[runtime > 160]
        df_drama_runtime2 = df_drama[(runtime <= 160) & (runtime > 130)]
        df_drama_runtime3 = df_drama[(runtime <= 130) & (runtime > 100)]
        df_drama_runtime4 = df_drama[(runtime <= 100)]

        rtimeList2 = []
        rtimeList2.append(len(df_drama_runtime1))
        rtimeList2.append(len(df_drama_runtime2))
        rtimeList2.append(len(df_drama_runtime3))
        rtimeList2.append(len(df_drama_runtime4))

        # 코미디
        runtime = df_comedy['러닝시간']
        df_comedy_runtime1 = df_comedy[runtime > 160]
        df_comedy_runtime2 = df_comedy[(runtime <= 160) & (runtime > 130)]
        df_comedy_runtime3 = df_comedy[(runtime <= 130) & (runtime > 100)]
        df_comedy_runtime4 = df_comedy[(runtime <= 100)]

        rtimeList3 = []
        rtimeList3.append(len(df_comedy_runtime1))
        rtimeList3.append(len(df_comedy_runtime2))
        rtimeList3.append(len(df_comedy_runtime3))
        rtimeList3.append(len(df_comedy_runtime4))

        rtimeGenreList = [rtimeList, rtimeList1, rtimeList2, rtimeList3]

        return rtimeGenreList

    #러닝타임 별 시간 그래프
    def JWRuntimeByGenreGraph(self, title, rtimeGenre):
        #그래프그리기
        labels = ['160초과', '160이하 130초과', '130이하 100초과', '100이하']
        values = rtimeGenre  # [2] = rtimeList2

        fig = plt.figure(figsize=(2, 2))  # 창 크기
        fig.set_facecolor('white')  # 배경색

        ax = fig.add_subplot()  # 프레임 생성
        pie = ax.pie(values,
                     startangle=90,
                     counterclock=False,  # 시계방향으로 그리기
                     autopct=lambda p: '{:.2f}%'.format(round(p)) if p > 0 else '', #0값 제거
                     colors=['snow', 'pink', 'lavender', 'beige', ],
                     pctdistance=0.5,  # 그래프 떨어트리기
                     explode=[0.05] * 4)
        plt.legend(pie[0], labels)  # 범례 추가하기
        ax.set_title(title)
        ax.grid()
        return fig #plt.pigure -> CanvasFigure

#개봉시기
class GraphData2:
    def __init__(self):
        #한글폰트 설정
        fm.get_fontconfig_fonts()
        font_location = 'C:\\Windows\\Fonts\\malgun.ttf'  # For Windows
        font_name = fm.FontProperties(fname=font_location).get_name()
        mpl.rc('font', family=font_name)

    def getDataValue(self, index):
        #년도 데이터 가공하기
        if(index == 0):
            df_date = df['개봉일']  # 개봉일 속성을 df_date로 불러오기

            # 날짜 데이터 처리위한 전처리 단계
            list = np.array(df_date.tolist())  # np배열로 df_date값 리스트로 넘기기
            for i in range(len(list)):  # 리스트 개수만큼 반복
                list[i] = list[i][0:4]  # ex) 2012-02-01 -> 2012로 자르기

            df['개봉년도'] = list  # 데이터프레임에 '개봉년도'속성 추가
            df_years = df['개봉년도']  # df_years시리즈로 개봉년도속성 추출

            yearlist = df_years.drop_duplicates()  # 중복값 제거

            self.sortedYear = sorted(yearlist)  # 연도 오름차순 정리
            # print(sortedYear)

            yearvalues = []
            for years in self.sortedYear:  # 연도 요소에 대해서
                yearvalues.append(len(df[df_years == years]))  # 연도리스트 값과 일치하는 영화의 개수를 yearvalues리스트에 저장
            return yearvalues

        #월 데이터 가공
        elif(index == 1):
            df_date = df['개봉일']
            # print(df_date)
            # a = df_date[0][5:7]
            # print(a)

            list1 = np.array(df_date.tolist())

            for i in range(len(list1)):
                list1[i] = list1[i][5:7]  # 2001-12-22 -> 12

            df['개봉월'] = list1
            df_months = df['개봉월']
            monthlist = df_months.drop_duplicates()
            self.sortedMonth = sorted(monthlist)
            # print(sortedMonth)

            monthvalues = []
            for months in self.sortedMonth:
                monthvalues.append(len(df[df_months == months]))
            return monthvalues
    #영화 흥행작 개봉연도 추이
    def JHSortedByYearGraph(self, yearValues):
        fig = plt.figure(figsize=(12, 6))  # 12,6 사이즈의 캔버스 생성
        ax = fig.add_subplot()
        ax.bar(self.sortedYear, yearValues, color="springgreen",
                edgecolor="gray", linewidth=3)  # 막대그래프 x=해당 연도 y=영화 수
        plt.xticks(rotation=30, fontsize=17)
        plt.yticks(rotation=0, fontsize=15)
        plt.title("연도별 500만 관객 이상 영화 개수", fontsize=20)  # 그래프 제목설정, 글씨크기
        plt.xlabel("연도", fontsize=18)  # x축 레이블 설정
        plt.ylabel("영화 개수", fontsize=18)  # y축 레이블 설정
        plt.axhline(6.11, 0, 1.55, color='gray', linestyle='--', linewidth='3')

        return fig

    # 영화 흥행작 개봉월 추이
    def JHSortedByMonthGraph(self, monthValues):
        fig = plt.figure(figsize=(12, 6))
        plt.bar(self.sortedMonth, monthValues, color="springgreen",
                edgecolor="gray", linewidth=3)
        plt.xticks(rotation=0, fontsize=18)
        plt.yticks(rotation=0, fontsize=15)
        plt.title("월별 500만 관객 이상 영화 개수", fontsize=20)
        plt.xlabel("월", fontsize=18)
        plt.ylabel("영화 개수", fontsize=18)
        plt.axhline(9.16, 0, 1, color='gray', linestyle='--', linewidth='3', label='평균')

        return fig #CanvasFigure(fig)

#연령등급
class GraphData3:
    df = pd.read_csv("./movie_new.csv")

    def __init__(self):
        # 한글폰트 설정
        fm.get_fontconfig_fonts()
        font_location = 'C:\\Windows\\Fonts\\malgun.ttf'  # For Windows
        font_name = fm.FontProperties(fname=font_location).get_name()
        mpl.rc('font', family=font_name)

    #(1) " 연령등급별 개봉1일차 평균관객 수 "
    def YJMeanAgesPerDayGraph(self):
        group_ages = df.groupby('등급')  # 연령등급별로 그룹묶기
        group_ages_1day = group_ages['첫날관객수']  # 연령등급별그룹에서 첫날관객수
        mean_ages_1day = group_ages_1day.mean()  # 연령등급별 첫날관객수의 평균
        # print(mean_ages_1day)

        fig = plt.figure(figsize=(2,2))
        ax = fig.add_subplot()
        mean_ages_1day.plot.bar(title='연령등급별 첫날 평균 관객 수', figsize=(23, 7), legend=True, fontsize=13);

        plt.xticks(rotation=0)  # 글자방향

        return fig

    #(2) " 흥행하는 영화의 주 연령등급 "
    def YJRatingByAgesGraph(self):
        fig, ax = plt.subplots()
        ax = sns.countplot('등급', data=df)
        ax.set_title('흥행 영화의 주 연령등급')
        ax.set_xlabel('연령등급')
        ax.set_ylabel('영화수')

        plt.xticks(rotation=0, fontsize=10)
        plt.yticks(fontsize=10)
        return fig

    # (3) " 장르별 개봉1일차 평균관객 수 "
    def YJMeanThemesGraph(self):
        group_themes = df.groupby('장르')  # 장르별로 그룹묶기
        group_themes_1day = group_themes['첫날관객수']  # 장르별그룹에서 첫날관객수
        mean_themes_1day = group_themes_1day.mean()  # 장르별 첫날관객수의 평균
        # print(mean_themes_1day)

        # 축적막대그래프 (세로)
        fig = plt.figure()
        ax = fig.add_subplot()
        g = mean_themes_1day.plot.bar(title='장르별 개봉 1일차 평균 관객 수', figsize=(23, 7), legend=True, fontsize=13);
        plt.xticks(rotation=- 20)  # 글자방향

        return fig


    # (4) 장르별 첫날 관객수 평균과 최대최소폭
    def YJMinMaxThemes1dayGraph(self):
        fig = plt.figure(figsize=(20, 10), dpi=80)
        ax = fig.add_subplot()
        g =sns.lineplot(x="장르", y="첫날관객수", data=df)

        return fig

class GraphData4:
    def __init__(self):
        fm.get_fontconfig_fonts()
        # font_location = '/usr/share/fonts/truetype/nanum/NanumGothicOTF.ttf'
        font_location = 'C:\\Windows\\Fonts\\malgun.ttf'  # For Windows
        font_name = fm.FontProperties(fname=font_location).get_name()
        mpl.rc('font', family=font_name)

    def getDataValue(self, index):
        #흥행 영화들의 총 관객 수 지분을 퍼센트로 수치화
        df['관객수'] = df2['관객수']
        tmplist = np.array(df['관객수'].tolist())  # 총 관객수를 리스트로 읽기
        for i in range(len(tmplist)):  # 전체 영화 데이터에 대하여
            tmplist[i] = tmplist[i].replace(',', '')  # 전처리(관객수에서 ,값 삭제)
        tmplist2 = np.array(tmplist, dtype=np.int64)  # string값을 정수 값으로 변환
        popRatio = []
        for i in range(len(tmplist)):
            popRatio.append((tmplist2[i] / sum(tmplist2)) * 100)  # 전체 관객수에 대한 비율값으로 정규화
        df['관객수비중'] = popRatio  # 불러온 데이터프레임에 추가

        self.new_df = df #관객수비중 추가한 데이터테이블

        df_genre = df['장르']  # 장르 속성 가져오기
        # list_genre = df_genre.drop_duplicates()  # 중복값 제거하여 장르의 종류 추출
        # list_genre = df_genre.value_counts()
        #pd.value_counts로 상위 그룹 장르에 대한 글자수 분포 및 중요도 확인
        self.df_genreHead = df[(df_genre == '액션') | (df_genre == '범죄') | (df_genre == '드라마') | (df_genre == '코미디')]

        if index == 0:
            return self.new_df
        elif index == 1:
            return self.df_genreHead

    #관객수 비중에 대한 글자수 분포 그래프
    def lettersbyPopRatioGraph(self, df):
        fig = plt.figure(figsize=(13, 4))

        ax1 = fig.add_subplot(121)
        g = sns.stripplot(x="글자수", y="관객수비중", jitter=False, data=df, ax=ax1)
        ax2 = fig.add_subplot(1, 2, 2)
        g = sns.boxplot(x="글자수", y="관객수비중", palette='Set2', data=df, ax=ax2)
        return fig

    #상위 4개장르의 글자수 분포 확인 그래프
    def PopularGenrelettersGraph(self,df):
        fig = plt.figure(figsize=(5, 4))
        ax = fig.subplots()
        g = sns.stripplot(x="글자수", y="관객수비중", hue="장르",
                      data=df, palette="Set2", jitter=False)

        return fig

class ResultData:
    def __init__(self):
        self.resData = pd.read_csv('./movie_new.csv')

    #스코어 재료
    def getAttrData(self):
        df_letter_cnt = self.resData['글자수'].value_counts()
        df_run_cnt = self.resData['러닝시간'].value_counts()
        df_age_cnt = self.resData['등급'].value_counts()
        df_genre_cnt = self.resData['장르'].value_counts()

        # 월 처리
        df_date = self.resData['개봉일']
        list1 = np.array(df_date.tolist())

        for i in range(len(list1)):
            list1[i] = list1[i][5:7]  # 2001-12-22 -> 12

        self.resData['개봉월'] = list1
        monthlist = sorted(self.resData['개봉월'].drop_duplicates())

        monthvalues = []
        for month in monthlist:
            monthvalues.append(len(self.resData[self.resData['개봉월'] == month]))
        #글자수, 러닝시간, 연령등급, 장르, 월 => 흥행지수 스코어링
        return df_letter_cnt, df_run_cnt, df_age_cnt, df_genre_cnt, monthvalues