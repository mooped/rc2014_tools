RC2014 Loader Tools
-------------------

Tools for assembling and loading binaries onto an unmodified [RC2014](http://rc2014.co.uk/) computer.

No need to burn roms to experiment with assembly/machine code.

Depends on python2.x.x, xxd, z80asm, and z80dasm. Assumes you are running Linux or similar and the RC2014 is on /dev/ttyACM0 by default.

**make**
Assemble, load, and run the target program.

**make load**
Assemble and load the target program

**make run**
Run the target program (assuming it is still resident)

**make assemble**
Assemble the target program, write the annotated listing to aout.lst

**make dump**
Assemble and hexdump the target program.

**make interactive**
Load and run a slow but interactive monitor program.
