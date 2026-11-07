create database sistema_marmitas;
use sistema_marmitas;

create table planos (
 id_plano int auto_increment primary key,
 nome varchar(50) not null,
 qtd_refeicoes int not null,
 preco decimal(10, 2) not null
 );
 
 create table clientes (
 id_cliente int auto_increment primary key,
 nome varchar(50) not null,
 sobrenome varchar(100) not null,
 email varchar(100) unique not null,
 telefone varchar(20),
 senha varchar(255) not null,
 cidade varchar(50),
 estado char(2),
 cep varchar(10)
 );
CREATE TABLE pratos (
    id_prato INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    calorias INT NOT NULL,
    peso DECIMAL(10,2) NOT NULL
);
 alter table pratos
 add column proteinas int not null,
 add column carboidratos int not null,
 add column gorduras int not null,
 add column alergenicos varchar(255);
 create table motoristas (
  id_motoristas int auto_increment primary key,
  nome varchar(60) not null,
  telefone varchar(20) not null
  );
 create table assinaturas (
  id_assinatura int auto_increment primary key,
  status_assinatura varchar(20) not null,
  id_cliente int not null,
  id_plano int not null,
  foreign key (id_cliente) references clientes(id_cliente),
  foreign key (id_plano) references planos(id_plano)
  );
 create table pedidos (
  id_pedido int auto_increment primary key,
  id_cliente int not null,
  id_motorista int,
  status_pedido varchar(50) not null,
  valor_total decimal(10,2) not null,
  data_criacao timestamp default current_timestamp,
  data_atualizacao timestamp default current_timestamp on update current_timestamp,
  foreign key (id_cliente) references clientes(id_cliente),
  foreign key (id_motorista) references motoristas(id_motoristas)
  );
 alter table clientes
 add column rua varchar(150) not null,
 add column numero varchar(20) not null,
 add column complemento varchar(50);
 
 create table itens_pedidos (
 id_item int auto_increment primary key,
 id_pedido int not null,
 id_prato int not null,
 quantidade int not null,
 foreign key (id_pedido) references pedidos(id_pedido),
 foreign key (id_prato) references pratos(id_prato)
 );
 INSERT INTO clientes (nome, sobrenome, email, senha, rua, numero)
VALUES ('Carlos', 'Ferreira', 'carlos.ferreira@email.com', 'senhaSegura123', 'Rua Principal', '123');
 DESCRIBE planos;
INSERT INTO planos (nome, preco, qtd_refeicoes)
VALUES ('Plano Fit Mensal', 350.00, 10);
INSERT INTO pratos (nome, descricao, calorias, peso, proteinas, carboidratos, gorduras, alergenicos)
VALUES ('Frango com Batata Doce', 'Marmita clássica de baixa caloria', 350, 300.00, 40, 30, 5, 'Nenhum');
SELECT * FROM clientes;
SELECT * FROM pedidos;
SELECT 
    clientes.nome, 
    clientes.email, 
    pedidos.valor_total, 
    pedidos.data_criacao
FROM clientes
INNER JOIN pedidos 
    ON clientes.id_cliente = pedidos.id_cliente
ORDER BY pedidos.valor_total DESC;

 