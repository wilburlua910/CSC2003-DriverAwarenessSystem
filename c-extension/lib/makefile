CC = gcc

default: libblink.a

libblink.a: blink.o
	ar rcs $@ $^

blink.o: blink.c
	$(CC) -c $<

clean:
	rm *.o *.a