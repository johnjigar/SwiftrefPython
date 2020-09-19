# SwiftrefPython

# Instructions for creating Pandas layer

% docker run -ti --entrypoint /bin/bash ubuntu

apt-get update

root@600e51f11253:/# apt-get upgrade

root@600e51f11253:/# apt-get install python3.8 -y

root@600e51f11253:/# apt-get install python3-pip -y

root@600e51f11253:/# apt-get install zip -y

apt-get install python3-pandas -y

apt-get install tree -y

root@600e51f11253:/# mkdir -p build/python/lib/python3.8/site-packages

root@600e51f11253:/build# tree

cd build

root@600e51f11253:/build# echo pandas > requirements.txt 

root@600e51f11253:/build# echo fsspec> requirements.txt 

root@600e51f11253:/build# pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/

root@600e51f11253:/build# zip -X -r Pandas.zip python/*

root@600e51f11253:/build#exit

docker cp <<dockerid>>:/build/Pandas.zip .

aws s3 cp Pandas.zip s3://lambda-functions-kkaws/Pandas.zip

aws lambda publish-layer-version --layer-name Pandas --content S3Bucket=lambda-functions-kkaws,S3Key=Pandas.zip --region us-east-1 --compatible-runtime python3.8

