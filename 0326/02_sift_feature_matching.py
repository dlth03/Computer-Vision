import cv2 as cv                               # OpenCV 라이브러리
import matplotlib.pyplot as plt                # 결과 시각화를 위한 matplotlib

# 첫 번째 이미지 불러오기
img1 = cv.imread('mot_color70.jpg')

# 두 번째 이미지 불러오기
img2 = cv.imread('mot_color83.jpg')

# 첫 번째 이미지가 정상적으로 로드되었는지 확인
if img1 is None:
    print("첫 번째 이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# 두 번째 이미지가 정상적으로 로드되었는지 확인
if img2 is None:
    print("두 번째 이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# OpenCV는 BGR 형식으로 이미지를 읽기 때문에 matplotlib 출력용으로 RGB로 변환
img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)

# 두 번째 이미지도 RGB로 변환
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)

# SIFT 객체 생성
# nfeatures를 사용하여 특징점 개수를 적절히 제한
sift = cv.SIFT_create(nfeatures=200)

# 첫 번째 이미지에서 특징점 검출 및 descriptor 계산
keypoints1, descriptors1 = sift.detectAndCompute(img1, None)

# 두 번째 이미지에서 특징점 검출 및 descriptor 계산
keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

# BFMatcher 객체 생성
# SIFT descriptor는 실수형 벡터이므로 NORM_L2 사용
bf = cv.BFMatcher(cv.NORM_L2)

# 각 descriptor에 대해 가장 가까운 2개의 매칭을 찾음
# ratio test를 적용하기 위해 k=2로 설정
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# 좋은 매칭만 저장할 리스트 생성
good_matches = []

# Lowe's ratio test 적용
# 첫 번째 후보가 두 번째 후보보다 충분히 더 가까운 경우만 좋은 매칭으로 선택
for m, n in matches:
    if m.distance < 0.6 * n.distance:
        good_matches.append(m)

# distance가 작은 순서대로 정렬
# distance가 작을수록 두 특징점이 더 유사함
good_matches = sorted(good_matches, key=lambda x: x.distance)

# 시각적으로 너무 복잡하지 않도록 상위 20개만 선택
good_matches = good_matches[:20]

# drawMatches를 사용하여 두 이미지 간 특징점 매칭 결과를 시각화
img_matches = cv.drawMatches(
    img1,                                        # 첫 번째 이미지
    keypoints1,                                  # 첫 번째 이미지의 특징점
    img2,                                        # 두 번째 이미지
    keypoints2,                                  # 두 번째 이미지의 특징점
    good_matches,                                # 시각화할 좋은 매칭 결과
    None,                                        # 출력 이미지
    flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS  # 매칭된 점만 표시
)

# matplotlib에서 올바르게 출력하기 위해 BGR → RGB 변환
img_matches_rgb = cv.cvtColor(img_matches, cv.COLOR_BGR2RGB)

# 결과 출력을 위한 figure 생성
plt.figure(figsize=(16, 8))

# 매칭 결과 이미지 출력
plt.imshow(img_matches_rgb)

# 제목 설정
plt.title(f'SIFT Feature Matching ({len(good_matches)} Good Matches)')

# 축 제거
plt.axis('off')

# 레이아웃 자동 조정
plt.tight_layout()

# 결과 화면 출력
plt.show()

# 첫 번째 이미지의 특징점 개수 출력
print("첫 번째 이미지 특징점 개수:", len(keypoints1))

# 두 번째 이미지의 특징점 개수 출력
print("두 번째 이미지 특징점 개수:", len(keypoints2))

# knn 매칭 개수 출력
print("knn 매칭 개수:", len(matches))

# ratio test를 통과한 전체 좋은 매칭 개수 출력
print("좋은 매칭 개수:", len(good_matches))

# 첫 번째 이미지 descriptor 크기 출력
if descriptors1 is not None:
    print("descriptors1 shape:", descriptors1.shape)

# 두 번째 이미지 descriptor 크기 출력
if descriptors2 is not None:
    print("descriptors2 shape:", descriptors2.shape)