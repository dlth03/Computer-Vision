import cv2                          # OpenCV: 이미지 처리 및 컴퓨터 비전 라이브러리
import numpy as np                  # NumPy: 수치 계산 및 배열 처리 라이브러리
import matplotlib.pyplot as plt     # Matplotlib: 데이터 시각화 라이브러리

# 이미지 불러오기
img = cv2.imread('coffee cup.jpg')

# 이미지 정상 로드 여부 확인
if img is None:
    print("이미지를 찾을 수 없습니다. 파일명을 확인해주세요.")
else:
    # OpenCV는 BGR 형식으로 읽기 때문에 matplotlib 출력용으로 RGB 변환
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 이미지 높이(h), 너비(w) 가져오기
    h, w = img.shape[:2]

    # 초기 사각형 영역 설정 (x, y, width, height)
    # 이미지의 가장자리 5%씩 제외한 영역을 잡음
    rect = (int(w*0.05), int(h*0.05), int(w*0.9), int(h*0.9))

    # GrabCut에서 사용할 마스크 초기화
    mask = np.zeros(img.shape[:2], np.uint8)
    # 배경/전경 모델 초기화
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # GrabCut 실행 
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)  # 5회 반복하여 최적의 마스크 추출
    # (입력 이미지, 초기 마스크, 초기 사각형 영역 지정, 배경, 전경 모델, 반복횟수, 초기화 모드)

    # 마스크 후처리
    mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype('uint8')

    # 배경 제거 이미지 생성
    result = img_rgb * mask2[:, :, np.newaxis]

    # 시각화
    plt.figure(figsize=(15, 5))

    # 원본 이미지 출력
    plt.subplot(1, 3, 1)                # 1행 3열 중 첫 번째
    plt.imshow(img_rgb)                 # 원본 이미지 출력
    plt.title('Original Image')         # 제목
    plt.axis('off')                     # 축 제거    

    # 마스크 이미지 출력
    plt.subplot(1, 3, 2)                # 1행 3열 중 두 번째
    plt.imshow(mask2, cmap='gray')      # 흑백 출력
    plt.title('Mask Image')             # 제목  
    plt.axis('off')                     # 축 제거

    # 배경 제거된 이미지 출력
    plt.subplot(1, 3, 3)                # 1행 3열 중 세 번째
    plt.imshow(result)                  # 배경 제거된 이미지 출력
    plt.title('Background Removed')     # 제목
    plt.axis('off')                     # 축 제거

    plt.tight_layout()        # 레이아웃 자동 정렬
    plt.show()                # 화면에 출력