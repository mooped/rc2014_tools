import sys
import time

def emit(line):
  delay = 0.001
  for char in line:
    sys.stdout.write(char)
    time.sleep(delay)
  sys.stdout.write("\r")
  time.sleep(delay)
  sys.stdout.write("\n")
  time.sleep(delay)

lineno = 100
def emit_data(items):
  global lineno
  buf = "%d data " % lineno
  buf += ", ".join(items)
  emit(buf)
  lineno += 10

loader = [
  #10 LET ADDR = <starting address>
  "20 READ BYTE",
  "30 POKE ADDR,BYTE",
  "40 ADDR = ADDR + 1",
  "50 GOTO 20",
]

launcher = [
  #10 LET LOW = <low byte of starting address>
  #20 LET HIGH = <high byte of starting address>
  "30 POKE &h8049, LOW",
  "40 POKE &h804a, HIGH",
  "50 PRINT USR(0)",
]

def load(filename, offset):
  emit("NEW")
  time.sleep(0.1)

  for line in loader:
    emit(line)

  items_per_line = 16
  with open(filename, "rb") as f:
    item = 0
    buf = ""
    byte = ""
    items = []
    for byte in f.read():
      if item > 0 and ((item % items_per_line) == 0):
        emit_data(items)
        items = []
      items.append(str(ord(byte)))
      item += 1
  if len(items) > 0:
    emit_data(items)

  emit("10 LET ADDR = &h%x" % int(offset, 16))

  time.sleep(0.1)
  emit("RUN")

def run(offset):
  emit("NEW")
  time.sleep(0.1)

  for line in launcher:
    emit(line)

  org = int(offset, 16)
  low = org & 0xff
  high = (org & 0xff00) >> 8
  emit("10 LET LOW = &h%x" % low)
  emit("20 LET HIGH = &h%x" % high)

  emit("RUN")

args = sys.argv[1:]

sys.stderr.write("Processing args [%s]\r\n" % " ".join(args))
while len(args):
  if args[0] == 'load':
    sys.stderr.write("Loading \"%s\" at %s\r\n" % (args[1], args[2]))
    load(args[1], args[2])
    args = args[3:]
  elif args[0] == 'run':
    sys.stderr.write("Running from %s\r\n" % (args[1]))
    run(args[1])
    args = args[2:]
  else:
    sys.stderr.write("Unknown argument at [%s]\r\n" % " ".join(args))
    break
  time.sleep(0.5)

