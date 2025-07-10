# Estoque Fácil - Sistema de Controle de Estoque

## Descrição

O **Estoque Fácil** é um sistema web desenvolvido em Streamlit para pequenas e médias empresas gerenciarem seu estoque de produtos de forma eficiente e intuitiva.

## Funcionalidades Principais

### 📊 Dashboard Interativo
- Visão geral do estoque com métricas importantes
- Gráficos interativos por categoria e status do estoque
- Alertas visuais de estoque baixo e produtos esgotados
- Cálculo automático do valor total do estoque

### 📦 Gerenciamento de Produtos
- Cadastro completo de produtos com validação
- Edição e remoção de produtos (soft delete)
- Filtros avançados por nome, categoria e status
- Controle de estoque mínimo com alertas automáticos

### 🔔 Sistema de Alertas
- Notificações automáticas de estoque baixo
- Lista detalhada de produtos esgotados
- Monitoramento em tempo real dos níveis de estoque

### 📚 Histórico de Movimentações
- Registro automático de todas as movimentações
- Filtros por produto e tipo de movimentação
- Rastreamento completo de entradas e saídas

## Pré-requisitos

- Python 3.8 ou superior
- Conexão com a internet (para instalação de dependências)
- Navegador web moderno

## Instalação e Execução na Sua Máquina - Passo a Passo

### Passo 1: Verificar Pré-requisitos

#### Verificar se o Python está instalado
```bash
# Verificar versão do Python (deve ser 3.8 ou superior)
python --version
# ou
python3 --version

# Se não tiver Python instalado, baixe em: https://python.org/downloads/
```

#### Verificar se o pip está funcionando
```bash
# Verificar se o pip está instalado
pip --version
# ou
pip3 --version
```

### Passo 2: Preparar o Ambiente de Trabalho

#### Criar uma pasta para o projeto
```bash
# Criar pasta para o projeto
mkdir estoque-facil
cd estoque-facil

# Ou no Windows:
md estoque-facil
cd estoque-facil
```

#### Baixar e extrair os arquivos
1. Baixe o arquivo ZIP do projeto
2. Extraia todos os arquivos na pasta `estoque-facil`
3. Verifique se os arquivos estão na pasta:
   - `streamlit_app.py`
   - `streamlit_requirements.txt`
   - `README.md`
   - `.streamlit/config.toml`

### Passo 3: Criar Ambiente Virtual (Recomendado)

#### Para Windows:
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Você verá (venv) no início da linha de comando
```

#### Para macOS/Linux:
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Você verá (venv) no início da linha de comando
```

### Passo 4: Instalar as Dependências

```bash
# Atualizar o pip (recomendado)
python -m pip install --upgrade pip

# Instalar as dependências do projeto
pip install -r streamlit_requirements.txt

# Aguardar a instalação (pode demorar alguns minutos)
```

#### Verificar se a instalação foi bem-sucedida
```bash
# Verificar se o Streamlit foi instalado
streamlit --version

# Listar todas as dependências instaladas
pip list
```

### Passo 5: Executar a Aplicação

```bash
# Executar a aplicação
streamlit run streamlit_app.py

# Você verá mensagens como:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

### Passo 6: Acessar a Aplicação

1. **Automático**: A aplicação abrirá automaticamente no seu navegador padrão
2. **Manual**: Se não abrir automaticamente, acesse: `http://localhost:8501`
3. **Alternativa**: Use o Network URL se quiser acessar de outro dispositivo na mesma rede

### Passo 7: Primeiro Uso

1. **Dashboard Inicial**: Você verá o dashboard vazio (normal para primeira execução)
2. **Adicionar Produto**: Clique em "Adicionar Produto" no menu lateral
3. **Cadastrar Primeiro Produto**:
   - Nome: Ex: "Notebook Dell"
   - Categoria: Selecione "Eletrônicos"
   - Preço: Ex: 2500.00
   - Quantidade: Ex: 10
   - Estoque Mínimo: Ex: 2
   - Descrição: Ex: "Notebook para uso profissional"
4. **Salvar**: Clique em "Salvar Produto"
5. **Verificar**: Volte ao Dashboard para ver as estatísticas atualizadas

### Passo 8: Parar a Aplicação

```bash
# Para parar a aplicação, pressione:
Ctrl + C

# Para desativar o ambiente virtual:
deactivate
```

## Execução Rápida (Próximas Vezes)

Após a primeira instalação, para executar o sistema novamente:

```bash
# 1. Entrar na pasta do projeto
cd estoque-facil

# 2. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Executar aplicação
streamlit run streamlit_app.py

# 4. Acessar: http://localhost:8501
```

## Solução de Problemas Comuns

### Erro: "python: command not found"
```bash
# Instalar Python em:
# Windows: https://python.org/downloads/
# macOS: brew install python3
# Linux: sudo apt install python3 python3-pip
```

### Erro: "streamlit: command not found"
```bash
# Verificar se o ambiente virtual está ativado
# Você deve ver (venv) no início da linha

# Reinstalar Streamlit
pip install streamlit --force-reinstall
```

### Erro: "No module named 'streamlit'"
```bash
# Verificar se está no ambiente virtual correto
# Ativar ambiente virtual novamente
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r streamlit_requirements.txt
```

### Erro: "Port 8501 is already in use"
```bash
# Usar uma porta diferente
streamlit run streamlit_app.py --server.port 8502

# Ou finalizar processos que estão usando a porta
# Windows: taskkill /f /im python.exe
# macOS/Linux: pkill -f streamlit
```

