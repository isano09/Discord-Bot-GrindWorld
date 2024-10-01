from discord.ext import commands
from database.models import Player, get_db

@commands.command(name='guadagna_xp')
async def guadagna_xp(ctx, xp: int):
    session = get_db()

    # Recupera il giocatore dal database
    player = session.query(Player).filter_by(discord_id=str(ctx.author.id)).first()
    if not player:
        await ctx.send("Non hai ancora creato un personaggio. Usa il comando /start per iniziare.")
        session.close()
        return

    # Aggiungi XP al giocatore
    player.add_experience(xp)
    session.commit()

    await ctx.send(f"Hai guadagnato {xp} XP! Sei ora al livello {player.level} con {player.stat_points} punti statistica da distribuire.")

    session.close()
