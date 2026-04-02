# 01_mnist_classifier.py

* 손글씨 숫자 이미지(MNIST 데이터셋)를 이용하여 간단한 이미지 분류기를 구현

---

# 기능

* MNIST 데이터셋을 불러오고 훈련/테스트 데이터로 분리한다.
* 데이터를 0~1 범위로 정규화한다.
* Flatten, Dense 레이어로 구성된 Sequential 모델을 생성한다.
* Adam 옵티마이저와 sparse_categorical_crossentropy 손실 함수로 모델을 컴파일한다.
* 5 에포크 동안 모델을 학습하고 검증 데이터로 성능을 확인한다.
* 테스트 데이터로 최종 손실과 정확도를 평가한다.
* 테스트 이미지 10개에 대해 예측값과 실제값을 비교 출력한다.
* 샘플 이미지와 예측 결과를 matplotlib으로 시각화한다.

---

# 요구사항

* MNIST 데이터셋을 로드
* 데이터를 훈련 세트와 테스트 세트로 분할
* 간단한 신경망 모델을 구축
* 모델을 훈련시키고 정확도를 평가

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기
```python
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
import numpy as np
import matplotlib.pyplot as plt
```

* tensorflow : 딥러닝 모델 구성 및 학습을 위한 라이브러리
* mnist : Keras에 내장된 MNIST 손글씨 데이터셋
* Sequential : 레이어를 순서대로 쌓는 모델 구조
* Flatten, Dense : 입력 펼치기 및 완전 연결 레이어
* numpy : 배열 처리 및 수치 계산을 위한 라이브러리
* matplotlib : 이미지 및 결과 시각화를 위한 라이브러리

---

## 2. 데이터 로드
```python
(x_train, y_train), (x_test, y_test) = mnist.load_data()
```

MNIST 데이터셋을 불러와 훈련 데이터와 테스트 데이터로 분리한다.
```python
print("훈련 이미지 shape :", x_train.shape)
print("테스트 이미지 shape :", x_test.shape)
```

각 데이터의 shape을 출력하여 구조를 확인한다.

---

## 3. 데이터 정규화
```python
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
```

픽셀 값을 0~255에서 **0~1 범위로 정규화**한다.  
정규화를 통해 학습 속도와 모델 성능을 향상시킨다.

---

## 4. 샘플 이미지 확인
```python
plt.imshow(x_train[0], cmap="gray")
plt.title(f"Train Image / Label: {y_train[0]}")
plt.show()
```

첫 번째 훈련 이미지를 그레이스케일로 출력하여 데이터를 시각적으로 확인한다.

---

## 5. 모델 생성
```python
model = Sequential()
model.add(Flatten(input_shape=(28, 28)))
model.add(Dense(128, activation="relu"))
model.add(Dense(10, activation="softmax"))
```

세 개의 레이어로 구성된 Sequential 모델을 생성한다.

* **Flatten** : 28×28 이미지를 784 크기의 1차원 벡터로 펼친다.
* **Dense(128, ReLU)** : 128개의 뉴런을 가진 은닉층, 비선형 활성화 함수 ReLU 사용
* **Dense(10, Softmax)** : 0~9 숫자 클래스 각각의 확률을 출력하는 출력층

---

## 6. 모델 컴파일
```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
```

모델 학습에 필요한 설정을 지정한다.

* **optimizer** : Adam 최적화 알고리즘 사용
* **loss** : 정수 라벨을 그대로 사용하는 다중 분류 손실 함수
* **metrics** : 정확도를 평가 지표로 사용

---

## 7. 모델 학습
```python
history = model.fit(
    x_train,
    y_train,
    epochs=5,
    validation_split=0.1
)
```

훈련 데이터로 모델을 학습한다.

* **epochs=5** : 전체 데이터를 5회 반복 학습
* **validation_split=0.1** : 훈련 데이터의 10%를 검증 데이터로 사용

---

## 8. 모델 평가
```python
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("테스트 손실 :", test_loss)
print("테스트 정확도 :", test_accuracy)
```

테스트 데이터로 학습된 모델의 최종 손실과 정확도를 평가한다.

---

## 9. 예측 및 결과 출력
```python
predictions = model.predict(x_test[:10])

for i in range(10):
    print(f"{i+1}번째 테스트 이미지")
    print("예측값 :", np.argmax(predictions[i]))
    print("실제값 :", y_test[i])
```

테스트 이미지 10개에 대해 예측을 수행한다.

* `model.predict()` : 각 클래스에 대한 확률 배열을 반환한다.
* `np.argmax()` : 확률이 가장 높은 클래스를 최종 예측값으로 선택한다.
* 예측값과 실제값을 비교하여 출력한다.

---

## 10. 결과 이미지 시각화
```python
plt.imshow(x_test[0], cmap="gray")
plt.title(f"Predicted: {np.argmax(predictions[0])}, Actual: {y_test[0]}")
plt.axis("off")
plt.show()
```

