from discord.ext import commands
from database.models import Player, get_db

# Comando per creare il personaggio
@commands.command(name='create')
async def create_character(ctx):
    session = get_db()

    # Controlla se il giocatore ha già un personaggio
    existing_player = session.query(Player).filter_by(discord_id=str(ctx.author.id)).first()
    if existing_player:
        await ctx.send(f"Hai già creato un personaggio con la classe {existing_player.class_name}. Usa /profilo per visualizzarlo.")
        session.close()
        return

    # Introduzione
    await ctx.send("Benvenuto in GrindWorld! Scegli la tua classe: Guerriero, Mago, Ladro, Chierico, Cacciatore.")
    
    def check(m):
        return m.author == ctx.author and m.content in ["Guerriero", "Mago", "Ladro", "Chierico", "Cacciatore"]

    try:
        # Usa ctx.bot.wait_for per accedere al bot
        class_choice = await ctx.bot.wait_for('message', timeout=30.0, check=check)
        await ctx.send(f'Hai scelto la classe: {class_choice.content}. Il tuo personaggio è stato creato!')

        # Salva il nuovo personaggio nel database
        new_player = Player(discord_id=str(ctx.author.id), class_name=class_choice.content)
        session.add(new_player)
        session.commit()
    except TimeoutError:
        await ctx.send("Tempo scaduto. Riprova il comando /create per creare un personaggio.")
    finally:
        session.close()
