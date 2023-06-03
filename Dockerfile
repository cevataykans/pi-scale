FROM python

WORKDIR /pi-scale

COPY hx711.py server.py scale.py ./

VOLUME [ "/dev/mem" ]

RUN pip install numpy
RUN pip install Rpi.GPIO
RUN pip install fastapi

EXPOSE 80

CMD ["python3", "server.py"]
