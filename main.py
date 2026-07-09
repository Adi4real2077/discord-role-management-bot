import discord
from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1522614796149588088)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')
        
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hey there {message.author}')

        await self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        
        guild = reaction.message.guild

        if not guild:
            return
        
        if hasattr(self, 'colour_role_message_id') and reaction.message.id != self.colour_role_message_id:
            return
        
        emoji = str(reaction.emoji)

        reaction_role_map = {
            '❤️': 'Red',
            '💙': 'Blue',
            '💚': 'Green',
            '💛': 'Yellow',
            '🧡': 'Orange'
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.add_roles(role)
                print(f"Assigned {role_name} to {user}")
    
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        
        guild = reaction.message.guild

        if not guild:
            return
        
        if hasattr(self, 'colour_role_message_id') and reaction.message.id != self.colour_role_message_id:
            return
        
        emoji = str(reaction.emoji)

        reaction_role_map = {
            '❤️': 'Red',
            '💙': 'Blue',
            '💚': 'Green',
            '💛': 'Yellow',
            '🧡': 'Orange'
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.remove_roles(role)
                print(f"Removed {role_name} from {user}")   



intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
client = Client(command_prefix="!", intents=intents)


GUILD_ID = discord.Object(id=1522614796149588088)

@client.tree.command(name="colourroles", description="Create a message that lets users pick a colour role", guild=GUILD_ID)
async def colour_roles(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You must be an admin to run this commmand", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)

    description = (
    "React to this message to get your color role!\n\n"
    "❤️ Red\n"
    "💙 Blue\n"
    "💚 Green\n"
    "💛 Yellow\n"
    "🧡 Orange\n"
    )
    
    embed = discord.Embed(title="Pick your Colour!", description=description, color=discord.Color.blurple())
    message = await interaction.channel.send(embed=embed)

    emojis = ['❤️', '💙', '💚', '💛', '🧡']

    for emoji in emojis:
        await message.add_reaction(emoji)

    client.colour_role_message_id = message.id

    await interaction.followup.send("Colour role message created!", ephemeral=True)



@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey there!")

@client.tree.command(name="printer", description="Print a message!", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="embed", description="Embed demo!", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a title", url="https://ankergames.net/", description="I am the description", color=discord.Color.red())
    embed.set_thumbnail(url="https://media.istockphoto.com/id/1293449386/vector/computer-hand-cursor-click-hand-pointer-clicking-effect-vector-illustration.jpg?s=612x612&w=0&k=20&c=R4nrm79AFGbksqq3JEck-XrF9X9upggOHfUsS5mGQOo=")
    embed.add_field(name="Field 1", value="Check the Anker Games website!", inline=False)
    embed.add_field(name="Field 2", value="Hey check it out!", inline=True)
    embed.add_field(name="Field 3", value="Download any game!", inline=True)
    embed.set_footer(text="The footer")
    embed.set_author(name=interaction.user.name, url="https://ankergames.net/", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPAYrDWP8MnZqdooaOCepJTAdLdsHtHzoePnWtbNshgn84eNKj8ouN71c2&s=10") 
    await interaction.response.send_message(embed=embed)   

class View(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red, emoji="✅")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have clicked the button!")


    @discord.ui.button(label="2nd button", style=discord.ButtonStyle.blurple, emoji="😂")
    async def two_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have clicked the 2nd button!")

    @discord.ui.button(label="3rd button", style=discord.ButtonStyle.green, emoji="🤓")
    async def three_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have clicked the 3rd button!")


@client.tree.command(name="button", description="Displaying a button", guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="This is option 1", emoji="🍎"),
            discord.SelectOption(label="Option 2", description="This is option 2", emoji="🍌"),
            discord.SelectOption(label="Option 3", description="This is option 3", emoji="🍇"),
        ]

        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Option 1":
            await interaction.response.send_message("You have selected Option 1!")

        elif self.values[0] == "Option 2":
            await interaction.response.send_message("This is now Option 2!")

        elif self.values[0] == "Option 3":
            await interaction.response.send_message("This is the last Option!")

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())



@client.tree.command(name="menu", description="Displaying a drop down menu", guild=GUILD_ID)
async def myMenu(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())




client.run(TOKEN)
