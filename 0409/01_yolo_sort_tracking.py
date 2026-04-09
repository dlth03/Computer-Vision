import cv2                                          # OpenCV 라이브러리 import
import numpy as np                                  # NumPy 라이브러리 import
from scipy.optimize import linear_sum_assignment    # Hungarian 알고리즘 사용
from filterpy.kalman import KalmanFilter            # 칼만 필터 사용
import os                                           # 파일 존재 확인용
import random                                       # 색상 생성을 위한 random 모듈 import
import time                                         # FPS 측정을 위한 time 모듈 import

classes = [
    "person", "bicycle", "car", "motorbike", "aeroplane",
    "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird",
    "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut",
    "cake", "chair", "sofa", "pottedplant", "bed",
    "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# 클래스별 색상 생성 함수
def create_class_colors(num_classes):
    random.seed(42)                                # 실행할 때마다 같은 색상 나오도록 seed 고정
    colors = []                                    # 색상 저장 리스트 생성

    for _ in range(num_classes):                   # 클래스 개수만큼 반복
        color = (
            random.randint(0, 255),                # 파란색 값
            random.randint(0, 255),                # 초록색 값
            random.randint(0, 255)                 # 빨간색 값
        )
        colors.append(color)                       # 생성한 색상을 리스트에 추가

    return colors                                  # 색상 리스트 반환

# IoU(Intersection over Union) 계산 함수
# 두 bounding box 사이의 겹치는 비율을 계산
def iou_batch(bb_test, bb_gt):
    bb_gt = np.expand_dims(bb_gt, 0)               # bb_gt 차원 확장
    bb_test = np.expand_dims(bb_test, 1)           # bb_test 차원 확장

    xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])   # 겹치는 영역의 왼쪽 x
    yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])   # 겹치는 영역의 위쪽 y
    xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])   # 겹치는 영역의 오른쪽 x
    yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])   # 겹치는 영역의 아래쪽 y

    w = np.maximum(0., xx2 - xx1)                  # 겹치는 너비 계산
    h = np.maximum(0., yy2 - yy1)                  # 겹치는 높이 계산
    intersection = w * h                           # 교집합 넓이 계산

    area_test = (bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])   # test 박스 넓이
    area_gt = (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1])             # gt 박스 넓이
    union = area_test + area_gt - intersection     # 합집합 넓이 계산

    iou = intersection / (union + 1e-6)            # 0으로 나누는 것 방지를 위해 작은 값 더함
    return iou                                     # IoU 반환

# bounding box를 중심좌표 기반 형식으로 변환
# [x1, y1, x2, y2] -> [x, y, s, r]
# x, y: 중심 좌표
# s: 면적
# r: 종횡비
def convert_bbox_to_z(bbox):
    w = bbox[2] - bbox[0]                          # 박스 너비 계산
    h = bbox[3] - bbox[1]                          # 박스 높이 계산
    x = bbox[0] + w / 2.0                          # 중심 x 좌표 계산
    y = bbox[1] + h / 2.0                          # 중심 y 좌표 계산
    s = w * h                                      # 면적 계산
    r = w / float(h + 1e-6)                        # 종횡비 계산
    return np.array([x, y, s, r]).reshape((4, 1)) # 칼만 필터 입력 형태로 반환

# 칼만 필터 상태값을 다시 bounding box 형식으로 변환
# [x, y, s, r] -> [x1, y1, x2, y2]
def convert_x_to_bbox(x, score=None):
    w = np.sqrt(x[2] * x[3])                       # 너비 계산
    h = x[2] / (w + 1e-6)                          # 높이 계산

    if score is None:                              # score가 없는 경우
        return np.array([
            x[0] - w / 2.0,                        # x1
            x[1] - h / 2.0,                        # y1
            x[0] + w / 2.0,                        # x2
            x[1] + h / 2.0                         # y2
        ]).reshape((1, 4))                         # shape 맞춰 반환
    else:                                          # score가 있는 경우
        return np.array([
            x[0] - w / 2.0,                        # x1
            x[1] - h / 2.0,                        # y1
            x[0] + w / 2.0,                        # x2
            x[1] + h / 2.0,                        # y2
            score                                  # score 추가
        ]).reshape((1, 5))                         # shape 맞춰 반환

