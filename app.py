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
    if not os.path.exists('images'):
        os.makedirs('images')

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imwrite('images/frame{:d}.jpg'.format(count), frame)

        count += 1

    cap.release()
    cv2.destroyAllWindows()
    return jsonify({'result': 'success'})

@app.route('/download_video', methods=['GET'])
def download_video():
    trimmed_video_path = request.args.get('path')
    return send_file(trimmed_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)