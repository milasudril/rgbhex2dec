#!/usr/bin/env python3

import sys
import getopt

prgname = 'rgbhex2dec'

def from_g22(value):
	return pow(value, 2.2)

def from_linear(value):
	return value

def to_g22(value):
	return pow(value, 1/2.2)

def to_linear(value):
	return value

def to_unknown(value):
	raise('Missing output color space')

def from_unknown(value):
	raise('Missing input color space')

decoders = {'g22':from_g22, 'linear':from_linear}
encoders = {'g22':to_g22, 'linear':to_linear}

def printHelp():
	print('''Usage: %s [options]
Options:
  --help  print this text and exet
  --output-space=g22|linear
  --output-space=g22|linear
'''%prgname)

def readAndConvertValues(src, decoder, dest, encoder):
	for line in src:
		line = line.strip()
		r = int(line[0:2], 16)
		g = int(line[2:4], 16)
		b = int(line[4:6], 16)
		a = int(line[6:8], 16) if len(line) == 8 else 255

		r = decoder(r/255)
		g = decoder(g/255)
		b = decoder(b/255)
		a = a/255

		print('%.8f %.8f %.8f %.8f'%(encoder(r), encoder(g), encoder(b), a))
	pass

def main(argv):
	try:
		opts, args = getopt.gnu_getopt(argv, '', ['help', 'output-space=', 'input-space='])
		encoder = to_unknown
		decoder = from_unknown
		for opt, arg in opts:
			if opt == '--help':
				printHelp()
				return 0

			if opt == '--output-space':
				if not arg in encoders:
					raise Exception('Unsupported output color space')
				encoder = encoders[arg]
			elif opt == '--input-space':
				if not arg in decoders:
					raise Exception('Unsupported input color space')
				decoder = decoders[arg]

		readAndConvertValues(sys.stdin, decoder, sys.stdout, encoder)
		return 0

	except Exception as e:
		print('%s: %s'%(prgname, str(e)))
		return 1

if __name__ == "__main__":
	exit(main(sys.argv[1:]))