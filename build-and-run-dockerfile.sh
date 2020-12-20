docker build -t opencvtest .


# docker run -p 8080:8080 -it -v /Users/stanislawpulawski/data/dockervolumes/opencv:/data/workspace opencvtest

docker run -d -p 8080:8080 -it -v /Users/stanislawpulawski/data/dockervolumes/minio/photo:/data/minio/photo opencvtest
