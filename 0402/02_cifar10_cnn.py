import tensorflow as tf   # TensorFlow
from tensorflow.keras.datasets import cifar10   # CIFAR-10 데이터셋
from tensorflow.keras.models import Sequential   # Sequential 모델
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense   # CNN 레이어
import numpy as np   # 배열 처리
import matplotlib.pyplot as plt   # 시각화
from tensorflow.keras.preprocessing import image   # 이미지 로드
import os   # 파일 존재 확인


# CIFAR-10 클래스 이름 정의
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']   # 클래스 목록


# 데이터 로드
(x_train, y_train), (x_test, y_test) = cifar10.load_data()   # CIFAR-10 불러오기


# 데이터 shape 출력
print("훈련 이미지 shape :", x_train.shape)   # 훈련 이미지 크기
print("훈련 라벨 shape :", y_train.shape)   # 훈련 라벨 크기
print("테스트 이미지 shape :", x_test.shape)   # 테스트 이미지 크기
print("테스트 라벨 shape :", y_test.shape)   # 테스트 라벨 크기


# 정규화 전 확인
print("정규화 전 최소값 :", x_train.min())   # 최소값
print("정규화 전 최대값 :", x_train.max())   # 최대값


# 정규화 (0~255 → 0~1)
x_train = x_train.astype("float32") / 255.0   # 훈련 데이터 정규화
x_test = x_test.astype("float32") / 255.0   # 테스트 데이터 정규화


# 정규화 후 확인
print("정규화 후 최소값 :", x_train.min())   # 정규화 후 최소값
print("정규화 후 최대값 :", x_train.max())   # 정규화 후 최대값


# 샘플 이미지 확인
print("첫 번째 훈련 이미지의 라벨 :", class_names[y_train[0][0]])   # 첫 번째 라벨 출력
plt.imshow(x_train[0])   # 첫 번째 이미지 출력
plt.title(f"Train Image / Label: {class_names[y_train[0][0]]}")   # 제목 설정
plt.axis("off")   # 축 제거
plt.show()   # 화면 출력


# 모델 생성
model = Sequential()   # Sequential 모델 생성

# 합성곱층 1
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))   # Conv2D 추가

# 풀링층 1
model.add(MaxPooling2D((2, 2)))   # MaxPooling 추가

# 합성곱층 2
model.add(Conv2D(64, (3, 3), activation="relu"))   # Conv2D 추가

# 풀링층 2
model.add(MaxPooling2D((2, 2)))   # MaxPooling 추가

# 합성곱층 3
model.add(Conv2D(64, (3, 3), activation="relu"))   # Conv2D 추가

# 평탄화층
model.add(Flatten())   # 1차원 변환

# 은닉층
model.add(Dense(64, activation="relu"))   # Dense 은닉층

# 출력층
model.add(Dense(10, activation="softmax"))   # 10개 클래스 출력


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
    x_train,   # 훈련 이미지
    y_train,   # 훈련 라벨
    epochs=20,   # 반복 횟수
    validation_data=(x_test, y_test)   # 검증 데이터
)


# 평가
test_loss, test_accuracy = model.evaluate(x_test, y_test)   # 테스트 데이터 평가

print("테스트 손실 :", test_loss)   # 손실 출력
print("테스트 정확도 :", test_accuracy)   # 정확도 출력


# 테스트 데이터 10개 예측
predictions = model.predict(x_test[:10])   # 10개 이미지 예측


# 예측 결과 출력
for i in range(10):   # 10개 반복
    predicted_label = np.argmax(predictions[i])   # 예측값
    true_label = y_test[i][0]   # 실제값

    print(f"{i+1}번째 테스트 이미지")   # 번호 출력
    print("예측값 :", class_names[predicted_label])   # 예측 클래스 출력
    print("실제값 :", class_names[true_label])   # 실제 클래스 출력
    print("-" * 30)   # 구분선 출력


# 첫 번째 테스트 이미지 출력
plt.imshow(x_test[0])   # 테스트 이미지 출력
plt.title(f"Predicted: {class_names[np.argmax(predictions[0])]}, Actual: {class_names[y_test[0][0]]}")   # 제목 설정
plt.axis("off")   # 축 제거
plt.show()   # 화면 출력


# dog.jpg 파일 확인
if os.path.exists("dog.jpg"):   # dog.jpg 존재 여부 확인

    # 외부 이미지 로드
    img = image.load_img("dog.jpg", target_size=(32, 32))   # 이미지 크기 조정

    # 배열 변환
    img_array = image.img_to_array(img)   # PIL 이미지를 배열로 변환

    # 배치 차원 추가
    img_array = np.expand_dims(img_array, axis=0)   # (1, 32, 32, 3) 형태로 변환

    # 정규화
    img_array = img_array.astype("float32") / 255.0   # 0~1 범위 정규화

    # 예측 수행
    dog_prediction = model.predict(img_array)   # dog.jpg 예측

    # 예측 클래스 추출
    dog_predicted_label = np.argmax(dog_prediction[0])   # 가장 높은 확률의 클래스 선택

    # 결과 출력
    print("dog.jpg 예측 결과 :", class_names[dog_predicted_label])   # 예측 클래스 출력

    # 이미지 표시
    plt.imshow(img)   # dog.jpg 출력
    plt.title(f"dog.jpg Prediction: {class_names[dog_predicted_label]}")   # 제목 설정
    plt.axis("off")   # 축 제거
    plt.show()   # 화면 출력

else:   # dog.jpg가 없을 경우
    print("dog.jpg 파일이 현재 폴더에 없습니다.")   # 안내 메시지 출력