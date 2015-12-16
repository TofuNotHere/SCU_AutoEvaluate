#author: Chenshufu
#date:2015年12月15日15:32:02
from urllib import request, parse
from http import cookiejar
from html.parser import HTMLParser 

PJ_url = 'http://202.115.47.141/jxpgXsAction.do'

class ListName(HTMLParser):
    def __init__(self,opener):
        HTMLParser.__init__(self)
        self.opener = opener
        self.is_PJ = False
        self.val = ""
    def handle_starttag(self,tag,attrs):
        if tag == 'img':
            for (attr,value) in attrs:
                if attr == 'name':
                    self.val = value
                if attr == 'title':
                    if value == '评估':
                        self.is_PJ = True
                    if value == '查看':
                        s = self.val.split("#@")
                        print(s[4],"-",s[2], "--" ,"已评过")
                        self.is_PJ = False
                if self.is_PJ:
                	self.show()
                	self.autoPJ()
                	self.is_PJ = False
    def handle_endtag(self,tag):
        self.is_PJ= False
    def show(self):
    	s = self.val.split("#@")
    	format_ch = parse.urlencode([
				("wjbm" , s[0]),
				("bpr"  , s[1]),
				("bprm" , s[2]),
				("wjmc" , s[3]),
				("pgnrm", s[4]),
				("pgnr" , s[5]),
				("oper" , "wjShow")])
    	opener.open(PJ_url,format_ch.encode('gbk'))
    def autoPJ(self):
        s = self.val.split("#@")
        format = ""
        if(s[3] == '学评教'):
            print(s[4],"-",s[2], "--" ," ",end="");
            format_teacher = parse.urlencode([
            	('oper','wjpg'),
                ('wjbm', s[0]),
                ('bpr', s[1]),
                ('pgnr', s[5]),
                ('0000000005', '10_1'),
                ('0000000006', '10_1'),
                ('0000000007', '10_1'),
                ('0000000008', '10_1'),
                ('0000000009', '10_1'),
                ('0000000010', '10_1'),
                ('0000000035', '10_1'),
                ('zgpj','非常好的老师'.encode('gbk'))])
            format = format_teacher
        if(s[3] == '研究生助教'):
            print(s[4],"-助教-",s[2], "--" ," ",end="");
            format_stu = parse.urlencode([
            	('oper','wjpg'),
                ('wjbm', s[0]),
                ('bpr', s[1]),
                ('pgnr', s[5]),
                ('0000000028', '10_1'),
                ('0000000029', '10_1'),
                ('0000000030', '10_1'),
                ('0000000031', '10_1'),
                ('0000000032', '10_1'),
                ('0000000033', '10_1'),
                ('zgpj','非常好的老师'.encode('gbk'))])
            format = format_stu
        opener.open(PJ_url,format.encode('gbk'))
        print("完成")

username = input('学号:')
passwd = input('密码:')
print("Login...")
login_url = 'http://202.115.47.141/loginAction.do'
login_data = parse.urlencode([
    ('zjh', username),
    ('mm', passwd),
])
PJ_data = parse.urlencode([('oper','listWj'),
    ('pageSize', '300'),])

cookie = cookiejar.CookieJar()
opener=request.build_opener(request.HTTPCookieProcessor(cookie))
opener.addheaders = [
    ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    ,('Cache-Control','max-age=0')
    ,('Host','202.115.47.141')
    ,('Connection','keep-alive')
    ,('Origin', 'http://202.115.47.141')
    ,('DNT','1')
    ,('Content-Length','197')
    ,('Upgrade-Insecure-Requests','1')
    ,('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]

try:
        ht = opener.open(login_url,login_data.encode('gbk'))
        #print(ht.read().decode('gbk'))
        htmldoc = opener.open(PJ_url,PJ_data.encode('gbk'))
        parser = ListName(opener)
        parser.feed(htmldoc.read().decode('gbk'));
except:
        print('网络状况不佳。。。评教失败 ╮(╯▽╰)╭')
input('Press <enter> to exit!')
