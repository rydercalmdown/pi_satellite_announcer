#!/bin/bash
# install_raspberry_pi.sh

cd ../

echo "Installing base dependencies"
sudo apt-get update
sudo apt-get install -y ffmpeg \
    mpg321 \
    espeak \
    python3-pip

python3 -m pip install virtualenv
python3 -m virtualenv -p python3 env
. env/bin/activate

pip install -r src/requirements.txt
