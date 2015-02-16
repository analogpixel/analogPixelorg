#!/usr/bin/python

# python -m SimpleHTTPServer 8000

import ConfigParser
import glob
import os
import os.path
import time
import pystache
import sys

config = ConfigParser.SafeConfigParser()

if os.path.isfile("makeindex.cfg"):
  config.read('makeindex.cfg')
  C_HTMLPATH      = config.get('main', 'htmlPath')
  C_TEMPLATE_FILE = config.get('main','template')
  C_TEMPLATE      = open(C_TEMPLATE_FILE).read()
  C_UNPROCESSED   = config.get('main','unprocessed')
  C_PROCESSED     = config.get('main','processed')


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

fileList = { C_UNPROCESSED:{}, C_PROCESSED:{} }
for scan in [ C_UNPROCESSED, C_PROCESSED ]:
  for fileName in glob.glob( C_HTMLPATH + "/*." + scan ):
    baseName           = os.path.basename(fileName)
    name               = "".join(baseName.split('.')[:-1])
    parts              = baseName.split("-")
    timeString         = "%s %s %s" % (parts[0], parts[1], parts[2])
    postDate           = time.strptime(timeString, "%Y %m %d")
    title              = " ".join(parts[3:])
    title              = " ".join(title.split('.')[:-1])
    title              = " ".join(title.split('-'))
    fileList[scan][baseName] = {'date': postDate, 'title': title, 'path': fileName, 'baseName': name + "." + scan }

    # create a stub file so when we scan for all html files to build the index, we find them
    if scan == C_UNPROCESSED:
      touch( C_HTMLPATH + "/" + name + "." + C_PROCESSED )


# Create the sidebar that links to all the pages
sidebar = ""
for item in sorted(fileList[C_PROCESSED].values() , key=lambda p: p['date'], reverse=True ):
  i = item
  sidebar = sidebar + "<div class=menuItem><a href=../html/" + i['baseName'] + ">" + i['title'] + "</a></div>"

# files that emacs write are .htm this script will create an html and
# delete the htm
for item in fileList[C_UNPROCESSED].values():
  data = {'content': file( item['path']).read() , 'sidebar': sidebar }
  with open( item['path'] + "l" , "w") as f:
    f.write(  pystache.render( C_TEMPLATE, data ) )

  #os.unlink( item['path'] )