# SORT에서 사용하는 개별 객체 추적기 클래스
# 각 객체마다 하나씩 생성됨
class KalmanBoxTracker(object):
    count = 0                                      # tracker ID 생성을 위한 클래스 변수

    def __init__(self, bbox, class_id):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)   # 상태 7차원, 측정 4차원 칼만 필터 생성

        self.kf.F = np.array([                     # 상태 전이 행렬 설정
            [1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])

        self.kf.H = np.array([                     # 관측 행렬 설정
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ])

        self.kf.R[2:, 2:] *= 10.                  # 관측 노이즈 조정
        self.kf.P[4:, 4:] *= 1000.                # 초기 속도 항목 불확실성 크게 설정
        self.kf.P *= 10.                          # 공분산 전체 조정
        self.kf.Q[-1, -1] *= 0.01                 # 프로세스 노이즈 조정
        self.kf.Q[4:, 4:] *= 0.01                 # 속도 관련 프로세스 노이즈 조정

        self.kf.x[:4] = convert_bbox_to_z(bbox)   # 초기 상태값을 bbox로 설정

        self.time_since_update = 0                # 마지막 업데이트 이후 경과 프레임 수
        self.id = KalmanBoxTracker.count          # 고유 ID 저장
        KalmanBoxTracker.count += 1               # 다음 ID를 위해 count 증가
        self.history = []                         # 예측 history 저장 리스트
        self.hits = 0                             # 총 업데이트 횟수
        self.hit_streak = 0                       # 연속 업데이트 횟수
        self.age = 0                              # tracker 생성 후 지난 프레임 수
        self.class_id = class_id                  # 클래스 ID 저장

    def update(self, bbox, class_id):
        self.time_since_update = 0                # 업데이트 되었으므로 0으로 초기화
        self.history = []                         # history 비우기
        self.hits += 1                            # 총 업데이트 수 증가
        self.hit_streak += 1                      # 연속 업데이트 수 증가
        self.kf.update(convert_bbox_to_z(bbox))   # 칼만 필터 업데이트
        self.class_id = class_id                  # 최신 클래스 ID 반영

    def predict(self):
        if (self.kf.x[6] + self.kf.x[2]) <= 0:    # 예측 면적이 음수 되는 상황 방지
            self.kf.x[6] *= 0.0                   # 보정

        self.kf.predict()                         # 칼만 필터 예측 수행
        self.age += 1                             # age 증가

        if self.time_since_update > 0:            # 이전 프레임에서 업데이트 안 되었으면
            self.hit_streak = 0                   # 연속 업데이트 수 초기화

        self.time_since_update += 1               # 업데이트 이후 경과 프레임 증가
        self.history.append(convert_x_to_bbox(self.kf.x))  # 현재 예측 bbox 저장
        return self.history[-1]                   # 마지막 예측 bbox 반환

    def get_state(self):
        return convert_x_to_bbox(self.kf.x)       # 현재 상태를 bbox 형식으로 반환

# detection과 tracker를 IoU 기반으로 매칭하는 함수
def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    if len(trackers) == 0:                        # 기존 tracker가 하나도 없으면
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0), dtype=int)

    iou_matrix = iou_batch(detections[:, :4], trackers)    # detection과 tracker 간 IoU 계산

    if min(iou_matrix.shape) > 0:                # IoU 행렬이 비어 있지 않으면
        a = (iou_matrix > iou_threshold).astype(np.int32)  # threshold 이상 여부를 0/1로 변환

        if a.sum(1).max() == 1 and a.sum(0).max() == 1:    # 단순 1:1 매칭 가능한 경우
            matched_indices = np.stack(np.where(a), axis=1) # 바로 매칭
        else:
            row_ind, col_ind = linear_sum_assignment(-iou_matrix)  # Hungarian 알고리즘 사용
            matched_indices = np.stack((row_ind, col_ind), axis=1) # 매칭 결과 저장
    else:
        matched_indices = np.empty((0, 2), dtype=int)      # 매칭 결과 없으면 빈 배열

    unmatched_detections = []                    # 매칭 안 된 detection 저장 리스트
    for d in range(len(detections)):             # 모든 detection 반복
        if d not in matched_indices[:, 0]:       # 매칭되지 않았으면
            unmatched_detections.append(d)       # unmatched에 추가

    unmatched_trackers = []                      # 매칭 안 된 tracker 저장 리스트
    for t in range(len(trackers)):               # 모든 tracker 반복
        if t not in matched_indices[:, 1]:       # 매칭되지 않았으면
            unmatched_trackers.append(t)         # unmatched에 추가

    matches = []                                 # 최종 매칭 저장 리스트
    for m in matched_indices:                    # 매칭된 결과 반복
        if iou_matrix[m[0], m[1]] < iou_threshold:  # IoU가 기준보다 작으면
            unmatched_detections.append(m[0])       # detection unmatched 처리
            unmatched_trackers.append(m[1])         # tracker unmatched 처리
        else:
            matches.append(m.reshape(1, 2))         # 정상 매칭이면 저장

    if len(matches) == 0:                        # 매칭 결과가 없으면
        matches = np.empty((0, 2), dtype=int)    # 빈 배열 생성
    else:
        matches = np.concatenate(matches, axis=0) # 배열로 결합

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)    # 매칭 결과, 매칭 안 된 detection, 매칭 안 된 tracker 반환

