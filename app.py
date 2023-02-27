from flask import Flask, request, jsonify
from flask_cors import CORS
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

app = Flask(__name__)
CORS(app)

@app.route('/trim_video', methods=['POST'])
def trim_video():
    print(request.files['video'])
    file = request.files['video']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    clip = VideoFileClip(file_path)
    trimmed_clip = clip.subclip(10)
    trimmed_path = os.path.join('trimmed', file.filename)
    trimmed_clip.write_videofile(trimmed_path)
    os.remove(file_path)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)