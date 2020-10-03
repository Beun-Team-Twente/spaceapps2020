API_SERVER = "http://localhost:5000/upload" # Test API server runs on a free Heroku Dyno

_HELP_STR = "The first command-line argument is the path of an image (JPG or PNG file)"

import requests
import sys


if len(sys.argv) == 1:
    print("Invalid input path: " + _HELP_STR)
    print(f"\nExample Usage: python3 {__file__} image.jpg")
    exit(1)

files = {'drawing': open(sys.argv[1], 'rb')}
print("\nServer-response:")
print(requests.post(API_SERVER, files=files).content.decode())
