from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import ttk
import sqlite3
import os

pastaApp = os.path.dirname(__file__)

#CORES
azul = '#87CEEB' #SkyBlue
azulEscuro = '#1E90FF'
branco = '#F5FFFA' #MintCream
cinza = '#C0C0C0' #Silver
vermelho = '#FF7F50' #Coral

'''###################################################'''
'''####   FUNÇÕES SECONDARIAS E BANCO DE DADOS    ####'''
class Funcoes():
    # LIMPA TELA
    def limparTela(self):
        self.entryNome.delete(0,END)
        self.entryID.delete(0,END)
        self.entrySenha.delete(0,END)
    def limpaEscola(self):
        self.entryEscola.delete(0,END)
        self.entryCidade.delete(0,END)
    def limpaTurma(self):
        self.entryTurma.delete(0,END)
        self.entryDisciplina.delete(0,END)
        self.comboEntry.delete(0,END)

    ############################################
    ########    BANCO DE DADOS

    ## FUNÇÕES CONECTANDO E DESCONECTANDO AO BANCO
    def conectaDB(self, arquivo='diario.db'):
        self.connU = sqlite3.connect(arquivo)
        self.cursor = self.connU.cursor()
            
    def verificaDB(self):
        if os.path.exists('diario.db') == False:
            self.connU = sqlite3.connect('diario.db')
            self.cursor = self.connU.cursor()
    
    def desconectaBDusuarios(self):
        self.connU.close()       

    ## MONTANDO TABELA DE USUARIOS
    def montaTabela(self):
        self.conectaDB()
        #TABELA DE USUÁRIOS
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS usuarios (
                cod integer PRIMARY KEY AUTOINCREMENT,
                nmUsuario varchar(30) not null,
                idUsuario varchar(20) not null,
                senhaUsuario varchar(20)
            );
        """)
        self.connU.commit()

        #TABELA DE ALUNOS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                codAluno INTEGER PRIMARY KEY AUTOINCREMENT,
                nmAluno VARCHAR(20),
                idade VARCHAR(15)
            );
        """)
        self.connU.commit()


        #TABELA ESCOLAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Escolas (
                codEscola INTEGER PRIMARY KEY AUTOINCREMENT,
                nmEscola VARCHAR(50),
                cidEscola VARCHAR(20)
            )
        """)
        self.connU.commit()

        #TABELA DE TURMAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                codTurma INTEGER PRIMARY KEY AUTOINCREMENT,
                nmTurma VARCHAR(10) NOT NULL,
                disciplina VARCHAR(15),
                escola  INTEGER      REFERENCES Escolas (nmEscola) ON DELETE CASCADE
                                                                    ON UPDATE CASCADE,
                prof    INTEGER      REFERENCES Usuario (cod) ON DELETE CASCADE
                                                                ON UPDATE CASCADE
            );
        """)
        self.connU.commit()

        self.desconectaBDusuarios()

