import sys

scale = Scale()
scale.tare()
while True:
    try:
        scale.weight()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        scale.clean()
        sys.exit()