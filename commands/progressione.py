from discord.ext import commands
from database.models import Player, get_db

@commands.command(name='distribuisci')
async def distribuisci_punti(ctx, stat, punti: int):
    session = get_db()

    # Recupera il giocatore dal database
    player = session.query(Player).filter_by(discord_id=str(ctx.author.id)).first()
    if not player:
        await ctx.send("Non hai ancora creato un personaggio. Usa il comando /create per iniziare.")
        session.close()
        return

    if player.stat_points < punti:
        await ctx.send(f"Non hai abbastanza punti da distribuire. Hai {player.stat_points} punti disponibili.")
        session.close()
        return

    # Distribuisci i punti nelle statistiche richieste
    if stat.lower() in ['vigor', 'mind', 'endurance', 'strength', 'dexterity', 'intelligence', 'faith', 'arcane']:
        setattr(player, stat.lower(), getattr(player, stat.lower()) + punti)
        player.stat_points -= punti
        session.commit()
        await ctx.send(f"Hai assegnato {punti} punti a {stat.capitalize()}. Statistiche aggiornate!")
    else:
        await ctx.send("Statistiche non valide. Scegli tra: Vigor, Mind, Endurance, Strength, Dexterity, Intelligence, Faith, Arcane.")

    session.close()