첫 번째 테스트 이미지를 출력하고 예측값과 실제값을 제목으로 표시한다.

---

# 폴더 구조
```
project_folder
│
├── 01_mnist_classifier.py
│
└── README.md
```

---

# 실행 방법

1. TensorFlow 설치
```
pip install tensorflow
```

2. 프로그램 실행
```
python 01_mnist_classifier.py
```

---

# 주의사항

* MNIST 데이터셋은 최초 실행 시 자동으로 다운로드된다.
* 정규화를 반드시 수행한 뒤 모델에 입력해야 한다.
* epochs와 validation_split 값에 따라 학습 결과가 달라질 수 있다.
* Dense 레이어의 뉴런 수와 활성화 함수를 변경하면 모델 성능이 달라질 수 있다.

  <img width="642" height="547" alt="01_mnist_classifier 결과" src="https://github.com/user-attachments/assets/74cada6c-bf0c-4ab7-9541-af8e7cd304b6" />
<img width="343" height="200" alt="01_mnist_classifier 출력" src="https://github.com/user-attachments/assets/4aa3df81-99c0-4e6e-8769-8e795d4e8ac5" />

---

<img width="640" height="543" alt="01_mnist_classifier 결과2" src="https://github.com/user-attachments/assets/cc7a1a57-530d-4e61-b5c3-9b291936ace8" />
<img width="480" height="899" alt="01_mnist_classifier 출력2" src="https://github.com/user-attachments/assets/099984ad-5821-4d90-9da9-c78310a9dbae" />

---

# 02_cifar10_cnn.py

* CIFAR-10 데이터셋을 활용하여 합성곱 신경망(CNN)을 구축하고, 이미지 분류를 수행

---

# 기능

* CIFAR-10 데이터셋을 불러오고 훈련/테스트 데이터로 분리한다.
* 데이터를 0~1 범위로 정규화한다.
* Conv2D, MaxPooling2D, Flatten, Dense 레이어로 구성된 CNN 모델을 생성한다.
* Adam 옵티마이저와 sparse_categorical_crossentropy 손실 함수로 모델을 컴파일한다.
* 20 에포크 동안 모델을 학습하고 테스트 데이터로 검증한다.
* 테스트 데이터로 최종 손실과 정확도를 평가한다.
* 테스트 이미지 10개에 대해 예측 클래스와 실제 클래스를 비교 출력한다.
* dog.jpg 파일이 존재하면 외부 이미지에 대한 예측을 수행한다.
* 샘플 이미지와 예측 결과를 matplotlib으로 시각화한다.

---

# 요구사항

* CIFAR-10 데이터셋을 로드
* 데이터 전처리(정규화등)를 수행
* CNN 모델을 설계하고 훈련
* 모델의 성능을 평가하고, 테스트 이미지(dog.jpg)에 대한 예측을 수행

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기
```python
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import os
```

* tensorflow : 딥러닝 모델 구성 및 학습을 위한 라이브러리
* cifar10 : Keras에 내장된 CIFAR-10 이미지 데이터셋
* Sequential : 레이어를 순서대로 쌓는 모델 구조
* Conv2D, MaxPooling2D, Flatten, Dense : CNN 구성 레이어
* numpy : 배열 처리 및 수치 계산을 위한 라이브러리
* matplotlib : 이미지 및 결과 시각화를 위한 라이브러리
* image : 외부 이미지 파일을 불러오고 전처리하기 위한 모듈
* os : 파일 존재 여부를 확인하기 위한 라이브러리

---

## 2. 클래스 이름 정의
```python
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
```

CIFAR-10의 10개 클래스 이름을 리스트로 정의한다.
예측 결과를 숫자 인덱스 대신 클래스 이름으로 출력할 때 사용한다.

---

## 3. 데이터 로드
```python
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
```

CIFAR-10 데이터셋을 불러와 훈련 데이터와 테스트 데이터로 분리한다.
```python
print("훈련 이미지 shape :", x_train.shape)
print("테스트 이미지 shape :", x_test.shape)
```

각 데이터의 shape을 출력하여 구조를 확인한다.

---

## 4. 데이터 정규화
```python
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
```

픽셀 값을 0~255에서 **0~1 범위로 정규화**한다.
정규화를 통해 학습 속도와 모델 성능을 향상시킨다.

---

## 5. 샘플 이미지 확인
```python
plt.imshow(x_train[0])
plt.title(f"Train Image / Label: {class_names[y_train[0][0]]}")
plt.show()
```

첫 번째 훈련 이미지를 컬러로 출력하여 데이터를 시각적으로 확인한다.

---

## 6. 모델 생성
```python
model = Sequential()
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(Flatten())
model.add(Dense(64, activation="relu"))
model.add(Dense(10, activation="softmax"))
```

