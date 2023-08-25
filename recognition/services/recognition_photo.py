from ultralytics import YOLO
from PIL import Image
import cv2
import os
import gunicorn
from pathlib import Path


def recognition_license_plate_photo(path_img, date):
    path_img = str(Path(Path.cwd(), 'answer', 'images', path_img.split('/')[-1]))
    # распознает номер авто, выделяет и подписывает, сохраняет в папку ответа у пользователя
    model = YOLO(str(Path(Path.cwd(), 'recognition', 'services', 'best.pt')))
    results = model.predict(Image.open(path_img))
    result = results[0]
    output = []
    coord = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
            x1, y1, x2, y2, result.names[class_id], prob
        ])
        coord.append([x1, y1, x2, y2])
    print(output)

    path_answer = str(Path(Path.cwd(), 'answer'))
    img = cv2.imread(path_img)
    for c in coord:
        img = selection(img, c)
    if not os.path.exists(path_answer):
        os.makedirs(path_answer)
    path_to_save = path_img.split("\\")[-1]
    path_to_save = path_to_save.split(".")[0] + '-' + str(int(date)) + '.' + path_to_save.split(".")[1]
    cv2.imwrite(f'{path_answer + "/" + path_to_save}', img)
    if os.path.isfile(path_img):
        os.remove(path_img)
    return "answer/" + path_to_save


def selection(img, coord):
    img_with_rect = cv2.rectangle(img,
                                  (int(coord[0]), int(coord[1])),
                                  (int(coord[2]), int(coord[3])),
                                  (0, 255, 0),
                                  5)
    start = (int(coord[0]), int(coord[1]) - 10)
    font_size = 0.5
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 2
    text = 'license plate'
    img_with_rect = cv2.putText(img_with_rect, text, start, font,
                                font_size, (0, 255, 0), width, cv2.LINE_AA)
    return img_with_rect


def crop(img, coord):
    img_crop = img[coord[1]:coord[3], coord[0]:coord[2]]
    return img_crop
