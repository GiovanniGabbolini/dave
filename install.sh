# Install conda

# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# and then run installer


# Set up environment

sudo apt-get update &&
sudo apt-get upgrade &&
sudo apt-get install build-essential &&
conda create -n segue-eval-website python=3.7.3 &&
source ~/miniconda3/bin/activate &&
conda activate segue-eval-website &&
pip install -r requirements.txt &&
python3 -c 'import nltk; nltk.download("punkt")' &&
python3 -c 'import nltk; nltk.download("stopwords")' &&
python3 -c 'import nltk; nltk.download("wordnet")' &&
python3 -c 'import nltk; nltk.download("averaged_perceptron_tagger")' &&
python3 -c 'import nltk; nltk.download("omw")' &&
python3 -c 'import nltk; nltk.download("cmudict")' &&

# Authbind

sudo apt-get install authbind &&
sudo touch /etc/authbind/byport/80 &&
sudo chmod 777 /etc/authbind/byport/80


# Install mongodb

wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add - &&
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list &&
sudo apt-get update &&
sudo apt-get install -y mongodb-org &&
echo "mongodb-org hold" | sudo dpkg --set-selections && 
echo "mongodb-org-server hold" | sudo dpkg --set-selections && 
echo "mongodb-org-shell hold" | sudo dpkg --set-selections && 
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections && 
echo "mongodb-org-tools hold" | sudo dpkg --set-selections


# Start mongodb

mongod --port 27017 --dbpath /var/lib/mongodb &


# https://docs.mongodb.com/manual/tutorial/enable-authentication/
# Populate database and setup access control

mongo --port 27017 user_trial/config_db.js

# Start mongodb with access control
# Use this to start mongodb also after startup

mongod --auth --port 27017 --dbpath /var/lib/mongodb &


# Run app with authbind -deep python3 main.py
