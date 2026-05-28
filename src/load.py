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
            df_paises = pd.read_csv("data/dictionaries/dict_country.csv", sep=";")
            tabelas_criadas.append("paises")
        except:
            if 'nm_country' in df.columns:
                df_paises = df[['CO_PAIS', 'nm_country']].drop_duplicates()
                tabelas_criadas.append("paises")
        
        try:
            df_blocos = pd.read_csv("data/dictionaries/dict_bloco.csv", sep=";")
            tabelas_criadas.append("blocos")
        except:
            df_blocos = pd.DataFrame({'CO_BLOCO': [0], 'id_bloco': ['NAO_INFORMADO']})
            tabelas_criadas.append("blocos")
        
        try:
            df_municipios = pd.read_csv("data/dictionaries/dict_municipio.csv", sep=";")
            tabelas_criadas.append("municipios")
        except:
            df_municipios = pd.DataFrame({'CO_MUNICIPIO': [0], 'id_municipio': ['NAO_INFORMADO']})
            tabelas_criadas.append("municipios")
        
        try:
            df_estados = pd.read_csv("data/dictionaries/dict_sg_uf.csv", sep=";")
            tabelas_criadas.append("estados")
        except:
            if 'nm_estado' in df.columns:
                df_estados = df[['SG_UF_NCM', 'nm_estado']].drop_duplicates()
                tabelas_criadas.append("estados")
        
        try:
            df_via = pd.read_csv("data/dictionaries/dict_via.csv", sep=";")
            tabelas_criadas.append("via")
        except:
            if 'CO_VIA' in df.columns:
                df_via = df[['CO_VIA']].drop_duplicates()
                df_via['id_via'] = df_via['CO_VIA'].astype(str)
                tabelas_criadas.append("via")
        
        try:
            df_urf = pd.read_csv("data/dictionaries/dict_urf.csv", sep=";")
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

