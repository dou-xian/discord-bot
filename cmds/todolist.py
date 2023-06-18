import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class TodoList(Cog_Extension):
    # Initialization 
    def __init__(self, bot):
        self.todo = []

        '''
        todo 是一個 list 變數
        你可以在各個function中對self.todo做操作
        來當作模擬todolist

        你可能需要用到的function 
        list : append, remove, sort
        ctx.send(str)

        '''
    
    # Add todolist 
    # item 是要增加的待辨事項
    @commands.command()
    async def AddTodoList(self, ctx, item):
        if item in self.todo:
            await ctx.send("待辦事項已存在")
        else:
            self.todo.append(item)
            await ctx.send("已加入")

    # Remove todolist
    # item 是要移除的待辨事項
    @commands.command()
    async def RemoveTodoList(self, ctx, item):
        if item in self.todo:
            self.todo.remove(item)
            await ctx.send("已刪除")
        else:
            await ctx.send("此待辨事項不存在")

    # Sort todolist
    @commands.command()
    async def SortTodoList(self, ctx):
        self.todo.sort()
        for i in self.todo:
            await ctx.send(i)

    # Clear todolist
    @commands.command()
    async def ClearTodoList(self, ctx):
       self.todo.clear()
       await ctx.send("已清除所有待辦事項") 

async def setup(bot):
    await bot.add_cog(TodoList(bot))