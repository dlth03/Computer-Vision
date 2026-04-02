import tensorflow as tf     # TensorFlow 라이브러리

from tensorflow.keras.datasets import mnist   # MNIST 데이터셋 로드
from tensorflow.keras.models import Sequential   # Sequential 모델
from tensorflow.keras.layers import Flatten, Dense   # 레이어 구성

import numpy as np   # 배열 처리용 NumPy
import matplotlib.pyplot as plt   # 시각화용 matplotlib


# 데이터 로드
(x_train, y_train), (x_test, y_test) = mnist.load_data()   # MNIST 데이터 불러오기


# 데이터 shape 출력
print("훈련 이미지 shape :", x_train.shape)   # 훈련 이미지 크기 출력
print("훈련 라벨 shape :", y_train.shape)   # 훈련 라벨 크기 출력
print("테스트 이미지 shape :", x_test.shape)   # 테스트 이미지 크기 출력
print("테스트 라벨 shape :", y_test.shape)   # 테스트 라벨 크기 출력


# 정규화 전 확인
print("정규화 전 최소값 :", x_train.min())   # 최소값 확인
print("정규화 전 최대값 :", x_train.max())   # 최대값 확인


# 정규화 (0~255 → 0~1)
x_train = x_train.astype("float32") / 255.0   # 훈련 데이터 정규화
x_test = x_test.astype("float32") / 255.0   # 테스트 데이터 정규화


# 정규화 후 확인
print("정규화 후 최소값 :", x_train.min())   # 정규화 후 최소값
print("정규화 후 최대값 :", x_train.max())   # 정규화 후 최대값


# 샘플 이미지 확인
print("첫 번째 훈련 이미지의 라벨 :", y_train[0])   # 라벨 출력
plt.imshow(x_train[0], cmap="gray")   # 이미지 출력
plt.title(f"Train Image / Label: {y_train[0]}")   # 제목 설정
plt.axis("off")   # 축 제거
plt.show()   # 화면 출력


# 모델 생성
model = Sequential()   # Sequential 모델 생성

# 입력층 (28x28 → 784)
model.add(Flatten(input_shape=(28, 28)))   # Flatten 레이어

# 은닉층 (128개, ReLU)
model.add(Dense(128, activation="relu"))   # Dense 은닉층

# 출력층 (10개, softmax)
model.add(Dense(10, activation="softmax"))   # 출력층


# 모델 구조 출력
model.summary()   # 모델 구조 확인


# 컴파일
model.compile(   # 모델 컴파일
    optimizer="adam",   # 최적화 함수
    loss="sparse_categorical_crossentropy",   # 손실 함수
    metrics=["accuracy"]   # 평가 지표
)


# 학습
history = model.fit(   # 모델 학습
    x_train,   # 입력 데이터
    y_train,   # 정답 라벨
    epochs=5,   # 반복 횟수
    validation_split=0.1   # 검증 데이터 비율
)


# 평가
test_loss, test_accuracy = model.evaluate(x_test, y_test)   # 테스트 데이터 평가

print("테스트 손실 :", test_loss)   # 손실 출력
print("테스트 정확도 :", test_accuracy)   # 정확도 출력


# 예측
predictions = model.predict(x_test[:10])   # 10개 데이터 예측


# 예측 결과 출력
for i in range(10):   # 10개 반복
    print(f"{i+1}번째 테스트 이미지")   # 번호 출력
    print("예측값 :", np.argmax(predictions[i]))   # 예측값
    print("실제값 :", y_test[i])   # 실제값
    print("-" * 20)   # 구분선


# 결과 이미지 출력
plt.imshow(x_test[0], cmap="gray")   # 테스트 이미지 출력
plt.title(f"Predicted: {np.argmax(predictions[0])}, Actual: {y_test[0]}")   # 제목
plt.axis("off")   # 축 제거
plt.show()   # 화면 출력