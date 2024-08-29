# USB camera Prusa Connect

## Prusa Connect

### Login to Prusa Connect
Navigate to your printer that you want to pair the camera with
Navigate to Camera


    + Add new other camera

Note the “Token”, We will need that later

## Raspberry Pi
Starting with fresh SD image of Bookworm

### Setup

#### Update and Upgrade
    sudo apt update
    sudo apt upgrade -y
    
#### Install Python 3 and Pip
Python 3 should be pre-installed, but you may need to install pip for package management

    sudo apt install python3-pip -y

#### Install git

    sudo apt install git

#### Clone this repo

    git clone https://github.com/nickjvturner/prusa-connect-rpi-camera

Navigate into the cloned dir

    cd prusa_connect_camera

#### Create a Virtual Environment

    python3 -m venv venv

Activate venv

    source venv/bin/activate

#### Install OpenCV and uuidgen (apt)
    sudo apt install python3-opencv -y
    sudo apt-get install uuid-runtime

#### Install requests, OpenCV, Flask (pip3)
    pip3 install requests
    pip3 install opencv-python
    pip3 install flask

#### Generate an UUID for the camera
The camera requires an UUID, we can generate one using uuidgen

    uuidgen

#### Update secrets.py
Add the freshly created UUID into the secrets.py file
Add the token from earlier to secrets.py

#### Review code before execution
It is good practice to quickly look through ‘simple’ scripts created by others before running them.

Review:
- pc-cam-local.py
- pc-cam-uploader.py

## Configure scripts to run on boot

### Create a service file for pc-cam-local.py
    sudo nano /etc/systemd/system/pc-cam-local.service

```[Unit]
Description=RPi Camera Local Web Server
After=network.target

[Service]
ExecStart=/home/pi/prusa-connect-rpi-camera/venv/bin/python /home/pi/prusa-connect-rpi-camera/pc-cam-local.py
WorkingDirectory=/home/pi/prusa-connect-rpi-camera
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

#### Enable and start the service
    sudo systemctl daemon-reload
    sudo systemctl enable prusa_connect_camera
    sudo systemctl start prusa_connect_camera

### Create a service file for pc-cam-uploader.py
    sudo nano /etc/systemd/system/pc-cam-uploader.service

```[Unit]
Description=Prusa Connect RPi Camera image uploader
After=network.target

[Service]
ExecStart=/home/pi/prusa-connect-rpi-camera/venv/bin/python /home/pi/prusa-connect-rpi-camera/pc-cam-uploader.py
WorkingDirectory=/home/pi/prusa-connect-rpi-camera
Restart=always
User=pi

[Install]
WantedBy=multi-user.target