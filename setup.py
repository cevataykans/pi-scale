from setuptools import setup

setup(
    name='hx711 server',
    version='0.1',
    description='HX711 Python Library for Raspberry Pi',
    py_modules=['hx711'],
    install_requires=['Rpi.GPIO', 'numpy', 'fastapi', 'uvicorn', 'Jinja2', 'websockets'],
)

