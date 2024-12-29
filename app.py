from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the home page or upload form
@app.route('/index')
def index():
    return render_template('index.html')  # Create 'index.html' for your upload form

# Route for previewing the video
@app.route('/')
def display_video():
    video_name = 'camera.mp4'  # Replace with your logic to get the video name
    return render_template('preview.html', video_name=video_name)

if __name__ == '__main__':
    app.run(debug=True)
