-- =====================================================
-- COMEX Stat 2025 - Banco de Dados MySQL
-- Modelo Dimensional: Star Schema
-- Tecnologias: MySQL, Power BI Desktop, CSV
-- Gerado em: 12/05/2026 07:03:33
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
(2025, 1, 'Janeiro', 1, 1, 'T1', '2025-01'),
(2025, 2, 'Fevereiro', 1, 1, 'T1', '2025-02'),
(2025, 3, 'Março', 1, 1, 'T1', '2025-03'),
(2025, 4, 'Abril', 2, 1, 'T2', '2025-04'),
(2025, 5, 'Maio', 2, 1, 'T2', '2025-05'),
(2025, 6, 'Junho', 2, 1, 'T2', '2025-06'),
(2025, 7, 'Julho', 3, 2, 'T3', '2025-07'),
(2025, 8, 'Agosto', 3, 2, 'T3', '2025-08'),
(2025, 9, 'Setembro', 3, 2, 'T3', '2025-09'),
(2025, 10, 'Outubro', 4, 2, 'T4', '2025-10'),
(2025, 11, 'Novembro', 4, 2, 'T4', '2025-11'),
(2025, 12, 'Dezembro', 4, 2, 'T4', '2025-12');

-- População da Dimensão Produto
INSERT INTO dim_produto (CO_NCM, id_product, descricao_produto, categoria_produto) VALUES
(4061090, 'LACTEOS', 'LACTEOS', 'OUTROS'),
(21032010, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(7039010, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(87162000, 'MAQUINAS_AGRICOLAS', 'MAQUINAS_AGRICOLAS', 'MAQUINAS'),
(15171000, 'OLEOS_VEGETAIS', 'OLEOS_VEGETAIS', 'OLEOS'),
(3061690, 'CARNES', 'CARNES', 'OUTROS'),
(17049020, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(4011010, 'LACTEOS', 'LACTEOS', 'OUTROS'),
(8043000, 'FRUTAS', 'FRUTAS', 'OUTROS'),
(7099300, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(19041000, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(20081100, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(7070000, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(16042010, 'PREPARACOES_ALIMENTICIAS_CONSERVAS', 'PREPARACOES_ALIMENTICIAS_CONSERVAS', 'PREPARACOES'),
(2032900, 'CARNES', 'CARNES', 'OUTROS'),
(12024200, 'AMENDOIM', 'AMENDOIM', 'OUTROS'),
(11022000, 'FARINHAS', 'FARINHAS', 'OUTROS'),
(15121911, 'OLEOS_VEGETAIS', 'OLEOS_VEGETAIS', 'OLEOS'),
(20081900, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(15079011, 'OLEOS_VEGETAIS', 'OLEOS_VEGETAIS', 'OLEOS'),
(20019000, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(23099010, 'FARELOS_TORTAS_PREPARACOES_PARA_ALIMENTACAO_ANIMAL', 'FARELOS_TORTAS_PREPARACOES_PARA_ALIMENTACAO_ANIMAL', 'FARELOS'),
(19053100, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(8093010, 'FRUTAS', 'FRUTAS', 'OUTROS'),
(3049900, 'CARNES', 'CARNES', 'OUTROS'),
(10063011, 'ARROZ', 'ARROZ', 'OUTROS'),
(9041200, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(2064900, 'CARNES', 'CARNES', 'OUTROS'),
(41071220, 'COUROS_PELES', 'COUROS_PELES', 'COUROS'),
(2023000, 'CARNES', 'CARNES', 'OUTROS'),
(8039000, 'FRUTAS', 'FRUTAS', 'OUTROS'),
(7039090, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(62063000, 'VESTUARIO', 'VESTUARIO', 'OUTROS'),
(7093000, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF'),
(43021910, 'ARTIGOS_COUROS_PELES', 'ARTIGOS_COUROS_PELES', 'ARTIGOS'),
(4011090, 'LACTEOS', 'LACTEOS', 'OUTROS'),
(19059090, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(45049000, 'CORTICA', 'CORTICA', 'OUTROS'),
(18069000, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(22089000, 'BEBIDAS_ALCOOLICAS', 'BEBIDAS_ALCOOLICAS', 'BEBIDAS'),
(2071100, 'CARNES', 'CARNES', 'OUTROS'),
(3035400, 'CARNES', 'CARNES', 'OUTROS'),
(10059010, 'MILHO', 'MILHO', 'OUTROS'),
(17011400, 'ACUCAR_ADOCANTES', 'ACUCAR_ADOCANTES', 'ACUCAR'),
(84329000, 'MAQUINAS_AGRICOLAS', 'MAQUINAS_AGRICOLAS', 'MAQUINAS'),
(4072100, 'OVOS', 'OVOS', 'OUTROS'),
(4090000, 'MEL', 'MEL', 'OUTROS'),
(19059020, 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS_MOLHOS_SUCOS_PREPARACOES_CONSERVAS_MASSAS_BOLACHAS_PAES_DOCES_GELEIAS_POS', 'EXTRATOS'),
(22060090, 'BEBIDAS_ALCOOLICAS', 'BEBIDAS_ALCOOLICAS', 'BEBIDAS'),
(7095900, 'HF_LEGUMES_TEMPEROS', 'HF_LEGUMES_TEMPEROS', 'HF');

-- População da Dimensão País
INSERT INTO dim_pais (CO_PAIS, id_country, nome_pais, CO_BLOCO, nome_bloco) VALUES
(741, 'SINGAPURA', 'SINGAPURA', NULL, NULL),
(163, 'CHIPRE', 'CHIPRE', NULL, NULL),
(190, 'COREIA_DO_SUL', 'COREIA_DO_SUL', NULL, NULL),
(63, 'ARGENTINA', 'ARGENTINA', NULL, NULL),
(434, 'LIBERIA', 'LIBERIA', NULL, NULL),
(301, 'GRECIA', 'GRECIA', NULL, NULL),
(351, 'HONG_KONG', 'HONG_KONG', NULL, NULL),
(293, 'GIBRALTAR', 'GIBRALTAR', NULL, NULL),
(476, 'MARSHALL_ILHAS', 'MARSHALL_ILHAS', NULL, NULL),
(586, 'PARAGUAI', 'PARAGUAI', NULL, NULL),
(580, 'PANAMA', 'PANAMA', NULL, NULL),
(232, 'DINAMARCA', 'DINAMARCA', NULL, NULL),
(795, 'TIMOR_LESTE', 'TIMOR_LESTE', NULL, NULL),
(158, 'CHILE', 'CHILE', NULL, NULL),
(275, 'FRANCA', 'FRANCA', NULL, NULL),
(538, 'NORUEGA', 'NORUEGA', NULL, NULL),
(845, 'URUGUAI', 'URUGUAI', NULL, NULL),
(40, 'ANGOLA', 'ANGOLA', NULL, NULL),
(756, 'AFRICA_DO_SUL', 'AFRICA_DO_SUL', NULL, NULL),
(160, 'CHINA', 'CHINA', NULL, NULL);

-- População da Dimensão Localidade
INSERT INTO dim_localidade (SG_UF_NCM, nm_estado, CO_URF, id_urf) VALUES
('PR', 'Paraná', 917800, 'PARANAGUA'),
('ES', 'Espírito Santo', 727600, 'VITORIA'),
('ES', 'Espírito Santo', 717800, 'ITAGUAI'),
('RS', 'Rio Grande do Sul', 1017500, 'URUGUAIANA'),
('MA', 'Maranhão', 317903, 'SAO_LUIS'),
('RJ', 'Rio de Janeiro', 717800, 'ITAGUAI'),
('SP', 'São Paulo', 817800, 'SANTOS'),
('RS', 'Rio Grande do Sul', 1017700, 'RIO_GRANDE'),
('RJ', 'Rio de Janeiro', 717600, 'RIO_DE_JANEIRO'),
('SC', 'Santa Catarina', 1017700, 'RIO_GRANDE'),
('SC', 'Santa Catarina', 917501, 'GUAIRA'),
('GO', 'Goiás', 927700, 'SAO_FRANCISCO_DO_SUL'),
('PR', 'Paraná', 927502, 'IMBITUBA'),
('MG', 'Minas Gerais', 817800, 'SANTOS'),
('ES', 'Espírito Santo', 710251, 'CAMPOS_DOS_GOYTACAZES'),
('SP', 'São Paulo', 917500, 'FOZ_DO_IGUACU'),
('SP', 'São Paulo', 1017500, 'URUGUAIANA'),
('SP', 'São Paulo', 812051, 'SAO_SEBASTIAO'),
('MG', 'Minas Gerais', 927700, 'SAO_FRANCISCO_DO_SUL'),
('RS', 'Rio Grande do Sul', 817700, 'CAMPINAS');

-- População da Dimensão Via
INSERT INTO dim_via (CO_VIA, id_via, descricao_via) VALUES
(1, 'VIA_1', 'Via Transporte 1'),
(7, 'VIA_7', 'Via Transporte 7'),
(15, 'VIA_15', 'Via Transporte 15'),
(4, 'VIA_4', 'Via Transporte 4'),
(0, 'VIA_0', 'Via Transporte 0'),
(3, 'VIA_3', 'Via Transporte 3'),
(2, 'VIA_2', 'Via Transporte 2'),
(6, 'VIA_6', 'Via Transporte 6'),
(9, 'VIA_9', 'Via Transporte 9'),
(12, 'VIA_12', 'Via Transporte 12');

-- População da Dimensão Unidade
INSERT INTO dim_unidade (CO_UNID, descricao_unidade) VALUES
(10, 'Unidade 10'),
(11, 'Unidade 11'),
(21, 'Unidade 21'),
(15, 'Unidade 15'),
(17, 'Unidade 17'),
(20, 'Unidade 20'),
(13, 'Unidade 13'),
(16, 'Unidade 16'),
(12, 'Unidade 12'),
(22, 'Unidade 22');

-- =====================================================
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
