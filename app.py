import os
import re
import subprocess
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL이 필요합니다.'}), 400

    # Clean up old downloads
    for f in os.listdir(DOWNLOAD_DIR):
        os.remove(os.path.join(DOWNLOAD_DIR, f))

    try:
        result = subprocess.run(
            [
                'python3', '-m', 'yt_dlp',
                '-f', 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best[ext=mp4]/best',
                '--merge-output-format', 'mp4',
                '-o', os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
                '--no-playlist',
                url
            ],
            capture_output=True, text=True, timeout=300
        )

        if result.returncode != 0:
            return jsonify({'error': f'다운로드 실패: {result.stderr}'}), 500

        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.mp4')]
        if not files:
            return jsonify({'error': '다운로드된 파일을 찾을 수 없습니다.'}), 500

        filename = files[0]
        return jsonify({'filename': filename, 'url': f'/video/{filename}'})

    except subprocess.TimeoutExpired:
        return jsonify({'error': '다운로드 시간 초과 (5분)'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)


if __name__ == '__main__':
    print("앱이 실행되었습니다! 브라우저에서 http://localhost:5000 을 열어주세요.")
    app.run(debug=False, host='0.0.0.0', port=5000)