class Janela(Funcoes): 
#############################################
########    JANELA DE INICIAL *LOGIN*
    def __init__(self):
        self.diario = diario
        self.diario.iconbitmap(pastaApp+"\\img/icon2.ico")
        self.framesTela1()
        self.botoes()
        self.montaTabela()
        self.diario.title('Login')
        self.diario.configure(background=azul)
        self.diario.geometry('250x200+500+200')
        self.diario.resizable(False,False)
        self.diario.mainloop()
        
    ########    FRAMES, ENTRYS, LABELS E BOTÕES *LOGIN*
    def framesTela1(self):
        self.cont1 = Frame(self.diario, bg=branco)
        self.cont1.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)

        self.imgLogo = PhotoImage(file=pastaApp+"\\img/logo.png")
        self.lbLogo = Label(self.cont1,image=self.imgLogo, bg=branco)
        self.lbLogo.place(relx=0.35, rely=0.02)
        
        self.lbLogin = Label(self.cont1, text='ID', width=5, font=('verdana',10,), bg=branco, fg = cinza)
        self.lbLogin.place(relx=0.05,rely=0.20)
        self.loginEntry = Entry(self.cont1)
        self.loginEntry.place(relx=0.11, rely=0.30, relwidth=0.80)

        self.lbSenha = Label(self.cont1, text='Senha', width=8, font=('verdana',10,), bg=branco, fg = cinza)
        self.lbSenha.place(relx=0.05,rely=0.45)
        self.senhaEntry = Entry(self.cont1, show='*')
        self.senhaEntry.place(relx=0.11, rely=0.55, relwidth=0.80)

    def botoes(self):
        self.entrar = Button(self.cont1, text='Login', font=('arial','12'), width=5,
                                bg='#1E90FF', fg='#F8F8FF',command= self.verificaLogin)
        self.entrar.place(relx=0.74,rely=0.80)

        self.cadastro = Button(self.cont1, text='Novo Usuário', font=('arial','10'), width=10,
                                bg='#1E90FF', fg='#F8F8FF', command= self.telaCadastro)
        self.cadastro.place(relx=0.02,rely=0.80)       


    def verificaLogin(self):        
        self.conectaDB()
        self.regID = self.loginEntry.get()
        self.regSenha = self.senhaEntry.get()
    
        if self.regID.__len__() == 0:
            self.aviso(texto='ERRO!\nPor favor,\ninforme o seu\nUsuário')
        elif self.regSenha.__len__() == 0:
            self.aviso(texto='ERRO!\nPor favor,\ninforme a sua\nSenha')
        else:    
            try:
                self.teste = self.cursor.execute("""SELECT * FROM usuarios WHERE idUsuario = '{}'""".format(self.regID))
                linha = self.teste.fetchall()
                cdSenha = linha[0][3]
                if cdSenha == self.senhaEntry.get():
                    self.tela2()
                else:
                    self.aviso(texto='ERRO!\nSenha ou usuário\n incorretos!')
            except:
                self.aviso(texto='ERRO!\nUsuário não\nEncontrado!')
        self.loginEntry.delete(0,END)
        self.senhaEntry.delete(0,END)
        self.connU.commit()
        self.desconectaBDusuarios()

###############################################
####  JANELA PRINCIPAL DO PROGRAMA
###########################################
    def tela2(self):
        self.telaPrincipal = Toplevel()
        self.telaPrincipal.iconbitmap(pastaApp+"\\img/icon2.ico")
        self.telaPrincipal.title('Diário Escolar')
        self.telaPrincipal.geometry('900x750+200+0')
        self.telaPrincipal.resizable(False,False)
        self.telaPrincipal.configure(background=azul)
        self.menus()
        self.listaTurmas()
        self.telaPrincipal.transient(self.diario)
        self.telaPrincipal.focus_force()
        self.telaPrincipal.grab_set()
        
        self.imglogo = PhotoImage(file=pastaApp+"\\img/logotipo.png")
        self.lLogo = Label(self.telaPrincipal,image=self.imglogo, bg=azul)
        self.lLogo.place(relx=0.30, rely=0)


    def menus(self):
        self.barraDeMenus = Menu(self.telaPrincipal)
        self.menuCadastro = Menu(self.barraDeMenus,tearoff=0)
        self.barraDeMenus.add_cascade(label="Cadastro",menu=self.menuCadastro)
        self.menuCadastro.add_command(label="Escolas", command=self.cadastroEscola)
        self.menuCadastro.add_command(label="Turmas", command=self.cadastroTurmas)
        
        self.telaPrincipal.config(menu=self.barraDeMenus)
           
    def listaTurmas(self):
        self.listaturma = ttk.Treeview(self.telaPrincipal, height=3, columns=('col1','col2','col3','col4','col5'))
        self.listaturma.heading('#0',text='')
        self.listaturma.heading('#1',text='cod')
        self.listaturma.heading('#2',text='Turma')
        self.listaturma.heading('#3',text='Disciplina')
        self.listaturma.heading('#4',text='Escola')
        self.listaturma.heading('#5',text='Usuário')

        self.listaturma.column('#0', width=5)
        self.listaturma.column('#1', width=45)
        self.listaturma.column('#2', width=100)
        self.listaturma.column('#3', width=100)
        self.listaturma.column('#4', width=200)
        self.listaturma.column('#5', width=100)

        self.listaturma.place(relx=0.01,rely=0.42,relwidth=0.96,relheight=0.70)

        self.scrollLista = Scrollbar(self.telaPrincipal, orient='vertical')
        self.listaturma.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.97, rely=0.42, relwidth=0.02, relheight=0.70)

        self.listaturma.bind('<Double-1>',self.editaTurma)
        self.atualizaTurma()
    
    """def framesTela2(self):
        #Frame do delete
        self.cont2_2 = Frame(self.telaPrincipal,bg=azul, highlightthickness=1)
        self.cont2_2.place(relx=0.70, rely=0.41, relwidth=0.28,relheight=0.08)

        self.cont3 = Frame(self.telaPrincipal,bg=branco)
        self.cont3.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)"""        
