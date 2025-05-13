import sqlite3

con = sqlite3.connect("times.db")
cursor = con.cursor()

# CRIANDO AS TABELAS

cursor.execute("""
               
PRAGMA foreign_keys = ON;
               
""")

cursor.execute("""
               
CREATE TABLE IF NOT EXISTS Campeonato (
    id_campeonato INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    formato ENUM('mata-mata', 'liga', 'misto'),
    tem_rebaixamento INTEGER DEFAULT 0,
    tamanho_zona_rebaixamento INTEGER CHECK (tamanho_zona_rebaixamento <= qtde_times),
    tem_zona_classificacao INTEGER DEFAULT 1,
    tem_ida_volta INTEGER DEFAULT 0,
    qtde_times INTEGER NOT NULL
    qtde_grupos INTEGER NOT NULL CHECK ((qtde_grupos <= qtde_times / 2) and (qtde_times % qtde_grupos = 0))
);
               
""") 

# considero mudar esse check, para uma função de validação dentro do próprio python

cursor.execute("""
CREATE TABLE IF NOT EXISTS Time (
    id_time INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL, 
    sigla VARCHAR(3),
    escudo TEXT,
    id_campeonato INTEGER,
        FOREIGN KEY (id_campeonato) REFERENCES Campeonato(id_campeonato)
);

""")

# ajeitar todas as fk's depois

# colocar uma função que valida o nome do time, ou seja, somente caracteres alfanuméricos


cursor.execute("""
               
CREATE TABLE IF NOT EXISTS Partida (
    id_partida INTEGER PRIMARY KEY AUTOINCREMENT,
    id_time_casa INTEGER REFERENCES Time(id_time),
    id_time_visitante INTEGER REFERENCES Time(id_time),
    id_campeonato INTEGER REFERENCES Campeonato(id_campeonato),
    placar_casa INTEGER DEFAULT 0,
    placar_visitante INTEGER DEFAULT 0,
    placar_penaltis_casa INTEGER,
    placar_penaltis_visitante INTEGER,
    teve_disputa_penaltis INTEGER DEFAULT 0,
    status ENUM('a realizar', 'em andamento', 'concluída'), 
    data DATE,
    hora TIME,
    fase ENUM('Fase de grupos', '16 avos de final', 'Oitavas de final', 'Quartas de final', 'Semifinal', 'Disputa de 3° lugar', 'Final')  
    juiz VARCHAR(100)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Estatistica (
    id_jogador INTEGER REFERENCES Jogador(id_jogador),
    id_partida INTEGER REFERENCES Partida(id_partida),
    gols INTEGER DEFAULT 0,
    assistencias INTEGER DEFAULT 0,
    cartoes INTEGER DEFAULT 0,
    PRIMARY KEY (id_jogador, id_partida)
);

""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Jogador (
    id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_jogador VARCHAR(100),
    id_time INTEGER 
        FOREIGN KEY Jogador(id_time) REFERENCES Time(id_time)
);
""")