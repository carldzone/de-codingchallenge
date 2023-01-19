# de-codingchallenge
Coding Challenge for Red Elsevier - Data Engineer I role

## Getting started
This project will use Python 3.7. To make sure you have Python 3.7, install it if your default python version is not 3.7
### NOTE: This method was done using a Linux OS
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
```

Install venv for python3.7
```
sudo apt install python3.7-venv
```

Create your virtual environment
```
python3.7 -m venv decc-venv
```

To activate the virtualenvironment
```
source decc-venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

## To test on your local machine:
Setup your geckodriver to your local machine.
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```