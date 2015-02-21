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


# stage one render all the htm files into html files
for filename in glob.glob( C_HTMLPATH + "/*." + C_UNPROCESSED):
  data = {'content': file( filename ).read() }
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
postData = ""
for post in sorted(postIndex, key=lambda p: p['postDate'], reverse=True):
  postData += "<div class=post>"
  postData += "<div class=postTitle>" + post['title'] + "</div>"
  postData += "<div class=postDate>" + post['date'] + "</div>"
  postData += "</div>"

print postData, postIndex

# stage 4 print out the index.html
with open('index.html', "w") as f:
  f.write( pystache.render(C_INDEXTEMPLATE, {'content': postData}))
