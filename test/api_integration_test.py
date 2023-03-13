from uuid import uuid4
import requests
from PIL import Image


ENDPOINT="YOUR END POINT"

def test_post_image():
    imageFile = Image.open(requests.get(url, stream=True).raw)
    request = f"task content: {uuid4().hex}"
    create_response = post_image(imageFile, request)
    assert create_response.status_code == 200


    print(get_task_response)
    assert get_task_response.json()["content"] == random_task_content

def post_image(imageFile: str, request : Request) -> dict:
    payload = {
        "file": imageFile,
        "request": request,
    }
    return requests.post(f"{ENDPOINT}/", json=payload)