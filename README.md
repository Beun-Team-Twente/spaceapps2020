# Python Dependencies
Run `pip install -r requirements.txt` to install all project dependencies.

# REST API
- `/upload`

  **Description:** Upload a drawing image. It will be stored in the Database. The server will return its ID (used later to land to a certain location), the processed image in JPEG base-64 format and other drawings and their location.

  **Request Type:** POST

  **POST Parameters:**

  1. `drawing`: A multipart/x-form image file.

  
  **Returns:** JSON

  **Example Response:**
    ``` 
    {
        "error":"",
        "drawing_id": drawing_id,
        "drawing": "base-64 image data",
        "other_drawings": [
            {
                {"data": "base-64 image data", "location": [x,y]},
                ...
            }
        ]
    }
    ```


- `/land`

  **Description:** Update the location of the newly-uploaded drawing. It requires an ID and a location in x,y format. If successful, the response includes an empty error field (otherwise a description of the error).

  **Request Type:** GET

  **GET Parameters:**

  1. `drawing_id`: The drawing ID obtained from the `/upload` endpoint.
  2. `location`: X,Y location

  **Returns:** JSON

  **Example Request:** `/land?drawing_id=42&location=180,30`

  **Example Response:**

    ``` 
    {
        "error":""
    }
    ```
    

- `/request_site`

  **Description:** Retrieve all drawings with a valid location.

  **Request Type:** GET

  **GET Parameters:** None

  **Returns:** JSON

  **Example Response:**

    ``` 
    {
        "error":"",
        "drawings": [
            {
                {"data": "base-64 image data", "location": [x,y]},
                ...
            }
        ]
    }
    ```
    