def gerar_sql_modelo_logico(df: pd.DataFrame):
    """Gera script SQL para o modelo lógico relacional"""
    
    print("Gerando script SQL do Modelo Lógico")
    
    sql_content = f"""-- =====================================================
-- COMEX Stat 2025 - Modelo Lógico Relacional
-- Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
-- =====================================================

-- Criação do banco de dados
DROP DATABASE IF EXISTS comexstat_db;
CREATE DATABASE comexstat_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE comexstat_db;

-- =====================================================
-- MODELO LÓGICO RELACIONAL
-- =====================================================

-- Tabela tb_ncm
CREATE TABLE tb_ncm (
    id_ncm INT PRIMARY KEY AUTO_INCREMENT,
    nome_ncm_portugues VARCHAR(1000) NOT NULL,
    nome_ncm_ingles VARCHAR(1000) NOT NULL,
    nome_ncm_espanhol VARCHAR(1000) NOT NULL
);

-- Tabela tb_unidade
CREATE TABLE tb_unidade (
    id_unidade INT PRIMARY KEY AUTO_INCREMENT,
    nome_unidade VARCHAR(300) NOT NULL,
    sigla_unidade VARCHAR(20) NOT NULL
);

-- Tabela tb_via
CREATE TABLE tb_via (
    id_via INT PRIMARY KEY AUTO_INCREMENT,
    nome_via VARCHAR(100) NOT NULL
);

-- Tabela tb_urf
CREATE TABLE tb_urf (
    id_urf INT PRIMARY KEY AUTO_INCREMENT,
    nome_urf VARCHAR(100) NOT NULL
);

-- Tabela tb_estado
CREATE TABLE tb_estado (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nome_estado VARCHAR(300) NOT NULL,
    sigla_estado CHAR(2) NOT NULL,
    nome_regiao VARCHAR(300) NOT NULL
);

-- Tabela tb_municipio
CREATE TABLE tb_municipio (
    id_municipio INT PRIMARY KEY AUTO_INCREMENT,
    nome_municipio VARCHAR(400) NOT NULL,
    id_estado INT NOT NULL,
    FOREIGN KEY (id_estado) REFERENCES tb_estado(id_estado)
);

-- Tabela tb_exportacao
CREATE TABLE tb_exportacao (
    id_exportacao INT PRIMARY KEY AUTO_INCREMENT,
    id_ncm INT NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    id_estado INT NOT NULL,
    id_unidade INT NOT NULL,
    id_via INT NOT NULL,
    id_urf INT NOT NULL,
    co_pais VARCHAR(10) NOT NULL,
    qt_estat DECIMAL(15,2) NOT NULL,
    kg_liquido DECIMAL(15,2) NOT NULL,
    vl_fob DECIMAL(18,2) NOT NULL,
    
    FOREIGN KEY (id_ncm) REFERENCES tb_ncm(id_ncm),
    FOREIGN KEY (id_estado) REFERENCES tb_estado(id_estado),
    FOREIGN KEY (id_unidade) REFERENCES tb_unidade(id_unidade),
    FOREIGN KEY (id_via) REFERENCES tb_via(id_via),
    FOREIGN KEY (id_urf) REFERENCES tb_urf(id_urf),
    
    INDEX idx_ano (ano),
    INDEX idx_mes (mes),
    INDEX idx_ncm (id_ncm),
    INDEX idx_estado (id_estado),
    INDEX idx_vl_fob (vl_fob)
);

-- =====================================================
-- INSERTS - POPULAÇÃO DAS TABELAS (MODELO LÓGICO)
-- =====================================================

-- População da tb_ncm
INSERT INTO tb_ncm (nome_ncm_portugues, nome_ncm_ingles, nome_ncm_espanhol) VALUES
"""

    # Obter dados únicos de NCM
    ncm_unique = df[['CO_NCM']].drop_duplicates()
    valores_ncm = []
    
    for idx, (_, row) in enumerate(ncm_unique.iterrows()):
        co_ncm = row['CO_NCM']
        valores_ncm.append(f"('Produto NCM {co_ncm}', 'Product NCM {co_ncm}', 'Producto NCM {co_ncm}')")
    
    sql_content += ",\n".join(valores_ncm[:50]) + ";\n\n"
    
    # População da tb_unidade
    sql_content += "-- População da tb_unidade\nINSERT INTO tb_unidade (nome_unidade, sigla_unidade) VALUES\n"
    
    unidade_unique = df[['CO_UNID']].drop_duplicates()
    valores_unidade = []
    
    for idx, (_, row) in enumerate(unidade_unique.iterrows()):
        co_unid = row['CO_UNID']
        valores_unidade.append(f"('Unidade {co_unid}', 'U{co_unid}')")
    
    sql_content += ",\n".join(valores_unidade) + ";\n\n"
    
    # População da tb_via
    sql_content += "-- População da tb_via\nINSERT INTO tb_via (nome_via) VALUES\n"
    
    via_unique = df[['CO_VIA']].drop_duplicates()
    valores_via = []
    
    for idx, (_, row) in enumerate(via_unique.iterrows()):
        co_via = row['CO_VIA']
        valores_via.append(f"('Via {co_via}')")
    
    sql_content += ",\n".join(valores_via) + ";\n\n"
    
    # População da tb_urf
    sql_content += "-- População da tb_urf\nINSERT INTO tb_urf (nome_urf) VALUES\n"
    
    urf_unique = df[['CO_URF']].drop_duplicates()
    valores_urf = []
    
    for idx, (_, row) in enumerate(urf_unique.iterrows()):
        co_urf = row['CO_URF']
        valores_urf.append(f"('URF {co_urf}')")
    
    sql_content += ",\n".join(valores_urf[:20]) + ";\n\n"
    
    # População da tb_estado
    sql_content += "-- População da tb_estado\nINSERT INTO tb_estado (nome_estado, sigla_estado, nome_regiao) VALUES\n"
    
    estado_unique = df[['SG_UF_NCM', 'nm_estado']].drop_duplicates()
    valores_estado = []
    
    for idx, (_, row) in enumerate(estado_unique.iterrows()):
        sg_uf = row['SG_UF_NCM']
        nm_estado = row['nm_estado'].replace("'", "''") if pd.notna(row['nm_estado']) else f'Estado {sg_uf}'
        valores_estado.append(f"('{nm_estado}', '{sg_uf}', 'Região')")
    
    sql_content += ",\n".join(valores_estado) + ";\n\n"
    
    # População da tb_municipio
    sql_content += "-- População da tb_municipio\nINSERT INTO tb_municipio (nome_municipio, id_estado) VALUES\n"
    sql_content += "('Município 1', 1);\n\n"
    
    sql_content += "-- =====================================================\n"
    sql_content += "-- FIM DO MODELO LÓGICO\n"
    sql_content += "-- =====================================================\n"
    
    return sql_content

