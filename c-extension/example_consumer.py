import pyblink
from time import sleep

pyblink.start_blink()

for i in range(30):
    print("hello %d" % i)
    sleep(0.5)