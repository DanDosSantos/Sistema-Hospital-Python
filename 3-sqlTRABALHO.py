from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

# Configuração do banco de dados
engine = create_engine('sqlite:///server.db')

class Base(DeclarativeBase):
    pass

class Paciente(Base):
    __tablename__ = 'PACIENTE'
    id = Column('ID', Integer, primary_key=True)
    nome = Column('NOME', String(255))
    cpf = Column('CPF', String(255))
    idade = Column('IDADE', Integer)

class Medico(Base):
    __tablename__ = 'MEDICO'
    id = Column('ID', Integer, primary_key=True)
    nome = Column('NOME', String(255))
    crm = Column('CRM', String(255))
    especializacao = Column('ESPECIALIZACAO', String(255))

class Exame(Base):
    __tablename__ = 'EXAME'
    id = Column('ID', Integer, primary_key=True)
    id_medico = Column('ID_MEDICO', Integer, ForeignKey("MEDICO.ID"))
    id_paciente = Column('ID_PACIENTE', Integer, ForeignKey("PACIENTE.ID"))
    descricao = Column('DESCRICAO', String(255))
    resultado = Column('RESULTADO', String(255))

    medico = relationship("Medico")
    paciente = relationship("Paciente")

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_medico():
    while True:
        nome = input('Nome do Médico: ')
        if nome == '':
            break
        crm = input('Digite seu CRM: ')
        especializacao = input('Informe sua especialização: ')

        med = Medico(nome=nome, crm=crm, especializacao=especializacao)
        session.add(med)
    session.commit()

def cadastrar_paciente():
    while True:
        nome = input('Nome do Paciente: ')
        if nome == '':
            break
        cpf = input('Digite seu CPF: ')
        idade = int(input('Informe sua idade: '))

        pac = Paciente(nome=nome, cpf=cpf, idade=idade)
        session.add(pac)
    session.commit()

def cadastrar_exame():
    while True:
        nome_medico = input('Nome do médico: ')
        if nome_medico == '':
            break
        nome_paciente = input('Nome do paciente: ')
        descricao = input('Descrição: ')
        resultado = input('Resultado: ')

        medico = session.query(Medico).filter_by(nome=nome_medico).first()
        paciente = session.query(Paciente).filter_by(nome=nome_paciente).first()
        
        if not medico or not paciente:
            print('Médico ou paciente não encontrado!')
            continue

        exame = Exame(id_medico=medico.id, id_paciente=paciente.id, descricao=descricao, resultado=resultado)
        session.add(exame)
    session.commit()

def consultar_exames():
    nome_paciente = input('Digite o nome do paciente: ')
    paciente = session.query(Paciente).filter_by(nome=nome_paciente).first()
    if not paciente:
        print('Paciente não encontrado!')
        return

    exames = session.query(Exame).filter_by(id_paciente=paciente.id).all()
    print('-' * 40)
    for exame in exames:
        medico = session.query(Medico).filter_by(id=exame.id_medico).first()
        print(f'ID: {exame.id}, Médico: {medico.nome}, Paciente: {paciente.nome}, Descrição: {exame.descricao}, Resultado: {exame.resultado}')
    print('-' * 40)

while True:
    print('1 - Cadastrar Médico')
    print('2 - Cadastrar Paciente')
    print('3 - Cadastrar Exame')
    print('4 - Consultar Exames')
    print('5 - Sair')
    opcao = int(input('Escolha uma opção: '))
    match opcao:
        case 1:
            cadastrar_medico()
        case 2:
            cadastrar_paciente()
        case 3:
            cadastrar_exame()
        case 4:
            consultar_exames()
        case 5:
            break
        case _:
            print('Opção inválida')

# Fechar a sessão corretamente
session.close()