'''
可以複製todolist的架構, 但請記得更改class & function的名稱
這個檔案的名字也可以改
'''

import discord
from discord.ext import commands
from core import Cog_Extension
import random

class Diction(Cog_Extension): #不同語言間的語詞對照表，又稱「字典」
    def __init__(self, bot):
        self.language1 = []#第一種語言所有語詞對照的list
        self.language2 = []#第二種語言所有語詞對照的list
        self.part_of_speech = []#語詞的詞性

    @commands.command()
    async def AddVocab(self, ctx, item):#輸入樣式：$AddVocab 第一種語言;詞性;第二種語言
        try:
            lan1, pos, lan2 = str(item).split(";")
        except:
            await ctx.send("語法：`$AddVocab 第一種語言;詞性;第二種語言`")
            return
        if (lan1 in self.language1) or (lan2 in self.language2):#單字重複
            await ctx.send("此字詞已收錄於字典了，請換別的吧。")
            return
        self.language1.append(lan1)
        self.part_of_speech.append(pos)
        self.language2.append(lan2)
        await ctx.send("字典收錄成功！")
    
    @commands.command()
    async def ViewVocab(self, ctx):
        for i in range(len(self.language1)):
            await ctx.send(self.language1[i] + " 詞性:" + self.part_of_speech[i] + " 解釋:" + self.language2[i])
        return
  
    @commands.command()
    async def Test(self, ctx, selection):#selection即為題目之出題語言，1表示第一個語言，2表示第二個語言，其餘皆為錯誤語法
        try: select = int(selection)
        except: await ctx.send("語法：`$Test 數字`，數字只能為1或2")
        if select != 1 and select != 2:
            await ctx.send("請在$Test指令後方輸入1或2，選擇出題語言，並用空格格開")
            return
        num = random.randint(0,len(self.language1)-1)
        if select == 1:
            question = self.language1[num]
            self.pos = self.part_of_speech[num]
            self.ans = self.language2[num]
        elif select == 2:
            question = self.language2[num]
            self.pos = self.part_of_speech[num]
            self.ans = self.language1[num]
        else:
            await ctx.send("發生未知錯誤，請重試")
            return
        self.answer_situation = False
        await ctx.send(f"你選擇的題目語言為第{select}種語言，請輸入{question}對應語言的語詞")
        return

    @commands.command()
    async def Hint(self, ctx):
        if self.answer_situation == False:
            await ctx.send(f"是不是太難了，提示：詞性為{self.pos}，祝好運！")
            return
        else:
            await ctx.send("請先使用`$Test`指令後再使用`$Hint`指令!")
            return

    @commands.command()
    async def Answer(self, ctx, ans):
        answer = str(ans)
        if self.answer_situation == False:
            if answer == self.ans:
                await ctx.send("恭喜答對！")
            else: 
                if self.ans.lower() == ans.lower():
                    await ctx.send("請注意大小寫！再給你一次機會！")
                    return
                else:
                    await ctx.send(f"很可惜你答錯了！正確答案是：{self.ans}！")
        self.answer_situation = True
        await ctx.send("請記得重新使用`$Test`指令產生問題後，再使用`$Answer`回答問題或`$Hint`取得詞性提示")
        return

async def setup(bot):
    await bot.add_cog(Diction(bot))