# SORT 전체 클래스
# tracker들을 관리하는 역할
class Sort(object):
    def __init__(self, max_age=10, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age                   # 업데이트 없이 유지 가능한 최대 프레임 수
        self.min_hits = min_hits                 # 정식 track으로 인정할 최소 hit 수
        self.iou_threshold = iou_threshold       # IoU 매칭 기준
        self.trackers = []                       # tracker 저장 리스트
        self.frame_count = 0                     # 현재까지 처리한 프레임 수

    def update(self, dets=np.empty((0, 6))):
        self.frame_count += 1                    # 프레임 수 증가

        trks = np.zeros((len(self.trackers), 5)) # 예측 tracker bbox 저장 배열
        to_del = []                              # 삭제할 tracker index 저장 리스트
        ret = []                                 # 최종 출력 결과 저장 리스트

        for t, trk in enumerate(trks):           # 모든 tracker 반복
            pos = self.trackers[t].predict()[0]  # 다음 위치 예측
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]  # 예측 bbox 저장
            if np.any(np.isnan(pos)):            # NaN이 있으면
                to_del.append(t)                 # 삭제 대상에 추가

        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))  # invalid 행 제거

        for t in reversed(to_del):               # 뒤에서부터 삭제
            self.trackers.pop(t)                 # tracker 삭제

        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(
            dets, trks, self.iou_threshold
        )                                        # detection과 tracker 매칭 수행

        for m in matched:                        # 매칭된 결과 반복
            det_index = m[0]                     # detection 인덱스
            trk_index = m[1]                     # tracker 인덱스
            bbox = dets[det_index, :4]           # bbox 추출
            class_id = int(dets[det_index, 5])   # class_id 추출
            self.trackers[trk_index].update(bbox, class_id)  # 해당 tracker 업데이트

        for i in unmatched_dets:                 # 매칭되지 않은 detection 반복
            trk = KalmanBoxTracker(dets[i, :4], int(dets[i, 5]))  # 새 tracker 생성
            self.trackers.append(trk)            # tracker 리스트에 추가

        i = len(self.trackers)                   # tracker 개수 저장
        for trk in reversed(self.trackers):      # tracker를 뒤에서부터 순회
            d = trk.get_state()[0]               # 현재 bbox 상태 가져오기

            if (trk.time_since_update < 1) and (
                trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits
            ):
                ret.append(np.concatenate((d, [trk.id + 1], [trk.class_id])).reshape(1, -1))    # 결과 형식: [x1, y1, x2, y2, id, class_id]

            i -= 1                               # index 감소
            if trk.time_since_update > self.max_age:  # 너무 오래 업데이트 안 되면
                self.trackers.pop(i)             # tracker 삭제

        if len(ret) > 0:                         # 반환할 결과가 있으면
            return np.concatenate(ret)           # 배열로 합쳐 반환

        return np.empty((0, 6))                  # 결과 없으면 빈 배열 반환

# YOLOv3 모델 로드 함수
def load_yolo_model(cfg_path, weights_path):
    net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)     # cfg와 weights로 YOLO 네트워크 생성

    # GPU 가속 설정 (GPU 없으면 CPU로 자동 fallback)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)           # CUDA 백엔드 설정
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)             # CUDA 타겟 설정

    layer_names = net.getLayerNames()                            # 전체 레이어 이름 가져오기
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]   # 출력 레이어 이름 추출
    return net, output_layers                                    # 네트워크와 출력 레이어 반환

