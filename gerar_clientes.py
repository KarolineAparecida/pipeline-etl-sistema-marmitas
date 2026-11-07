import mysql.connector
from faker import Faker

# Inicializa a biblioteca para gerar dados com padrão brasileiro
fake = Faker('pt_BR')

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="sistema_marmitas"
    )
    
    # O Cursor é o "entregador" que leva o comando do Python para o MySQL
    cursor = conexao.cursor()
    
    print("Iniciando a injeção de clientes...")
    
    # O Loop: Vai repetir a criação e injeção 5 vezes
    for _ in range(5):
        nome = fake.first_name()
        sobrenome = fake.last_name()
        email = f"{nome.lower()}.{sobrenome.lower()}@emailfalso.com"
        senha = "senha_segura_123"
        rua = fake.street_name()
        numero = fake.building_number()
        
        # A instrução SQL. O "%s" funciona como um espaço em branco seguro.
        sql = "INSERT INTO clientes (nome, sobrenome, email, senha, rua, numero) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nome, sobrenome, email, senha, rua, numero)
        
        # O entregador leva os dados
        cursor.execute(sql, valores)

    # REGRA DE OURO DA INJEÇÃO: Confirmar a gravação no banco
    conexao.commit()
    
    print(f"Sucesso! 5 clientes foram cadastrados automaticamente.")

except mysql.connector.Error as erro:
    print(f"Erro ao injetar dados: {erro}")
    
finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()