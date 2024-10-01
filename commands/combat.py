import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from database.models import Player, get_db
from database.enemies import Enemy
import random

@commands.command(name='combatti')
async def combatti(ctx):
    session = get_db()

    # Recupera il giocatore
    player = session.query(Player).filter_by(discord_id=str(ctx.author.id)).first()
    if not player:
        await ctx.send("Non hai ancora creato un personaggio. Usa il comando /start per iniziare.")
        session.close()
        return

    # Genera un nemico casuale (es. un lupo)
    enemy = Enemy(name="Lupo", level=player.level, hp=50, attack=8, defense=3)

    # Determina chi attacca per primo in base a Dexterity
    if player.dexterity >= random.randint(1, 20):
        player_turn = True
    else:
        player_turn = False

    # Inizia il ciclo di combattimento
    while player.current_hp > 0 and enemy.hp > 0:  # Usa current_hp per il giocatore
        if player_turn:
            await ctx.send(f"È il tuo turno! Sei contro {enemy.name}. Che cosa vuoi fare? (attacca / difendi)")
            def check(m):
                return m.author == ctx.author and m.content in ["attacca", "difendi"]

            try:
                action = await ctx.bot.wait_for('message', timeout=30.0, check=check)
                if action.content == "attacca":
                    # Calcola il danno inflitto
                    damage = max(player.strength - enemy.defense, 1)
                    enemy.hp -= damage
                    await ctx.send(f"Hai inflitto {damage} danni a {enemy.name}. HP del nemico: {enemy.hp}/{enemy.hp}.")
                elif action.content == "difendi":
                    await ctx.send("Ti sei difeso! Riceverai meno danni nel prossimo turno.")

            except TimeoutError:
                await ctx.send("Non hai agito in tempo!")
            player_turn = False
        else:
            # Turno del nemico
            damage = max(enemy.attack - player.endurance, 1)  # Usa endurance del giocatore come difesa
            player.current_hp -= damage  # Usa current_hp per il giocatore
            await ctx.send(f"{enemy.name} ti ha attaccato! Hai subito {damage} danni. HP: {player.current_hp}/{player.max_hp}.")  # Usa current_hp e max_hp
            player_turn = True

    # Fine del combattimento
    if player.current_hp <= 0:  # Usa current_hp per il giocatore
        await ctx.send(f"Sei stato sconfitto da {enemy.name}.")
    else:
        await ctx.send(f"Hai sconfitto {enemy.name}!")
        player.add_experience(enemy.level * 50)  # Guadagna XP in base al livello del nemico
        session.commit()

    session.close()