# 한 프레임에서 YOLOv3로 객체 검출하는 함수
# 반환 형식: [x1, y1, x2, y2, score, class_id]
def detect_objects(frame, net, output_layers, conf_threshold=0.5, nms_threshold=0.4):
    height, width = frame.shape[:2]                              # 프레임 높이와 너비 저장

    blob = cv2.dnn.blobFromImage(
        frame,                                                   # 입력 프레임
        1 / 255.0,                                               # 픽셀 정규화
        (416, 416),                                              # YOLO 입력 크기
        swapRB=True,                                             # BGR -> RGB 변환
        crop=False                                               # 크롭하지 않음
    )

    net.setInput(blob)                                           # 네트워크 입력 설정
    outputs = net.forward(output_layers)                         # forward 수행

    boxes = []                                                   # 박스 정보 저장 리스트
    confidences = []                                             # confidence 저장 리스트
    class_ids = []                                               # class_id 저장 리스트

    for output in outputs:                                       # 각 출력 레이어 반복
        for detection in output:                                 # 각 detection 반복
            scores = detection[5:]                               # 클래스별 점수 추출
            class_id = np.argmax(scores)                         # 가장 높은 점수의 클래스 선택
            confidence = scores[class_id]                        # 해당 클래스 confidence 저장

            if confidence > conf_threshold:                      # confidence 기준 이상이면
                center_x = int(detection[0] * width)             # 중심 x 좌표 복원
                center_y = int(detection[1] * height)            # 중심 y 좌표 복원
                w = int(detection[2] * width)                    # 박스 너비 복원
                h = int(detection[3] * height)                   # 박스 높이 복원

                x = int(center_x - w / 2)                        # 왼쪽 위 x 좌표 계산
                y = int(center_y - h / 2)                        # 왼쪽 위 y 좌표 계산

                boxes.append([x, y, w, h])                       # boxes 리스트에 추가
                confidences.append(float(confidence))            # confidence 리스트에 추가
                class_ids.append(class_id)                       # class_id 리스트에 추가

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)   # NMS 수행하여 중복 박스 제거

    detections = []                                              # 최종 detection 결과 저장 리스트

    if len(indices) > 0:                                         # 남은 박스가 있으면
        for i in indices.flatten():                              # 살아남은 인덱스 반복
            x, y, w, h = boxes[i]                                # 박스 정보 가져오기
            score = confidences[i]                               # confidence 가져오기
            class_id = class_ids[i]                              # class_id 가져오기

            x1 = max(0, x)                                       # 화면 밖 좌표 방지
            y1 = max(0, y)                                       # 화면 밖 좌표 방지
            x2 = min(width - 1, x + w)                           # 화면 범위 내로 제한
            y2 = min(height - 1, y + h)                          # 화면 범위 내로 제한

            detections.append([x1, y1, x2, y2, score, class_id]) # SORT 입력 형식으로 저장

    if len(detections) == 0:                                     # 검출 결과가 없으면
        return np.empty((0, 6))                                  # 빈 배열 반환

    return np.array(detections)                                  # NumPy 배열로 반환

