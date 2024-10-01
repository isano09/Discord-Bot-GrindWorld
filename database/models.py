from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definiamo il modello di base
Base = declarative_base()

# Definiamo la classe Player (equivalente alla tabella players nel DB)
class Player(Base):
    __tablename__ = 'players'

    # (Colonne già esistenti)
    id = Column(Integer, primary_key=True)
    discord_id = Column(String(255), unique=True, nullable=False)
    class_name = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    stat_points = Column(Integer, default=0)
    vigor = Column(Integer, default=10)
    mind = Column(Integer, default=10)
    endurance = Column(Integer, default=10)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    faith = Column(Integer, default=10)
    arcane = Column(Integer, default=10)

    # Funzione per aggiungere XP e controllare se si sale di livello
    def add_experience(self, xp_gain):
        self.experience += xp_gain
        level_up_exp = int(100 * (self.level ** 2.5))

        if self.experience >= level_up_exp:
            self.level_up()

    # Funzione per salire di livello
    def level_up(self):
        self.level += 1
        self.stat_points += 3  # 3 punti statistica per livello
        self.experience = 0  # Resetta l'XP per il prossimo livello



# Configurazione della connessione al database
def get_db():
    engine = create_engine('mysql+mysqlconnector://root:chu=athuf8wrE=IhEde1@localhost/grindworld')
    Session = sessionmaker(bind=engine)
    return Session()
