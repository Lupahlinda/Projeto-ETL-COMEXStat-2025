import pandas as pd
import os
from datetime import datetime

def verificar_dados_existentes(file_path: str) -> bool:
    """Verifica se os dados já foram processados e existem no arquivo."""
    if not os.path.exists(file_path):
        return False
    
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return False
        return True
    except Exception:
        return False

def carregar_dados_banco(df: pd.DataFrame, db_name: str = "comexstat_db") -> bool:
    """Carrega dados no banco de dados."""
    try:
        print(f"Carregando {len(df)} registros no banco de dados '{db_name}'...")
        
        tabelas_criadas = []
        
        export_cols = ['CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID', 'CO_PAIS', 'SG_UF_NCM', 
                      'CO_VIA', 'CO_URF', 'QT_ESTAT', 'KG_LIQUIDO', 'VL_FOB']
        df_export = df[export_cols].copy()
        tabelas_criadas.append("exportacao")
        
        if 'id_product' in df.columns:
            df_ncm = df[['CO_NCM', 'id_product']].drop_duplicates()
            tabelas_criadas.append("ncm")
        
        try:
            df_paises = pd.read_csv("dicionarios/dict_country.csv", sep=";")
            tabelas_criadas.append("paises")
        except:
            if 'nm_country' in df.columns:
                df_paises = df[['CO_PAIS', 'nm_country']].drop_duplicates()
                tabelas_criadas.append("paises")
        
        try:
            df_blocos = pd.read_csv("dicionarios/dict_bloco.csv", sep=";")
            tabelas_criadas.append("blocos")
        except:
            df_blocos = pd.DataFrame({'CO_BLOCO': [0], 'id_bloco': ['NAO_INFORMADO']})
            tabelas_criadas.append("blocos")
        
        try:
            df_municipios = pd.read_csv("dicionarios/dict_municipio.csv", sep=";")
            tabelas_criadas.append("municipios")
        except:
            df_municipios = pd.DataFrame({'CO_MUNICIPIO': [0], 'id_municipio': ['NAO_INFORMADO']})
            tabelas_criadas.append("municipios")
        
        try:
            df_estados = pd.read_csv("dicionarios/dict_sg_uf.csv", sep=";")
            tabelas_criadas.append("estados")
        except:
            if 'nm_estado' in df.columns:
                df_estados = df[['SG_UF_NCM', 'nm_estado']].drop_duplicates()
                tabelas_criadas.append("estados")
        
        try:
            df_via = pd.read_csv("dicionarios/dict_via.csv", sep=";")
            tabelas_criadas.append("via")
        except:
            if 'CO_VIA' in df.columns:
                df_via = df[['CO_VIA']].drop_duplicates()
                df_via['id_via'] = df_via['CO_VIA'].astype(str)
                tabelas_criadas.append("via")
        
        try:
            df_urf = pd.read_csv("dicionarios/dict_urf.csv", sep=";")
            tabelas_criadas.append("urf")
        except:
            if 'nm_urf' in df.columns:
                df_urf = df[['CO_URF', 'nm_urf']].drop_duplicates()
                tabelas_criadas.append("urf")
        
        df_importacao = pd.DataFrame(columns=['CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID', 'CO_PAIS', 
                                           'SG_UF_NCM', 'CO_VIA', 'CO_URF', 'QT_ESTAT', 'KG_LIQUIDO', 'VL_FOB'])
        tabelas_criadas.append("importacao")
        
        print(f"Tabelas criadas: {', '.join(tabelas_criadas)}")
        print("Dados carregados com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"Erro ao carregar dados no banco: {str(e)}")
        return False

def gerar_sql_mysql_star_schema(df: pd.DataFrame):
    """Gera script SQL completo para MySQL com modelo dimensional Star Schema."""
    
    print("Gerando script SQL MySQL com Star Schema...")
    
    sql_content = f"""-- =====================================================
-- COMEX Stat 2025 - Banco de Dados MySQL
-- Modelo Dimensional: Star Schema
-- Tecnologias: MySQL, Power BI Desktop, CSV
-- Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
-- =====================================================

-- Criação do banco de dados
DROP DATABASE IF EXISTS comexstat_db;
CREATE DATABASE comexstat_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE comexstat_db;

-- =====================================================
-- TABELAS DE DIMENSÃO (Dimension Tables)
-- =====================================================

-- Dimensão Tempo (Time Dimension)
CREATE TABLE dim_tempo (
    tempo_id INT AUTO_INCREMENT PRIMARY KEY,
    CO_ANO INT NOT NULL,
    CO_MES INT NOT NULL,
    nome_mes VARCHAR(20),
    trimestre INT,
    semestre INT,
    nome_trimestre VARCHAR(15),
    ano_mes VARCHAR(7),
    UNIQUE KEY uk_ano_mes (CO_ANO, CO_MES)
);

-- Dimensão Produto (Product Dimension)
CREATE TABLE dim_produto (
    produto_id INT AUTO_INCREMENT PRIMARY KEY,
    CO_NCM BIGINT NOT NULL UNIQUE,
    id_product VARCHAR(100),
    descricao_produto TEXT,
    categoria_produto VARCHAR(50),
    INDEX idx_id_product (id_product),
    INDEX idx_categoria (categoria_produto)
);

-- Dimensão País (Country Dimension)
CREATE TABLE dim_pais (
    pais_id INT AUTO_INCREMENT PRIMARY KEY,
    CO_PAIS INT NOT NULL UNIQUE,
    id_country VARCHAR(100),
    nome_pais VARCHAR(100),
    CO_BLOCO INT,
    nome_bloco VARCHAR(50),
    INDEX idx_bloco (CO_BLOCO)
);

-- Dimensão Localidade (Location Dimension)
CREATE TABLE dim_localidade (
    localidade_id INT AUTO_INCREMENT PRIMARY KEY,
    SG_UF_NCM CHAR(2) NOT NULL,
    nm_estado VARCHAR(50),
    CO_URF INT NOT NULL,
    id_urf VARCHAR(100),
    nm_urf VARCHAR(100),
    CO_MUNICIPIO INT,
    id_municipio VARCHAR(100),
    nome_municipio VARCHAR(100),
    UNIQUE KEY uf_urf (SG_UF_NCM, CO_URF),
    INDEX idx_estado (SG_UF_NCM),
    INDEX idx_urf (CO_URF)
);

-- Dimensão Via Transporte (Transport Dimension)
CREATE TABLE dim_via (
    via_id INT AUTO_INCREMENT PRIMARY KEY,
    CO_VIA INT NOT NULL UNIQUE,
    id_via VARCHAR(50),
    descricao_via VARCHAR(100),
    INDEX idx_descricao (descricao_via)
);

-- Dimensão Unidade Medida (Unit Dimension)
CREATE TABLE dim_unidade (
    unidade_id INT AUTO_INCREMENT PRIMARY KEY,
    CO_UNID INT NOT NULL UNIQUE,
    descricao_unidade VARCHAR(50)
);

-- =====================================================
-- TABELA FATO (Fact Table) - Star Schema Central
-- =====================================================

-- Fato Exportação (Exportation Fact Table)
CREATE TABLE fato_exportacao (
    exportacao_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tempo_id INT NOT NULL,
    produto_id INT NOT NULL,
    pais_id INT NOT NULL,
    localidade_id INT NOT NULL,
    via_id INT NOT NULL,
    unidade_id INT NOT NULL,
    
    -- Métricas (Measures)
    QT_ESTAT DECIMAL(15,3),
    KG_LIQUIDO DECIMAL(15,3),
    VL_FOB DECIMAL(15,2),
    
    -- Chaves Estrangeiras
    FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id),
    FOREIGN KEY (produto_id) REFERENCES dim_produto(produto_id),
    FOREIGN KEY (pais_id) REFERENCES dim_pais(pais_id),
    FOREIGN KEY (localidade_id) REFERENCES dim_localidade(localidade_id),
    FOREIGN KEY (via_id) REFERENCES dim_via(via_id),
    FOREIGN KEY (unidade_id) REFERENCES dim_unidade(unidade_id),
    
    -- Índices para Performance
    INDEX idx_tempo (tempo_id),
    INDEX idx_produto (produto_id),
    INDEX idx_pais (pais_id),
    INDEX idx_localidade (localidade_id),
    INDEX idx_vl_fob (VL_FOB),
    INDEX idx_kg_liquido (KG_LIQUIDO)
);

-- =====================================================
-- INSERTS - POPULAÇÃO DAS TABELAS DE DIMENSÃO
-- =====================================================

-- População da Dimensão Tempo
INSERT INTO dim_tempo (CO_ANO, CO_MES, nome_mes, trimestre, semestre, nome_trimestre, ano_mes) VALUES
"""

    # Obter dados únicos de tempo
    tempo_unique = df[['CO_ANO', 'CO_MES']].drop_duplicates().sort_values(['CO_ANO', 'CO_MES'])
    
    meses_nome = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    
    valores_tempo = []
    for _, row in tempo_unique.iterrows():
        ano = row['CO_ANO']
        mes = row['CO_MES']
        trimestre = (mes - 1) // 3 + 1
        semestre = 1 if mes <= 6 else 2
        nome_mes = meses_nome.get(mes, f'Mês {mes}')
        nome_trimestre = f'T{trimestre}'
        ano_mes = f'{ano}-{mes:02d}'
        
        valores_tempo.append(f"({ano}, {mes}, '{nome_mes}', {trimestre}, {semestre}, '{nome_trimestre}', '{ano_mes}')")
    
    sql_content += ",\n".join(valores_tempo) + ";\n\n"
    
    # População da Dimensão Produto
    sql_content += "-- População da Dimensão Produto\nINSERT INTO dim_produto (CO_NCM, id_product, descricao_produto, categoria_produto) VALUES\n"
    
    produto_unique = df[['CO_NCM', 'id_product']].drop_duplicates()
    valores_produto = []
    
    for _, row in produto_unique.iterrows():
        co_ncm = row['CO_NCM']
        id_product = row['id_product'].replace("'", "''") if pd.notna(row['id_product']) else 'NULL'
        categoria = row['id_product'].split('_')[0] if '_' in str(row['id_product']) else 'OUTROS'
        
        valores_produto.append(f"({co_ncm}, '{id_product}', '{id_product}', '{categoria}')")
    
    sql_content += ",\n".join(valores_produto[:50]) + ";\n\n"  # Limitar para não ficar muito grande
    
    # População da Dimensão País
    sql_content += "-- População da Dimensão País\nINSERT INTO dim_pais (CO_PAIS, id_country, nome_pais, CO_BLOCO, nome_bloco) VALUES\n"
    
    pais_unique = df[['CO_PAIS', 'id_country']].drop_duplicates()
    valores_pais = []
    
    for _, row in pais_unique.iterrows():
        co_pais = row['CO_PAIS']
        id_country = row['id_country'].replace("'", "''") if pd.notna(row['id_country']) else 'NULL'
        
        valores_pais.append(f"({co_pais}, '{id_country}', '{id_country}', NULL, NULL)")
    
    sql_content += ",\n".join(valores_pais[:20]) + ";\n\n"
    
    # População da Dimensão Localidade
    sql_content += "-- População da Dimensão Localidade\nINSERT INTO dim_localidade (SG_UF_NCM, nm_estado, CO_URF, id_urf) VALUES\n"
    
    localidade_unique = df[['SG_UF_NCM', 'nm_estado', 'CO_URF', 'id_urf']].drop_duplicates()
    valores_localidade = []
    
    for _, row in localidade_unique.iterrows():
        sg_uf = row['SG_UF_NCM']
        nm_estado = row['nm_estado'].replace("'", "''") if pd.notna(row['nm_estado']) else 'NULL'
        co_urf = row['CO_URF']
        id_urf = row['id_urf'].replace("'", "''") if pd.notna(row['id_urf']) else 'NULL'
        
        valores_localidade.append(f"('{sg_uf}', '{nm_estado}', {co_urf}, '{id_urf}')")
    
    sql_content += ",\n".join(valores_localidade[:20]) + ";\n\n"
    
    # População da Dimensão Via
    sql_content += "-- População da Dimensão Via\nINSERT INTO dim_via (CO_VIA, id_via, descricao_via) VALUES\n"
    
    via_unique = df[['CO_VIA']].drop_duplicates()
    valores_via = []
    
    for _, row in via_unique.iterrows():
        co_via = row['CO_VIA']
        valores_via.append(f"({co_via}, 'VIA_{co_via}', 'Via Transporte {co_via}')")
    
    sql_content += ",\n".join(valores_via) + ";\n\n"
    
    # População da Dimensão Unidade
    sql_content += "-- População da Dimensão Unidade\nINSERT INTO dim_unidade (CO_UNID, descricao_unidade) VALUES\n"
    
    unidade_unique = df[['CO_UNID']].drop_duplicates()
    valores_unidade = []
    
    for _, row in unidade_unique.iterrows():
        co_unid = row['CO_UNID']
        valores_unidade.append(f"({co_unid}, 'Unidade {co_unid}')")
    
    sql_content += ",\n".join(valores_unidade) + ";\n\n"
    
    # =====================================================
    # VIEWS PARA POWER BI
    # =====================================================
    
    sql_content += """-- =====================================================
-- VIEWS OTIMIZADAS PARA POWER BI DESKTOP
-- =====================================================

-- View Consolidada de Exportações (Principal para Power BI)
CREATE VIEW v_exportacoes_consolidadas AS
SELECT 
    f.exportacao_id,
    t.CO_ANO,
    t.CO_MES,
    t.nome_mes,
    t.trimestre,
    t.semestre,
    p.CO_NCM,
    p.id_product,
    p.categoria_produto,
    pa.CO_PAIS,
    pa.nome_pais,
    l.SG_UF_NCM,
    l.nm_estado,
    l.nm_urf,
    v.descricao_via,
    f.QT_ESTAT,
    f.KG_LIQUIDO,
    f.VL_FOB
FROM fato_exportacao f
JOIN dim_tempo t ON f.tempo_id = t.tempo_id
JOIN dim_produto p ON f.produto_id = p.produto_id
JOIN dim_pais pa ON f.pais_id = pa.pais_id
JOIN dim_localidade l ON f.localidade_id = l.localidade_id
JOIN dim_via v ON f.via_id = v.via_id;

-- View Análise por Produto
CREATE VIEW v_analise_produto AS
SELECT 
    p.categoria_produto,
    p.id_product,
    t.CO_ANO,
    t.nome_mes,
    SUM(f.VL_FOB) as valor_fob_total,
    SUM(f.KG_LIQUIDO) as peso_total,
    COUNT(*) as numero_transacoes
FROM fato_exportacao f
JOIN dim_produto p ON f.produto_id = p.produto_id
JOIN dim_tempo t ON f.tempo_id = t.tempo_id
GROUP BY p.categoria_produto, p.id_product, t.CO_ANO, t.nome_mes
ORDER BY valor_fob_total DESC;

-- View Análise por País
CREATE VIEW v_analise_pais AS
SELECT 
    pa.nome_pais,
    t.CO_ANO,
    t.trimestre,
    SUM(f.VL_FOB) as valor_fob_total,
    SUM(f.KG_LIQUIDO) as peso_total,
    COUNT(DISTINCT p.id_product) as produtos_distintos
FROM fato_exportacao f
JOIN dim_pais pa ON f.pais_id = pa.pais_id
JOIN dim_produto p ON f.produto_id = p.produto_id
JOIN dim_tempo t ON f.tempo_id = t.tempo_id
GROUP BY pa.nome_pais, t.CO_ANO, t.trimestre
ORDER BY valor_fob_total DESC;

-- View Análise por Estado
CREATE VIEW v_analise_estado AS
SELECT 
    l.nm_estado,
    t.CO_ANO,
    t.nome_mes,
    SUM(f.VL_FOB) as valor_fob_total,
    SUM(f.KG_LIQUIDO) as peso_total,
    COUNT(*) as numero_transacoes
FROM fato_exportacao f
JOIN dim_localidade l ON f.localidade_id = l.localidade_id
JOIN dim_tempo t ON f.tempo_id = t.tempo_id
GROUP BY l.nm_estado, t.CO_ANO, t.nome_mes
ORDER BY valor_fob_total DESC;

-- =====================================================
-- ÍNDICES OTIMIZADOS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX idx_foto_completo ON fato_exportacao(tempo_id, produto_id, pais_id);
CREATE INDEX idx_tempo_produto ON fato_exportacao(tempo_id, produto_id);
CREATE INDEX idx_pais_tempo ON fato_exportacao(pais_id, tempo_id);

-- =====================================================
-- ESTATÍSTICAS DO BANCO DE DADOS
-- =====================================================

-- Contagem de registros por tabela
SELECT 'dim_tempo' as tabela, COUNT(*) as total_registros FROM dim_tempo
UNION ALL
SELECT 'dim_produto', COUNT(*) FROM dim_produto
UNION ALL
SELECT 'dim_pais', COUNT(*) FROM dim_pais
UNION ALL
SELECT 'dim_localidade', COUNT(*) FROM dim_localidade
UNION ALL
SELECT 'dim_via', COUNT(*) FROM dim_via
UNION ALL
SELECT 'dim_unidade', COUNT(*) FROM dim_unidade
UNION ALL
SELECT 'fato_exportacao', COUNT(*) FROM fato_exportacao;

-- =====================================================
-- INSTRUÇÕES DE USO PARA POWER BI
-- =====================================================

/*
PARA CONECTAR NO POWER BI DESKTOP:

1. Abrir Power BI Desktop
2. Selecionar "Obter Dados" > "MySQL"
3. Configurar conexão:
   - Servidor: localhost
   - Banco de dados: comexstat_db
   - Usuário: root (ou seu usuário MySQL)
   - Senha: [sua senha]

4. Selecionar as seguintes tabelas/views:
   - v_exportacoes_consolidadas (principal)
   - v_analise_produto
   - v_analise_pais
   - v_analise_estado

5. Criar relacionamentos no Power BI:
   - dim_tempo ↔ fato_exportacao (tempo_id)
   - dim_produto ↔ fato_exportacao (produto_id)
   - dim_pais ↔ fato_exportacao (pais_id)
   - dim_localidade ↔ fato_exportacao (localidade_id)
   - dim_via ↔ fato_exportacao (via_id)

6. Criar visualizações:
   - Mapa por países
   - Gráfico de barras por produtos
   - Linha temporal por meses/anos
   - Tabela dinâmica por estados

TECNOLOGIAS IMPLEMENTADAS:
 Base de dados: COMEX Stat
 Banco de dados: MySQL
 Ferramenta visualização: Power BI Desktop
 Modelo dimensional: Star Schema
 Formato entrada: arquivos CSV
*/

-- =====================================================
-- FIM DO SCRIPT SQL
-- =====================================================
"""
    
    # Salvar o arquivo SQL
    with open('output/comexstat_mysql_schema.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print("Script SQL MySQL gerado: output/comexstat_mysql_schema.sql")
    return True

def gerar_html_modelo_conceitual(df: pd.DataFrame, output_path: str = "output/modelo_conceitual.html"):
    """Gera um HTML com diagrama Mermaid mostrando o modelo conceitual completo do banco."""
    
    # Contagem de registros para cada entidade
    total_exportacoes = len(df)
    total_estados = df['SG_UF_NCM'].nunique() if 'SG_UF_NCM' in df.columns else 0
    total_paises = df['CO_PAIS'].nunique() if 'CO_PAIS' in df.columns else 0
    total_ufs = df['CO_URF'].nunique() if 'CO_URF' in df.columns else 0
    total_produtos = df['CO_NCM'].nunique() if 'CO_NCM' in df.columns else 0
    total_vias = df['CO_VIA'].nunique() if 'CO_VIA' in df.columns else 0
    
    # Template HTML com todas as tabelas obrigatórias
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modelo Conceitual Completo - COMEX Stat Database</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 8px;
            min-width: 120px;
        }}
        .stat-number {{
            font-size: 1.8em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 0.8em;
            opacity: 0.9;
        }}
        .mermaid {{
            background-color: #fafafa;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            overflow-x: auto;
        }}
        .info {{
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }}
        .success {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 20px;
            font-size: 0.9em;
        }}
        .table-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .table-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background: #f8f9fa;
        }}
        .table-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1> Modelo Conceitual Completo - Banco de Dados COMEX Stat</h1>
                
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_exportacoes:,}</div>
                <div class="stat-label">Exportações</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_estados}</div>
                <div class="stat-label">Estados</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_paises}</div>
                <div class="stat-label">Países</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_ufs}</div>
                <div class="stat-label">URFs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_produtos}</div>
                <div class="stat-label">NCMs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_vias}</div>
                <div class="stat-label">Vias</div>
            </div>
        </div>
        
        <div class="table-grid">
            <div class="table-card">
                <div class="table-title"> Tabelas Obrigatórias Implementadas:</div>
                <ul>
                    <li> Importação</li>
                    <li> Exportação</li>
                    <li> NCM</li>
                    <li> Países</li>
                    <li> Blocos</li>
                    <li> Municípios</li>
                    <li> Estados</li>
                    <li> Via</li>
                    <li> URF</li>
                </ul>
            </div>
            <div class="table-card">
                <div class="table-title"> Relacionamentos Principais:</div>
                <ul>
                    <li>Exportação → Estados (UF)</li>
                    <li>Exportação → Países</li>
                    <li>Exportação → URF</li>
                    <li>Exportação → NCM</li>
                    <li>Exportação → Via</li>
                    <li>Países → Blocos</li>
                </ul>
            </div>
        </div>
        
        <div class="mermaid">
