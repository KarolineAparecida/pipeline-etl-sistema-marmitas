import mysql.connector
import random

try:
    # 1. CONEXÃO (Estabelecendo a ponte)
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="sistema_marmitas"
    )
    cursor = conexao.cursor()

    print("Iniciando o Pipeline de ETL...")

    # 2. EXTRAÇÃO (Extract - Letra E do ETL)
    # O Python vai lá no MySQL e busca quem são os clientes cadastrados
    cursor.execute("SELECT id_cliente FROM clientes;")
    clientes_encontrados = cursor.fetchall() 
    
    if not clientes_encontrados:
        print("Nenhum cliente encontrado. Verifique a tabela 'clientes'.")
    else:
        print(f"Sucesso na Extração! {len(clientes_encontrados)} clientes encontrados.")
        print("Iniciando a geração de pedidos...")

        # 3. TRANSFORMAÇÃO E CARGA (Transform & Load - Letras T e L)
        # Para cada cliente que o Python encontrou, ele vai gerar um pedido novo
        for cliente in clientes_encontrados:
            id_do_cliente = cliente[0] 
            
            # Sorteia um valor de conta entre 50 e 250 reais para ficar realista
            valor_da_compra = random.uniform(50.0, 250.0) 
            
            # Prepara a injeção na Tabela Fato (Pedidos)
            # O status será "Entregue" e o motorista ainda fica vazio (NULL) pela nossa regra de negócio
            sql_pedido = "INSERT INTO pedidos (id_cliente, status_pedido, valor_total) VALUES (%s, %s, %s)"
            valores_pedido = (id_do_cliente, "Entregue", round(valor_da_compra, 2))
            
            cursor.execute(sql_pedido, valores_pedido)

        # Regra de Ouro: Confirmar a gravação no banco
        conexao.commit()
        print("Carga concluída! Os pedidos foram registrados no banco com sucesso.")

except mysql.connector.Error as erro:
    print(f"Erro ao processar os dados: {erro}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão encerrada com segurança.")