import datetime
import base64
import io 

from . import db

ROCKET_TIME_LIMIT_MINS = 10
ROCKET_AMOUNT_LIMIT = 10

# Convert time-delta to minutes
timedelta_minutes = lambda td: (td.seconds // 60) % 60

def get_other_drawings(drawing_id):
    # Retrieves other people's rockets which already landed on Mars
    # Basic logic: If amount limit is exceeded, delete old rockets using the time limit
    query_results = db.query_db("SELECT ID, drawing, created, location from Drawings ORDER BY datetime(created) DESC")

    # Filter out all the results which don't have a location
    # results = tuple(filter(lambda r: (not r[3]) and (r[0] != drawing_id), results))
    results = []
    for k in query_results:
        if k[0] == drawing_id:
            continue
        elif k[3] == "":
            continue

        results.append(k)


    if len(results) < ROCKET_AMOUNT_LIMIT:
        return results
    else:
        returnables = []
        for r in range(len(results)):
            created = results[r][2]

            # Parse stored created datetime
            dt = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S.%f')

            if timedelta_minutes(datetime.datetime.now() - dt) > ROCKET_TIME_LIMIT_MINS: # Ordered descending; we can stop searching
                break

            returnables.append(results[r])

        return returnables

def land(drawing_id, location):
    # Update the location of a given ID
    # Returns error description
    try:
        drawing_id = int(drawing_id)
        results = db.query_db(f"SELECT ID, drawing, created, location from Drawings WHERE ID={drawing_id}")
        if len(results): # ID exists
            location_ok = len([int(i) for i in location.replace(" ","").split(",")]) == 2

            if(location_ok):
                sqlite_update_query = f"UPDATE 'Drawings' SET location='{location}' WHERE ID={drawing_id}"
                drawing_id = db.store_db(sqlite_update_query)
                return ""
            else:
                return "Invalid Location"
        else:
            return "Wrong ID"
    except Exception as e:
        return f"Error while landing in drawing_handler: {e}"

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
    rockets = [{'drawing': i[1], 'location': i[3]} for i in get_other_drawings(drawing_id)]

    return drawing_id, drawing_blob.decode('utf-8'), rockets