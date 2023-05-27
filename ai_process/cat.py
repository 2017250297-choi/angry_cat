import cv2
import dlib
import numpy as np
import random

h, w = 0, 0


# a, d 에서 사용
def width_control(pt1, pt2, control_y):
    if abs(pt2[0] - pt1[0]) < w * 0.4:
        width_increase = int((pt2[0] - pt1[0]) * 0.3)
        down_width_increase = pt1[0]
        up_width_increase = pt2[0]
        down_width_increase -= width_increase
        up_width_increase += width_increase
        half_y = control_y
        pt1 = [down_width_increase, pt1[1]]
        pt2 = [up_width_increase, half_y]
        return pt1, pt2
    else:
        return pt1, pt2


# b, c에서 사용
def height_control(pt1, pt2, center_x):
    if abs(pt2[1] - pt1[1]) < h * 0.4:
        height_increase = int(abs(pt2[1] - pt1[1]) * 0.2)
        down_height_increase = pt1[1]
        up_height_increase = pt2[1]
        down_height_increase -= height_increase
        up_height_increase += height_increase
        half_x = center_x
        pt1 = [pt1[0], down_height_increase]
        pt2 = [half_x, up_height_increase]
        return pt1, pt2
    else:
        return pt1, pt2


def random_contorl(random_images):
    random_image = random.choice(random_images)
    sticker_img_path = random_image["img"]
    return sticker_img_path


def select_target(target, a, b, c, d, x1, x2, y1, y2, center_x, center_y):
    if target == a:
        # 랜덤 이미지 딕셔너리
        random_images = [
            {"num": 0, "img": "static/imgs/up_cat.png"},
            {"num": 1, "img": "static/imgs/top_cat1.png"},
        ]
        sticker_img_path = random_contorl(random_images)
        # 스티커 이미지 로드
        sticker_img = cv2.imread(sticker_img_path, cv2.IMREAD_UNCHANGED)
        control_y = a // 2
        pt1 = x1, y1
        pt2 = x2, 0
        pt1, pt2 = width_control(pt1, pt2, control_y)
    elif target == b:
        # 랜덤 이미지 딕셔너리
        random_images = [
            {"num": 0, "img": "static/imgs/left_cat1.png"},
            {"num": 1, "img": "static/imgs/left_cat2.png"},
        ]
        sticker_img_path = random_contorl(random_images)
        # 스티커 이미지 로드
        sticker_img = cv2.imread(sticker_img_path, cv2.IMREAD_UNCHANGED)
        center_x = b // 2
        pt1 = x1, y1
        pt2 = 0, y2
        pt1, pt2 = height_control(pt1, pt2, center_x)
    elif target == c:
        # 랜덤 이미지 딕셔너리
        random_images = [
            {"num": 0, "img": "static/imgs/right_cat.png"},
            {"num": 1, "img": "static/imgs/right_cat1.png"},
        ]
        sticker_img_path = random_contorl(random_images)
        # 스티커 이미지 로드
        sticker_img = cv2.imread(sticker_img_path, cv2.IMREAD_UNCHANGED)
        control_x = center_x + c // 2
        pt1 = x2, y1
        pt2 = w, y2
        pt1, pt2 = height_control(pt1, pt2, control_x)
    elif target == d:
        # 랜덤 이미지 딕셔너리
        random_images = [
            {"num": 0, "img": "static/imgs/under_cat.png"},
            {"num": 1, "img": "static/imgs/under_cat1.png"},
            {"num": 2, "img": "static/imgs/under_cat2.png"},
        ]
        sticker_img_path = random_contorl(random_images)
        # 스티커 이미지 로드
        sticker_img = cv2.imread(sticker_img_path, cv2.IMREAD_UNCHANGED)
        control_y = center_y + d // 2
        pt1 = x1, y2
        pt2 = x2, h
        pt1, pt2 = width_control(pt1, pt2, control_y)
    return pt1, pt2, sticker_img, target


def picture_generator(input_pic_url):
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(input_pic_url[1:])
    dets = detector(img)
    # 얼굴이 1개 이상 감지된 경우에만 스티커 적용
    if len(dets) >= 1:
        # 얼굴 선택 랜덤
        face_index = random.randrange(len(dets))
        det = dets[face_index]
        x1 = det.left()
        y1 = det.top()
        x2 = det.right()
        y2 = det.bottom()
        h, w, c = img.shape
        center_x = (x2 + x1) // 2
        center_y = (y2 + y1) // 2
        a = center_y
        b = center_x
        c = w - b
        d = h - a
        # target = None
        target_list = [a, b, c, d]
        target = target_list.pop(target_list.index(max(target_list)))
        # target = search_target
        while True:
            pt1, pt2, sticker_img, target = select_target(
                target, a, b, c, d, x1, x2, y1, y2, center_x, center_y
            )
            cv2.rectangle(img, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=2)
            # 스티커 이미지 크기 변경
            sticker_width = int(abs(pt2[0] - pt1[0]))
            sticker_height = int(abs(pt2[1] - pt1[1]))
            sticker_resized = cv2.resize(
                sticker_img, dsize=(sticker_width, sticker_height)
            )
            # 알파 채널 값(투명도) 계산
            alpha = sticker_resized[:, :, 3] / 255.0
            alpha = np.expand_dims(alpha, axis=2)
            overlay_rgb = sticker_resized[:, :, :3]
            try:
                img[
                    min(pt1[1], pt2[1]) : max(pt1[1], pt2[1]),
                    min(pt1[0], pt2[0]) : max(pt1[0], pt2[0]),
                ] = (
                    alpha * overlay_rgb
                    + (1.0 - alpha)
                    * img[
                        min(pt1[1], pt2[1]) : max(pt1[1], pt2[1]),
                        min(pt1[0], pt2[0]) : max(pt1[0], pt2[0]),
                    ]
                )[
                    :, :, :3
                ]
            except:
                target = target_list.pop(target_list.index(max(target_list)))
                # pt1, pt2, sticker_img, target = select_target(
                #     target, a, b, c, d, x1, x2, y1, y2, center_x, center_y
                # )
                continue
            break
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    else:
        print("얼굴이 탐지되지 않았다.")
    # 출력
    cv2.imwrite(input_pic_url[1:].replace("input", "change"), img)
    return input_pic_url.replace("input", "change")
