import requests
import time

from secrets import prusa_connect_camera_url, image_path, prusa_camera_api_token


def upload_image(url, fingerprint, token, image_path):
    """Upload an image over HTTP"""
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.put(
                url,
                headers={
                    "accept": "*/*",
                    "content-type": "image/jpg",
                    "fingerprint": fingerprint,
                    "token": token,
                },
                data=image_file,
                stream=True,
            )
            response.raise_for_status()  # Raise an HTTPError on bad responses
            print(response.text)
            return response
    except requests.exceptions.RequestException as e:
        print(f"Error uploading image: {e}")
        return None


if __name__ == '__main__':
    while True:
        upload_image(url, camera_fingerprint, prusa_camera_api_token, image_path)
        time.sleep(10)  # Upload every 10 seconds