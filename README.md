# 🍱 Pipeline ETL & Arquitetura de Dados: Sistema de Delivery de Marmitas

Projeto prático de **Engenharia de Dados** focado na construção de um banco de dados relacional (OLTP), automação de ingestão de dados sintéticos via Python (Pipeline ETL) e extração de indicadores gerenciais (KPIs) com SQL.

---

## 🎯 1. Objetivo de Negócio (Visão Analítica)
Simular a infraestrutura de dados de uma empresa de *Meal Prep* (venda de marmitas e planos de assinatura). O objetivo principal é garantir a **integridade referencial** da operação — impedindo falhas como vendas para clientes inexistentes ou pedidos sem vínculo cadastral — e fornecer consultas analíticas rápidas sobre faturamento e comportamento de consumo para tomada de decisão.

---

## 🗄️ 2. Arquitetura do Banco de Dados (MySQL)
O modelo relacional foi desenhado separando dados cadastrais estáticos das movimentações financeiras:

* **Tabelas de Dimensão (Cadastros Base):**
  * `planos`: Regras comerciais dos pacotes de refeições.
  * `clientes`: Dados cadastrais, credenciais e endereço de entrega, com restrição `UNIQUE` no e-mail para evitar duplicidades.
  * `pratos`: Catálogo de produtos contendo informações nutricionais detalhadas (calorias, peso, proteínas, carboidratos, gorduras e alergênicos).
  * `motoristas`: Cadastro dos entregadores responsáveis pela logística.
* **Tabelas Fato e de Junção (Transacionais):**
  * `assinaturas`: Conecta clientes aos planos contratados (`FOREIGN KEY`).
  * `pedidos`: Registra as vendas realizadas, status da entrega, valor total e auditoria temporal automática (`TIMESTAMP`).
  * `itens_pedido`: Tabela associativa que detalha quais pratos e quantidades compõem cada pedido.

---

## ⚙️ 3. Pipeline de Dados (Python ETL)
A automação do fluxo de dados foi construída em Python seguindo o padrão **PEP 8** e **PEP 249 (DB-API 2.0)**:

1. **Conexão Segura (`conexao_banco.py`):** Valida a comunicação entre o ambiente Python e o servidor MySQL utilizando blocos de tratamento de exceções (`try/except/finally`).
2. **Geração de Dados e Ingestão (`gerar_clientes.py`):** Utiliza a biblioteca `Faker` configurada para o idioma local (`pt_BR`) para simular o cadastro de clientes reais e popular a base de dados.
3. **Pipeline ETL de Vendas (`gerar_pedidos.py`):**
   * **Extração (*Extract*):** Consulta o banco de dados para listar apenas os IDs de clientes ativos e válidos.
   * **Transformação (*Transform*):** Gera transações financeiras aleatórias e atribui o status operacional do pedido.
   * **Carga (*Load*):** Insere os registros na tabela fato utilizando consultas parametrizadas (`%s`) para prevenção contra *SQL Injection* e confirma a transação com `.commit()` (garantia ACID).

---

## 📊 4. Business Intelligence & Analytics (SQL)
Com o banco populado pelo pipeline, foram desenvolvidas consultas analíticas utilizando funções de agregação e cruzamento de tabelas:
* **Resumo Financeiro:** Cálculo do volume total de vendas (`COUNT`), faturamento bruto (`SUM`) e ticket médio por pedido (`AVG`).
* ** Identificação de Clientes VIP:** Cruzamento entre as tabelas `clientes` e `pedidos` utilizando `INNER JOIN` e ordenação decrescente (`ORDER BY ... DESC`) para ranquear os clientes de maior valor para ações de Marketing.

---

## 🚀 5. Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.x e MySQL Server instalados.

### Passo a Passo
1. Instale as dependências listadas no projeto:
   ```bash
   pip install -r requirements.txt

   python gerar_clientes.py
python gerar_pedidos.py