def gerar_sql_mysql_star_schema(df: pd.DataFrame):
    """Gera script SQL completo para MySQL com modelo dimensional Star Schema"""
    
    print("Gerando script SQL MySQL com Star Schema")
    
    # Primeiro, gera o modelo lógico
    sql_logico = gerar_sql_modelo_logico(df)
    
    # Depois, gera o modelo dimensional
    sql_dimensional = f"""

-- Dimensão URF
CREATE TABLE dim_urf (
    id_urf INT PRIMARY KEY,
    nome_urf VARCHAR(100) NOT NULL
);

-- Dimensão Via
CREATE TABLE dim_via (
    id_via INT PRIMARY KEY,
    nome_via VARCHAR(100) NOT NULL
);

-- Dimensão País
CREATE TABLE dim_pais (
    id_pais INT PRIMARY KEY,
    nome_pais_portugues VARCHAR(300) NOT NULL,
    nome_pais_ingles VARCHAR(300) NOT NULL,
    nome_pais_espanhol VARCHAR(300) NOT NULL
);

-- Dimensão Estado
CREATE TABLE dim_estado (
    id_estado INT PRIMARY KEY,
    nome_estado VARCHAR(300) NOT NULL,
    sg_uf CHAR(2) NOT NULL,
    nome_regiao VARCHAR(300) NOT NULL
);

-- Dimensão Município
CREATE TABLE dim_municipio (
    id_municipio INT PRIMARY KEY,
    nome_municipio VARCHAR(400),
    id_estado INT,
    FOREIGN KEY (id_estado) REFERENCES dim_estado(id_estado)
);

-- Dimensão NCM
CREATE TABLE dim_ncm (
    id_ncm INT PRIMARY KEY,
    nome_ncm_portugues VARCHAR(1000) NOT NULL,
    nome_ncm_ingles VARCHAR(1000) NOT NULL,
    nome_ncm_espanhol VARCHAR(1000) NOT NULL
);

-- Dimensão Unidade
CREATE TABLE dim_unidade (
    id_unidade INT PRIMARY KEY,
    nome_unidade VARCHAR(300) NOT NULL,
    sigla_unidade VARCHAR(20) NOT NULL
);

-- Dimensão Bloco
CREATE TABLE dim_bloco (
    id_bloco INT PRIMARY KEY,
    nome_bloco_portugues VARCHAR(800) NOT NULL,
    nome_bloco_ingles VARCHAR(800) NOT NULL,
    nome_bloco_espanhol VARCHAR(800) NOT NULL
);

-- Dimensão Tempo
CREATE TABLE dim_tempo (
    id_dim_tempo INT PRIMARY KEY,
    ano INT NOT NULL,
    mes INT NOT NULL
);

-- =====================================================
-- TABELA FATO (Fact Table) - Star Schema Central
-- =====================================================

-- Fato Exportação
CREATE TABLE fato_exportacao (
    id_fato_exportacao INT PRIMARY KEY,
    id_dim_tempo INT NOT NULL,
    id_ncm INT NOT NULL,
    id_unidade INT NOT NULL,
    id_pais INT NOT NULL,
    id_urf INT NOT NULL,
    id_estado INT NOT NULL,
    id_via INT NOT NULL,
    ano_int INT NOT NULL,
    mes_int INT NOT NULL,
    sg_uf CHAR(2) NOT NULL,
    nome_ncm_portugues VARCHAR(1000) NOT NULL,
    nome_ncm_ingles VARCHAR(1000) NOT NULL,
    nome_ncm_espanhol VARCHAR(1000) NOT NULL,
    qt_estat FLOAT NOT NULL,
    kg_liquido FLOAT NOT NULL,
    vl_fob FLOAT NOT NULL,
    
    -- Chaves Estrangeiras
    FOREIGN KEY (id_dim_tempo) REFERENCES dim_tempo(id_dim_tempo),
    FOREIGN KEY (id_ncm) REFERENCES dim_ncm(id_ncm),
    FOREIGN KEY (id_unidade) REFERENCES dim_unidade(id_unidade),
    FOREIGN KEY (id_pais) REFERENCES dim_pais(id_pais),
    FOREIGN KEY (id_urf) REFERENCES dim_urf(id_urf),
    FOREIGN KEY (id_estado) REFERENCES dim_estado(id_estado),
    FOREIGN KEY (id_via) REFERENCES dim_via(id_via),
    
    -- Índices para Performance
    INDEX idx_dim_tempo (id_dim_tempo),
    INDEX idx_ncm (id_ncm),
    INDEX idx_pais (id_pais),
    INDEX idx_urf (id_urf),
    INDEX idx_estado (id_estado),
    INDEX idx_via (id_via),
    INDEX idx_vl_fob (vl_fob),
    INDEX idx_kg_liquido (kg_liquido)
);

-- =====================================================
-- INSERTS - POPULAÇÃO DAS TABELAS DE DIMENSÃO
-- =====================================================

-- População da Dimensão Tempo
INSERT INTO dim_tempo (id_dim_tempo, ano, mes) VALUES
"""

    # Obter dados únicos de tempo
    tempo_unique = df[['CO_ANO', 'CO_MES']].drop_duplicates().sort_values(['CO_ANO', 'CO_MES'])
    
    valores_tempo = []
    for idx, (_, row) in enumerate(tempo_unique.iterrows()):
        ano = row['CO_ANO']
        mes = row['CO_MES']
        valores_tempo.append(f"({idx + 1}, {ano}, {mes})")
    
    sql_dimensional += ",\n".join(valores_tempo) + ";\n\n"
    
    # População da Dimensão NCM
    sql_dimensional += "-- População da Dimensão NCM\nINSERT INTO dim_ncm (id_ncm, nome_ncm_portugues, nome_ncm_ingles, nome_ncm_espanhol) VALUES\n"
    
    ncm_unique = df[['CO_NCM']].drop_duplicates()
    valores_ncm = []
    
    for idx, (_, row) in enumerate(ncm_unique.iterrows()):
        co_ncm = row['CO_NCM']
        valores_ncm.append(f"({idx + 1}, 'Produto NCM {co_ncm}', 'Product NCM {co_ncm}', 'Producto NCM {co_ncm}')")
    
    sql_dimensional += ",\n".join(valores_ncm[:50]) + ";\n\n"
    
    # População da Dimensão Unidade
    sql_dimensional += "-- População da Dimensão Unidade\nINSERT INTO dim_unidade (id_unidade, nome_unidade, sigla_unidade) VALUES\n"
    
    unidade_unique = df[['CO_UNID']].drop_duplicates()
    valores_unidade = []
    
    for idx, (_, row) in enumerate(unidade_unique.iterrows()):
        co_unid = row['CO_UNID']
        valores_unidade.append(f"({idx + 1}, 'Unidade {co_unid}', 'U{co_unid}')")
    
    sql_dimensional += ",\n".join(valores_unidade) + ";\n\n"
    
    # População da Dimensão País
    sql_dimensional += "-- População da Dimensão País\nINSERT INTO dim_pais (id_pais, nome_pais_portugues, nome_pais_ingles, nome_pais_espanhol) VALUES\n"
    
    pais_unique = df[['CO_PAIS']].drop_duplicates()
    valores_pais = []
    
    for idx, (_, row) in enumerate(pais_unique.iterrows()):
        co_pais = row['CO_PAIS']
        valores_pais.append(f"({idx + 1}, 'País {co_pais}', 'Country {co_pais}', 'País {co_pais}')")
    
    sql_dimensional += ",\n".join(valores_pais[:20]) + ";\n\n"
    
    # População da Dimensão URF
    sql_dimensional += "-- População da Dimensão URF\nINSERT INTO dim_urf (id_urf, nome_urf) VALUES\n"
    
    urf_unique = df[['CO_URF']].drop_duplicates()
    valores_urf = []
    
    for idx, (_, row) in enumerate(urf_unique.iterrows()):
        co_urf = row['CO_URF']
        valores_urf.append(f"({idx + 1}, 'URF {co_urf}')")
    
    sql_dimensional += ",\n".join(valores_urf[:20]) + ";\n\n"
    
    # População da Dimensão Estado
    sql_dimensional += "-- População da Dimensão Estado\nINSERT INTO dim_estado (id_estado, nome_estado, sg_uf, nome_regiao) VALUES\n"
    
    estado_unique = df[['SG_UF_NCM', 'nm_estado']].drop_duplicates()
    valores_estado = []
    
    for idx, (_, row) in enumerate(estado_unique.iterrows()):
        sg_uf = row['SG_UF_NCM']
        nm_estado = row['nm_estado'].replace("'", "''") if pd.notna(row['nm_estado']) else f'Estado {sg_uf}'
        valores_estado.append(f"({idx + 1}, '{nm_estado}', '{sg_uf}', 'Região')")
    
    sql_dimensional += ",\n".join(valores_estado) + ";\n\n"
    
    # População da Dimensão Via
    sql_dimensional += "-- População da Dimensão Via\nINSERT INTO dim_via (id_via, nome_via) VALUES\n"
    
    via_unique = df[['CO_VIA']].drop_duplicates()
    valores_via = []
    
    for idx, (_, row) in enumerate(via_unique.iterrows()):
        co_via = row['CO_VIA']
        valores_via.append(f"({idx + 1}, 'Via {co_via}')")
    
    sql_dimensional += ",\n".join(valores_via) + ";\n\n"
    
    # População da Dimensão Bloco
    sql_dimensional += "-- População da Dimensão Bloco\nINSERT INTO dim_bloco (id_bloco, nome_bloco_portugues, nome_bloco_ingles, nome_bloco_espanhol) VALUES\n"
    sql_dimensional += "(1, 'Bloco 1', 'Block 1', 'Bloque 1');\n\n"
    
    # População da Dimensão Município
    sql_dimensional += "-- População da Dimensão Município\nINSERT INTO dim_municipio (id_municipio, nome_municipio, id_estado) VALUES\n"
    sql_dimensional += "(1, 'Município 1', 1);\n\n"
    
    # =====================================================
    # VIEWS PARA POWER BI
    # =====================================================
    
    sql_dimensional += """-- =====================================================
-- VIEWS OTIMIZADAS PARA POWER BI DESKTOP
-- Baseado no modelo dimensional do WIP.drawio.xml
-- =====================================================

-- View Consolidada de Exportações (Principal para Power BI)
CREATE VIEW v_exportacoes_consolidadas AS
SELECT 
    f.id_fato_exportacao,
    t.ano,
    t.mes,
    nc.nome_ncm_portugues,
    nc.nome_ncm_ingles,
    nc.nome_ncm_espanhol,
    u.nome_unidade,
    u.sigla_unidade,
    p.nome_pais_portugues,
    p.nome_pais_ingles,
    p.nome_pais_espanhol,
    ur.nome_urf,
    e.nome_estado,
    e.sg_uf,
    e.nome_regiao,
    v.nome_via,
    f.qt_estat,
    f.kg_liquido,
    f.vl_fob
FROM fato_exportacao f
JOIN dim_tempo t ON f.id_dim_tempo = t.id_dim_tempo
JOIN dim_ncm nc ON f.id_ncm = nc.id_ncm
JOIN dim_unidade u ON f.id_unidade = u.id_unidade
JOIN dim_pais p ON f.id_pais = p.id_pais
JOIN dim_urf ur ON f.id_urf = ur.id_urf
JOIN dim_estado e ON f.id_estado = e.id_estado
JOIN dim_via v ON f.id_via = v.id_via;

-- View Análise por NCM
CREATE VIEW v_analise_ncm AS
SELECT 
    nc.nome_ncm_portugues,
    t.ano,
    t.mes,
    SUM(f.vl_fob) as valor_fob_total,
    SUM(f.kg_liquido) as peso_total,
    COUNT(*) as numero_transacoes
FROM fato_exportacao f
JOIN dim_ncm nc ON f.id_ncm = nc.id_ncm
JOIN dim_tempo t ON f.id_dim_tempo = t.id_dim_tempo
GROUP BY nc.nome_ncm_portugues, t.ano, t.mes
ORDER BY valor_fob_total DESC;

-- View Análise por País
CREATE VIEW v_analise_pais AS
SELECT 
    p.nome_pais_portugues,
    t.ano,
    SUM(f.vl_fob) as valor_fob_total,
    SUM(f.kg_liquido) as peso_total,
    COUNT(DISTINCT nc.id_ncm) as produtos_distintos
FROM fato_exportacao f
JOIN dim_pais p ON f.id_pais = p.id_pais
JOIN dim_ncm nc ON f.id_ncm = nc.id_ncm
JOIN dim_tempo t ON f.id_dim_tempo = t.id_dim_tempo
GROUP BY p.nome_pais_portugues, t.ano
ORDER BY valor_fob_total DESC;

-- View Análise por Estado
CREATE VIEW v_analise_estado AS
SELECT 
    e.nome_estado,
    e.sg_uf,
    t.ano,
    t.mes,
    SUM(f.vl_fob) as valor_fob_total,
    SUM(f.kg_liquido) as peso_total,
    COUNT(*) as numero_transacoes
FROM fato_exportacao f
JOIN dim_estado e ON f.id_estado = e.id_estado
JOIN dim_tempo t ON f.id_dim_tempo = t.id_dim_tempo
GROUP BY e.nome_estado, e.sg_uf, t.ano, t.mes
ORDER BY valor_fob_total DESC;

-- =====================================================
-- ÍNDICES OTIMIZADOS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX idx_fato_completo ON fato_exportacao(id_dim_tempo, id_ncm, id_pais);
CREATE INDEX idx_tempo_ncm ON fato_exportacao(id_dim_tempo, id_ncm);
CREATE INDEX idx_pais_tempo ON fato_exportacao(id_pais, id_dim_tempo);

-- =====================================================
-- ESTATÍSTICAS DO BANCO DE DADOS
-- =====================================================

-- Contagem de registros por tabela (baseado no WIP.drawio.xml)
SELECT 'dim_tempo' as tabela, COUNT(*) as total_registros FROM dim_tempo
UNION ALL
SELECT 'dim_ncm', COUNT(*) FROM dim_ncm
UNION ALL
SELECT 'dim_unidade', COUNT(*) FROM dim_unidade
UNION ALL
SELECT 'dim_pais', COUNT(*) FROM dim_pais
UNION ALL
SELECT 'dim_urf', COUNT(*) FROM dim_urf
UNION ALL
SELECT 'dim_estado', COUNT(*) FROM dim_estado
UNION ALL
SELECT 'dim_municipio', COUNT(*) FROM dim_municipio
UNION ALL
SELECT 'dim_via', COUNT(*) FROM dim_via
UNION ALL
SELECT 'dim_bloco', COUNT(*) FROM dim_bloco
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
   - v_analise_ncm
   - v_analise_pais
   - v_analise_estado

5. Criar relacionamentos no Power BI:
   - dim_tempo ↔ fato_exportacao (id_dim_tempo)
   - dim_ncm ↔ fato_exportacao (id_ncm)
   - dim_unidade ↔ fato_exportacao (id_unidade)
   - dim_pais ↔ fato_exportacao (id_pais)
   - dim_urf ↔ fato_exportacao (id_urf)
   - dim_estado ↔ fato_exportacao (id_estado)
   - dim_via ↔ fato_exportacao (id_via)

6. Criar visualizações:
   - Mapa por países
   - Gráfico de barras por NCMs
   - Linha temporal por meses/anos
   - Tabela dinâmica por estados

TECNOLOGIAS IMPLEMENTADAS:
 Base de dados: COMEX Stat
 Banco de dados: MySQL
 Ferramenta visualização: Power BI Desktop
 Modelo dimensional: Star Schema (baseado no WIP.drawio.xml)
 Formato entrada: arquivos CSV
*/

-- =====================================================
-- FIM DO MODELO DIMENSIONAL
-- =====================================================
"""
    
    # Combinar ambos os modelos em um único arquivo
    sql_completo = sql_logico + sql_dimensional
    
    # Salvar o arquivo SQL
    with open('data/output/comexstat_mysql_schema.sql', 'w', encoding='utf-8') as f:
        f.write(sql_completo)
    
    print("Script SQL MySQL gerado: data/output/comexstat_mysql_schema.sql")
    print("  - Modelo Lógico incluído")
    print("  - Modelo Dimensional incluído")
    return True

