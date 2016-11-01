all: dump load run

.phony: assemble dump load interactive

assemble: aout.bin

aout.bin: sd_init.asm
	z80asm --list sd_init.asm -o aout.bin 2> aout.lst

dump: aout.bin
	xxd aout.bin

load: aout.bin
	python2 loader.py load aout.bin 0xf000 > /dev/ttyACM0

run:
	python2 loader.py run 0xf000 > /dev/ttyACM0

interactive:
	python2 loader_slow.py > /dev/ttyACM0

