'''数据结构'''
from configuration import prompt,HASH
import re

class Problem():
    '''一个题目对象'''
    def __init__(self,question,options,answer,**_addition):
        '''由问题、选项、答案基本构成，其他信息需要以字典形式额外传入，默认将其他信息作为答案一部分'''
        self.question = question
        HASH.update(self.question.encode("UTF-8"))
        self.ID = HASH.hexdigest()
        self.options = options
        self.answer = answer
        self.addition = None
        if _addition:
            self.addition = _addition

    def info_original(self):
        '''返回原题信息，格式与读入时相同'''
        info = self.question+self.options+self.answer
        return info

    def info_markdown(self):
        '''返回原题信息，使用markdown格式'''
        info = '## '+self.question+self.options+self.answer+'\n'
        return info
    
    def test(self,dispAnswer = True):
        '''格式化地提问该问题并等待用户作答，默认作答后立即显示答案，返回值为作答是否正确'''
        print("[ID:{}]\n{}\n{}".format(self.ID,self.question,self.options))
        ans = input(prompt.INPUT).strip()
        if re.match(r".*"+ans,self.answer,re.IGNORECASE):#忽略大小写
            ans = True
            print(prompt.OUTPUT_RIGHT)
        else:
            ans = False 
            print(prompt.OUTPUT_WRONG)
        if dispAnswer: 
            print(self.answer)
            if self.addition:
                for k,v in self.addition.items():
                    print("{}:{}".format(k,v))
        return ans #交由上层处理结果     

    def show(self):
        '''格式化地显示完整问题，特殊显示需求建议在上层实现，最后转换为str类型即可'''
        print("[ID:{ID}]\n{Q}\n{O}\n{A}".format(ID=self.ID,Q=self.question,O=self.options,A=self.answer))
        if self.addition:
            for k,v in self.addition.items():
                print("{}:{}".format(k,v))

    def check(self,checkAddtion = False):
        '''用于检测题目完整性，默认不检测addition内容'''
        res = ""
        if not self.question:res += "题目内容为空\n"
        if not self.options:res += "题目选项为空\n"
        if not self.answer:res += "题目答案为空\n"
        if checkAddtion and not self.addition:res += "题目额外信息为空\n"
        return res
        