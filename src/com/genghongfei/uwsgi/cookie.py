# -*- coding:utf8 -*-
import time
# Cookie 设置相关
class Cookie:
    def __init__(self,cookiestr = ''):
        self.cookies = {}
        ks = cookiestr.split(";")
        for item in ks:
            item = item.strip()
            if item is not '':
                k,v = item.split("=")
                self.cookies[k] = v
        self.saveCookies = {}
    # 设置参数
    def setCookie(self,name,val,expire = None,path = None,domain = None,secure = False):
        data = "%s=%s;" % (name,val)
        if expire is not None:
            if expire is 0:
                data = "%s=deleted;" % (name)
                data += " expires=Thu, 01-Jan-1970 00:00:01 GMT;" %(path)
            else:
                data += " expires=%s; max-age=%d;" %(time.strftime("%a %d-%b-%Y %H:%M:%S GMT", time.gmtime(time.time() + expire)),expire )
        if path is not None:
            data += " path=%s;" %(path)
        if domain is not None:
            data += " domain=%s;" %(domain)
        if secure:
            data += " HttpOnly"
        self.saveCookies[name] = data
    # 获取Cookie信息
    def get(self,name,defval = ''):
        if name in self.cookies:
            return self.cookies[name]
        else:
            return defval
    # 设置的Cookie内容
    def getCookieStr(self):
        data = ""
        for k in self.saveCookies.keys():
            data += "Set-Cookie: %s\r\n" %(self.saveCookies[k])
        return data

# c = Cookie()
# c.setCookie("1","123")
# c.setCookie("12","123",3600)
# c.setCookie("13","123",3600,'/')
# c.setCookie("14","123",3600,'/','.baidu.com')
# c.setCookie("15","123",3600,'/','.baidu.com',True)
# print c.getCookieStr()