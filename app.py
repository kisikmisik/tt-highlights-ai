from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import cv2

app = Flask(__name__)
CORS(app)

@app.route('/trim_video', methods=['POST'])
def trim_video():
    file = request.files['video']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    # clip = VideoFileClip(file_path)
    # trimmed_clip = clip.subclip(10)
    # trimmed_path = os.path.join('trimmed', file.filename)
    # trimmed_clip.write_videofile(trimmed_path)
    # os.remove(file_path)
    print('VIDEO CAPTURE HERE')
    cap = cv2.VideoCapture(file_path)
    print(cap)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        img = cv2.imread(frame)

        # преобразование изображения в оттенки серого
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # применение фильтрации Гаусса для сглаживания изображения
        gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

        # применение алгоритма Хафа для поиска кругов на изображении
        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20,
                                param1=50, param2=30, minRadius=0, maxRadius=0)

        # проверка наличия кругов (мячей)
        if circles is not None:
            # если есть круги, то рисуем их на изображении
            circles = circles[0] # получаем координаты кругов
            for (x, y, r) in circles:
                cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            print('Мяч для настольного тенниса найден на изображении!')
        else:
            print('Мяч для настольного тенниса не найден на изображении.')

        # отображение изображения с выделенными кругами
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cap.release()
    cv2.destroyAllWindows()
    return jsonify({'result': 'success'})

@app.route('/download_video', methods=['GET'])
def download_video():
    trimmed_video_path = request.args.get('path')
    return send_file(trimmed_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)