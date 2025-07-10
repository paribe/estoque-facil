import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import os
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(
    page_title="Estoque Fácil",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema escuro
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2e5984 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    
    .alert-low {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Função para inicializar o banco de dados
@st.cache_resource
def init_database():
    conn = sqlite3.connect('estoque_facil.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Criar tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            estoque_minimo INTEGER NOT NULL DEFAULT 0,
            ativo BOOLEAN DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criar tabela de movimentações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            produto_id INTEGER,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    conn.commit()
    return conn

# Função para obter dados dos produtos
@st.cache_data
def get_produtos():
    conn = init_database()
    query = '''
        SELECT id, nome, descricao, categoria, preco, quantidade, estoque_minimo, 
               ativo, criado_em, atualizado_em
        FROM produtos 
        WHERE ativo = 1
        ORDER BY nome
    '''
    df = pd.read_sql_query(query, conn)
    return df

# Função para obter estatísticas
@st.cache_data
def get_estatisticas():
    conn = init_database()
    cursor = conn.cursor()
    
    # Total de produtos
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = 1")
    total_produtos = cursor.fetchone()[0]
    
    # Produtos com estoque baixo
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = 1 AND quantidade <= estoque_minimo")
    produtos_baixo_estoque = cursor.fetchone()[0]
    
    # Valor total do estoque
    cursor.execute("SELECT SUM(preco * quantidade) FROM produtos WHERE ativo = 1")
    valor_total = cursor.fetchone()[0] or 0
    
    # Produtos esgotados
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = 1 AND quantidade = 0")
    produtos_esgotados = cursor.fetchone()[0]
    
    return {
        'total_produtos': total_produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'valor_total': valor_total,
        'produtos_esgotados': produtos_esgotados
    }

# Função para adicionar produto
def adicionar_produto(nome, descricao, categoria, preco, quantidade, estoque_minimo):
    conn = init_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, categoria, preco, quantidade, estoque_minimo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, categoria, preco, quantidade, estoque_minimo))
        
        produto_id = cursor.lastrowid
        
        # Adicionar movimentação inicial se houver quantidade
        if quantidade > 0:
            cursor.execute('''
                INSERT INTO movimentacoes (tipo, quantidade, produto_id, observacao)
                VALUES (?, ?, ?, ?)
            ''', ('ENTRADA', quantidade, produto_id, 'Estoque inicial'))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao adicionar produto: {str(e)}")
        return False

# Função para editar produto
def editar_produto(produto_id, nome, descricao, categoria, preco, quantidade, estoque_minimo):
    conn = init_database()
    cursor = conn.cursor()
    
    try:
        # Obter quantidade anterior
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        quantidade_anterior = cursor.fetchone()[0]
        
        # Atualizar produto
        cursor.execute('''
            UPDATE produtos 
            SET nome = ?, descricao = ?, categoria = ?, preco = ?, 
                quantidade = ?, estoque_minimo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (nome, descricao, categoria, preco, quantidade, estoque_minimo, produto_id))
        
        # Registrar movimentação se houve mudança na quantidade
        if quantidade != quantidade_anterior:
            diferenca = quantidade - quantidade_anterior
            if diferenca > 0:
                cursor.execute('''
                    INSERT INTO movimentacoes (tipo, quantidade, produto_id, observacao)
                    VALUES (?, ?, ?, ?)
                ''', ('ENTRADA', diferenca, produto_id, 'Ajuste de estoque'))
            else:
                cursor.execute('''
                    INSERT INTO movimentacoes (tipo, quantidade, produto_id, observacao)
                    VALUES (?, ?, ?, ?)
                ''', ('SAIDA', abs(diferenca), produto_id, 'Ajuste de estoque'))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao editar produto: {str(e)}")
        return False

# Função para remover produto (soft delete)
def remover_produto(produto_id):
    conn = init_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao remover produto: {str(e)}")
        return False

# Função para obter movimentações
@st.cache_data
def get_movimentacoes(produto_id=None):
    conn = init_database()
    if produto_id:
        query = '''
            SELECT m.*, p.nome as produto_nome
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE m.produto_id = ?
            ORDER BY m.criado_em DESC
        '''
        df = pd.read_sql_query(query, conn, params=(produto_id,))
    else:
        query = '''
            SELECT m.*, p.nome as produto_nome
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            ORDER BY m.criado_em DESC
            LIMIT 50
        '''
        df = pd.read_sql_query(query, conn)
    return df

# Página principal (Dashboard)
def dashboard():
    st.markdown('<div class="main-header"><h1>📦 Estoque Fácil - Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Obter estatísticas
    stats = get_estatisticas()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Produtos",
            value=stats['total_produtos'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Estoque Baixo",
            value=stats['produtos_baixo_estoque'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="Valor Total",
            value=f"R$ {stats['valor_total']:,.2f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Produtos Esgotados",
            value=stats['produtos_esgotados'],
            delta=None
        )
    
    # Alertas
    if stats['produtos_baixo_estoque'] > 0:
        st.markdown(f'''
        <div class="alert-low">
            <strong>⚠️ Atenção!</strong> Você tem {stats['produtos_baixo_estoque']} produto(s) com estoque baixo.
        </div>
        ''', unsafe_allow_html=True)
    
    if stats['produtos_esgotados'] > 0:
        st.markdown(f'''
        <div class="alert-danger">
            <strong>🚨 Alerta!</strong> Você tem {stats['produtos_esgotados']} produto(s) esgotado(s).
        </div>
        ''', unsafe_allow_html=True)
    
    # Gráficos
    df_produtos = get_produtos()
    
    if not df_produtos.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Produtos por Categoria")
            categoria_count = df_produtos['categoria'].value_counts()
            fig_categoria = px.pie(
                values=categoria_count.values,
                names=categoria_count.index,
                title="Distribuição por Categoria"
            )
            st.plotly_chart(fig_categoria, use_container_width=True)
        
        with col2:
            st.subheader("📈 Status do Estoque")
            df_produtos['status'] = df_produtos.apply(lambda row: 
                'Esgotado' if row['quantidade'] == 0 
                else 'Baixo' if row['quantidade'] <= row['estoque_minimo']
                else 'Normal', axis=1)
            
            status_count = df_produtos['status'].value_counts()
            colors = {'Esgotado': '#FF6B6B', 'Baixo': '#FFD93D', 'Normal': '#6BCF7F'}
            
            fig_status = px.bar(
                x=status_count.index,
                y=status_count.values,
                color=status_count.index,
                color_discrete_map=colors,
                title="Status do Estoque"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Tabela de produtos com estoque baixo
        st.subheader("🔔 Produtos com Estoque Baixo")
        produtos_baixo = df_produtos[df_produtos['quantidade'] <= df_produtos['estoque_minimo']]
        
        if not produtos_baixo.empty:
            st.dataframe(
                produtos_baixo[['nome', 'categoria', 'quantidade', 'estoque_minimo', 'preco']],
                use_container_width=True
            )
        else:
            st.success("🎉 Nenhum produto com estoque baixo!")

# Página de produtos
def produtos():
    st.markdown('<div class="main-header"><h1>📦 Gerenciar Produtos</h1></div>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_nome = st.text_input("🔍 Buscar por nome:")
    
    with col2:
        categorias = ['Todos', 'Eletrônicos', 'Roupas', 'Casa e Decoração', 'Esporte e Lazer', 
                     'Livros', 'Alimentação', 'Beleza e Cuidados', 'Automotivo', 'Ferramentas', 'Outros']
        filtro_categoria = st.selectbox("📂 Categoria:", categorias)
    
    with col3:
        filtro_status = st.selectbox("📊 Status:", ['Todos', 'Normal', 'Estoque Baixo', 'Esgotado'])
    
    # Obter produtos
    df_produtos = get_produtos()
    
    if not df_produtos.empty:
        # Aplicar filtros
        if filtro_nome:
            df_produtos = df_produtos[df_produtos['nome'].str.contains(filtro_nome, case=False, na=False)]
        
        if filtro_categoria != 'Todos':
            df_produtos = df_produtos[df_produtos['categoria'] == filtro_categoria.lower()]
        
        if filtro_status != 'Todos':
            if filtro_status == 'Normal':
                df_produtos = df_produtos[df_produtos['quantidade'] > df_produtos['estoque_minimo']]
            elif filtro_status == 'Estoque Baixo':
                df_produtos = df_produtos[
                    (df_produtos['quantidade'] <= df_produtos['estoque_minimo']) & 
                    (df_produtos['quantidade'] > 0)
                ]
            elif filtro_status == 'Esgotado':
                df_produtos = df_produtos[df_produtos['quantidade'] == 0]
        
        # Adicionar status e formatação
        df_produtos['status'] = df_produtos.apply(lambda row: 
            '🔴 Esgotado' if row['quantidade'] == 0 
            else '🟡 Baixo' if row['quantidade'] <= row['estoque_minimo']
            else '🟢 Normal', axis=1)
        
        df_produtos['preco_formatado'] = df_produtos['preco'].apply(lambda x: f"R$ {x:,.2f}")
        
        # Mostrar produtos
        st.subheader(f"📋 Produtos Encontrados: {len(df_produtos)}")
        
        if not df_produtos.empty:
            # Configurar editor de dados
            edited_df = st.data_editor(
                df_produtos[['nome', 'categoria', 'preco_formatado', 'quantidade', 'estoque_minimo', 'status']],
                column_config={
                    'nome': 'Nome',
                    'categoria': 'Categoria',
                    'preco_formatado': 'Preço',
                    'quantidade': 'Estoque',
                    'estoque_minimo': 'Estoque Mínimo',
                    'status': 'Status'
                },
                disabled=['preco_formatado', 'status'],
                use_container_width=True,
                key="produtos_editor"
            )
            
            # Botões de ação
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Remover Produto Selecionado"):
                    if 'produtos_editor' in st.session_state:
                        # Aqui você implementaria a lógica de remoção
                        st.info("Funcionalidade de remoção em desenvolvimento")
            
            with col2:
                if st.button("📝 Editar Produto Selecionado"):
                    if 'produtos_editor' in st.session_state:
                        # Aqui você implementaria a lógica de edição
                        st.info("Funcionalidade de edição em desenvolvimento")
        else:
            st.info("Nenhum produto encontrado com os filtros aplicados.")
    else:
        st.info("Nenhum produto cadastrado ainda.")

# Página para adicionar produto
def adicionar_produto_page():
    st.markdown('<div class="main-header"><h1>➕ Adicionar Novo Produto</h1></div>', unsafe_allow_html=True)
    
    with st.form("adicionar_produto_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Produto*", placeholder="Ex: Notebook Dell")
            categoria = st.selectbox("Categoria*", [
                'eletronicos', 'roupas', 'casa', 'esporte', 'livros',
                'alimentacao', 'beleza', 'automotivo', 'ferramentas', 'outros'
            ], format_func=lambda x: {
                'eletronicos': 'Eletrônicos',
                'roupas': 'Roupas',
                'casa': 'Casa e Decoração',
                'esporte': 'Esporte e Lazer',
                'livros': 'Livros',
                'alimentacao': 'Alimentação',
                'beleza': 'Beleza e Cuidados',
                'automotivo': 'Automotivo',
                'ferramentas': 'Ferramentas',
                'outros': 'Outros'
            }[x])
            preco = st.number_input("Preço Unitário (R$)*", min_value=0.01, step=0.01)
        
        with col2:
            quantidade = st.number_input("Quantidade em Estoque*", min_value=0, step=1)
            estoque_minimo = st.number_input("Estoque Mínimo*", min_value=0, step=1)
            descricao = st.text_area("Descrição", placeholder="Descrição opcional do produto")
        
        submitted = st.form_submit_button("💾 Salvar Produto")
        
        if submitted:
            if nome and categoria and preco > 0:
                if adicionar_produto(nome, descricao, categoria, preco, quantidade, estoque_minimo):
                    st.success("✅ Produto adicionado com sucesso!")
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.error("❌ Por favor, preencha todos os campos obrigatórios.")

# Página de alertas
def alertas():
    st.markdown('<div class="main-header"><h1>🔔 Alertas de Estoque</h1></div>', unsafe_allow_html=True)
    
    df_produtos = get_produtos()
    
    if not df_produtos.empty:
        # Produtos com estoque baixo
        produtos_baixo = df_produtos[df_produtos['quantidade'] <= df_produtos['estoque_minimo']]
        
        if not produtos_baixo.empty:
            st.subheader(f"⚠️ Produtos com Estoque Baixo ({len(produtos_baixo)})")
            
            for _, produto in produtos_baixo.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_icon = "🔴" if produto['quantidade'] == 0 else "🟡"
                    st.write(f"{status_icon} **{produto['nome']}** - {produto['categoria'].title()}")
                
                with col2:
                    st.write(f"Estoque: {produto['quantidade']}")
                
                with col3:
                    st.write(f"Mínimo: {produto['estoque_minimo']}")
        else:
            st.success("🎉 Nenhum produto com estoque baixo!")
    else:
        st.info("Nenhum produto cadastrado ainda.")

# Página de histórico
def historico():
    st.markdown('<div class="main-header"><h1>📚 Histórico de Movimentações</h1></div>', unsafe_allow_html=True)
    
    df_movimentacoes = get_movimentacoes()
    
    if not df_movimentacoes.empty:
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            produtos_lista = df_movimentacoes['produto_nome'].unique()
            filtro_produto = st.selectbox("Filtrar por produto:", ['Todos'] + list(produtos_lista))
        
        with col2:
            filtro_tipo = st.selectbox("Tipo de movimentação:", ['Todos', 'ENTRADA', 'SAIDA'])
        
        # Aplicar filtros
        df_filtrado = df_movimentacoes.copy()
        
        if filtro_produto != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['produto_nome'] == filtro_produto]
        
        if filtro_tipo != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['tipo'] == filtro_tipo]
        
        # Mostrar movimentações
        st.subheader(f"📋 Movimentações: {len(df_filtrado)}")
        
        for _, mov in df_filtrado.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
            
            with col1:
                st.write(f"**{mov['produto_nome']}**")
            
            with col2:
                icon = "📥" if mov['tipo'] == 'ENTRADA' else "📤"
                st.write(f"{icon} {mov['tipo']}")
            
            with col3:
                st.write(f"Qtd: {mov['quantidade']}")
            
            with col4:
                st.write(f"{mov['criado_em'][:16]}")
            
            if mov['observacao']:
                st.caption(f"📝 {mov['observacao']}")
            
            st.divider()
    else:
        st.info("Nenhuma movimentação registrada ainda.")

# Menu principal
def main():
    # Inicializar banco de dados
    init_database()
    
    # Menu lateral
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f4e79/ffffff?text=Estoque+Fácil", width=200)
        
        selected = option_menu(
            menu_title="Menu Principal",
            options=["Dashboard", "Produtos", "Adicionar Produto", "Alertas", "Histórico"],
            icons=["house", "box", "plus-circle", "exclamation-triangle", "clock-history"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#1f4e79", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#1f4e79"},
            }
        )
    
    # Renderizar página selecionada
    if selected == "Dashboard":
        dashboard()
    elif selected == "Produtos":
        produtos()
    elif selected == "Adicionar Produto":
        adicionar_produto_page()
    elif selected == "Alertas":
        alertas()
    elif selected == "Histórico":
        historico()

if __name__ == "__main__":
    main()