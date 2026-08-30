import requests

from secrets import camera_fingerprint, prusa_camera_api_token, camera_name

prusa_connect_info_url = "https://connect.prusa3d.com/c/info"


def rename_camera(url, fingerprint, token, name):
    """Rename the camera in Prusa Connect"""
    try:
        response = requests.put(
            url,
            headers={
                "Content-Type": "application/json",
                "Fingerprint": fingerprint,
                "Token": token,
            },
            json={"config": {"name": name}},
        )
        response.raise_for_status()  # Raise an HTTPError on bad responses
        print(response.text)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error renaming camera: {e}")
        return None


if __name__ == '__main__':
    rename_camera(prusa_connect_info_url, camera_fingerprint, prusa_camera_api_token, camera_name)
