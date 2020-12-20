docker build -t opencvtest .

# docker run -d -p 8080:8080 -it -v /Users/stanislawpulawski/data/dockervolumes/minio/photo:/data/minio/photo --name=opencvtestcontainer opencvtest
docker run -d -p 8080:8080 -it -v /home/zombie/data/minio/photo:/data/minio/photo opencvtest

# sudo docker run -d -p 9000:9000 --restart=always --name minio-storage   -e "MINIO_ACCESS_KEY=miniouseradmin"   -e "MINIO_SECRET_KEY=wJalrXUtnFEMK7MDEPxRfiCYEXAMPLEKEY"   -v /home/zombie/data/minio:/data/minio   minio/minio server /data/minio
