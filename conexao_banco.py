import mysql.connector

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="sistema_marmitas"
    )
    if conexao.is_connected():
        print("Conexão com o sistema de marmitas realizada com sucesso!")
        conexao.close() # Boa prática: fechar após usar
        
except mysql.connector.Error as erro:
    print(f"Erro prático na conexão: {erro}")