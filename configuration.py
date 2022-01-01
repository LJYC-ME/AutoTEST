'''系统配置文件'''
import re
import hashlib

APP_MODE = "DEBUG" #NORMAL:正常模式 DEBUG:检测题库错误
APP_TITILE = "马原期末题库"
APP_OPT_SAVE_AUTO = True #是否自动生成错题集和收藏(防止忘记手动导出)
APP_OPT_SAVE_MARKDOWN = True #是否额外生成Markdown错题集

FILE_PATH = r'./resource/Mayuan单选.txt'# 题库文件目录
FILE_CODER = "UTF-8"# 文件编码类型（可以改用chardet库自动推测优化）

HASH = hashlib.md5()# 文件ID生成方法（不建议修改）

class Pattern():
    '''
    题目的匹配规则
    1.采用正则表达式，使用match方法从头匹配
    2.按顺序匹配，在没有找到下一个匹配规则之前，所有内容将归纳到当前匹配对象内
    3.匹配之后的操作需要按需求设计
    '''
    def __init__(self):
        #章节的匹配规则
        self.Chapter = r'# '
        #选择题对象最基本的三要素（1.题目 2.选项 3.回答）
        self.Question = r'\d+\.'#题目的匹配规则
        self.Option = r'[AaBbCcDd]|.[AaBbCcDd].' #选项的匹配规则
        self.Anwser = r'答案：' #答案的匹配规则
    
    def match(self,content):
        '''将内容与所有匹配项进行匹配，返回最终匹配结果，结果包括C,Q,O,A,None分别代表章节、问题、选项、答案、匹配失败'''
        if re.match(pattern.Chapter,content): return 'C'
        elif re.match(pattern.Question,content): return 'Q'
        elif re.match(pattern.Option,content): return 'O'
        elif re.match(pattern.Anwser,content): return 'A'
        else: return None

pattern = Pattern() #singleton

class Prompt():
    '''各种提示信息'''
    def __init__(self):
        self.INPUT = "你的选择是（直接Enter跳过此题）:"
        self.OUTPUT_RIGHT = "回答正确"
        self.OUTPUT_WRONG = "回答错误"
        self.NEXT = "(输入e退出，否则进入下一题，如果输入为s会将此题加入收藏夹)"

prompt = Prompt()#singleton

if __name__ == "__main__":
    #单元测试，通过以下几项基本测试后，题库理论可以正常运行
    print(re.match(pattern.Chapter,r"# 第一章"))    #章节匹配
    print(re.match(pattern.Question,r"22.细胞学"))  #问题匹配
    print(re.match(pattern.Option,r"(D) 掌握理论")) #选项匹配
    print(re.match(pattern.Anwser,r"答案："))       #答案匹配
    #print(re.match(r".*ABC",r"答案：ABC"))#测试作答（一般不需要测试，默认是N个任意字符前缀+答案）