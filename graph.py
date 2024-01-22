import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os

# 파일 경로
path = "C:/leve/project3/csv/city"

# 파일 내의 모든 CSV 파일 가져오기
all_paths = glob.glob(path + "/*.csv")

# 맑은 고딕 폰트 경로 설정 (Windows 기본 제공)
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 맑은 고딕 폰트 파일의 경로로 수정

# 맑은 고딕 폰트로 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# 모든 파일을 하나의 DataFrame으로 합침
dfs = [pd.read_csv(file, encoding='euc-kr') for file in all_paths]  # 한글 인코딩
city_csv = pd.concat(dfs, ignore_index=True)

# 데이터명 뽑아내기
city_names = city_csv['ename'].unique()
city_dataDate = city_csv['dataDate'].unique()
city_issueVal = city_csv['issueVal']

# 생성된 그래프를 저장할 디렉토리 경로
save_path = "C:/leve/project3/static/image/"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 각 도시에 대한 그래프 생성 및 저장
for city_name in city_names:
    select_city = city_csv[city_csv['ename'] == city_name]

    # 그래프 그리기
    plt.title(f'{select_city["ename"].iloc[0]}')  # 타이틀 - 선택된 도시 이름 가져옴
    plt.ylabel("미세먼지 농도")  # y축 레이블
    plt.xlabel("날짜")  # x축 레이블
    date_format = DateFormatter("24-%m-%d")  # 날짜 포맷 설정
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))  # X축에 표시될 최대 눈금 수 설정
    plt.gca().xaxis.set_major_formatter(date_format)  # 날짜 포맷 적용
    min_val = select_city['issueVal'].min()
    max_val = select_city['issueVal'].max()
    y_ticks = [min_val + i * ((max_val - min_val) / 3) for i in range(4)]
    y_tick_labels = ['좋음', '보통', '나쁨', '매우 나쁨']
    plt.yticks(y_ticks, y_tick_labels)
    # 좋음 ~ 보통

    for i in range(len(select_city) - 1):
        value1 = select_city['issueVal'].iloc[i]
        value2 = select_city['issueVal'].iloc[i + 1]

        if value1 <= y_ticks[1]:  # 좋음 ~ 보통 (초록)
            color = 'green'
        elif value1 <= y_ticks[2] or value2 <= y_ticks[2]:  # 보통 ~ 나쁨 (주황)
            color = 'orange'
        else:  # 나쁨 ~ 매우 나쁨 (빨강)
            color = 'red'

        plt.plot(select_city['dataDate'].iloc[i:i + 2],
                 select_city['issueVal'].iloc[i:i + 2], color=color, label=city_name)

    # 파일로 저장
    save_filename = f"{city_name}_graph.png"
    save_filepath = os.path.join(save_path, save_filename)
    plt.savefig(save_filepath)
    plt.close()  # 그래프 초기화

print("그래프 저장이 완료되었습니다.")
