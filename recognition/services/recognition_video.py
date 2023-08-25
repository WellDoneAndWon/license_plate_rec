from ultralytics import YOLO
from PIL import Image
import cv2
import os
from pathlib import Path


def recognition_license_plate_video(path_video, date):
    print(path_video)
    try:
        # распознает номер авто, выделяет и подписывает, сохраняет в папку ответа у пользователя
        path_video = str(Path(Path.cwd(), 'answer', 'videos', path_video.split('/')[-1]))
        model = YOLO(str(Path(Path.cwd(), 'recognition', 'services', 'best.pt')))
        path_answer = str(Path(Path.cwd(), 'answer'))

        start_video_object_detection(path_answer, path_video, model)

        out = cv2.VideoWriter(f'{path_answer}\\output-{str(int(date))}.webm', cv2.VideoWriter_fourcc(*'VP80'), 30, (1920 // 2, 1080 // 2))
        lst = os.listdir(f'{path_answer}/images_from_video')

        for i in range(1, len(lst) - 1):
            img = cv2.imread(f'{path_answer}/images_from_video/frame{i}.jpg')
            out.write(img)

        out.release()

        # очищение временой папки с кадрами
        folder_path = f'{path_answer}/images_from_video'
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')
        if os.path.isfile(path_video):
            os.remove(path_video)
        return f'answer/output-{str(int(date))}.webm'
    except Exception as e:
        print(f'Ошибка при обработке видео: {e}')


def apply_yolo_object_detection(image_to_process, model):
    """
    Распознавание и определение координат объектов на кадре из видео
    :параметр image_to_process: исходное изображение
    :return: изображение с отмеченными объектами и подписями к ним
    """
    license_plates = model(image_to_process)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        box = [int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1)]

        image_to_process = draw_object_bounding_box(image_to_process, box)

    final_image = image_to_process
    return final_image


def draw_object_bounding_box(image_to_process, box):
    """
    Рисование границ объектов с подписями
    :параметр image_to_process: исходное изображение
    :параметр box: координаты области вокруг объекта
    :return: изображение с отмеченными объектами
    """

    x, y, w, h = box
    start = (x, y)
    end = (x + w, y + h)
    color = (0, 255, 0)
    width = 2
    final_image = cv2.rectangle(image_to_process, start, end, color, width)

    start = (x, y - 10)
    font_size = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 2
    text = 'license plates'
    final_image = cv2.putText(final_image, text, start, font,
                              font_size, color, width, cv2.LINE_AA)

    return final_image


def start_video_object_detection(path, video: str, model):
    try:
        """
        Захват и анализ видео
        """
        # Захват изображения из видео
        video_camera_capture = cv2.VideoCapture(video)

        # my
        index = 0
        ret = True
        while ret:  # video_camera_capture.isOpened():
            ret, frame = video_camera_capture.read()
            if not ret:
                break

            # Применение методов распознавания объектов на видеокадре от YOLO
            frame = apply_yolo_object_detection(frame, model)

            # уменьшенние размера окна обработанного изображения
            frame = cv2.resize(frame, (1920 // 2, 1080 // 2))

            # сохранение кадра
            path_for_frame = f'{path}/images_from_video/'
            if not os.path.exists(path_for_frame):
                os.makedirs(path_for_frame)
            name = f'{path_for_frame}/frame' + str(index) + '.jpg'
            cv2.imwrite(name, frame)

            # следующий кадр
            index += 1
    except Exception as e:
        print(f'Ошибка при обработке видео: {e}')
