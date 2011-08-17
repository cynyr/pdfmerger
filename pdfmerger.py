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
    """ Merges files in the order given. Make sure to sort first."""
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
        files.sort()
        merge_pdfs(out_name, files)

def check_path(p, cwd):
    """make_abs would be a better name for this"""
    if not path.isabs(p):
        p = path.normpath(path.join(cwd,p))
    return p

def main(things):
    files = []
    dirs = []
    cwd = path.split(path.commonprefix(things))[0]
    if cwd =="":
        cwd = os.getcwd()
    """Get the date code to use on merged files."""
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
