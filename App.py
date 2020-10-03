from flask import Flask
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

PORT = 5000

if 'PORT' in os.environ:
    # Needed for Heroku
    PORT = int(os.environ['PORT'])
    print(f"Using port {PORT}")

@app.route("/")
def root():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    print(f"Using port {PORT}")
    app.run(threaded=True, host='0.0.0.0', port=PORT)