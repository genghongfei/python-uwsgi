# -*- coding:utf8 -*-
import os
import io
#判断变量是否存在
def isset(obj):
    try:
        type(eval(obj))
    except:
        return False
    return True
class Template(object):
    # black notag foreach if
    # func include
    # modify
    #
    def __init__(self,root):
        self.vars = {}
        self.root = root
        self.left = '{'
        self.right = '}'
        self.call_func = {'include' : self.func_include,'if' : self.func_if,'else' : self.func_else,'elif' : self.func_elif}
        self.buffer = io.StringIO()
        self.tab = '    '
        self.tabIndex = 0
        self.files = []
    # 注册块Tag标签
    def reg_black(self,tag,func,funcType = 'func'):
        if tag not in self.call_func.keys():
            self.call_func[tag] = {'func' : func,'type' : funcType}
        else:
            # @todo 是否可以抛出异常
            pass
    def func_foreach(self):
        pass
    def func_if(self,params):
        self.write("if %s:" % (params))
        self.tabIndex += 1
        pass
    def func_elif(self,params):
        self.tabIndex -= 1
        self.write("elif %s:" %(params))
        self.tabIndex += 1
    def func_else(self,params):
        self.tabIndex -= 1
        self.write("else:")
        self.tabIndex += 1
    def func_include(self,params):
        if 'file' in params.keys():
            self.parseTemp(self.readFile(params['file']))
    def echo(self,nameName):
        nameName = nameName[1:]
        self.write("if isset('%s'):" %(nameName))
        self.tabIndex += 1
        self.write("out.write(%s)" % (nameName))
        self.tabIndex -= 1
    # 设置变量到
    def set(self,name,val):
        self.vars[name] = val
    # 展示内容
    def fetch(self,templateFile,vars = {}):
        for name in vars.keys():
            self.set(name,vars[name])
        self.parseTemp(self.readFile(templateFile),True)
        #self.write("print(out.getvalue())")
        #print(self.buffer.getvalue())
        if self.tabIndex > 0:
            raise Exception
        code = compile(self.buffer.getvalue(),'','exec')
        ret = {}
        exec(code,self.vars,ret)
        print(ret['out'].getvalue())
    # 解析数据内容
    def parseTemp(self,contents,isFrist = False):
        if isFrist:
            self.write("import io")
            self.write("out = io.StringIO()")
            self.write('''def isset(obj):
    try:
        type(eval(obj))
    except:
        return False
    return True''')
        index = contents.find(self.left)
        while index != -1:
            self.write(contents[0:index],True)
            contents = contents[index+1:]
            end = contents.find(self.right)
            tagContent = contents[:end]
            contents = contents[end + 1:]
            if tagContent == 'notag':
                end = contents.find('{/notag}')
                self.write(contents[:end],True)
                contents = contents[end+len('{/notag}'):]
                break
            self.parseTag(tagContent)
            index = contents.find(self.left)
        self.write(contents,True)
    def parseTag(self,tagContent):
        if tagContent[0] == '$':
            self.echo(tagContent)
        elif tagContent[0] == '/':
            self.tabIndex -= 1
        else:
            args = tagContent.split(" ")
            tag = args[0]
            params = {}
            if tagContent.find('=') != -1:
                if len(args) > 1:
                    for item in args:
                        kv = item.split("=")
                        if len(kv) == 2:
                            params[kv[0]] = kv[1].strip('"\'')
            else:
                params = tagContent.replace(tag + " ",'')
            if tag in self.call_func.keys():
                self.call_func[tag](params)

    def write(self,data,isText = False):
        msg = ""
        if isText:
            msg = "%sout.write('''%s''')\n" % (self.tab * self.tabIndex, data)
        else:
            msg = "%s%s\n" %(self.tab*self.tabIndex ,data)
        self.buffer.write(msg)
    # 读取文件内容，一次读取全部的内容
    def readFile(self,fileName):
        path = self.root +"/"+fileName
        if os.path.exists(path):
            self.files.append(path)
            f = open(path)
            ret = f.read()
            f.close()
            return ret
        raise FileNotFoundError
def test():
    tp = Template("View")
    tp.set('title',"测试")
    tp.set('list',[1,2,3,4,5])
    tp.set('dict',{"a" : '1',"b" : 2})
    tp.fetch("test.html")
    #print()

test()