# E-Shop Brasil - Aplicação Prática de Banco de Dados e Big Data

## 1. Introdução

Este projeto foi desenvolvido para a empresa fictícia **E-Shop Brasil**, uma plataforma de comércio eletrônico de grande porte que atende milhões de clientes e processa milhares de pedidos diariamente.

O objetivo é demonstrar, de forma prática, como tecnologias de banco de dados NoSQL e Big Data podem auxiliar na gestão de dados, personalização da experiência do cliente, controle de pedidos e análise de informações logísticas.

A aplicação utiliza:

- Docker
- MongoDB
- Python
- Streamlit
- Pandas

## 2. Objetivos do Projeto

A solução tem como objetivos principais:

- Simular a gestão de dados de clientes, produtos e pedidos;
- Inserir dados no banco MongoDB;
- Consultar dados por meio de uma interface gráfica;
- Editar e excluir registros;
- Concatenar informações de diferentes coleções;
- Visualizar indicadores básicos em um dashboard;
- Demonstrar o uso de tecnologias modernas aplicadas ao contexto de Big Data.

## 3. Tecnologias Utilizadas

### Docker

Utilizado para criar containers e facilitar a execução do ambiente da aplicação.

### MongoDB

Banco de dados NoSQL documental utilizado para armazenar os dados da E-Shop Brasil.

### Streamlit

Framework Python utilizado para criar a interface gráfica da aplicação.

### Pandas

Biblioteca utilizada para manipulação, análise e concatenação dos dados.

## 4. Estrutura do Projeto

```txt
eshop_brasil_bigdata/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
└── exemplos/
```

## 5. Funcionalidades da Aplicação

A aplicação possui as seguintes funcionalidades:

### Inserção de Dados

Permite cadastrar clientes, produtos e pedidos diretamente pela interface gráfica.

### Consulta de Dados

Permite visualizar e pesquisar registros armazenados no MongoDB.

### Edição de Dados

Permite alterar valores de registros existentes a partir do ID do documento.

### Exclusão de Dados

Permite remover registros do banco de dados.

### Concatenação de Dados

Combina informações de clientes, produtos e pedidos para gerar uma visão integrada.

### Dashboard

Exibe indicadores gerais, como:

- Total de clientes cadastrados;
- Total de produtos cadastrados;
- Total de pedidos registrados;
- Pedidos por status;
- Faturamento total simulado.

## 6. Como Executar o Projeto

### Pré-requisitos

Antes de executar, é necessário ter instalado:

- Docker
- Docker Compose

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/seu-usuario/eshop-brasil-bigdata.git
cd eshop-brasil-bigdata
```

### Passo 2: Executar com Docker Compose

```bash
docker-compose up --build
```

### Passo 3: Acessar a aplicação

Abra o navegador e acesse:

```txt
http://localhost:8501
```

## 7. Como Testar

Após abrir a aplicação:

1. Acesse o menu **Carga de Dados de Exemplo**;
2. Clique em **Carregar Dados de Exemplo**;
3. Vá até **Dashboard** para visualizar os indicadores;
4. Acesse **Consultar Dados** para visualizar clientes, produtos e pedidos;
5. Teste as funções de edição e exclusão;
6. Acesse **Concatenação de Dados** para visualizar os dados combinados.

## 8. Relação com Big Data

Embora a aplicação seja uma simulação acadêmica, ela representa conceitos fundamentais de Big Data:

- Armazenamento flexível com NoSQL;
- Manipulação de dados semiestruturados;
- Escalabilidade por meio de containers;
- Consultas e visualização de dados;
- Integração de dados de múltiplas fontes;
- Apoio à tomada de decisão.

## 9. Segurança e Privacidade

Em um ambiente real, a E-Shop Brasil deveria aplicar práticas como:

- Criptografia de dados sensíveis;
- Mascaramento de dados pessoais;
- Controle de acesso por perfil;
- Autenticação forte;
- Auditoria de acessos;
- Conformidade com a LGPD.

## 10. Conclusão

O projeto demonstra como MongoDB, Docker e Streamlit podem ser utilizados para criar uma solução prática de gestão e análise de dados em um cenário de comércio eletrônico.

A proposta atende aos requisitos de inserção, manipulação, consulta, exclusão, concatenação e visualização de dados, simulando uma aplicação voltada à gestão de informações da E-Shop Brasil.
