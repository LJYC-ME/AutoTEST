'''题库的核心解释模块'''

import sys
import objects
import datetime #datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
from configuration import *
import os
from random import shuffle

class Application():
    '''复习软件'''
    def __init__(self):
        # 题库文件
        self.Qlibrary = {} # 题库{章节A:list(题目对象),章节B:...}
        self.Qerror = [] # 错题集
        self.Qfavorites = [] # 收藏的问题（蒙对了之类的）
        # 用户信息
        self.user = "Frozen"
        # 应用状态
        self.running = True

    def __del__(self):    
        print("Goodbye {} !".format(self.user))

    def init(self):
        '''初始化应用'''
        print("当前模式",APP_MODE)
        self.load()# 载入文件并生成题库
        if APP_MODE == "DEBUG":
            print("正在进行题库完整性检验")
            self.check_library()
        
    def start(self):
        '''启动应用'''
        self.init()#初始化
        #用户登录（未做）
        while self.running:#应用主循环
            self.menu()
        self.exit()

    def exit(self):
        '''退出应用'''
        if APP_OPT_SAVE_AUTO:
            self.save()
            print("已自动导出当前的错题和收藏")

    def menu(self):
        '''菜单'''
        print("\n{}\n".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        print(APP_TITILE)
        print("1.正序单元测验")
        print("2.乱序单元测验")
        print("3.乱序全库测验")
        print("A.导出错题+收藏（保存后会清空内存记录）")
        print("Others:Exit")
        op = self.user_input()
        if op == '1':
            self.test_unit()
        elif op == '2':
            self.test_unit(_random=True)
        elif op == '3':
            self.test_random()
        elif op == 'A':
            self.save()
        else: self.running = False

    def save(self):
        '''分别保存错题集和收藏，时间有限不检测异常了'''
        T = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        if self.Qerror:#如果有错题
            path_errors = './datas/ERRORS-' + T
            fp_e = open(path_errors + '.txt','w')
            fp_e.write(pattern.Chapter+'错题集-'+T+'\n')
            if APP_OPT_SAVE_MARKDOWN:#如果需要额外生成Markdown格式
                fp_e_m = open(path_errors + '.md','w') 
                fp_e_m.write('# 错题集-'+T+'\n')
            for e in self.Qerror:
                fp_e.write(e.info_original())
                if APP_OPT_SAVE_MARKDOWN:
                    fp_e_m.write(e.info_markdown())
            if APP_OPT_SAVE_MARKDOWN:fp_e_m.close()
            print("错题保存在:{}".format(os.path.abspath('./datas')))
            fp_e.close()
        else:
            print("当前没有错题")
        if self.Qfavorites:#如果有收藏
            path_favor = './datas/FAVOR-' + T
            fp_f = open(path_favor + '.txt','w')
            fp_f.write(pattern.Chapter+'收藏-'+T+'\n')
            if APP_OPT_SAVE_MARKDOWN:#如果需要额外生成Markdown格式
                fp_f_m = open(path_favor + '.md','w') 
                fp_f_m.write('# 收藏-'+T+'\n')
            for f in self.Qfavorites:
                fp_f.write(f.info_original())
                if APP_OPT_SAVE_MARKDOWN:
                    fp_f_m.write(f.info_markdown())
            if APP_OPT_SAVE_MARKDOWN:fp_f_m.close()
            print("收藏题保存在:{}".format(os.path.abspath('./datas')))
            fp_f.close()
        else:
            print("当前没有收藏题")
        self.Qerror.clear()
        self.Qfavorites.clear()

    def test_unit(self,_random=False):
        '''单元检测（通过修改参数可以乱序测试）'''
        while True:
            print("--------请选择测试单元序号--------")
            cnt = ord('A')
            for chapter,quetions in self.Qlibrary.items():
                print("({}):{}题目数量:{}".format(chr(cnt),chapter,len(quetions)))
                cnt += 1
            print("[Others:Exit]")
            op = self.user_input().upper()
            if op: op=op[0]
            if  not 'A'<=op<chr(cnt):
                print(">>[退出或序号超出范围]")
                break
            else:
                op = ord(op)-ord('A')
                cnt = 0
                for chapter,quetions in self.Qlibrary.items():
                    if cnt == op:
                        qsum = len(quetions)
                        asum = 1
                        cnt_right = 0
                        questionS = quetions[:]
                        if _random : shuffle(questionS)
                        for q in questionS:
                            ratio_right = 0.0
                            if asum > 1:
                                ratio_right = cnt_right*100/(asum-1)
                            print("\n测试进度：{}/{} [{:.1f}%] 当前正确率：{}/{} [{:.1f}%]\n".
                                format(asum,qsum,asum*100/qsum,cnt_right,asum-1,ratio_right))
                            right = q.test()
                            if right: cnt_right += 1#统计正确率
                            else:
                                self.Qerror.append(q)#将错题加入错题集
                            asum += 1
                            #数据统计
                            #Haimeizuo
                            ans = input(prompt.NEXT).strip()
                            if ans == 'e':
                                return
                            elif ans == 's':
                                self.Qfavorites.append(q) #加入收藏夹
                        break
                    cnt += 1       

    def test_random(self):
        '''乱序检测'''
        questions = []
        for qlist in self.Qlibrary.values():
            for q in qlist:
                questions.append(q)
        shuffle(questions)
        qsum = len(questions)
        asum = 1
        cnt_right = 0
        for q in questions:
            ratio_right = 0.0
            if asum > 1:
                ratio_right = cnt_right*100/(asum-1)
            print("\n测试进度：{}/{} [{:.1f}%] 当前正确率：{}/{} [{:.1f}%]\n".
                format(asum,qsum,asum*100/qsum,cnt_right,asum-1,ratio_right))
            right = q.test()
            if right: cnt_right += 1#统计正确率
            else:
                self.Qerror.append(q)#将错题加入错题集
            asum += 1
            #数据统计
            #Haimeizuo
            ans = input(prompt.NEXT).strip()
            if ans == 'e':
                return
            elif ans == 's':
                self.Qfavorites.append(q) #加入收藏夹


    def user_input(self):
        return input("[{}]>>".format(self.user)).strip()
         
    def load(self):
        '''读入题库文件'''
        with open(FILE_PATH,'r',encoding=FILE_CODER) as fp:
            if not fp:
                print("{}:题库文件加载失败".format(__class__))
                sys.exit(-1)
            content = fp.readlines()
            self.parser(content)#对内容解析，生成Qlibrary

    def parser(self,content):
        '''根据configuration配置，解析题库文件'''
        chapter = ""#当前章节
        question = ""
        options = ""
        answer = ""
        currentType = None#当前处理的数据类型，应为是readlines所以可能面临不匹配的情况
        for line in content:
            if line.isspace(): continue
            #print(type(line))#是str类型
            category = pattern.match(line) 
            if category == 'C':#新的章节
                currentType = category
                chapter = line
                self.Qlibrary[chapter]=[] #初始化该章节
            elif category =='Q':#新的问题
                currentType = category
                if question:#如果不是第一个问题则加载到题库
                    self.Qlibrary[chapter].append(objects.Problem(question,options,answer))
                question = line#初始化一个新问题
                options = ""
                answer = ""
            elif category == 'O':#刚到选项
                currentType = category
                options += line #选项可能多行同时匹配，所用默认拼接
            elif category == 'A':#刚到答案
                currentType = category
                answer = line
            else:#无匹配的类型 
                if not currentType:
                    print("{}:未知的数据类型，请检查文件和匹配规则".format(__class__))
                    sys.exit(-1)
                if currentType == 'C':
                    chapter+=line
                elif currentType == 'Q':
                    question+=line    
                elif currentType == 'O':
                    options+=line   
                elif currentType == 'A':
                    answer+=line

    def show_library(self):
        '''输出题库（测试用）'''
        for chapter,questions in self.Qlibrary.items():
            print("{}".format(chapter))
            for q in questions:
                q.show()
        
    def check_library(self):
        '''检测题库题目完整性'''
        for chapter,questions in self.Qlibrary.items():
            num = 1
            for q in questions:
                res = q.check()
                if res:
                    print("{}{}:\n{}".format(chapter,num,res))
                num+=1

APP = Application() #singleton

if __name__ == "__main__":
    APP.init()