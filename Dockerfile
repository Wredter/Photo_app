FROM jjanzic/docker-python3-opencv:latest

RUN ["pip", "install", "web.py"]

COPY . ./app/
RUN pwd
# WORKDIR /app/
EXPOSE 8080
# CMD ["python", "Start.py", "-f './Data/IMG_20201216_185903.jpg'"]
CMD ["python", "/app/Server.py"]
# CMD ["bash"]
