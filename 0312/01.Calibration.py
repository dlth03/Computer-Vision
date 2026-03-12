import cv2                   # OpenCV 라이브러리
import numpy as np           # 배열 처리를 위한 NumPy 라이브러리 불러오기
import glob                  # 파일 검색을 위한 glob 라이브러리 불러오기

# 체크보드 내부 코너 개수 (가로 9, 세로 6)
CHECKERBOARD = (9, 6)

# 체크보드 한 칸 실제 크기 (mm 단위)
square_size = 25.0

# 코너 정밀화 조건 : 반복 최대 30회, 정확도 0.001
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 실제 좌표 생성 (z=0, 평면)
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)  # 모든 점 초기화
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)  # x, y 좌표 설정
objp *= square_size

# 저장할 좌표
objpoints = []  # 3D 실제 좌표
imgpoints = []  # 2D 이미지 좌표

# 캘리브레이션에 사용할 이미지 불러오기
images = glob.glob("calibration_images/left*.jpg")  # left로 시작하는 모든 jpg 이미지

img_size = None # 이미지 크기 저장 변수

# -----------------------------
# 1. 체크보드 코너 검출
# -----------------------------
for fname in images:

    img = cv2.imread(fname) # 이미지 읽기
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 그레이스케일로 변환 (코너 검출용)


    if img_size is None:
        img_size = gray.shape[::-1]  # 첫 번째 이미지 크기로 저장 (w, h)

    # 체스보드 코너 찾기
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:  # 코너를 찾았다면
        objpoints.append(objp)  # 3D 실제 좌표 저장

        # 코너 정밀화
        corners2 = cv2.cornerSubPix(
            gray,       # 입력 이미지
            corners,    # 초기 코너 좌표
            (11,11),    # 검색 윈도우 크기
            (-1,-1),    # 검색 영역 없음
            criteria    # 정밀화 종료 조건
        )

        imgpoints.append(corners2)  # 2D 이미지 좌표 저장

        # 코너 시각화
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

        cv2.imshow("Corners", img)  # 코너 표시 이미지 보기
        cv2.waitKey(300)    #0.3초 대기

cv2.destroyAllWindows() # 모든 창 닫기

# -----------------------------
# 2. 카메라 캘리브레이션
# -----------------------------
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,  # 3D 실제 좌표
    imgpoints,  # 2D 이미지 좌표
    img_size,   # 이미지 크기
    None,       # 초기 카메라 매트릭스 (자동 계산)
    None        # 초기 왜곡 계수 (자동 계산)
)

print("Camera Matrix K:")   # 카메라 매트릭스 K 출력
print(K)

print("\nDistortion Coefficients:") # 렌즈 왜곡 계수 출력
print(dist)

# -----------------------------
# 3. 왜곡 보정 시각화
# -----------------------------
for fname in images:

    img = cv2.imread(fname) # 이미지 읽기
    h, w = img.shape[:2]    # 이미지 높이, 너비

    # 렌즈 왜곡 계수 출력
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        K,  # 기존 카메라 행렬
        dist,   # 왜곡 계수
        (w,h),  # 이미지 크기
        1,      # 스케일 1 = 전체 영역
        (w,h)   # 출력 이미지 크기
    )

    # 이미지 왜곡 보정
    dst = cv2.undistort(
        img,            # 원본 이미지
        K,              # 기존 카메라 행렬
        dist,           # 왜곡 계수
        None,           # 변환 행렬
        newcameramtx    # 새로운 카메라 행렬
    )

    # 결과 비교
    cv2.imshow("Original", img)     # 원본 이미지 보기
    cv2.imshow("Undistorted", dst)  # 보정된 이미지
    cv2.waitKey(0)                  # 키 입력 대기

cv2.destroyAllWindows()              # 모든 창 닫기
