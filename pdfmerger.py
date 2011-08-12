#!/usr/bin/env 
from __future__ import print_function
import sys
import os
from os import path
import re
from time import strftime
from time import localtime

try:
    from pyPdf import PdfFileWriter
    from pyPdf import PdfFileReader
    from pyPdf.utils import PdfReadError
except ImportError as e:
    print("Please install pyPdf module from http://pybrary.net/pyPdf/")
    sys.exit(2)

prog = re.compile(".*\.[Pp][Dd][Ff]$")

def do_help():
    print("this will be helpful later")
    sys.exit(1)

def merge_pdfs(output_name, files):
    output = PdfFileWriter()
    for f in files:
        try:
            i = PdfFileReader(file(f, "rb"))
        except IOError as e:
            print(e)
        except PdfReadError as e:
            print(e)
        else:
            for p in i.pages:
                output.addPage(p)
    if output.getNumPages():
        ostream = file(output_name, "wb")
        output.write(ostream)
        ostream.close()

def npath(*args):
    return path.normpath(path.join(*args))

def walk_paths(top, ctime):
    """
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    """

    for root, dirs, files in os.walk(top, topdown=False):
        out_name = "%s %s.pdf" %(root,ctime)
        files = [npath(root,x) for x in files if bool(prog.match(x))]
        merge_pdfs(out_name, files)

def check_path(p, cwd):
    if not path.isabs(p):
        p = path.normpath(path.join(cwd,p))
    return p

def main(things):
    files = []
    dirs = []
    cwd = path.split(path.commonprefix(things))[0]
    if cwd =="":
        cwd = os.getcwd()
    ctime = strftime("%Y%m%d%H%M%S", localtime())
    for thing in things:
        if path.isfile(thing) and bool(prog.match(thing)):
            files.append(check_path(thing, cwd))
        if path.isdir(thing):
            thing = check_path(thing, cwd)
            dirs.append(thing)
            files.append("%s %s.pdf" %(thing,ctime))
    files.sort()
    dirs.sort()
    #print((files, dirs))
    for d in dirs:
        walk_paths(d, ctime)
    p = "%s/../" %(cwd,)
    output_name = check_path("%s %s.pdf" %(path.split(cwd)[-1],ctime), p)
    print(output_name)
    merge_pdfs(output_name, files)
    


if __name__ == "__main__":
    if len(sys.argv) == 1 or "-h" in sys.argv:
        do_help()
    main(sys.argv[1:])

            

"""
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
"""


"""
from pyPdf import PdfFileWriter, PdfFileReader

output = PdfFileWriter()
input1 = PdfFileReader(file("document1.pdf", "rb"))

# print the title of document1.pdf
print "title = %s" % (input1.getDocumentInfo().title)

# add page 1 from input1 to output document, unchanged
output.addPage(input1.getPage(0))

# add page 2 from input1, but rotated clockwise 90 degrees
output.addPage(input1.getPage(1).rotateClockwise(90))

# add page 3 from input1, rotated the other way:
output.addPage(input1.getPage(2).rotateCounterClockwise(90))
# alt: output.addPage(input1.getPage(2).rotateClockwise(270))

# add page 4 from input1, but first add a watermark from another pdf:
page4 = input1.getPage(3)
watermark = PdfFileReader(file("watermark.pdf", "rb"))
page4.mergePage(watermark.getPage(0))

# add page 5 from input1, but crop it to half size:
page5 = input1.getPage(4)
page5.mediaBox.upperRight = (
    page5.mediaBox.getUpperRight_x() / 2,
    page5.mediaBox.getUpperRight_y() / 2
)
output.addPage(page5)

# print how many pages input1 has:
print "document1.pdf has %s pages." % input1.getNumPages()

# finally, write "output" to document-output.pdf
outputStream = file("document-output.pdf", "wb")
output.write(outputStream)
outputStream.close()
"""
