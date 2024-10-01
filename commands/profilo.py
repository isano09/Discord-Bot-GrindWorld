from discord.ext import commands
from database.models import Player, get_db

# Comando per mostrare il profilo del giocatore
@commands.command(name='profilo')
async def profilo(ctx):
    await ctx.send(f"Profilo di {ctx.author.name}.")
    session = get_db()

    # Recupera il giocatore dal database
    player = session.query(Player).filter_by(discord_id=str(ctx.author.id)).first()
    if not player:
        await ctx.send("Non hai ancora creato un personaggio. Usa il comando /create per iniziare.")
        session.close()
        return

    # Mostra i dettagli del personaggio
    await ctx.send(f"Profilo di {ctx.author.name}:\n"
                   f"Classe: {player.class_name}\n"
                   f"Livello: {player.level}\n"
                   f"Esperienza: {player.experience}")
    
    session.close()
