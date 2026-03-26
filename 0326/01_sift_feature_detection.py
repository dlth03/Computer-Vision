import cv2 as cv                      # OpenCV 라이브러리 (이미지 처리)
import matplotlib.pyplot as plt       # 결과 시각화를 위한 matplotlib

# 이미지 불러오기
img = cv.imread('mot_color70.jpg')

# 이미지가 정상적으로 로드되었는지 확인
if img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요.")   # 오류 메시지 출력
    exit()                                                      # 프로그램 종료

# OpenCV는 BGR 형식이므로 matplotlib 출력을 위해 RGB로 변환
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# SIFT 생성 (특징점 개수 제한)
sift = cv.SIFT_create(nfeatures=100)

# detectAndCompute 함수:
# - 특징점(keypoints) 검출
# - 각 특징점에 대한 descriptor(128차원 벡터) 계산
keypoints, descriptors = sift.detectAndCompute(img, None)

# drawKeypoints 함수:
# - 검출된 특징점을 이미지 위에 시각화
# - color: 특징점 색상 (BGR → 노란색)
# - flags: 특징점의 크기와 방향까지 함께 표시
img_keypoints = cv.drawKeypoints(
    img,                                      # 원본 이미지
    keypoints,                                # 검출된 특징점
    None,                                     # 출력 이미지 (None이면 새로 생성)
    color=(0, 255, 255),                      # 노란색 (BGR 기준)
    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS  # 크기/방향 포함 표시
)

# matplotlib 출력용 RGB 변환
img_keypoints_rgb = cv.cvtColor(img_keypoints, cv.COLOR_BGR2RGB)

# 결과 출력
plt.figure(figsize=(14, 6)) # 결과를 시각화하기 위한 figure 생성 (가로로 길게 설정)

# 첫 번째 subplot: 원본 이미지 출력
plt.subplot(1, 2, 1)               # 1행 2열 중 첫 번째
plt.imshow(img_rgb)                # 이미지 표시
plt.title('Original Image')        # 제목 설정
plt.axis('off')                    # 축 제거

# 두 번째 subplot: 특징점이 표시된 이미지 출력
plt.subplot(1, 2, 2)               # 1행 2열 중 두 번째
plt.imshow(img_keypoints_rgb)      # 특징점 이미지 표시
plt.title(f'SIFT Keypoints ({len(keypoints)})')  # 특징점 개수 포함 제목
plt.axis('off')                    # 축 제거

# subplot 간 간격 자동 조정
plt.tight_layout()

# 화면에 결과 출력
plt.show()

# 콘솔에 특징점 개수 출력
print("검출된 특징점 개수:", len(keypoints))

# descriptor가 정상적으로 생성되었는지 확인 후 shape 출력
if descriptors is not None:
    print("descriptor shape:", descriptors.shape)  # (특징점 수, 128)