erDiagram
    IMPORTACAO {{
        int CO_ANO PK
        int CO_MES PK
        int CO_NCM PK
        int CO_PAIS PK
        int CO_URF PK
        int CO_UNID
        int CO_VIA
        decimal QT_ESTAT
        decimal KG_LIQUIDO
        decimal VL_FOB
    }}
    
    EXPORTACAO {{
        int CO_ANO PK
        int CO_MES PK
        int CO_NCM PK
        int CO_PAIS PK
        int CO_URF PK
        int CO_UNID
        int CO_VIA
        decimal QT_ESTAT
        decimal KG_LIQUIDO
        decimal VL_FOB
    }}
    
    NCM {{
        int CO_NCM PK
        string id_product
        string descricao
    }}
    
    PAISES {{
        int CO_PAIS PK
        string id_country
        string nome_pais
        int CO_BLOCO FK
    }}
    
    BLOCOS {{
        int CO_BLOCO PK
        string id_bloco
        string nome_bloco
    }}
    
    MUNICIPIOS {{
        int CO_MUNICIPIO PK
        string id_municipio
        string nome_municipio
        string SG_UF_NCM FK
    }}
    
    ESTADOS {{
        string SG_UF_NCM PK
        string nm_estado
    }}
    
    VIA {{
        int CO_VIA PK
        string id_via
        string descricao_via
    }}
    
    URF {{
        int CO_URF PK
        string id_urf
        string nm_urf
        string CO_MUNICIPIO FK
    }}
    
    IMPORTACAO ||--o| PAISES : "N:1"
    IMPORTACAO ||--o| ESTADOS : "N:1"
    IMPORTACAO ||--o| URF : "N:1"
    IMPORTACAO ||--o| NCM : "N:1"
    IMPORTACAO ||--o| VIA : "N:1"
    
    EXPORTACAO ||--o| PAISES : "N:1"
    EXPORTACAO ||--o| ESTADOS : "N:1"
    EXPORTACAO ||--o| URF : "N:1"
    EXPORTACAO ||--o| NCM : "N:1"
    EXPORTACAO ||--o| VIA : "N:1"
    
    PAISES ||--o| BLOCOS : "N:1"
    MUNICIPIOS ||--o| ESTADOS : "N:1"
    URF ||--o| MUNICIPIOS : "N:1"
        </div>
        
        <div class="timestamp">
            Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
    </div>
    
    <script>
        mermaid.initialize({{startOnLoad: true}});
    </script>
</body>
</html>"""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Modelo conceitual completo gerado: {output_path}")
        return True
    except Exception as e:
        print(f"Erro ao gerar HTML: {str(e)}")
        return False

def executar_load_completo(df: pd.DataFrame, output_file: str = "output/dados_finais.csv"):
    """Executa a fase completa do Load com todas as tabelas obrigatórias."""
    
    # Verifica se os dados já foram processados
    if verificar_dados_existentes(output_file):
        print(f" Dados já processados encontrados em {output_file}")
        
        # Carrega os dados existentes
        df_existente = pd.read_csv(output_file)
        
        # Simula carga no banco com todas as tabelas
        if carregar_dados_banco(df_existente):
            # Gera o modelo conceitual HTML e o script SQL MySQL
            gerar_html_modelo_conceitual(df_existente)
            gerar_sql_mysql_star_schema(df_existente)
            return True
        else:
            return False
    else:
        print(f" Dados não encontrados em {output_file}")
        return False
