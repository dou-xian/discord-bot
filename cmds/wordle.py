import discord
from discord.ext import commands
import json 
from core import Cog_Extension
import urllib
import random



class Wordle(Cog_Extension):
    # Initialization 
    def __init__(self, bot):
        self.wordbank = []
        
        '''
        TODO 
        要在init function 中載入單字庫

        Hint:
        1. 好像有import urllib
        2. data.json中有貼上url了
        '''
        url = "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt"
        with urllib.request.urlopen(url) as response:
            html = response.readlines()
        for i in html:
            word = str(i)
            self.wordbank.append(word[2:7])
        self.play = False

    @commands.command()
    async def Play(self, ctx):

        '''
        TODO 
        要在爬好的單字庫中, 隨機挑選一個單字做為預設的答案
        '''
        wordAmount = len(self.wordbank)
        a = random.randint(0, (wordAmount-1))
        self.chooseWord = self.wordbank[a]
        print(self.chooseWord)
        await ctx.send("來吧，準備好了嗎？")
        self.play = True
        self.playtimes = 0
    

    
    @commands.command()
    async def Ask(self, ctx, ans):
        anslower = ans.lower()
        '''
        ans 是使用者傳入的猜測答案

        TODO
        1. 沒有play直接ask : 請先輸入 Play 指令
        2. 不是5個字的單字 : 請輸入5個字母的單字
        3. 不是單字的英文組合(不在單字庫中) : 這好像不是個單字
        4. 答對 : 恭喜答對!!!
        5. 猜太多次了 : 真可惜, 答案是{answer}
        '''
        def GetWordleResult (answer, guess):#大寫代表字母位置完全正確，小寫代表字母正確位置錯誤，#代表字母錯誤
            response = ['#', '#', '#', '#', '#']
            for i in range(5):
                if guess[i] == answer[i]:
                    response[i] = guess[i].upper()
                elif guess[i] in answer:
                    if guess[0:i+1].count(guess[i]) > answer.count(guess[i]):#處理字母重複的問題
                        #guess已經有對應到answer的字母，但guess又出現相同字母，故視為字母錯誤
                        #例：輸入apple，解答pines，只能輸出一個'p'，故應為'#p##e'，第二個p會視為錯誤(#)
                        pass
                    else:
                        response[i] = guess[i].lower()
            return response

        anslower = ans.lower()

        if self.play == False:#未打play指令
            await ctx.send("請先輸入 Play 指令")
            return
        else:
            if len(anslower) != 5:#輸入不為5個字母
                await ctx.send("請輸入5個字母的單字")
                return
            elif anslower not in self.wordbank:#輸入不是單字
                await ctx.send("這好像不是個單字")
                return

            result = GetWordleResult(self.chooseWord, anslower)
            allcorrect = True
            for i in result:
                if i.isupper():
                    pass
                else:
                    allcorrect = False

            if allcorrect == True:#答對，遊戲結束歸零
                await ctx.send("恭喜答對!!!")
                self.play = False
                self.playtimes = 0
            else:
                await ctx.send(result[0]+result[1]+result[2]+result[3]+result[4])

            self.playtimes += 1

            if self.playtimes >= 6:#猜六次，遊戲結束歸零
                await ctx.send(f'真可惜, 答案是{self.chooseWord}')
                self.play = False
                self.playtimes = 0


async def setup(bot):
    await bot.add_cog(Wordle(bot))