import cv2 as cv                                # OpenCV 라이브러리
import numpy as np                              # 행렬 연산 및 배열 처리를 위한 NumPy
import matplotlib.pyplot as plt                 # 결과 시각화를 위한 matplotlib

img1 = cv.imread('img2.jpg')                    # 변환되어 붙여질 이미지
img2 = cv.imread('img1.jpg')                    # 기준이 되는 이미지

# 첫 번째 이미지가 정상적으로 로드되었는지 확인
if img1 is None:
    print("첫 번째 이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# 두 번째 이미지가 정상적으로 로드되었는지 확인
if img2 is None:
    print("두 번째 이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# OpenCV는 BGR 형식으로 이미지를 읽으므로 grayscale로 변환
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

# SIFT 객체 생성
# nfeatures를 사용해 검출할 특징점 개수를 제한
sift = cv.SIFT_create(nfeatures=300)

# 첫 번째 이미지에서 특징점 검출 및 descriptor 계산
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)

# 두 번째 이미지에서 특징점 검출 및 descriptor 계산
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# BFMatcher 객체 생성
# SIFT descriptor는 실수형 벡터이므로 NORM_L2 사용
bf = cv.BFMatcher(cv.NORM_L2)

# 각 descriptor에 대해 최근접 이웃 2개를 찾음
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# 좋은 매칭만 저장할 리스트 생성
good_matches = []

# Lowe의 ratio test 적용
# 첫 번째 후보가 두 번째 후보보다 충분히 가까울 때만 좋은 매칭으로 선택
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# 호모그래피는 최소 4개 이상의 대응점이 필요함
if len(good_matches) >= 4:

    # 첫 번째 이미지의 좋은 매칭 좌표 추출
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 두 번째 이미지의 좋은 매칭 좌표 추출
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # RANSAC을 사용하여 이상치를 제거하며 호모그래피 계산
    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    # 이미지 크기 가져오기
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # 첫 번째 이미지를 두 번째 이미지 기준으로 투영 변환
    # 출력 크기는 두 이미지를 가로로 합칠 수 있도록 설정
    warped_img = cv.warpPerspective(img1, H, (w1 + w2, max(h1, h2)))

    # 결과 이미지를 warped_img 복사본으로 생성
    result_img = warped_img.copy()

    # 기준 이미지(img2)를 결과 캔버스의 왼쪽 위에 배치
    result_img[0:h2, 0:w2] = img2

    # 결과 이미지를 그레이스케일로 변환
    gray_result = cv.cvtColor(result_img, cv.COLOR_BGR2GRAY)

    # 0이 아닌 픽셀 위치 찾기
    coords = cv.findNonZero(gray_result)

    # 유효한 픽셀이 존재하면 bounding box 계산 후 crop
    if coords is not None:
        x, y, w, h = cv.boundingRect(coords)
        cropped_result = result_img[y:y+h, x:x+w]
    else:
        cropped_result = result_img

    # 좋은 매칭들을 거리 기준으로 정렬
    good_matches = sorted(good_matches, key=lambda x: x.distance)

    # 시각적 가독성을 위해 상위 30개만 선택
    draw_matches = good_matches[:30]

    # 특징점 매칭 결과 시각화
    match_result = cv.drawMatches(
        img1,                                           # 첫 번째 이미지
        keypoints1,                                     # 첫 번째 이미지 특징점
        img2,                                           # 두 번째 이미지
        keypoints2,                                     # 두 번째 이미지 특징점
        draw_matches,                                   # 시각화할 좋은 매칭
        None,                                           # 출력 이미지
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    # matplotlib 출력용으로 BGR → RGB 변환
    match_result_rgb = cv.cvtColor(match_result, cv.COLOR_BGR2RGB)
    cropped_result_rgb = cv.cvtColor(cropped_result, cv.COLOR_BGR2RGB)

    # 결과 출력을 위한 figure 생성
    plt.figure(figsize=(18, 8))

    # 왼쪽: 특징점 매칭 결과 출력
    plt.subplot(1, 2, 1)
    plt.imshow(match_result_rgb)
    plt.title(f'Matching Result ({len(draw_matches)} Good Matches)')
    plt.axis('off')

    # 오른쪽: 호모그래피 기반 정합 결과 출력
    plt.subplot(1, 2, 2)
    plt.imshow(cropped_result_rgb)
    plt.title('Warped Image (Image Alignment)')
    plt.axis('off')

    # 레이아웃 자동 조정
    plt.tight_layout()

    # 화면에 출력
    plt.show()

    # 콘솔 출력 데이터
    print("첫 번째 이미지 특징점 개수:", len(keypoints1))
    print("두 번째 이미지 특징점 개수:", len(keypoints2))
    print("knn 매칭 개수:", len(matches))
    print("좋은 매칭 개수:", len(good_matches))
    print("시각화한 매칭 개수:", len(draw_matches))
    print("호모그래피 행렬 H:\n", H)

else:
    # 좋은 매칭점이 부족하면 호모그래피 계산 불가
    print("좋은 매칭점이 부족하여 호모그래피를 계산할 수 없습니다.")