###############################################
####  JANELA CADASTRO ESCOLAS
###########################################
    def cadastroEscola(self):
        self.cadEscola = Toplevel()
        self.cadEscola.title('')
        self.cadEscola.geometry('600x400+250+100')
        self.cadEscola.configure(background=azul)
        self.cadEscola.transient(self.telaPrincipal)
        self.cadEscola.focus_force()
        self.cadEscola.grab_set()        
        
        self.cont2 = Frame(self.cadEscola,bg=branco)
        self.cont2.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        self.lbEScola = Label(self.cont2, text= 'Nome da escola', width=12, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbEScola.place(relx=0.02, rely=0.02)
        self.entryEscola = Entry(self.cont2)
        self.entryEscola.place(relx=0.02, rely=0.12, relwidth=0.94)

        self.lbEScola = Label(self.cont2, text= 'Cidade', width=6, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbEScola.place(relx=0.02, rely=0.2)
        self.entryCidade = Entry(self.cont2)
        self.entryCidade.place(relx=0.02, rely=0.3, relwidth=0.5)
        
        self.btCadEScola = Button(self.cont2, text= 'Adicionar', font=('arial','10'), width=7,
                                bg='#1E90FF', fg='#F8F8FF',command=self.addEScola)
        self.btCadEScola.place(relx=0.55, rely=0.30)
        
        self.listaEscolas()
        
    def listaEscolas(self):
        self.listaEscola = ttk.Treeview(self.cont2, height=2, columns=('col1','col2','col3'))
        self.listaEscola.heading('#0', text='')
        self.listaEscola.heading('#1', text='cod')
        self.listaEscola.heading('#2', text='Escola')
        self.listaEscola.heading('#3', text='Cidade')

        self.listaEscola.column('#0', width=1)
        self.listaEscola.column('#1', width=20)
        self.listaEscola.column('#2', width=200)
        self.listaEscola.column('#3', width=100)

        self.listaEscola.place(relx=0.01, rely=0.45, relwidth=0.95, relheight=0.5)

        self.scrollLista = Scrollbar(self.cont2, orient='vertical')
        self.listaEscola.configure(yscroll=self.scrollLista.set)

        self.scrollLista.place(relx=0.96, rely=0.45, relwidth=0.03, relheight=0.5)

        self.listaEscola.bind('<Double-1>',self.duploClickEScola)

        self.atualizaEscola()

    #######################
    ##### ADICIONA ESCOLA NO BANCO
    def addEScola(self):   
        self.nmEscola = self.entryEscola.get()
        self.cidEscola = self.entryCidade.get()

        if self.nmEscola.__len__() == 0:
            self.aviso(texto='Por favor\nDigite o nome \nda escola!')
        else:
            self.conectaDB()
            self.cursor.execute("""INSERT INTO escolas (nmEScola, cidEScola)
                        VALUES (?,?)""",(self.nmEscola,self.cidEscola))
            self.connU.commit()
            self.desconectaBDusuarios()
            self.limpaEscola()
            self.atualizaEscola()
            self.selectEscola()

    #add na Lista
    def atualizaEscola(self):
        self.listaEscola.delete(*self.listaEscola.get_children())
        self.conectaDB()
        lista = self.cursor.execute(""" SELECT codEscola, nmEscola, cidEscola  FROM escolas
            ORDER BY codEscola ASC; """)
        for i in lista:
            self.listaEscola.insert("", END, values=i)
        self.desconectaBDusuarios()

    def deleteEscola(self):
        self.cod = self.entryCod.get()

        if self.cod.__len__() == 0:
            self.aviso(texto='ERRO!\nDigite um codigo\n válido!')
        else:
            try:
                self.conectaDB()
                self.cursor.execute("""DELETE FROM escolas WHERE codEscola = '{}'""".format(self.cod))
                self.connU.commit()
                self.desconectaBDusuarios()
                self.entryCod.delete(0,END)
                self.atualizaEscola()
                self.aviso2(texto='Escola deletada\ncom sucesso!')
            except sqlite3.Error:
                self.aviso(texto='ERRO!\nVerifique os dados e\ntente novamente')
        self.selectEscola()

    def duploClickEScola(self,event):
        self.limpaEscola()
        self.listaEscola.selection()

        for n in self.listaEscola.selection():
            col1, col2, col3= self.listaEscola.item(n,'values')
            self.entryEscola2.delete(0,END)
            self.entryEscola2.insert(END,col2)

###############################################
####  JANELA CADASTRO TURMAS
###########################################
    def cadastroTurmas(self):
        self.cadTurma = Toplevel()
        self.cadTurma.title('')
        self.cadTurma.geometry('600x400+250+100')
        self.cadTurma.configure(background=azul)
        self.cadTurma.transient(self.telaPrincipal)
        self.cadTurma.focus_force()
        self.cadTurma.grab_set()
        
        self.cont2_1 = Frame(self.cadTurma, bg= branco)
        self.cont2_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        self.lbNmTurma = Label(self.cont2_1, text= 'Ano da Turma:', width=11, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbNmTurma.place(relx=0.02, rely=0.05)
        self.entryTurma = Entry(self.cont2_1)
        self.entryTurma.place(relx=0.29, rely=0.05, relwidth=0.25)
        
        self.selectDisciplina()
        self.selectEscola()
        
        self.btCadTurma = Button(self.cont2_1, text= 'Adicionar', font=('arial','10'), width=10,
                                bg='#1E90FF', fg='#F8F8FF',command=self.addTurma)
        self.btCadTurma.place(relx=0.70, rely=0.80)
       
    def selectDisciplina(self):
        self.lbDisciplina = Label(self.cont2_1, text= 'Disciplina:', width=8, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbDisciplina.place(relx=0.02, rely=0.25)
        self.entryDisciplina = ttk.Combobox(self.cont2_1,values=["Biologia",
                                                                 "Ed. Física",
                                                                 "Geografia",
                                                                 "Matemática",
                                                                 "Física",
                                                                 "História",
                                                                 "Português",
                                                                 "Química",
                                                                 "Ciências",
                                                                 "Filosofia",
                                                                 "Religião",
                                                                 "Sociologia"])
        self.entryDisciplina.place(relx=0.29, rely=0.25, relwidth=0.35)
      
    def selectEscola(self):
        self.lbEScola2 = Label(self.cont2_1, text= 'Escola:', width=6, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbEScola2.place(relx=0.02, rely=0.45)
        #banco de dados
        self.conectaDB()
        self.listar = self.cursor.execute("""SELECT nmEscola FROM escolas""")
        lista = self.listar.fetchall()
        self.desconectaBDusuarios()
        
        self.comboEntry = ttk.Combobox(self.cont2_1,values=lista)
        self.comboEntry.place(relx=0.29, rely=0.45, relwidth=0.60)

    """def botoestela2(self):       
        self.lbcod = Label(self.cont2_2, text='cod', bg=azul, fg=branco, font=('arial',8,'bold') )
        self.lbcod.place(relx=0.04, rely=0.34)
        self.entryCod = Entry(self.cont2_2)
        self.entryCod.place(relx=0.15, rely=0.34, relwidth=0.20)
        
        self.btDelEScola = Button(self.cont2_2, text='Del Escola', bg=vermelho, fg=branco,command=self.deleteEscola)
        self.btDelEScola.place(relx=0.40, rely=0.30)
        self.btDelTurma = Button(self.cont2_2, text='Del Turma', bg=vermelho, fg=branco,command=self.deleteTurma)
        self.btDelTurma.place(relx=0.70, rely=0.30)"""
  
    def deleteTurma(self):
        self.cod = self.entryCod.get()
        
        if self.cod.__len__() == 0:
            self.aviso(texto='ERRO!\nDigite um codigo\n válido!')
        else:
            try:
                self.conectaDB()
                self.cursor.execute("""DELETE FROM TURMAS WHERE codTurma = '{}'""".format(self.cod))
                self.connU.commit()
                self.desconectaBDusuarios()
                self.entryCod.delete(0,END)
                self.atualizaTurma()
                self.aviso2(texto='Turma deletada\ncom sucesso!')
            except sqlite3.OperationalError:
                self.aviso(texto='ERRO!\nVerifique os dados e\ntente novamente')
        
    #######################
    ##### ADICIONA TURMA NO BANCO
    def addTurma(self):
        self.nmTurma = self.entryTurma.get()
        self.disciplina = self.entryDisciplina.get()
        self.escola = self.comboEntry.get()
        self.professor = self.regID

        if self.nmTurma.__len__() == 0 or self.disciplina.__len__() == 0 or self.escola.__len__() == 0:
            self.aviso(texto='Por favor\nDigite todos os dados')
        else:
            self.conectaDB()
            self.cursor.execute("""INSERT INTO turmas (nmTurma, disciplina, escola, prof)
                        VALUES (?,?,?,?)""",(self.nmTurma, self.disciplina, self.escola, self.professor))
            self.connU.commit()
            self.desconectaBDusuarios()
            self.limpaTurma()
            self.atualizaTurma()

    def atualizaTurma(self):
        self.listaturma.delete(*self.listaturma.get_children())
        self.conectaDB()
        lista = self.cursor.execute(""" SELECT codTurma, nmTurma, disciplina, escola, prof FROM turmas
            ORDER BY codTurma ASC; """)
        for i in lista:
            self.listaturma.insert("", END, values=i)
        self.desconectaBDusuarios()
    
#########################################
##### JANELA DE CADASTRO DE NOVO USUÁRIO

    def telaCadastro(self):
        self.cadastro = Toplevel()
        self.cadastro.iconbitmap(pastaApp+"\\img/icon2.ico")
        self.cadastro.title('Cadastro')
        self.cadastro.geometry('400x300+250+100')
        self.cadastro.configure(background=azul)
        self.cadastro.transient(self.diario)
        self.frameCadastro()
        self.cadastro.focus_force()
        self.cadastro.grab_set()
    
    def frameCadastro(self):
        self.cont4 = Frame(self.cadastro, bg=branco)
        self.cont4.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        self.add = Button(self.cont4, text='Salvar', font=('arial','10'), width=10,
                                bg='#1E90FF', fg='#F8F8FF', command=self.addUsuario)
        self.add.place(relx=0.76, rely=0.84)

        # Labels e Entrys
        self.lbnome = Label(self.cont4, text='Nome completo:', width=12, bg=branco, fg=cinza, font=('arial',8,'italic','bold'))
        self.lbnome.place(relx=0.02, rely=0.05)
        self.entryNome = Entry(self.cont4)
        self.entryNome.place(relx=0.02, rely=0.12, relwidth=0.94)

        self.lbID = Label(self.cont4, text='Usuário:', width=6, bg=branco, fg=cinza, font=('arial',8,'italic','bold'))
        self.lbID.place(relx=0.02, rely=0.40)
        self.entryID = Entry(self.cont4)
        self.entryID.place(relx=0.02, rely=0.47, relwidth=0.26)

        self.lbSenha = Label(self.cont4, text='Senha:', width=5, bg=branco, fg=cinza, font=('arial',8,'italic','bold'))
        self.lbSenha.place(relx=0.66, rely=0.4)
        self.entrySenha = Entry(self.cont4)
        self.entrySenha.place(relx=0.66, rely=0.47,  relwidth=0.30)
    
    def addUsuario(self):
        self.nome = self.entryNome.get()
        self.id = self.entryID.get()
        self.senha = self.entrySenha.get()

        if self.nome.__len__() == 0:
            self.aviso(texto='ERRO!\nPor favor,\ninforme o seu\nnome completo!')
        elif self.id.__len__() == 0:
            self.aviso(texto='ERRO!\nPrecisamos da sua \nID de usuário')
        elif self.senha.__len__() == 0:
            self.aviso(texto='ERRO!\nPor favor,\n digite uma senha!')
        else:
            self.conectaDB()

            self.cursor.execute(""" INSERT INTO usuarios (nmUsuario, idUsuario, senhaUsuario)
                            VALUES(?, ?, ?)""", (self.nome, self.id, self.senha))
            self.connU.commit()
            self.desconectaBDusuarios()
            self.aviso2(texto='Usuário cadastrado \ncom sucesso!')

            self.limparTela()

#########################################
##### JANELA DE EDIÇÃO DE TURMAS
    def editaTurma(self, event):
        self.edTurma = Toplevel()
        self.edTurma.title('')
        self.edTurma.geometry('700x500+250+100')
        self.edTurma.configure(background=azul)
        self.edTurma.transient(self.telaPrincipal)
        self.edTurma.focus_force()
        self.edTurma.grab_set()
        #self.addAluno()

        #FRAMES
        self.cont5 = Frame(self.edTurma, bg= branco)
        self.cont5.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.20)
        self.cont5_5 = Frame(self.edTurma, bg= branco)
        self.cont5_5.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.20)

        self.cont6 = Frame(self.edTurma, bg= branco)
        self.cont6.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

        #BOTÕES
        self.btAddAluno = Button(self.cont5_5, text= "Novo Aluno", bg=azulEscuro, fg=branco, command=self.addAluno)
        self.btAddAluno.place(relx=0.35, rely=0.69)
        self.btEdAluno = Button(self.cont5, text= "Editar Aluno", bg=azulEscuro, fg=branco)
        self.btEdAluno.place(relx=0.101, rely=0.50)

        self.btFrequencia = Button(self.cont5, text= "Frequência", bg=azulEscuro, fg=branco)
        self.btFrequencia.place(relx=0.45, rely=0.40)

        self.btNotas = Button(self.cont5, text= "NOTAS", bg=azulEscuro, fg=branco)
        self.btNotas.place(relx=0.80, rely=0.40)

        #LABELS E ENTRYs
        self.lbNmAluno = Label(self.cont5_5, text="Nome",  width=11, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbNmAluno.place(relx=0.02, rely=0.06)
        self.entryNmAluno = Entry(self.cont5_5)
        self.entryNmAluno.place(relx=0.06, rely=0.25, relwidth=0.4)

        self.lbIdade = Label(self.cont5_5, text="Nascimento",  width=12, bg=branco, fg=cinza, font=('arial',8,'italic','bold') )
        self.lbIdade.place(relx=0.04, rely=0.5)
        self.entryIdade = Entry(self.cont5_5)
        self.entryIdade.place(relx=0.06, rely=0.69, relwidth=0.12)

        #Lista Alunos
        self.listalunos = ttk.Treeview(self.cont6, height=3, columns=('col1','col2','col3','col4'))
        self.listalunos.heading('#0',text='')
        self.listalunos.heading('#1',text='Nº')
        self.listalunos.heading('#2',text='Aluno')
        self.listalunos.heading('#3',text='Nascimento')
        self.listalunos.heading('#4',text='Média')

        self.listalunos.column('#0', width=5)
        self.listalunos.column('#1', width=20)
        self.listalunos.column('#2', width=250)
        self.listalunos.column('#3', width=50)
        self.listalunos.column('#4', width=100)
        self.listalunos.place(relx=0.01,rely=0.1,relwidth=0.95,relheight=0.85)

        self.atualizaAlunos()

    def addAluno(self):
        self.nmAluno = self.entryNmAluno.get()
        self.idadeAluno = self.entryIdade.get()
        
        if self.nmAluno.__len__() == 0:
            self.aviso(texto='Por favor\nDigite o nome \ndo Aluno!')        
        else:
            self.conectaDB()
            self.cursor.execute("""INSERT INTO alunos (nmAluno, idade)
                        VALUES (?,?)""",(self.nmAluno,self.idadeAluno))
            self.connU.commit()
            self.desconectaBDusuarios()
            self.entryNmAluno.delete(0,END), self.entryIdade.delete(0,END)
            self.atualizaAlunos()
    
    def atualizaAlunos(self):
        self.listalunos.delete(*self.listalunos.get_children())
        self.conectaDB()
        lista = self.cursor.execute(""" SELECT codAluno, nmAluno, idade  FROM Alunos
            ORDER BY nmAluno ASC; """)
        for i in lista:
            self.listalunos.insert("", END, values=i)
        self.desconectaBDusuarios()

#########################################
##### JANELA DE NOTIFICAÇÕES 

    def aviso(self, texto):
        self.telaErro = Toplevel()
        self.telaErro.title('ERROR')
        self.telaErro.configure(background=vermelho)
        self.telaErro.geometry('250x100+500+200')
        self.telaErro.resizable(False,False)
        self.telaErro.focus_force()
        self.telaErro.grab_set()
        
        self.contAviso = Frame(self.telaErro, bg=branco)
        self.contAviso.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
        self.lbAviso = Label(self.contAviso, text=texto,font=('verdana','10'), bg=branco ,width=20, height=15)
        self.lbAviso.pack()

    def aviso2(self, texto):
        self.telaviso = Toplevel()
        self.telaviso.title('')
        self.telaviso.configure(background='green')
        self.telaviso.geometry('250x100+500+200')
        self.telaviso.resizable(False,False)
        self.telaviso.focus_force()
        self.telaviso.grab_set()
        
        self.contAviso2 = Frame(self.telaviso, bg=branco)
        self.contAviso2.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
        self.lbAviso = Label(self.contAviso2, text=texto,font=('verdana','10'), bg=branco ,width=20, height=15)
        self.lbAviso.pack()

diario = Tk()
Janela()