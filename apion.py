from flask import Flask, render_template
import requests
import json
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
import csv


# apion은 api 호출후 csv 저장까지 하는 곳

app = Flask(__name__)


def apion():
    # API 요청을 보낼 URL
    url = 'http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'
    # API 요청에 필요한 매개변수 설정
    all_data = []

    params_base = {
        'serviceKey': 'ZeDpCP/aGPPotON7mWn1rOKEkg/fKcDd+R2EFqLRJX6NWXzTPqN1lZAK50lg7nTKyAFabPpP300i5IQz1PDh5Q==',
        'returnType': 'json',
        'numOfRows': '100',
        'year': '필요한년도 입력',  # 필요한 자료의 년도 입력
        'itemCode': ''
    }

    # 페이지 합치기
    try:
        for page_no in range(1, 10):
            params = params_base.copy()
            params['pageNo'] = str(page_no)

            # requests 라이브러리를 사용하여 API에 GET 요청 보내기
            response = requests.get(url, params=params, timeout=(60, 60))
            # 요청이 실패한 경우에 예외 처리
            if response.status_code != 200:
                print(f"API 요청에 실패했습니다. (Status Code: {response.status_code})")
                return f"API 요청에 실패했습니다. (Status Code: {response.status_code})"

            # 응답 내용 출력
            print("API 응답 내용:", response.text)

            # JSON 데이터 파싱
            json_data = response.json()
            # 파싱된 데이터 중 필요한 부분만 추출
            items = json_data.get("response", {}).get(
                "body", {}).get("items", [])
            all_data.extend(items)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return all_data

# csv 파일 생성 코드


def save_to_csv(data, filename='필요한년도.csv', directory='csv'):  # 호출한 자료의 년도 입력
    try:
        # 지정된 디렉토리가 없으면 생성
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 파일 경로 설정
        filepath = os.path.join(directory, filename)

        with open(filepath, mode='w', newline='', encoding='euc-kr') as file:
            writer = csv.writer(file)
            # CSV 파일 헤더 작성
            writer.writerow(data[0].keys())
            # 데이터 작성
            for row in data:
                writer.writerow(row.values())

        return f"Data saved to {filepath} successfully."
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def index():
    # apion 함수 호출하여 데이터 가져오기
    apion_data = apion()

    # apion_data가 None이면 에러 처리
    if isinstance(apion_data, str):
        return apion_data

    # HTML 템플릿에 데이터 전달하여 렌더링
    return render_template('apion.html', items=apion_data)

# save 접속시 호출한 API정보를 csv 파일로 저장


@app.route('/save')
def save_to_csv_route():
    # apion 함수 호출하여 데이터 가져오기
    apion_data = apion()

    # apion_data가 None이면 에러 처리
    if isinstance(apion_data, str):
        return apion_data

    # CSV 파일로 데이터 저장
    result_message = save_to_csv(apion_data)

    return result_message


if __name__ == '__main__':
    app.run(debug=True)
