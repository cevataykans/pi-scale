FROM python AS library

RUN pip install numpy
RUN pip install Rpi.GPIO
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install Jinja2
RUN pip install websockets

FROM library AS app
WORKDIR /pi-scale
COPY hx711.py server.py scale.py static templates ./
VOLUME [ "/dev/mem" ]
EXPOSE 8000
CMD ["uvicorn", "server:app"]