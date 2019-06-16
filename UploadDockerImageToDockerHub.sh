#!/bin/bash
cat /home/ubuntu/dkrp | sudo docker login --username ilanbowen --password-stdin
sudo docker push ilanbowen/myflaskproj-img:latest