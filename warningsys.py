import re
import discord
from discord import embeds
from discord.ext import commands
import json
import pymongo
from pymongo import MongoClient
from pymongo import collection

class WarningSysCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(823787908678942721)
    async def warn(self,ctx,  user: discord.Member = None, *,reason = None):
        cluster = MongoClient("")#FILL IN DETAILS HERE
        db = cluster["discord"]
        collection = db["warningsys"]
	count = warningsys.count_documents({})

        post = {"_id": count + 1, "username": f"{user.name}", "reason":f"{reason}", "warner": f"{ctx.author.name}"}

        channel_em = discord.Embed(title = "__Warned__", description = f"{ctx.author.mention} warned {user.mention}",colour=0xD22063)
        channel_em.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/OVwUO6DhoIc7Lcyfgp97l1jgmASpGt50KSW26J-MPnA/%3Fsize%3D128/https/cdn.discordapp.com/icons/819636321223442472/67da9cfec011b8c455097752e3f4e2b7.png")
        channel_em.add_field(name = "Reason", value = f"{reason}", inline=False)
        channel_em.add_field(name = "Warn ID", value = f"{number}", inline=False)

        if reason == None:
            await ctx.send("You **must** include a reason.")
        else:

            collection.insert_one(post)

            await ctx.message.delete()
            channel_em = await ctx.send(embed=channel_em)
            await user.send(f"**You have been warned**\nBy {ctx.author.name}\nFor {reason}")

    @commands.command()
    @commands.has_role(823787908678942721)
    async def warnings(self,ctx, user: discord.Member = None):
        cluster = MongoClient("")#FILL IN DETAILS HERE
        db = cluster["discord"]
        collection = db["warningsys"]

        results = collection.find({"username":f"{user.name}"})

        embed = discord.Embed(title = f"__Warnings for {user.name}__",colour=0xD22063)
        embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/OVwUO6DhoIc7Lcyfgp97l1jgmASpGt50KSW26J-MPnA/%3Fsize%3D128/https/cdn.discordapp.com/icons/819636321223442472/67da9cfec011b8c455097752e3f4e2b7.png")
       	for result in results:
               _id = result["_id"]
               reason = result["reason"]
               warner = result["warner"]
               embed.add_field(name ="‎", value = f"**Warn ID:** {_id}, **Reason:** {reason}, **Warner:** {warner}", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_role(823787908678942721)
    async def delwarn(self,ctx, w_id):
        cluster = MongoClient("")#FILL IN DETAILS HERE
        db = cluster["discord"]
        collection = db["warningsys"]

        with open("counter.json") as f:
            data = json.load(f)

        number = int(data["counter"])
        number -= 1
        data["counter"] = int(number)
        with open("counter.json", 'w') as f:
            json.dump(data, f)
        
        results = collection.delete_one({"_id":f"{w_id}"})

        embed = discord.Embed(title = f"__Warning Deleted__",description = f"Deleted warning {w_id}",colour=0xD22063)
        embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/OVwUO6DhoIc7Lcyfgp97l1jgmASpGt50KSW26J-MPnA/%3Fsize%3D128/https/cdn.discordapp.com/icons/819636321223442472/67da9cfec011b8c455097752e3f4e2b7.png")
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_role(823787908678942721)
    async def editwarn(self,ctx, w_id, updated_reason):
        cluster = MongoClient("")#FILL IN DETAILS HERE
        db = cluster["discord"]
        collection = db["warningsys"]
     	
        results = collection.update_one({"_id":f"{w_id}"}, {"$set":{"reason":f"{updated_reason}"}})
        
        embed = discord.Embed(title = f"__Warning Edited__",description = f"Edited warning {w_id}",colour=0xD22063)
        embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/OVwUO6DhoIc7Lcyfgp97l1jgmASpGt50KSW26J-MPnA/%3Fsize%3D128/https/cdn.discordapp.com/icons/819636321223442472/67da9cfec011b8c455097752e3f4e2b7.png")
        embed.add_field(name ="New Reason", value = f"{updated_reason}", inline=False)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(WarningSysCog(bot))
