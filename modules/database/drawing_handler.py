import datetime
import base64
import io 

from . import db

ROCKET_TIME_LIMIT_MINS = 10
ROCKET_AMOUNT_LIMIT = 10

# Convert time-delta to minutes
timedelta_minutes = lambda td: (td.seconds//60)%60

def get_other_rockets(drawing_id):
    # Retrieves other people's rockets which already landed on Mars
    # Basic logic: If amount limit is exceeded, delete old rockets using the time limit
    results = db.query_db("SELECT id, drawing, created, location from Drawings ORDER BY datetime(created) DESC")

    if len(results) < ROCKET_AMOUNT_LIMIT:
        return results
    else:
        returnables = []
        for r in range(len(results)):
            if results[r][0] == drawing_id: # Skip the drawing that was just uploaded
                continue

            created = results[r][2]

            # Parse stored created datetime
            dt = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S.%f')

            if timedelta_minutes(datetime.datetime.now() - dt) > ROCKET_TIME_LIMIT_MINS: # Ordered descending; we can stop searching
                break

            returnables.append(results[r])

        return returnables

def store(img):
    # Store a processed (PIL) image to the database in base64 format
    created_date = datetime.datetime.now()
    
    # Create image blob
    buffer = io.BytesIO()
    img.save(buffer, format = "JPEG")
    drawing_blob = base64.b64encode(buffer.getvalue())

    # Store blob to database
    sqlite_insert_with_param = """INSERT INTO 'Drawings'
                          ('drawing', 'created', 'location') 
                          VALUES (?, ?, '');"""

    data_tuple = (drawing_blob, created_date)

    drawing_id = db.store_db(sqlite_insert_with_param, data_tuple)

    # Get other rockets in location
    rockets = [{'drawing': i[1], 'location': i[3]} for i in get_other_rockets(drawing_id)] # [{'blob': base-64 image, 'location': location}, ..]

    return drawing_id, drawing_blob.decode('utf-8'), rockets