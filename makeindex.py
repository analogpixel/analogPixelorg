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
  C_HTMLPATH           = config.get('main', 'htmlPath')
  C_TEMPLATE_FILE      = config.get('main','template')
  C_INDEXTEMPLATE_FILE = config.get('main','indextemplate')
  C_TEMPLATE           = open(C_TEMPLATE_FILE).read()
  C_INDEXTEMPLATE      = open(C_INDEXTEMPLATE_FILE).read()
  C_UNPROCESSED        = config.get('main','unprocessed')
  C_PROCESSED          = config.get('main','processed')
  C_SUBFOLDERS         = config.get('main', 'subfolders').split(',')
  C_DEBUG              = config.getboolean('main','debug')

# stage one render all the htm files into html files
for folder in [C_HTMLPATH] + C_SUBFOLDERS:
  if C_DEBUG: print folder
  for filename in glob.glob( folder + "/*." + C_UNPROCESSED):
    if C_DEBUG: print(filename)
    data = {'content': unicode(file( filename ).read(), "utf-8", errors="ignore")}
    with open( filename + "l" , "w") as f:
      f.write(  pystache.render( C_TEMPLATE, data ) )

  #os.unlink( item['path'] )


# stage 2, create an index of all the html files
postIndex = []
for filename in glob.glob( C_HTMLPATH + "/*." + C_PROCESSED):
  postIndex.append( {
    'baseName': os.path.basename(filename),
    'title': " ".join( os.path.basename(filename).split('.')[0].split('-')[3:] ),
    'postDate': time.strptime( "%s %s %s" %  tuple(os.path.basename(filename).split('-')[0:3]), "%Y %m %d")
  })

# stage 3 create the post list
postData = "<table class=postList>"
for post in sorted(postIndex, key=lambda p: p['postDate'], reverse=True):
  postData += "<tr class=post>"
  postData += "<td class=postDate>" + time.strftime("%Y &bull; %m &bull; %d", post['postDate']) + "</td>"
  postData += "<td class=postTitle><a href=./html/" + post['baseName'] + ">" + post['title'] + "</a></td>"
  postData += "</tr>"
postData += "</table>"

# stage 4 print out the index.html
with open('index.html', "w") as f:
  f.write( pystache.render(C_INDEXTEMPLATE, {'content': postData}))
