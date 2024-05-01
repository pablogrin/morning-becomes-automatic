docker build --platform linux/amd64 -t morning-becomes-automatic:1.0.0 .
docker tag morning-becomes-automatic:1.0.0 "$1".dkr.ecr.us-east-1.amazonaws.com/morning-becomes-automatic:1.0.0