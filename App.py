from flask import Flask, render_template, request
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='html')

PORT = 5000

if 'PORT' in os.environ:
    # Needed for Heroku
    PORT = int(os.environ['PORT'])
    print(f"Using port {PORT}")

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    f = request.files['drawing']
    img = request.files['img_data'].read()
    
    return ""
        

if __name__ == "__main__":
    print(f"Using port {PORT}")
    app.run(threaded = True, host = '0.0.0.0', port = PORT)