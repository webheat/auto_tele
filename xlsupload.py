#!/usr/bin/env python 
# -*- coding: UTF-8 -*- 
import tornado.ioloop 
import tornado.web 
import tornado.autoreload
import os,sys
settings = {'debug':True}
path ='/data/web/auto_insure/upfile'
filenames=os.listdir(path)

for a in xrange(len(filenames)):
    os.renames(path + os.sep + filenames[a],path + os.sep + str(a)+'.bak') 
class UploadFileHandler(tornado.web.RequestHandler): 
    def get(self): 
     self.write(''' 
     <html> <head><title>Upload File</title></head>
     <body> <form action='file' enctype="multipart/form-data" method='post'> 
     <input type='file' name='upfile'/><br/> <input type='submit' value='submit'/> </form> 
     </body> </html> ''') 
    def post(self): 
        #文件的暂存路径 
        upload_path=os.path.join(os.path.dirname(__file__),'upfile') 
	print upload_path
        #提取表单中‘name’为‘file’的文件元数据 
        file_metas=self.request.files['upfile'] 
        for meta in file_metas: 
          filename=meta['filename'] 
          filepath=os.path.join(upload_path,filename) 
          #有些文件需要已二进制的形式存储，实际中可以更改 
          with open(filepath,'wb') as up: 
	  	up.write(meta['body']) 
          self.write('finished!') 
#app=tornado.web.Application([ (r'/file',UploadFileHandler), ]) 
class MainHandler(tornado.web.RequestHandler):
	def get(self):
	     self.write('''
     		<html> <head><title>Upload File</title></head>
    		 <body>
		welcome to auto_insure query system click <a href="./file> here </a> for upload the excel file 
     </body> </html> ''')
app=tornado.web.Application([ 
	(r'/file',UploadFileHandler),
	(r'/',MainHandler),
   ],**settings) 


#if __name__ == '__main__': 
#     app.listen(7088) 
#     tornado.ioloop.IOLoop.instance().start()
def main():
	server=tornado.httpserver.HTTPServer(app)
	server.listen(7088)
	tornado.ioloop.IOLoop.instance().start()
