import mysql.connector

try:
    # 1. CONEXÃO
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MINHASENHA",  # Coloque a sua senha do MySQL aqui
        database="sistema_marmitas"
    )
    cursor = conexao.cursor()

    # 2. CARDÁPIO (Lista com os novos pratos)
    # Ordem: nome, descricao, calorias, peso, proteinas, carboidratos, gorduras, alergenicos, preco
    novos_pratos = [
        ("Patinho Moído com Purê de Mandioquinha", "Carne magra temperada com ervas e purê cremoso", 410, 350.00, 38, 42, 10, "Nenhum", 32.90),
        ("Salmão Grelhado com Arroz Integral", "Filé de salmão ao molho de maracujá com brócolis", 480, 350.00, 35, 38, 18, "Peixe", 49.90),
        ("Strogonoff Fit de Frango", "Frango em cubos ao molho de biomassa com arroz integral", 390, 320.00, 36, 35, 9, "Lactose", 29.90),
        ("Escondidinho Vegano de Grão-de-Bico", "Purê de abóbora cabotiá com recheio de grão-de-bico", 340, 350.00, 16, 48, 8, "Nenhum", 28.50),
        ("Tilápia Assada com Legumes", "Filé de tilápia com cenoura, abobrinha e batata rústica", 310, 300.00, 34, 25, 7, "Peixe", 36.00),
        ("Sobrecoxa Assada com Cuscuz Marroquino", "Sobrecoxa desossada com cuscuz e legumes salteados", 450, 350.00, 32, 44, 15, "Glúten", 31.50)
    ]

    # 3. CARGA NO BANCO
    sql = """
        INSERT INTO pratos 
        (nome, descricao, calorias, peso, proteinas, carboidratos, gorduras, alergenicos, preco) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # executemany insere a lista inteira de uma só vez
    cursor.executemany(sql, novos_pratos)
    conexao.commit()

    print(f"Sucesso! {cursor.rowcount} novos pratos foram cadastrados no cardápio.")

except mysql.connector.Error as erro:
    print(f"Erro ao cadastrar os pratos: {erro}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão encerrada com segurança.")
    
