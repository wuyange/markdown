# os模块

[os --- 多种操作系统接口 — Python 3.8.12 文档](https://docs.python.org/zh-cn/3.8/library/os.html#module-os)

[os.path --- 常用路径操作 — Python 3.10.0 文档](https://docs.python.org/zh-cn/3/library/os.path.html#module-os.path)

```python
import os    #导入os模块

os.sep    #获取系统的路径分隔符 windows是'\\'，linux是'/'
Out[106]: '\\'

os.name   #获取操作系统，windows是'nt',linux是'posix'

os.getcwd()    #获取当前的工作路径
Out[55]: 'D:\\python_work\\iSource_2.5'

os.listdir() #传入任意一个path路径，返回的是该路径下所有文件和目录组成的列表，不传参则为当前工作路径
Out[56]: ['.idea', 'logmanage', 'systemsetup']
os.listdir('D:\\python_work\\')
Out[57]: 
['.idea',
 '163mail_pytest',
 '163mail_pytest.zip',
 '163_mail_test_project']
 
os.makdir(ptah)  #生成一个空文件夹
os.mkdir('xxx1')
os.listdir()
Out[112]: ['.idea', 'logmanage', 'systemsetup', 'xx', 'xxx1']
os.mkdir(os.getcwd()+os.sep+'111')
os.listdir()
Out[115]: ['.idea', '111', 'logmanage', 'systemsetup', 'xx', 'xxx1']

os.makedirs(path)  #递归的创建文件夹
os.makedirs('555\\123')
os.listdir()
Out[117]: ['.idea', '111', '555', 'logmanage', 'systemsetup', 'xx', 'xxx1']
os.listdir('555')
Out[118]: ['123']

os.rmdir(path)   #删除一个空目录
os.removedirs(path)  #递归的删除空目录

os.chdir(path)   #切换到指定目录

os.rename(oldname,newname)   #重命名文件
os.renames('111','222')
os.listdir()
Out[120]: ['.idea', '222', '555', 'logmanage', 'systemsetup', 'xx', 'xxx1']

os.remove(path)   #删除文件
os.walk(path)     #传入任意一个path路径，深层次遍历指定路径下的所有子文件夹，返回的是一个由路径、文件夹列表、文件列表组成的元组生成器
for path,dirs,files in os.walk(os.getcwd()):
    print(path)
    print(dirs)
    print(files)
    for file in files:
        os.remove(path+os.sep+file)    	 
    
D:\python_work\iSource_2.5
['.idea', '222', '555', 'logmanage', 'systemsetup', 'xx', 'xxx1']
[]
D:\python_work\iSource_2.5\.idea
['inspectionProfiles']
['.gitignore', 'encodings.xml', 'iSource_2.5.iml', 'misc.xml', 'modules.xml', 'workspace.xml']

os.stat(path/filename) #获取文件/目录信息
os.stat('systemsetup')
Out[134]: os.stat_result(st_mode=16895, st_ino=562949953470458, st_dev=1547705744, st_nlink=1, st_uid=0,
 st_gid=0, st_size=4096, st_atime=1638414500, st_mtime=1638414078, st_ctime=1634266768)
 
os.system(command)   #运行shell命令
os.system('pwd')

os.path.exists(path)   #判断文件或者目录是否存在
os.path.isfile(path)   #判断是否为文件
os.path.isdir(path)    #判断是否为目录

os.path.abspath(path)  #返回绝对路径
os.path.abspath('xx')
Out[142]: 'D:\\python_work\\iSource_2.5\\xx'

os.path.getsize(path)  #返回path的大小，如果path是目录则返回0
os.path.getsize('xx')
Out[143]: 0
os.path.getsize(r'D:\python_work\iSource_2.5\systemsetup\hst\templates\project\scripts' + '\\test_script.py')
Out[145]: 2227

os.path.split(path)    #将path拆分为目录和文件名
os.path.split(os.getcwd())
Out[160]: ('D:\\python_work', 'iSource_2.5')

os.path.join(path, *paths)       #智能地拼接一个或多个路径
os.path.join('asd','bbb','ccc')
Out[161]: 'asd\\bbb\\ccc'
#当其中的路径参数有一个为绝对路径时，只有绝对路径以及其后的参数生效
os.path.join('xxx',os.getcwd(),'asd')
Out[162]: 'D:\\python_work\\iSource_2.5\\asd'

os.path.split()    #将路径的后缀拆分出来
os.path.splitext(os.getcwd() + os.sep + 'asd.json')
Out[167]: ('D:\\python_work\\iSource_2.5\\asd', '.json')

os.path.getatime(path)   #返回path的最后访问时间
os.path.getctime(path)   #返回path的最后创建时间
os.path.getmtime(path)   #返回path的最后修改时间  
```

