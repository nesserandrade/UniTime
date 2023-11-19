import sqlite3

class Database:
    
    def iniciar(self):
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()
        print("Database iniciado com sucesso ")
        self.create_tables()

    def inserir_professores(self, professor, disciplina, numero_aulas):
        self.cursor.execute('''
                INSERT INTO Professores (NomeProfessor, Disciplina, NumAulas)
                VALUES (?, ?, ?)
            ''', (professor, disciplina, numero_aulas))
        self.connection.commit()
    
    def get_all_professores(self):
        self.cursor.execute('SELECT * FROM Professores')
        professores = self.cursor.fetchall()
        return professores

    def delete_all_professores(self):
        self.cursor.execute('DELETE FROM Professores')
        self.connection.commit()

    def create_tables(self):
        # Table Professores
        criar_tabela_professores = """
        CREATE TABLE IF NOT EXISTS Professores (
            ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
            NomeProfessor TEXT NOT NULL,
            Disciplina TEXT NOT NULL,
            NumAulas INT NOT NULL
        )
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Professores'")
        tabela_professores_existe = self.cursor.fetchone()
        if tabela_professores_existe:
            print("Tabela 'Professores' já existe no banco de dados")
        else:
            self.cursor.execute(criar_tabela_professores)
            print("Tabela 'Professores' criada com sucesso")
            self.connection.commit()

        # Table ProfessoresPers
        criar_tabela_professorespers = """
        CREATE TABLE IF NOT EXISTS Professorespers (
            ProfessorpersID INTEGER PRIMARY KEY AUTOINCREMENT,
            NomeProfessor TEXT NOT NULL,
            Disciplina TEXT NOT NULL,
            NumAulas INT NOT NULL
        )
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Professorespers'")
        tabela_professorespers_existe = self.cursor.fetchone()
        if tabela_professorespers_existe:
            print("Tabela 'Professorespers' já existe no banco de dados")
        else:
            self.cursor.execute(criar_tabela_professorespers)
            print("Tabela 'Professorespers' criada com sucesso")
            self.connection.commit()

        # Table HorariosAula
        criar_tabela_horarios_aula = """
        CREATE TABLE IF NOT EXISTS HorariosAula (
            HorarioID INTEGER PRIMARY KEY AUTOINCREMENT,
            DiaSemana TEXT,
            HoraInicio TEXT,
            ProfessorpersID INT,
            Preferencia INT,
            FOREIGN KEY (ProfessorpersID) REFERENCES Professorespers(ProfessorpersID)

        )
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HorariosAula'")
        tabela_horarios_aula_existe = self.cursor.fetchone()
        if tabela_horarios_aula_existe:
            print("Tabela 'HorariosAula' já existe no banco de dados")
        else:
            self.cursor.execute(criar_tabela_horarios_aula)
            print("Tabela 'HorariosAula' criada com sucesso")
            self.connection.commit()

        # Table AlocacaoProfessores
        criar_tabela_alocacao_professores = """
        CREATE TABLE IF NOT EXISTS AlocacaoProfessores (
            AlocacaoID INTEGER PRIMARY KEY AUTOINCREMENT,
            HorarioID INT,
            ProfessorpersID INT,
            DisciplinaAlocada TEXT NOT NULL,
            FOREIGN KEY (HorarioID) REFERENCES HorariosAula(HorarioID),
            FOREIGN KEY (ProfessorpersID) REFERENCES Professorespers(ProfessorpersID)
        )
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='AlocacaoProfessores'")
        tabela_alocacao_professores_existe = self.cursor.fetchone()
        if tabela_alocacao_professores_existe:
            print("Tabela 'AlocacaoProfessores' já existe no banco de dados")
        else:
            self.cursor.execute(criar_tabela_alocacao_professores)
            print("Tabela 'AlocacaoProfessores' criada com sucesso")
            self.connection.commit()

        # Table ResultadoAlocacao
        criar_tabela_resultado_alocacao = """
        CREATE TABLE IF NOT EXISTS ResultadoAlocacao (
            ResultadoID INTEGER PRIMARY KEY AUTOINCREMENT,
            HorarioID INT,
            ProfessorpersID INT,
            DisciplinaAlocada TEXT NOT NULL,
            FOREIGN KEY (HorarioID) REFERENCES HorariosAula(HorarioID),
            FOREIGN KEY (ProfessorpersID) REFERENCES Professorespers(ProfessorpersID)
        )
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ResultadoAlocacao'")
        tabela_resultado_alocacao_existe = self.cursor.fetchone()
        if tabela_resultado_alocacao_existe:
            print("Tabela 'ResultadoAlocacao' já existe no banco de dados")
        else:
            self.cursor.execute(criar_tabela_resultado_alocacao)
            print("Tabela 'ResultadoAlocacao' criada com sucesso")
            self.connection.commit()
   
    def disconnect(self):
        print("Desconectando do banco de dados")
        self.connection.close()