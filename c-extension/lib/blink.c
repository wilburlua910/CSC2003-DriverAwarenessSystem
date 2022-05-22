// C extension to blink an led connected to BCM GPIO14 for 1 second every 10 second
// Uses wiringPi to control the GPIO, uses SIGALRM as timer interrupt

#include <wiringPi.h>
#include <signal.h>
#include <unistd.h>

void alarmHandler(int signal);

// "main" function
void startBlink(){
    // Set pin mode of wiringPi to wiringPi mapping, see http://wiringpi.com/pins/
    wiringPiSetup();

    // Set pin 15 (BCM GPIO14) to output
    pinMode(15, OUTPUT);

    // Register SIGALRM handler and request for alarm in 1 second
    signal(SIGALRM, alarmHandler);
    alarm(1);
}

// SIGALRM handler
void alarmHandler(int signal){
    // To remember the status of LED, 0 = off, 1 = on
    static unsigned char status = 0;

    if (signal == SIGALRM){
        // If LED is off, turn it on and request an alarm in 1 second
        // If LED is on, turn it off and request an alarm in 9 second
        if (status == 0){
            digitalWrite(15, HIGH);
            status = !status;
            alarm(1);
        } else if (status == 1){
            digitalWrite(15, LOW);
            status = !status;
            alarm(9);
        }
    }
}