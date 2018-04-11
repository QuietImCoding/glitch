#! /usr/bin/python
import random, sys
import argparse

# Method to update progress bar
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def scan_jpg(bytedata):
    byte_buffer = [0, 0]
    for k in range(len(bytedata)):
        byte_buffer[1] = byte_buffer[0]
        byte_buffer[0] = ord(bytedata[k])
        if byte_buffer == [218, 255]:
            return k

def scan_png(bytedata):
    byte_buffer = [0, 0, 0, 0]
    for k in range(len(bytedata)):
        byte_buffer[3] = byte_buffer[2]
        byte_buffer[2] = byte_buffer[1]
        byte_buffer[1] = byte_buffer[0]
        byte_buffer[0] = ord(bytedata[k])
        if byte_buffer == [84, 65, 68, 73]:
            return k

def prescan(fname):
    g = open(fname, 'rb')
    d = g.read()
    g.close()

    dotindex = fname.find('.')
    ftype = fname[dotindex+1:] if dotindex != -1 else "unknown"
    print "Dected filetype:", ftype
    if ftype == "jpg" or ftype == "jpeg":
        sof = scan_jpg(d)
    elif ftype == "png":
        sof = scan_png(d)
    elif ftype == "unknown":
        sof = 0
    else:
        sof = 50

    return (d, sof)

def corrupt(ns):
    fin = ns.fin
    fout = ns.fout
    flips = ns.flips
    diff = ns.diff
    rand = ns.rand
    if fout == "":
        fout = fin
    d, sof = prescan(fin)
    for f in range(int(flips)):
        bit2flip = random.randint(sof, len(d)-1)
        currentbit = d[bit2flip]
        if rand:
            newbit = chr((ord(currentbit) + random.randint(0, diff)) % 256)
        else:
            newbit = chr((ord(currentbit) + diff) % 256)
        d = d[:bit2flip] + bytes(newbit) + d[bit2flip+1:]
        update_progress(float(f)/flips)
    print("")
    newf = open(fout, 'wb')
    newf.write(d)
    newf.close()

def overwrite(ns):
    fin = ns.fin
    transplant = ns.transplant
    fout = ns.fout
    bits = ns.bits
    offset = ns.offset
    if fout == "":
        fout = fin
    d, sof = prescan(fin)
    d2, sof2 = prescan(transplant)
    d = d[:sof+offset] + d2[sof2+offset:sof2+offset+bits] + d[sof+offset+bits:]
    print d == d2
    newf = open(fout, 'wb')
    newf.write(d)
    newf.close()

parser = argparse.ArgumentParser(description='Glitchr. Used to mess with data of files')
parser.add_argument("--silent", action="store_true")

subparsers = parser.add_subparsers(help="Commands available: corrupt overwrite selective")

corrupt_parser = subparsers.add_parser('corrupt', help='Randomly corrupts image')
overwrite_parser = subparsers.add_parser('overwrite', help='Overwrites one section of a file with another')
parser.add_argument('fin')
parser.add_argument('-o', '--out', default="", dest="fout")
corrupt_parser.add_argument('-a', '--amount', type=int, default=40, dest="flips")
corrupt_parser.add_argument('-d', '--distance', type=int, default=10, dest="diff")
corrupt_parser.add_argument('-r', '--random', action='store_true', dest="rand")
corrupt_parser.set_defaults(func=corrupt)

overwrite_parser.add_argument('transplant')
overwrite_parser.add_argument('-a', '--bits', type=int, default=100)
overwrite_parser.add_argument('-d', '--offset', type=int, default=100)
overwrite_parser.set_defaults(func=overwrite)

args = parser.parse_args()
args.func(args)
