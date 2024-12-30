FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt