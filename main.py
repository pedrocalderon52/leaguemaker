import sqlite3

con = sqlite3.connect("times.db")
cursor = con.cursor()

# CRIANDO AS TABELAS

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
               
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    senha TEXT
);
               
""") 

cursor.execute("""
CREATE TABLE IF NOT EXISTS Campeonato (
    id_campeonato INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    formato TEXT CHECK (formato IN ('mata-mata', 'liga', 'misto')),
    tem_rebaixamento INTEGER DEFAULT 0,
    tem_zona_classificacao INTEGER DEFAULT 1,
    tem_ida_volta INTEGER DEFAULT 0,
    qtde_times INTEGER NOT NULL,
    qtde_grupos INTEGER NOT NULL,
    tamanho_zona_rebaixamento INTEGER,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    
    CHECK (qtde_grupos <= qtde_times / 2),
    CHECK (qtde_times % qtde_grupos = 0),
    CHECK (tamanho_zona_rebaixamento IS NULL OR tamanho_zona_rebaixamento <= qtde_times / qtde_grupos / 2)
);
""")


# considero mudar esse check, para uma função de validação dentro do próprio python

cursor.execute("""
CREATE TABLE IF NOT EXISTS Time (
    id_time INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL, 
    sigla TEXT CHECK (LENGTH(sigla) <= 3),
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
    id_time_casa INTEGER,
    id_time_visitante INTEGER,
    id_campeonato INTEGER,
    placar_casa INTEGER DEFAULT 0,
    placar_visitante INTEGER DEFAULT 0,
    placar_penaltis_casa INTEGER,
    placar_penaltis_visitante INTEGER,
    teve_disputa_penaltis INTEGER DEFAULT 0,
    status CHECK(status in ('a realizar', 'em andamento', 'concluída')), 
    data DATE,
    hora TIME,
    fase CHECK (fase in ('Fase de grupos', '16 avos de final', 'Oitavas de final', 'Quartas de final', 'Semifinal', 'Disputa de 3° lugar', 'Final')),
    juiz TEXT,
    
    FOREIGN KEY (id_time_casa) 
            REFERENCES Time(id_time),
    FOREIGN KEY (id_time_visitante)
            REFERENCES Time(id_time),
    FOREIGN KEY (id_campeonato)
            REFERENCES Campeonato(id_campeonato)

);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Estatistica (
    id_jogador INTEGER NOT NULL,
    id_partida INTEGER NOT NULL,
    gols INTEGER DEFAULT 0,
    assistencias INTEGER DEFAULT 0,
    cartoes INTEGER DEFAULT 0,
    PRIMARY KEY (id_jogador, id_partida)
        FOREIGN KEY (id_jogador) 
               REFERENCES Jogador(id_jogador),
        FOREIGN KEY (id_partida) 
               REFERENCES Partida(id_partida)
);

""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Jogador (
    id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_jogador TEXT,
    id_time INTEGER,
        FOREIGN KEY (id_time) REFERENCES Time(id_time)
);
""")