# 메인 함수
def main():
    KalmanBoxTracker.count = 0                                   # [수정1] 비디오 시작 시 ID 카운터 초기화

    base_dir = os.path.dirname(os.path.abspath(__file__))        # 현재 파이썬 파일이 있는 폴더 경로
    print(base_dir)                                              # 현재 기준 폴더 확인용 출력

    input_video = os.path.join(base_dir, "slow_traffic_small.mp4")   # 입력 비디오 절대경로
    output_video = os.path.join(base_dir, "output_tracking.mp4")     # 출력 비디오 절대경로
    yolo_cfg = os.path.join(base_dir, "yolov3.cfg")                  # cfg 파일 절대경로
    yolo_weights = os.path.join(base_dir, "yolov3.weights")          # weights 파일 절대경로

    if not os.path.exists(input_video):                          # 입력 비디오 존재 여부 확인
        print(f"입력 비디오 파일이 없습니다: {input_video}")      # 오류 메시지 출력
        return                                                   # 함수 종료

    if not os.path.exists(yolo_cfg):                             # cfg 파일 존재 여부 확인
        print(f"YOLO cfg 파일이 없습니다: {yolo_cfg}")           # 오류 메시지 출력
        return                                                   # 함수 종료

    if not os.path.exists(yolo_weights):                         # weights 파일 존재 여부 확인
        print(f"YOLO weights 파일이 없습니다: {yolo_weights}")   # 오류 메시지 출력
        return                                                   # 함수 종료

    colors = create_class_colors(len(classes))                   # 클래스별 색상 생성
    net, output_layers = load_yolo_model(yolo_cfg, yolo_weights) # YOLO 모델 로드
    tracker = Sort(max_age=15, min_hits=3, iou_threshold=0.3)    # SORT 추적기 생성

    cap = cv2.VideoCapture(input_video)                          # 비디오 캡처 객체 생성

    if not cap.isOpened():                                       # 비디오 열기 실패 시
        print("비디오를 열 수 없습니다.")                         # 오류 메시지 출력
        return                                                   # 함수 종료

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))               # 입력 비디오 너비 가져오기
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # 입력 비디오 높이 가져오기
    fps = cap.get(cv2.CAP_PROP_FPS)                              # 입력 비디오 FPS 가져오기

    if fps == 0:                                                 # FPS를 제대로 못 읽는 경우
        fps = 30.0                                               # 기본값 30으로 설정

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")                     # mp4 코덱 설정
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))   # 출력 비디오 저장 객체 생성

    frame_count = 0                                              # 프레임 카운터 초기화

    while True:                                                  # 비디오 끝까지 반복
        ret, frame = cap.read()                                  # 프레임 하나 읽기

        if not ret:                                              # 더 이상 프레임이 없으면
            break                                                # 반복 종료

        frame_count += 1                                         # 프레임 번호 증가
        start = time.time()                                      # [수정5] 프레임 처리 시작 시간 기록

        detections = detect_objects(
            frame,                                               # 현재 프레임 입력
            net,                                                 # YOLO 네트워크
            output_layers,                                       # 출력 레이어
            conf_threshold=0.5,                                  # confidence threshold
            nms_threshold=0.4                                    # NMS threshold
        )

        tracks = tracker.update(detections)                      # SORT 추적 결과 업데이트

        for track in tracks:                                     # 추적 결과 반복
            x1, y1, x2, y2, track_id, class_id = track           # 결과 분리
            x1 = int(x1)                                         # 정수형 변환
            y1 = int(y1)                                         # 정수형 변환
            x2 = int(x2)                                         # 정수형 변환
            y2 = int(y2)                                         # 정수형 변환
            track_id = int(track_id)                             # 정수형 변환
            class_id = int(class_id)                             # 정수형 변환

            if class_id < len(classes):                          # class_id가 유효 범위면
                class_name = classes[class_id]                   # 클래스 이름 가져오기
            else:                                                # 범위를 벗어나면
                class_name = "object"                            # 기본 이름 사용

            color = colors[track_id % len(colors)]               # [수정2] track_id 기준으로 색상 부여 (같은 클래스도 ID마다 다른 색상)
            label = f"ID:{track_id} {class_name}"                # 화면에 표시할 라벨 생성

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)   # 객체 bounding box 그리기

            text_y = y1 - 10                                     # 텍스트 y 위치 계산
            if text_y < 20:                                      # 화면 위쪽을 벗어나면
                text_y = y1 + 20                                 # 박스 아래쪽으로 조정

            cv2.putText(
                frame,                                           # 출력 프레임
                label,                                           # 텍스트
                (x1, text_y),                                    # 텍스트 위치
                cv2.FONT_HERSHEY_SIMPLEX,                        # 폰트
                0.6,                                             # 글자 크기
                color,                                           # 글자 색상
                2                                                # 글자 두께
            )

        elapsed = time.time() - start                            # [수정5] 프레임 처리 소요 시간 계산
        fps_realtime = 1 / elapsed if elapsed > 0 else 0         # [수정5] 실시간 FPS 계산 (0 나누기 방지)

        info_text = f"Frame: {frame_count}  Detections: {len(detections)}  Tracks: {len(tracks)}"   # 현재 프레임 정보 문자열 생성

        cv2.putText(
            frame,                                               # 출력 프레임
            info_text,                                           # 정보 문자열
            (10, 30),                                            # 좌측 상단 위치
            cv2.FONT_HERSHEY_SIMPLEX,                            # 폰트
            0.8,                                                 # 글자 크기
            (0, 255, 0),                                         # 초록색
            2                                                    # 글자 두께
        )

        print(f"Frame {frame_count}: detections={len(detections)}, tracks={len(tracks)}, FPS={fps_realtime:.1f}")   # [수정5] 터미널에 FPS 포함한 중간 결과 출력

        cv2.imshow("YOLOv3 + SORT Tracking", frame)              # 실시간 결과 화면 출력
        out.write(frame)                                         # 결과 프레임 저장

        key = cv2.waitKey(1) & 0xFF                              # 키 입력 대기
        if key == 27:                                            # ESC 키 누르면
            break                                                # 종료
        if cv2.getWindowProperty("YOLOv3 + SORT Tracking", cv2.WND_PROP_VISIBLE) < 1:  # X 버튼으로 창 닫히면
            break                                                # 종료

    cap.release()                                                # 입력 비디오 해제
    out.release()                                                # 출력 비디오 해제
    cv2.destroyAllWindows()                                      # 모든 창 닫기

    print("추적 완료!")                                           # 완료 메시지 출력
    print(f"결과 영상 저장 완료: {output_video}")                 # 저장된 파일명 출력

# 프로그램 시작점
if __name__ == "__main__":                                       # 현재 파일이 직접 실행될 때만
    main()                                                       # main 함수 실행