#!/bin/bash

# Checking to see if docker and docker-compose are installed, otherwise install them.

if [[ $(docker -v) ]]; 
then
  echo "Docker installed"
else
  curl -sSL https://get.docker.com/ | sh
fi

if [[ $(docker-compose -v) ]]; 
then
  echo "Docker-compose installed"
else
  curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose &&
  chmod +x /usr/local/bin/docker-compose
  sudo groupadd docker
  sudo usermod -aG docker $USER
fi

sudo systemctl start docker &&
sudo systemctl start containerd