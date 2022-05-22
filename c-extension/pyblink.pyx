cdef extern from "blink.c":
    void startBlink()

def start_blink():
    startBlink()