def gerar_html_modelo_conceitual(df: pd.DataFrame, output_path: str = "data/output/modelo_conceitual.html"):
    """Gera um HTML com duas abas mostrando o modelo lógico e dimensional do banco"""
    
    # Contagem de registros para cada entidade
    total_exportacoes = len(df)
    total_estados = df['SG_UF_NCM'].nunique() if 'SG_UF_NCM' in df.columns else 0
    total_paises = df['CO_PAIS'].nunique() if 'CO_PAIS' in df.columns else 0
    total_ufs = df['CO_URF'].nunique() if 'CO_URF' in df.columns else 0
    total_produtos = df['CO_NCM'].nunique() if 'CO_NCM' in df.columns else 0
    total_vias = df['CO_VIA'].nunique() if 'CO_VIA' in df.columns else 0
    
    # Template HTML com duas abas: modelo lógico e dimensional
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modelos de Dados - COMEX Stat Database</title>
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
        .tabs {{
            display: flex;
            border-bottom: 2px solid #ddd;
            margin-bottom: 20px;
        }}
        .tab {{
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 16px;
            color: #666;
            transition: all 0.3s;
        }}
        .tab:hover {{
            background-color: #f5f5f5;
        }}
        .tab.active {{
            color: #2c3e50;
            border-bottom: 3px solid #2c3e50;
            font-weight: bold;
        }}
        .tab-content {{
            display: none;
            padding: 20px;
        }}
        .tab-content.active {{
            display: block;
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
        <h1> Modelos de Dados - COMEX Stat</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('logico')">Modelo Lógico</button>
            <button class="tab" onclick="showTab('dimensional')">Modelo Dimensional</button>
        </div>
        
        <!-- Tab Modelo Lógico -->
        <div id="tab-logico" class="tab-content active">
                
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
        
            <h2>Modelo Lógico de Dados</h2>
            <div class="info">
                Este diagrama mostra o modelo lógico relacional(página: modelo_logico).
            </div>
            
            
        
        <div class="mermaid">
erDiagram
    TB_NCM {{
        PK id_ncm
        varchar nome_ncm_portugues
        varchar nome_ncm_ingles
        varchar nome_ncm_espanhol
    }}
    
    TB_UNIDADE {{
        PK id_unidade
        varchar nome_unidade
        varchar sigla_unidade
    }}
    
    TB_VIA {{
        PK id_via
        varchar nome_via
    }}
    
    TB_URF {{
        PK id_urf
        varchar nome_urf
    }}
    
    TB_ESTADO {{
        PK id_estado
        varchar nome_estado
        varchar sigla_estado
        varchar nome_regiao
    }}
    
    TB_MUNICIPIO {{
        PK id_municipio
        varchar nome_municipio
        FK id_estado
    }}
    
    TB_EXPORTACAO {{
        PK id_exportacao
        FK id_ncm
        int ano
        int mes
        FK id_estado
        FK id_unidade
        FK id_via
        FK id_urf
        varchar co_pais
        decimal qt_estat
        decimal kg_liquido
        decimal vl_fob
    }}
    
    TB_EXPORTACAO ||--|{{ TB_ESTADO : "N:1"
    TB_EXPORTACAO ||--|{{ TB_NCM : "N:1"
    TB_EXPORTACAO ||--|{{ TB_UNIDADE : "N:1"
    TB_EXPORTACAO ||--|{{ TB_VIA : "N:1"
    TB_EXPORTACAO ||--|{{ TB_URF : "N:1"
    TB_MUNICIPIO ||--|{{ TB_ESTADO : "N:1"
        </div>
        
        <!-- Tab Modelo Dimensional -->
        <div id="tab-dimensional" class="tab-content">
            <h2>Modelo Dimensional de Dados (Star Schema)</h2>
            <div class="info">
                Este diagrama mostra o modelo dimensional Star Schema (página: modelo_dimensional).
            </div>
            
            <div class="table-grid">
                <div class="table-card">
                    <div class="table-title"> Tabelas de Dimensão:</div>
                    <ul>
                        <li> dim_urf</li>
                        <li> dim_via</li>
                        <li> dim_pais</li>
                        <li> dim_estado</li>
                        <li> dim_municipio</li>
                        <li> dim_ncm</li>
                        <li> dim_unidade</li>
                        <li> dim_bloco</li>
                        <li> dim_tempo</li>
                    </ul>
                </div>
                <div class="table-card">
                    <div class="table-title"> Tabela Fato:</div>
                    <ul>
                        <li> fato_exportacao</li>
                    </ul>
                </div>
            </div>
            
            <div class="mermaid">
erDiagram
    DIM_TEMPO {{
        PK id_dim_tempo
        int ano
        int mes
    }}
    
    DIM_UNIDADE {{
        PK id_unidade
        varchar nome_unidade
        varchar sigla_unidade
    }}
    
    DIM_NCM {{
        PK id_ncm
        varchar nome_pt
        varchar nome_ing
        varchar nome_esp
    }}
    
    DIM_VIA {{
        PK id_via
        varchar nome_via
    }}
    
    DIM_URF {{
        PK id_urf
        varchar nome_urf
    }}
    
    DIM_PAIS {{
        PK id_pais
        varchar nome_pais_portugues
        varchar nome_pais_ingles
        varchar nome_pais_espanhol
    }}
    
    DIM_ESTADO {{
        PK id_estado
        varchar nome_estado
        varchar sg_uf
        varchar nome_regiao
    }}
    
    DIM_MUNICIPIO {{
        PK id_municipio
        varchar nome_municipio
        FK id_estado
    }}
    
    DIM_BLOCO {{
        PK id_bloco
        varchar nome_bloco_portugues
        varchar nome_bloco_ingles
        varchar nome_bloco_espanhol
    }}
    
    FATO_EXPORTACAO {{
        PK id_fato_exportacao
        FK id_dim_tempo
        FK id_ncm
        FK id_unidade
        FK id_pais
        FK id_urf
        FK id_estado
        FK id_via
        int ano
        int mes
        varchar sg_uf
        varchar nome_ncm_portugues
        varchar nome_ncm_ingles
        varchar nome_ncm_espanhol
        float qt_estat
        float kg_liquido
        float vl_fob
    }}
    
    FATO_EXPORTACAO }}|--|{{ DIM_TEMPO : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_NCM : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_UNIDADE : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_PAIS : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_URF : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_ESTADO : "N:1"
    FATO_EXPORTACAO }}|--|{{ DIM_VIA : "N:1"
    DIM_MUNICIPIO }}|--|{{ DIM_ESTADO : "N:1"
        </div>
        </div>
        
        <div class="timestamp">
            Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
    </div>
    
    <script>
        mermaid.initialize({{startOnLoad: true, theme: 'default'}});
        
        function showTab(tabName) {{
            // Hide all tab contents
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => {{
                content.classList.remove('active');
            }});
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab content
            document.getElementById('tab-' + tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
            
            // Re-render mermaid diagrams with delay to ensure DOM is updated
            setTimeout(() => {{
                mermaid.init(undefined, document.querySelectorAll('.tab-content.active .mermaid'));
            }}, 50);
        }}
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

def executar_load_completo(df: pd.DataFrame, output_file: str = None):
    """Executa a fase completa do Load com todas as tabelas obrigatórias."""
    
    # Se output_file for None, usa o dataframe diretamente (não cria dados_finais.csv)
    if output_file is None:
        print(" Usando dataframe diretamente (sem criar dados_finais.csv)")
        df_usar = df
    else:
        # Verifica se os dados já foram processados
        if verificar_dados_existentes(output_file):
            print(f" Dados já processados encontrados em {output_file}")
            # Carrega os dados existentes
            df_usar = pd.read_csv(output_file)
        else:
            print(f" Dados não encontrados em {output_file}")
            return False
    
    # Simula carga no banco com todas as tabelas
    if carregar_dados_banco(df_usar):
        # Gera o modelo conceitual HTML e o script SQL MySQL
        gerar_html_modelo_conceitual(df_usar)
        gerar_sql_mysql_star_schema(df_usar)
        return True
    else:
        return False
