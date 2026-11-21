import mysql.connector
import random

try:
    # 1. CONEXÃO (Estabelecendo a ponte)
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SENHA", 
        database="sistema_marmitas"
    )
    cursor = conexao.cursor()

    print("Iniciando o Pipeline de ETL (Versão 2.0)...")

    # 2. EXTRAÇÃO (Buscando Clientes e o Cardápio)
    cursor.execute("SELECT id_cliente FROM clientes;")
    clientes_encontrados = cursor.fetchall() 
    
    # Nova Extração: Busca o ID e o Preço de cada prato disponível
    cursor.execute("SELECT id_prato, preco FROM pratos;")
    pratos_disponiveis = cursor.fetchall()
    
    if not clientes_encontrados or not pratos_disponiveis:
        print("Erro: Verifique se existem clientes e pratos cadastrados no banco.")
    else:
        print(f"Sucesso! {len(clientes_encontrados)} clientes e {len(pratos_disponiveis)} pratos encontrados.")
        print("Gerando pedidos com itens reais e somando os valores da conta...")

        # 3. TRANSFORMAÇÃO E CARGA
        for cliente in clientes_encontrados:
            id_do_cliente = cliente[0] 
            
            # Sorteia quantos pratos o cliente vai comprar (de 1 a 3 marmitas)
            qtd_itens = random.randint(1, 3)
            
            # Escolhe aleatoriamente os pratos para compor o pedido
            pratos_escolhidos = random.choices(pratos_disponiveis, k=qtd_itens)
            
            # Calcula o valor total SOMANDO os preços reais dos pratos sorteados
            # prato[1] é a coluna 'preco' que puxamos do banco de dados
            valor_da_compra = sum(prato[1] for prato in pratos_escolhidos)
            
            # A) Injeção na Tabela Fato (Pedidos) - A capa da nota fiscal
            sql_pedido = "INSERT INTO pedidos (id_cliente, status_pedido, valor_total) VALUES (%s, %s, %s)"
            valores_pedido = (id_do_cliente, "Entregue", round(valor_da_compra, 2))
            cursor.execute(sql_pedido, valores_pedido)
            
            # Recupera o ID do pedido que o MySQL acabou de gerar para anexar os itens
            id_do_pedido_gerado = cursor.lastrowid
            
            # B) Injeção na Tabela Associativa (Itens do Pedido) - A lista detalhada
            sql_item = "INSERT INTO itens_pedido (id_pedido, id_prato) VALUES (%s, %s)"
            for prato in pratos_escolhidos:
                id_do_prato = prato[0]
                cursor.execute(sql_item, (id_do_pedido_gerado, id_do_prato))

        # Regra de Ouro: Confirmar a gravação transacional ponta a ponta
        conexao.commit()
        print("Carga concluída! Os pedidos e os itens foram registrados com sucesso.")

except mysql.connector.Error as erro:
    print(f"Erro ao processar os dados: {erro}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão encerrada com segurança.")
