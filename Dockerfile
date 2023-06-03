FROM python

WORKDIR /pi-scale

COPY hx711.py server.py scale.py static templates ./

VOLUME [ "/dev/mem" ]

RUN pip install numpy
RUN pip install Rpi.GPIO
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install Jinja2
RUN pip install websockets

EXPOSE 8000

CMD ["uvicorn", "server:app"]
