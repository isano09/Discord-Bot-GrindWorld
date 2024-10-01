import discord
from discord.ext import commands
from commands.profilo import profilo  # Importa il comando profilo correttamente
from commands.start import create_character  # Importa il comando create_character dal modulo start
from commands.progressione import distribuisci_punti
from commands.xp import guadagna_xp
from commands.combat import combatti
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True  # Necessario per leggere i messaggi del canale

# Inizializza il bot con il prefisso di comando "/"
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} è online e pronto per GrindWorld!')

# Registriamo i comandi
bot.add_command(create_character)  # Usa create_character direttamente senza alias
bot.add_command(profilo)  # Usa profilo direttamente senza alias
bot.add_command(distribuisci_punti)
bot.add_command(guadagna_xp)
bot.add_command(combatti)

bot.run(TOKEN)
