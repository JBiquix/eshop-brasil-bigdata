import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="E-Shop Brasil - Big Data",
    page_icon="🛒",
    layout="wide"
)

@st.cache_resource
def conectar_mongodb():
    client = MongoClient("mongodb://mongo:27017/")
    db = client["eshop_brasil"]
    return db

db = conectar_mongodb()
clientes = db["clientes"]
produtos = db["produtos"]
pedidos = db["pedidos"]

st.title("🛒 E-Shop Brasil - Gestão e Análise de Dados")
st.markdown("Aplicação prática com **Streamlit + MongoDB + Docker** para simular manipulação e análise de dados em um e-commerce.")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Inserir Dados",
        "Consultar Dados",
        "Editar Dados",
        "Excluir Dados",
        "Concatenação de Dados",
        "Carga de Dados de Exemplo"
    ]
)

def carregar_dataframe(collection):
    dados = list(collection.find())
    if not dados:
        return pd.DataFrame()
    for item in dados:
        item["_id"] = str(item["_id"])
    return pd.DataFrame(dados)

if menu == "Dashboard":
    st.header("📊 Dashboard Geral")

    total_clientes = clientes.count_documents({})
    total_produtos = produtos.count_documents({})
    total_pedidos = pedidos.count_documents({})

    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes cadastrados", total_clientes)
    col2.metric("Produtos cadastrados", total_produtos)
    col3.metric("Pedidos registrados", total_pedidos)

    df_pedidos = carregar_dataframe(pedidos)

    if not df_pedidos.empty:
        st.subheader("📦 Pedidos por Status")
        status_count = df_pedidos["status"].value_counts().reset_index()
        status_count.columns = ["Status", "Quantidade"]
        st.bar_chart(status_count.set_index("Status"))

        st.subheader("💰 Valor total de pedidos")
        if "valor_total" in df_pedidos.columns:
            st.metric("Faturamento simulado", f"R$ {df_pedidos['valor_total'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

if menu == "Inserir Dados":
    st.header("➕ Inserir Dados")

    tipo = st.selectbox("Escolha o tipo de dado", ["Cliente", "Produto", "Pedido"])

    if tipo == "Cliente":
        nome = st.text_input("Nome do cliente")
        email = st.text_input("E-mail")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        preferencia = st.text_input("Preferência de compra")

        if st.button("Inserir Cliente"):
            clientes.insert_one({
                "nome": nome,
                "email": email,
                "cidade": cidade,
                "estado": estado,
                "preferencia": preferencia,
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("Cliente inserido com sucesso!")

    elif tipo == "Produto":
        nome = st.text_input("Nome do produto")
        categoria = st.text_input("Categoria")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        estoque = st.number_input("Estoque", min_value=0, step=1)

        if st.button("Inserir Produto"):
            produtos.insert_one({
                "nome": nome,
                "categoria": categoria,
                "preco": preco,
                "estoque": estoque,
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("Produto inserido com sucesso!")

    elif tipo == "Pedido":
        cliente_email = st.text_input("E-mail do cliente")
        produto_nome = st.text_input("Nome do produto")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        valor_total = st.number_input("Valor total", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Pendente", "Em transporte", "Entregue", "Cancelado"])

        if st.button("Inserir Pedido"):
            pedidos.insert_one({
                "cliente_email": cliente_email,
                "produto_nome": produto_nome,
                "quantidade": quantidade,
                "valor_total": valor_total,
                "status": status,
                "data_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("Pedido inserido com sucesso!")

if menu == "Consultar Dados":
    st.header("🔎 Consultar Dados")

    colecao_nome = st.selectbox("Escolha a coleção", ["Clientes", "Produtos", "Pedidos"])
    termo = st.text_input("Pesquisar por palavra-chave")

    colecao = {"Clientes": clientes, "Produtos": produtos, "Pedidos": pedidos}[colecao_nome]
    df = carregar_dataframe(colecao)

    if df.empty:
        st.warning("Nenhum dado encontrado.")
    else:
        if termo:
            df_filtrado = df[df.apply(lambda row: row.astype(str).str.contains(termo, case=False).any(), axis=1)]
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

if menu == "Editar Dados":
    st.header("✏️ Editar Dados")

    colecao_nome = st.selectbox("Escolha a coleção para edição", ["Clientes", "Produtos", "Pedidos"])
    colecao = {"Clientes": clientes, "Produtos": produtos, "Pedidos": pedidos}[colecao_nome]
    df = carregar_dataframe(colecao)

    if df.empty:
        st.warning("Nenhum registro disponível para edição.")
    else:
        st.dataframe(df, use_container_width=True)
        id_registro = st.text_input("Informe o ID do registro que deseja editar")
        campo = st.text_input("Campo que deseja alterar")
        novo_valor = st.text_input("Novo valor")

        if st.button("Atualizar Registro"):
            try:
                colecao.update_one(
                    {"_id": ObjectId(id_registro)},
                    {"$set": {campo: novo_valor}}
                )
                st.success("Registro atualizado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")

if menu == "Excluir Dados":
    st.header("🗑️ Excluir Dados")

    colecao_nome = st.selectbox("Escolha a coleção para exclusão", ["Clientes", "Produtos", "Pedidos"])
    colecao = {"Clientes": clientes, "Produtos": produtos, "Pedidos": pedidos}[colecao_nome]
    df = carregar_dataframe(colecao)

    if df.empty:
        st.warning("Nenhum registro disponível para exclusão.")
    else:
        st.dataframe(df, use_container_width=True)
        id_registro = st.text_input("Informe o ID do registro que deseja excluir")

        if st.button("Excluir Registro"):
            try:
                colecao.delete_one({"_id": ObjectId(id_registro)})
                st.success("Registro excluído com sucesso!")
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")

if menu == "Concatenação de Dados":
    st.header("🔗 Concatenação de Dados")

    st.markdown("Nesta etapa, os dados de clientes, pedidos e produtos são combinados para gerar uma visão integrada.")

    df_clientes = carregar_dataframe(clientes)
    df_pedidos = carregar_dataframe(pedidos)
    df_produtos = carregar_dataframe(produtos)

    if df_clientes.empty or df_pedidos.empty or df_produtos.empty:
        st.warning("Cadastre ou carregue dados de exemplo antes de realizar a concatenação.")
    else:
        df_merged = df_pedidos.merge(df_clientes, left_on="cliente_email", right_on="email", how="left", suffixes=("_pedido", "_cliente"))
        df_merged = df_merged.merge(df_produtos, left_on="produto_nome", right_on="nome", how="left", suffixes=("", "_produto"))

        colunas_exibir = [
            "cliente_email", "nome_cliente", "cidade", "estado",
            "produto_nome", "categoria", "quantidade", "valor_total", "status"
        ]
        colunas_existentes = [col for col in colunas_exibir if col in df_merged.columns]

        st.dataframe(df_merged[colunas_existentes], use_container_width=True)

if menu == "Carga de Dados de Exemplo":
    st.header("📥 Carga de Dados de Exemplo")

    st.markdown("Clique no botão abaixo para inserir dados fictícios simulando clientes, produtos e pedidos da E-Shop Brasil.")

    if st.button("Carregar Dados de Exemplo"):
        clientes.delete_many({})
        produtos.delete_many({})
        pedidos.delete_many({})

        clientes.insert_many([
            {"nome": "Ana Souza", "email": "ana@email.com", "cidade": "São Paulo", "estado": "SP", "preferencia": "Eletrônicos"},
            {"nome": "Carlos Lima", "email": "carlos@email.com", "cidade": "Manaus", "estado": "AM", "preferencia": "Moda"},
            {"nome": "Mariana Alves", "email": "mariana@email.com", "cidade": "Recife", "estado": "PE", "preferencia": "Casa"},
            {"nome": "João Pereira", "email": "joao@email.com", "cidade": "Monte Mor", "estado": "SP", "preferencia": "Games"},
            {"nome": "Fernanda Rocha", "email": "fernanda@email.com", "cidade": "Curitiba", "estado": "PR", "preferencia": "Beleza"}
        ])

        produtos.insert_many([
            {"nome": "Notebook Gamer", "categoria": "Eletrônicos", "preco": 4500.00, "estoque": 15},
            {"nome": "Camiseta Premium", "categoria": "Moda", "preco": 89.90, "estoque": 100},
            {"nome": "Cafeteira Elétrica", "categoria": "Casa", "preco": 249.90, "estoque": 40},
            {"nome": "Mouse Gamer", "categoria": "Games", "preco": 159.90, "estoque": 80},
            {"nome": "Kit Skincare", "categoria": "Beleza", "preco": 199.90, "estoque": 60}
        ])

        pedidos.insert_many([
            {"cliente_email": "ana@email.com", "produto_nome": "Notebook Gamer", "quantidade": 1, "valor_total": 4500.00, "status": "Entregue", "data_pedido": "2026-05-01"},
            {"cliente_email": "carlos@email.com", "produto_nome": "Camiseta Premium", "quantidade": 2, "valor_total": 179.80, "status": "Em transporte", "data_pedido": "2026-05-03"},
            {"cliente_email": "mariana@email.com", "produto_nome": "Cafeteira Elétrica", "quantidade": 1, "valor_total": 249.90, "status": "Pendente", "data_pedido": "2026-05-05"},
            {"cliente_email": "joao@email.com", "produto_nome": "Mouse Gamer", "quantidade": 3, "valor_total": 479.70, "status": "Entregue", "data_pedido": "2026-05-08"},
            {"cliente_email": "fernanda@email.com", "produto_nome": "Kit Skincare", "quantidade": 1, "valor_total": 199.90, "status": "Cancelado", "data_pedido": "2026-05-10"}
        ])

        st.success("Dados de exemplo carregados com sucesso!")
