#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sphinxapi import *
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload
import os,sys
import MySQLdb
import xlrd
import types
reload(sys)
sys.setdefaultencoding('utf8')

#def Mysql_conn:
db=MySQLdb.connect(passwd="auto_insure123654",db="auto_insure",user="auto_insure")
c=db.cursor()

settings = {'debug':True}
path ='/data/web/auto_insure/upfile'
filenames=os.listdir(path)

for a in xrange(len(filenames)):
    os.renames(path + os.sep + filenames[a],path + os.sep + str(a)+'.bak')

def open_excel(file= '2014-01.xls'):
            try:    
                data = xlrd.open_workbook(file)
		print "xlrd data"
		print data
                return data
            except Exception,e:
                print str(e)





class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
     self.write('''
     <html> <head><title>Upload File</title></head>
     <body> <form action='upload' enctype="multipart/form-data" method='post'>
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
          self.write('finished!     click <a href="./dbimport">Import system</a>begin import the excel data          click <a href="./">home</a>back to the home')
class MainHandler(tornado.web.RequestHandler):
        def get(self):
             self.write('''
                <html> <head><title>Upload File</title></head>
                 <body>
                welcome to auto_insure query system click <a href="./upload"> here </a> for upload the excel file
     </body> </html> ''')
class dbimportHandler(tornado.web.RequestHandler):
        #def get(self):
	'''def open_excel(file= '2014-01.xls'):
	    try:
        	data = xlrd.open_workbook(file)
	        return data
	    except Exception,e:
        	print str(e)
        '''
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
	def excel_table_byindex(file= '2014-01.xls',colnameindex=0,by_index=0):
	    print "calling excel_table_byindex"
	    #data = open_excel(file)
	    data = open_excel(file='2014-01.xls')
            print "date info"
	    print data
	    table = data.sheets()[by_index]
	    nrows = table.nrows #行数
	    ncols = table.ncols #列数
	    colnames =  table.row_values(colnameindex) #某一行数据
	    list =[]
	    for rownum in range(1,nrows):
        	 row = table.row_values(rownum)
	         if row:
        	     app = {}
	             for i in range(len(colnames)):
        	        app[colnames[i]] = row[i]
             	     list.append(app)
	    return list

	#def main():
	def get(self):
	   tables = self.excel_table_byindex()
	   print type(tables)
	   #sql="insert into auto_insure_baseinfo(dxsj,pp,cx,cp,cjh,fdjh,xm,sjh,dz)values('%s','%s','%s')"%(game_url,res_url,ip)
	   sql="insert into auto_insure_baseinfo(sjh,pp,dxsj,dz,fdjh,xm,cjh,cx,cp)values('"
	   sqllst=[]
	   sqlstr=""
	   #c.execute("set autocomit=0")
	   for row in tables:
       		#print type(row)  # dict
		#for key,value in row.items():
	       sqlstr_tmp=""
	       sql="insert into auto_insure_baseinfo(sjh,pp,dxsj,dz,fdjh,xm,cjh,cx,cp)values("
	       for key,value in row.iteritems():
        	#print value
	        sqlstr_tmp+="'"+str(value)+"',"
        	#sqlstr_tmp+="'"+value+"',"  cannot concatenate 'str' and 'float' objects
	        #print sqlstr_tmp
	        sqlstr=sqlstr_tmp
	        #sql=sql+sqlstr
	        #sql=sql+sqlstr
	        #sqlstr_tmp=""
	        #sqllst.append(value)
	       sql=sql+sqlstr
	       #print sqlstr
	       reallen=len(sql)-1
               runsql=sql[0:reallen]+")"
	       print runsql+"<br>"
	       c.execute(runsql)
	       sql=""


setting={
        "debug":True
        }
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadFileHandler),
    (r"/dbimport", dbimportHandler),
],**setting)

http_server=tornado.httpserver.HTTPServer(application)
http_server.listen(8008)
print "server update"
loop=tornado.ioloop.IOLoop.instance()
tornado.autoreload.start(loop)
loop.start()
