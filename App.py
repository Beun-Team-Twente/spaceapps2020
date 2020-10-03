from flask import Flask, render_template, request
import os
from PIL import Image
import io
import json

from modules.database import db, drawing_handler

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
    drawing_blob = ""
    drawing_id = 0
    rockets = [] # [{'data': base64-image, 'location': location}, ..]
    try:
        f = request.files['drawing']
        img = request.files['drawing'].read()
        img = Image.open(io.BytesIO(img))

        drawing_id, drawing_blob, other_drawings = drawing_handler.store(img)
        drawing_blob = 'data:image/jpeg;base64,' + drawing_blob

        for r in range(len(other_drawings)):
            other_drawings[r]['drawing'] = 'data:image/jpeg;base64,' + other_drawings[r]['drawing'].decode('utf-8')
            other_drawings[r]['location'] = [int(i) for i in other_drawings[r]['location'].replace(" ","").split(",")]
    except Exception as e:
        return json.dumps({'error': str(e)})

    return json.dumps({
            'error':'',
            'drawing_id': drawing_id,
            'drawing': drawing_blob,
            'other_drawings': other_drawings
        })

@app.route("/land", methods=["GET"])
def land_rocket():
    drawing_id = request.args.get('drawing_id')
    drawing_location = request.args.get('location')
    result_error = ""
    try:
        result_error = drawing_handler.land(drawing_id, drawing_location)
    except Exception as e: 
        result_error = f"Error while landing: {e}"

    return json.dumps({"error": result_error})

@app.route("/request_site")
def request_drawings():
    try:
        drawings = [{'drawing': i[1], 'location': i[3]} for i in drawing_handler.get_other_drawings('')]
        for r in range(len(drawings)):
            drawings[r]['drawing'] = 'data:image/jpeg;base64,' + drawings[r]['drawing'].decode('utf-8')
            drawings[r]['location'] = [int(i) for i in drawings[r]['location'].replace(" ","").split(",")]

        return json.dumps({
            "error":'',
            "drawings": drawings
            })
    except Exception as e:
        return json.dumps({
            "error": f"Error while requesting site: {e}"
            })

@app.teardown_appcontext
def close_database_connection(exception): # Automatically close the DB when stopping the App
    db.close()

if __name__ == "__main__":
    print(f"Using port {PORT}")
    
    with app.app_context():
        db.init_db()

    app.run(threaded = True, host = '0.0.0.0', port = PORT)