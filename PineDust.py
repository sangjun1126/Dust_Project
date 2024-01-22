from flask import Flask, render_template
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

# CSV 파일 로드
fd = pd.read_csv("C:/leve/project3/csv/finedust.csv", encoding='euc-kr')

# 데이터프레임화
fdc_df = pd.DataFrame(fd)

# 데이터프레임 도시별 설정


def create_dataframe_for_city(data):
    try:
        # 기반으로 작업하기 위해 데이터프레임에서 clearVal 열만 추출
        time_series_data = data['clearVal'].values

        # MinMaxScaler 초기화
        scaler = MinMaxScaler(feature_range=(0, 1))

        # 시계열 데이터 정규화
        scaled_data = scaler.fit_transform(time_series_data.reshape(-1, 1))

        x_train = []
        y_train = []

        for i in range(60, len(scaled_data)):
            x_train.append(scaled_data[i - 60:i, 0])
            y_train.append(scaled_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.array(x_train)  # x_train을 numpy 배열로 변환
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        return x_train, y_train, scaler, scaled_data

    except Exception as e:
        print(f"An error occurred: {e}")
        # 예외가 발생했을 때 추가적인 작업을 수행하거나 오류 메시지를 기록하는 등의 작업 수행
        return None, None, None, None  # 예외가 발생한 경우 None을 반환하거나 다른 처리를 수행

# LSTM 모델 생성 함수


def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adadelta')
    return model


# 각 도시에 대한 LSTM 모델 생성 및 학습
city_names = fdc_df['ename'].unique()
for city in city_names:
    # 도시별로 데이터 추출
    city_data = fdc_df[fdc_df['ename'] == city]

    x_train, y_train, scaler, scaled_data = create_dataframe_for_city(
        city_data)

    # x_train이 None인 경우에 대한 처리
    if x_train is None:
        print("Error in create_dataframe_for_city function.")
    else:
        # 나머지 코드 실행
        model = create_lstm_model(input_shape=(x_train.shape[1], 1))
        model.fit(x_train, y_train, epochs=20, batch_size=1,
                  verbose=2, validation_split=0.1)

# LSTM 모델 생성 함수


def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adadelta')
    return model


# 각 도시에 대한 LSTM 모델 생성 및 학습
city_names = fdc_df['ename'].unique()
for city in city_names:
    # 도시별로 데이터 추출
    city_data = fdc_df[fdc_df['ename'] == city]

    x_train, y_train, scaler, scaled_data = create_dataframe_for_city(
        city_data)

    # 데이터를 훈련 세트와 검증 세트로 나누기 (80% 훈련, 20% 검증)
    split_index = int(0.8 * len(x_train))
    x_train, x_val = x_train[:split_index], x_train[split_index:]
    y_train, y_val = y_train[:split_index], y_train[split_index:]

    # LSTM 모델 생성 및 학습
    model = create_lstm_model(input_shape=(x_train.shape[1], 1))

    # 모델 학습
    history = model.fit(x_train, y_train, epochs=20,
                        batch_size=1, verbose=2, validation_data=(x_val, y_val))

    # # 학습 손실(loss) 그래프 출력
    # plt.plot(history.history['loss'], label='Training Loss')
    # plt.plot(history.history['val_loss'], label='Validation Loss')
    # plt.title('Training and Validation Loss')
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.legend()
    # plt.show()

    # 다음 미세먼지 데이터 예측
    inputs = scaled_data[len(scaled_data) - len(x_train) - 60:]
    inputs = np.reshape(inputs, (-1, 1))
    inputs = scaler.transform(inputs)
    pinedust_result = []
    for i in range(60, inputs.shape[0]):
        pinedust_result.append(inputs[i-60:i, 0])
    pinedust_result = np.array(pinedust_result)
    pinedust_result = np.reshape(
        pinedust_result, (pinedust_result.shape[0], pinedust_result.shape[1], 1))
    myclosing_priceresult = model.predict(pinedust_result)
    myclosing_priceresult = scaler.inverse_transform(myclosing_priceresult)

    print(len(pinedust_result))
    print(myclosing_priceresult)

    # 예측 결과와 실제값을 이어지는 그래프로 그리기
    plt.plot(myclosing_priceresult,
             label=f'{city} Predicted Values', linestyle='dashed')
    plt.plot(actual_values, label=f'{city} Actual Values', linestyle='solid')

    # 그래프에 제목과 축 레이블 추가
    plt.title(f'{city} Predicted vs Actual Values')
    plt.xlabel('Time Steps')
    plt.ylabel('Dust Concentration')

    # 범례 추가
    plt.legend()

    # 그래프 저장 (PNG 파일로)
    plt.savefig(f'{city}_predicted_vs_actual.png')

    # 그래프 초기화
    plt.clf()
