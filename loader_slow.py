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

loader = [
  "10 PRINT \"Hex Loader\"",
  "20 PRINT \"  Commands:\"",
  "30 PRINT \"    PUT XXXX:YY    - store byte 0xYY at location 0xXXXX\"",
  "40 PRINT \"    PEEK XXXX      - read 16 bytes starting from 0xXXXX\"",
  "50 PRINT \"    RUN XXXX       - jump to address 0xXXXX and begin execution\"",
  "60 PRINT \"    EXIT           - return to BASIC\"",

  "1000 INPUT \"\"; A$",
  "1010 LET VLD = 0",
  "1110 IF MID$(A$, 1, 3) = \"PUT\" AND MID$(A$, 9, 1) = \":\" THEN GOSUB 2000",
  "1120 IF MID$(A$, 1, 4) = \"PEEK\" THEN GOSUB 3000",
  "1130 IF MID$(A$, 1, 3) = \"RUN\" THEN GOSUB 4000",
  "1140 IF MID$(A$, 1, 4) = \"EXIT\" THEN STOP",
  "1900 IF VLD = 0 THEN PRINT \"INVALID COMMAND: \"; A$",
  "1950 GOTO 1000",

  "2000 LET D$ = MID$(A$, 5, 4)",
  "2010 LET B$ = MID$(A$, 10, 2)",
  "2020 LET I$ = D$: GOSUB 11000: LET DEST = T",
  "2030 LET I$ = B$: GOSUB 11000: LET BYTE = T",
  "2040 PRINT \"PUT 0x\";HEX$(DEST);\" = \";BYTE",
  "2050 POKE DEST, BYTE",
  "2900 LET VLD = 1",
  "2950 RETURN",

  "3000 LET S$ = MID$(A$, 6, 4)",
  "3010 LET I$ = S$: GOSUB 11000: LET SOURCE = T",
  "3020 PRINT HEX$(SOURCE);\": \";",
  "3030 FOR J = 0 to 15",
  "3040 PRINT HEX$(PEEK(SOURCE + J));\" \";",
  "3050 NEXT J",
  "3060 PRINT",
  "3900 LET VLD = 1",
  "3950 RETURN",

  "4000 LET H$ = MID$(A$, 5, 2)",
  "4010 LET L$ = MID$(A$, 7, 2)",
  "4020 LET I$ = H$: GOSUB 11000: LET HIGH = T",
  "4030 LET I$ = L$: GOSUB 11000: LET LOW = T",
  "4040 POKE &h8049, LOW",
  "4050 POKE &h804a, HIGH",
  "4052 PRINT \"POKE 0x8049, \"; HEX$(LOW)",
  "4054 PRINT \"POKE 0x804a, \"; HEX$(HIGH)",
  "4060 PRINT USR(0)",
  "4900 LET VLD = 1",
  "4950 RETURN",

  "11000 T = 0",
  "11020 FOR J = 1 TO LEN(I$)",
  "11030 T = T * 16",
  "11040 C$ = MID$(I$, J, 1)",
  "11050 IF C$ >= \"0\" AND C$ <= \"9\" THEN T = T + (ASC(C$) - ASC(\"0\"))",
  "11060 IF C$ >= \"A\" AND C$ <= \"F\" THEN T = T + (ASC(C$) - ASC(\"A\") + 10)",
  "11070 IF C$ >= \"a\" AND C$ <= \"f\" THEN T = T +  (ASC(C$) - ASC(\"a\") + 10)",
  "11080 NEXT J",
  "11090 IF T > 32768 THEN T = T - 65536",
  "11220 RETURN",
]

emit("EXIT")
emit("EXIT")

for line in loader:
  emit(line)

emit("RUN")
time.sleep(0.1)

def load(filename, offset):
  with open(filename, "rb") as f:
    org = int(offset, 16)
    for byte in f.read():
      emit("PUT %4.x:%2.x" % (org, ord(byte)))
      time.sleep(0.2)
      org = org + 1

def run(offset):
  org = int(offset, 16)
  emit("RUN %4.x" % org)

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