총 8개의 레이어로 구성된 CNN 모델을 생성한다.

* **Conv2D(32, ReLU)** : 32개의 필터로 이미지의 특징을 추출하는 첫 번째 합성곱층
* **MaxPooling2D** : 특징 맵의 크기를 절반으로 줄여 계산량을 감소시키는 풀링층
* **Conv2D(64, ReLU)** : 64개의 필터로 더 복잡한 특징을 추출하는 두 번째 합성곱층
* **MaxPooling2D** : 두 번째 풀링층
* **Conv2D(64, ReLU)** : 64개의 필터로 고수준 특징을 추출하는 세 번째 합성곱층
* **Flatten** : 3차원 특징 맵을 1차원 벡터로 펼친다
* **Dense(64, ReLU)** : 64개의 뉴런을 가진 완전 연결 은닉층
* **Dense(10, Softmax)** : 10개 클래스 각각의 확률을 출력하는 출력층

---

## 7. 모델 컴파일
```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
```

모델 학습에 필요한 설정을 지정한다.

* **optimizer** : Adam 최적화 알고리즘 사용
* **loss** : 정수 라벨을 그대로 사용하는 다중 분류 손실 함수
* **metrics** : 정확도를 평가 지표로 사용

---

## 8. 모델 학습
```python
history = model.fit(
    x_train,
    y_train,
    epochs=20,
    validation_data=(x_test, y_test)
)
```

훈련 데이터로 모델을 학습한다.

* **epochs=20** : 전체 데이터를 20회 반복 학습
* **validation_data** : 테스트 데이터 전체를 검증 데이터로 사용

---

## 9. 모델 평가
```python
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("테스트 손실 :", test_loss)
print("테스트 정확도 :", test_accuracy)
```

테스트 데이터로 학습된 모델의 최종 손실과 정확도를 평가한다.

---

## 10. 예측 및 결과 출력
```python
predictions = model.predict(x_test[:10])

for i in range(10):
    predicted_label = np.argmax(predictions[i])
    true_label = y_test[i][0]
    print("예측값 :", class_names[predicted_label])
    print("실제값 :", class_names[true_label])
```

테스트 이미지 10개에 대해 예측을 수행한다.

* `model.predict()` : 각 클래스에 대한 확률 배열을 반환한다.
* `np.argmax()` : 확률이 가장 높은 클래스를 최종 예측값으로 선택한다.
* 예측 클래스 이름과 실제 클래스 이름을 비교하여 출력한다.

---

## 11. 외부 이미지 예측 (dog.jpg)
```python
if os.path.exists("dog.jpg"):
    img = image.load_img("dog.jpg", target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype("float32") / 255.0
    dog_prediction = model.predict(img_array)
    dog_predicted_label = np.argmax(dog_prediction[0])
    print("dog.jpg 예측 결과 :", class_names[dog_predicted_label])
```

외부 이미지 파일(dog.jpg)이 존재할 경우 예측을 수행한다.

* `image.load_img()` : 이미지를 32×32 크기로 불러온다.
* `np.expand_dims()` : 배치 차원을 추가하여 (1, 32, 32, 3) 형태로 변환한다.
* 정규화 후 모델에 입력하여 예측 클래스를 출력한다.

---

# 폴더 구조
```
project_folder
│
├── 02_cifar10_cnn.py
├── dog.jpg             ← 선택 사항 (없어도 실행 가능)
│
└── README.md
```

---

# 실행 방법

1. TensorFlow 설치
```
pip install tensorflow
```

2. 프로그램 실행
```
python 02_cifar10_cnn.py
```

---

# 주의사항

* CIFAR-10 데이터셋은 최초 실행 시 자동으로 다운로드된다.
* 정규화를 반드시 수행한 뒤 모델에 입력해야 한다.
* dog.jpg 파일이 없으면 외부 이미지 예측은 건너뛰고 나머지 코드는 정상 실행된다.
* epochs 값이 크므로 GPU 환경에서 실행하면 학습 속도가 크게 향상된다.
* Conv2D 필터 수와 Dense 뉴런 수를 변경하면 모델 성능이 달라질 수 있다.

<img width="644" height="539" alt="02_cifar10_cnn 결과" src="https://github.com/user-attachments/assets/6408657e-c80b-483a-b0f6-8454af4c34ed" />
<img width="371" height="189" alt="02_cifar10_cnn 출력" src="https://github.com/user-attachments/assets/5303bf89-ed83-4f21-afda-2394c26b77d2" />

---

<img width="637" height="546" alt="02_cifar10_cnn 결과2" src="https://github.com/user-attachments/assets/de4f719d-0f92-42e4-94d1-86518bb7ca99" />
<img width="494" height="946" alt="02_cifar10_cnn 출력2" src="https://github.com/user-attachments/assets/b84ecf72-64d0-4e9a-8977-6c23b34df63e" />
