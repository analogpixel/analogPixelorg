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

# for each page in the path, render it with the correct template
def renderPages(path, C_TEMPLATE, C_UNPROCESSED  ):
  for filename in glob.glob( path + "/*." + C_UNPROCESSED):
    data = {'content': unicode(file( filename ).read(), "utf-8", errors="ignore")}
    with open( filename + "l" , "w") as f:
      f.write(  pystache.render( C_TEMPLATE, data ) )

def createDateIndex(C_HTMLPATH, C_PROCESSED):
  postIndex = []
  for filename in glob.glob( C_HTMLPATH + "/*." + C_PROCESSED):
    print filename
    postIndex.append( {
      'baseName': os.path.basename(filename),
      'title': " ".join( os.path.basename(filename).split('.')[0].split('-')[3:] ),
      'postDate': time.strptime( "%s %s %s" %  tuple(os.path.basename(filename).split('-')[0:3]), "%Y %m %d")
    })
  return postIndex

def htmlDateIndex(postIndex):
  postData = "<table class=postList>"
  for post in sorted(postIndex, key=lambda p: p['postDate'], reverse=True):
    postData += "<tr class=post>"
    postData += "<td class=postDate>" + time.strftime("%Y &bull; %m &bull; %d", post['postDate']) + "</td>"
    postData += "<td class=postTitle><a href=./html/" + post['baseName'] + ">" + post['title'] + "</a></td>"
    postData += "</tr>"
  postData += "</table>"
  return postData

# render all the pages
if os.path.isfile("makeindex.cfg"):
  config.read('makeindex.cfg')

  C_DEBUG         = config.getboolean('main','debug')
  C_INDEXTEMPLATE = config.get('main', 'indextemplate')
  C_UNPROCESSED   = config.get('main','unprocessed')
  C_PROCESSED     = config.get('main','processed')

  # render all html files to give them a header and footer and style
  for section in config.sections():
    if section != "main":
      C_TEMPLATE = open( config.get(section,'template')).read()
      C_PATH = config.get(section,'htmlPath')
      renderPages( C_PATH , C_TEMPLATE, C_UNPROCESSED)

    if section == "index":
      C_INDEX = open( config.get('main','indextemplate')).read()
      index = createDateIndex( C_PATH , C_PROCESSED)
      html = htmlDateIndex(index)

      with open('index.html', "w") as f:
        f.write( pystache.render(C_INDEX, {'content': html}))
