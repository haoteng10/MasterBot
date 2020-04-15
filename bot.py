import discord
# from discord.ext import commands

import keys
from translate import translate
from languages import LANGUAGES
from tiny_url import short_url

import warnings
# warnings.filterwarnings("error")

flags = {
    "🇨🇳": "zh-cn", #Chinese Simplified
    "🇪🇸": "es", #Spanish
    "🇮🇱": "he", #Hebrew
    "🇺🇸": "en", #English (USA)
    "🇬🇧": "en", #English (U.K.)
    "🇯🇵": "ja", #Japanese
    "🇮🇹": "it", #Italian
    "🇩🇪": "de", #German
    "🇫🇷": "fr", #French
    "🇵🇭": "tl", #Filipino
    "🇷🇺": "ru", #Russian
    "🇰🇷": "ko", #Korean
    "🇻🇳": "vi", #Vietnamese
    "🇸🇦": "ar", #Arabic
    "🇭🇺": "hu", #Hungarian
    "🇫🇮": "fi", #Finnish
    "🇳🇴": "no", #Norwegian
    "🇱🇦": "lo", #Laos
    "🇵🇱": "pl", #Polish
    "🇺🇦": "uk", #Ukrainian
    "🇵🇹": "pt", #Portuguese
    "🇲🇾": "ms", #Malay
    "🇷🇸": "sr", #Serbian
    "🇱🇺": "lb", #Luxembourgish
    "🇦🇹": "de", #German (Austria)
    "🇮🇳": "hi", #Hindi (India)
    "🇵🇰": "ur" #Urdu (Pakistan)
}

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
        bot_channel = discord.utils.get(self.get_all_channels(), name='bot-commands')
        await bot_channel.send("I'm up and ready to serve!")       

        
    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if(message.content == '*help'):
            embed = discord.Embed(title="MasterBot", color=discord.Color.blue())
            embed.add_field(name="What is this?",
                            value="A bot designed to make everything easier!")
            embed.add_field(name="Available Commands: ",
                            value="1. `ping`")
            embed.add_field(name="Available Actions: ", 
                            value="1. Place a country emoji to translate! (Type `*languages` to see supported languages!) \n 2. Place a watermelon to shorten URLs!")
            await message.channel.send(embed=embed)

        if(message.content == '*languages'):
            embed = discord.Embed(title="Supported languages for translation", color=discord.Color.green())
            embed.add_field(name="FLAG & LANGUAGE", value="🇨🇳 Chinese Simplified\n🇪🇸 Spanish\n🇮🇱 Hebrew\n🇺🇸 English (USA)\n🇬🇧 English (U.K.)\n🇯🇵 Japanese\n🇮🇹 Italian\n🇩🇪 German\n🇫🇷 French\n🇵🇭 Filipino\n🇷🇺 Russian\n🇰🇷 Korean\n🇻🇳 Vietnamese\n🇸🇦 Arabic\n🇭🇺 Hungarian\n🇫🇮 Finnish\n🇳🇴 Norwegian\n🇱🇦 Laos\n🇵🇱 Polish\n🇺🇦 Ukrainian\n🇵🇹 Portuguese\n🇲🇾 Malay\n🇷🇸 Serbian\n🇱🇺 Luxembourgish\n🇦🇹 German (Austria)\n🇮🇳 Hindi (India)\n🇵🇰 Urdu (Pakistan)")
            await message.channel.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        
        if(str(reaction.emoji) == "🍉" ):
            if ("http://" in reaction.message.content or "https://" in reaction.message.content):
                outputMessage = self.convertURL(reaction.message.content, reaction.message.author)
                await channel.send(outputMessage)
        try:
            translate(reaction.message.content, flags[str(reaction.emoji)])
        except KeyError:
            # if (str(reaction.emoji) in ALL_FLAG_EMOJIS):
                # await channel.send("Unsupported language! It will be added soon!")
            return

        translated_message = translate(reaction.message.content, flags[str(reaction.emoji)])

        origin_short_lang = translated_message.extra_data["original-language"]
        origin_emoji = ""
        for emoji, lang in flags.items():
            if lang == origin_short_lang:
                origin_emoji = emoji

        # await channel.send('{0} (Translated from {1} to {2})'.format(translated_message.text, LANGUAGES[translated_message.extra_data["original-language"]], LANGUAGES[flags[str(reaction.emoji)]]))
        embed = discord.Embed(title="Translation: ", color=discord.Color.purple())
        embed.add_field(name="From {2} {0} to {3} {1}".format(LANGUAGES[origin_short_lang], LANGUAGES[flags[str(reaction.emoji)]], origin_emoji, reaction.emoji), value=translated_message.text)
        await channel.send(embed=embed)

    def convertURL(self, content, author):
        splitStr = content.split()
        newStr = []
        newStr.append(author.name + ": ")

        for word in splitStr:
            if ("http://" in word or "https://" in word):
                if(word[0] != "`" and word[len(word)-1] != "`"):
                    # if (word[0] != "h")
                    shortened_url = short_url(word)
                    newStr.append(shortened_url)
                else:
                    shortened_url = short_url(word[1:-1])
                    newStr.append(shortened_url)
                continue
            newStr.append(word)

        return ' '.join(newStr)

bot = BotClient()
bot.run(keys.DISCORD_TOKEN)