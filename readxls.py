# -*- coding: utf-8 -*- 
import xdrlib
import sys
import xlrd
import types
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')

#def Mysql_conn:
db=MySQLdb.connect(passwd="auto_insure123654",db="auto_insure",user="auto_insure")
c=db.cursor()
def open_excel(file= '2014-01.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= '2014-01.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    #print type(colnames)
    #for i in colnames:
#print i 
    list =[]
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
#print row[i] 
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= '2014-01.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
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

def main():
   tables = excel_table_byindex()
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
       #print runsql
       c.execute(runsql)
       sql=""
   #print sqllst     
   #print sqlstr
#print value
#print row
        #vallst=list(row)
        #for i,val in enumerate(vallst):
#print i,val
       #print vallst
       #for i,v in vallst:
#print i
#print v
       #for d in row:
#print d
#print row[index]


#dxsj=row[0]
#pp=row[1]
#print dxsj
#print pp
       #print row

'''   tables = excel_table_byname()
   for row in tables:
       print row
'''

if __name__=="__main__":
    main()