### Erro: "Permission denied"
```bash
# Windows: Executar como administrador
# macOS/Linux: Verificar permissões da pasta
chmod +x streamlit_app.py
```

## Testando a Instalação

### Teste 1: Verificar se tudo está funcionando
```bash
# Executar teste básico
python -c "import streamlit; print('Streamlit OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import plotly; print('Plotly OK')"
```

### Teste 2: Verificar arquivos
```bash
# Listar arquivos do projeto
ls -la  # macOS/Linux
dir     # Windows

# Deve mostrar:
# streamlit_app.py
# streamlit_requirements.txt
# README.md
# .streamlit/
```

### Teste 3: Executar aplicação em modo de teste
```bash
# Executar sem abrir navegador
streamlit run streamlit_app.py --server.headless true

# Acessar manualmente: http://localhost:8501
```

## Estrutura de Arquivos

```
projeto/
├── streamlit_app.py              # Aplicação principal
├── streamlit_requirements.txt    # Dependências do projeto
├── README.md                    # Esta documentação
├── .streamlit/
│   └── config.toml              # Configurações do Streamlit
└── estoque_facil.db            # Banco de dados SQLite (criado automaticamente)
```

## Como Usar o Sistema

### 1. Dashboard
- Acesse métricas importantes do seu estoque
- Visualize gráficos de distribuição por categoria
- Monitore alertas de estoque baixo
- Acompanhe o valor total do estoque

### 2. Gerenciar Produtos
- **Listar**: Visualize todos os produtos com filtros
- **Buscar**: Use a caixa de busca para encontrar produtos específicos
- **Filtrar**: Filtre por categoria ou status do estoque
- **Editar**: Modifique informações dos produtos existentes

### 3. Adicionar Produtos
- **Nome**: Nome do produto (obrigatório)
- **Categoria**: Selecione uma das categorias disponíveis
- **Preço**: Valor unitário do produto
- **Quantidade**: Estoque atual
- **Estoque Mínimo**: Limite para alertas automáticos
- **Descrição**: Informações adicionais (opcional)

### 4. Sistema de Alertas
- Produtos com estoque igual ou abaixo do mínimo aparecem automaticamente
- Produtos esgotados são destacados em vermelho
- Use esta seção para priorizar reposição de estoque

### 5. Histórico
- Visualize todas as movimentações de estoque
- Filtre por produto específico
- Acompanhe entradas e saídas

## Deploy no Streamlit Cloud

### 1. Preparação
```bash
# Certifique-se de que todos os arquivos estão prontos
ls -la
# Deve mostrar: streamlit_app.py, streamlit_requirements.txt, README.md, .streamlit/
```

### 2. GitHub
1. Crie um repositório no GitHub
2. Faça upload de todos os arquivos do projeto
3. Certifique-se de que o repositório é público ou que você tem acesso

### 3. Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione seu repositório
5. Configure:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.8+ (automático)
   - **Requirements file**: `streamlit_requirements.txt`
6. Clique em "Deploy!"

### 4. Configuração Avançada (Opcional)
- O arquivo `.streamlit/config.toml` já está configurado
- Cores e tema personalizados já aplicados
- Não é necessário configuração adicional

## Categorias de Produtos Disponíveis

- **Eletrônicos**: Computadores, celulares, equipamentos
- **Roupas**: Vestimentas e acessórios
- **Casa e Decoração**: Móveis, decoração, utilidades domésticas
- **Esporte e Lazer**: Equipamentos esportivos, jogos
- **Livros**: Literatura, técnicos, educacionais
- **Alimentação**: Alimentos, bebidas, suplementos
- **Beleza e Cuidados**: Cosméticos, higiene, cuidados pessoais
- **Automotivo**: Peças, acessórios, ferramentas automotivas
- **Ferramentas**: Ferramentas manuais, elétricas, equipamentos
- **Outros**: Produtos que não se encaixam nas categorias acima

## Banco de Dados

O sistema utiliza SQLite, que é criado automaticamente:

### Tabela `produtos`
```sql
CREATE TABLE produtos (
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
);
```

### Tabela `movimentacoes`
```sql
CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    produto_id INTEGER,
    observacao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);
```

## Solução de Problemas

### Erro: "streamlit: command not found"
```bash
# Verifique se o Streamlit foi instalado corretamente
pip install streamlit

# Ou reinstale as dependências
pip install -r streamlit_requirements.txt
```

### Erro: "ModuleNotFoundError"
```bash
# Instale a dependência específica que está faltando
pip install nome_do_modulo

# Ou reinstale todas as dependências
pip install -r streamlit_requirements.txt --force-reinstall
```

### Erro: "Port already in use"
```bash
# Execute em uma porta diferente
streamlit run streamlit_app.py --server.port 8502
```

### Banco de dados não carrega
```bash
# Verifique se o arquivo .py está na pasta correta
ls -la streamlit_app.py

# O banco será criado automaticamente na primeira execução
```

## Backup e Restauração

### Backup
```bash
# Fazer backup do banco de dados
cp estoque_facil.db backup_estoque_$(date +%Y%m%d).db
```

### Restauração
```bash
# Restaurar backup
cp backup_estoque_YYYYMMDD.db estoque_facil.db
```

## Suporte e Contribuição

- **Documentação**: Consulte este README.md
- **Problemas**: Verifique a seção "Solução de Problemas"
- **Melhorias**: O código está pronto para customizações

## Licença

Este projeto é de código aberto e pode ser usado livremente para fins comerciais e educacionais.

---

**Desenvolvido para facilitar o controle de estoque de pequenos negócios**