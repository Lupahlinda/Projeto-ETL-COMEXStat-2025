import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def aplicar_regressao_completa(df, produto=None):
    """
    Aplica regressão para todos os produtos ou um produto específico.
    Se produto=None, processa todos os produtos disponíveis.
    """
    
    # Se não especificar produto, processa todos
    if produto is None:
        print("Aplicando modelo de regressão para TODOS os produtos...")
        df_analise = df.copy()
        produtos = df_analise['id_product'].unique()
        print(f"Produtos encontrados: {len(produtos)} tipos diferentes")
        print(f"Exemplos: {list(produtos[:10])}")
        produto_alvo = "TODOS_OS_PRODUTOS"
    else:
        print(f"Aplicando modelo de regressão para o produto {produto}...")
        df_analise = df[df['id_product'] == produto]
        produto_alvo = produto
    
    if df_analise.empty:
        print(f"O produto '{produto_alvo}' não foi encontrado no dataframe.")
        return
    
    # Selecionando variáveis preditoras (features) e variável alvo (target)
    X = df_analise[['CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID', 'CO_PAIS', 'SG_UF_NCM', 'CO_VIA', 'CO_URF', 'QT_ESTAT', 'KG_LIQUIDO']]
    y = df_analise['VL_FOB']
    
    # Dividindo os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Definindo um pipeline com pré-processamento e modelo
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['CO_PAIS', 'SG_UF_NCM'])  # Exemplo de variáveis categóricas
        ], 
        remainder='passthrough'  # As variáveis numéricas são passadas sem alteração
    )
    
    modelo = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())  # Modelo de regressão linear
    ])
    
    # Treinando o modelo
    modelo.fit(X_train, y_train)
    
    # Fazendo previsões
    y_pred = modelo.predict(X_test)
    
    # Exibindo as previsões e os valores reais
    print("Previsões:", y_pred[:5])  # Mostra as primeiras 5 previsões
    print("Valores reais:", y_test[:5].values)  # Mostra os primeiros valores reais
    
    # Calculando o erro quadrático médio (MSE)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Erro quadrático médio (MSE): {mse}")
    
    # Podemos também calcular o erro médio absoluto (MAE) para entender melhor a precisão
    mae = abs(y_test - y_pred).mean()
    print(f"Erro médio absoluto (MAE): {mae}")
    
    # Calcular R² Score para avaliar qualidade do modelo
    r2 = r2_score(y_test, y_pred)
    print(f"Coeficiente de Determinação (R²): {r2:.4f}")
    
    # Calcular RMSE
    rmse = np.sqrt(mse)
    print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse:,.2f}")
    
    # Calcular estatísticas do dataset para o novo card
    total_ncm = df['CO_NCM'].nunique()
    total_paises = df['CO_PAIS'].nunique()
    total_estados = df['SG_UF_NCM'].nunique()
    total_urfs = df['CO_URF'].nunique() if 'CO_URF' in df.columns else 0
    valor_total_fob = df['VL_FOB'].sum()
    peso_total_kg = df['KG_LIQUIDO'].sum()
    
    # Calcular top produtos e países para gráficos
    top_produtos = df.groupby('id_product')['VL_FOB'].sum().sort_values(ascending=False).head(10)
    top_paises = df.groupby('id_country')['VL_FOB'].sum().sort_values(ascending=False).head(10)
    
    # Função para truncar nomes longos
    def truncar_nome(nome, max_len=35):
        if len(nome) > max_len:
            return nome[:max_len-3] + '...'
        return nome
    
    # Aplicar truncamento nos índices
    top_produtos.index = [truncar_nome(str(x)) for x in top_produtos.index]
    top_paises.index = [truncar_nome(str(x), max_len=25) for x in top_paises.index]
    
    # Configurar estilo profissional
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor('#f8f9fa')
    
    # Título principal
    fig.suptitle(f' Análise de Regressão - COMEX Stat 2025\n{produto_alvo}', 
                 fontsize=16, fontweight='bold', color='#2c3e50', y=0.98)
    
    # ============================================
    # LINHA 1: CARD DATASET + GRÁFICOS DE DADOS
    # ============================================
    
    # === SUBPLOT 1: Estatísticas do Dataset (CARD) ===
    ax1 = plt.subplot(2, 3, 1)
    ax1.axis('off')
    ax1.set_facecolor('#f8f9fa')
    
    dataset_stats_text = f'''
    
                      ESTATÍSTICAS DO DATASET                   
    
                                                                   
       Total de Registros:      {len(df):>15,}                  
       Produtos NCM Únicos:     {total_ncm:>15,}                  
       Países de Destino:       {total_paises:>15,}                  
       Estados (UF):            {total_estados:>15,}                  
       URFs Utilizadas:         {total_urfs:>15,}                  
                                                                   
    
                         TOTAIS DE EXPORTAÇÃO                  
    
                                                                   
       Valor Total FOB:    R$ {valor_total_fob:>18,.2f}        
        Peso Total (kg):   {peso_total_kg:>18,.2f}               
                                                                   
    
                         MÉDIAS POR REGISTRO                   
    
                                                                   
       Média FOB:         R$ {valor_total_fob/len(df):>18,.2f}        
        Média Peso (kg):   {peso_total_kg/len(df):>18,.2f}               
                                                                   
    
    '''
    
    ax1.text(0.5, 0.5, dataset_stats_text, transform=ax1.transAxes, fontsize=9,
             verticalalignment='center', horizontalalignment='center',
             fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='white', 
             edgecolor='#28a745', linewidth=2, alpha=0.95), linespacing=1.1)
    
    # === SUBPLOT 2: Top 10 Produtos ===
    ax2 = plt.subplot(2, 3, 2)
    ax2.set_facecolor('#ffffff')
    
    top_produtos.plot(kind='barh', color='#3498db', ax=ax2, edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('Valor FOB (R$)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Produto (NCM)', fontsize=10, fontweight='bold')
    ax2.set_title(' Top 10 Produtos por Valor FOB', fontsize=12, fontweight='bold', pad=10)
    ax2.tick_params(axis='y', labelsize=8)
    ax2.invert_yaxis()  # Maior valor no topo
    
    # Formatar valores no eixo x
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x/1e6:.0f}M'))
    
    # === SUBPLOT 3: Top 10 Países ===
    ax3 = plt.subplot(2, 3, 3)
    ax3.set_facecolor('#ffffff')
    
    top_paises.plot(kind='barh', color='#e74c3c', ax=ax3, edgecolor='black', linewidth=0.5)
    ax3.set_xlabel('Valor FOB (R$)', fontsize=10, fontweight='bold')
    ax3.set_ylabel('País de Destino', fontsize=10, fontweight='bold')
    ax3.set_title(' Top 10 Países por Valor FOB', fontsize=12, fontweight='bold', pad=10)
    ax3.tick_params(axis='y', labelsize=8)
    ax3.invert_yaxis()  # Maior valor no topo
    
    # Formatar valores no eixo x
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x/1e6:.0f}M'))
    
    # ============================================
    # LINHA 2: CARD MODELO + GRÁFICOS DE MODELO
    # ============================================
    
    residuos = y_test - y_pred
    
    # === SUBPLOT 4: Estatísticas do Modelo (CARD) ===
    ax4 = plt.subplot(2, 3, 4)
    ax4.axis('off')
    ax4.set_facecolor('#f8f9fa')
    
    model_stats_text = f'''
    
                         ESTATÍSTICAS DO MODELO                 
    
                                                                  
       Registros Analisados:    {len(df_analise):>15,}          
       Total no Dataset:        {len(df):>15,}                  
                                                                  
    
                         MÉTRICAS DE ERRO                       
    
                                                                  
       MAE (Erro Absoluto):     R$ {mae:>15,.2f}                
       RMSE:                    R$ {rmse:>15,.2f}               
       MSE:                     R$ {mse:>15,.2e}                
                                                                  
    
                      QUALIDADE DO MODELO                       
    
                                                                  
       R² Score:                {r2:>16.4f}                     
       Precisão:                {(r2*100):>15.2f}%              
                                                                  
    
    
    INTERPRETAÇÃO:
    - R² = {r2:.4f} indica que {(r2*100):.2f}% da variância é explicada
    - Quanto mais próximo de 1.0, melhor o modelo
    - MAE médio de R$ {mae:,.2f} por previsão
    '''
    
    ax4.text(0.5, 0.5, model_stats_text, transform=ax4.transAxes, fontsize=9,
             verticalalignment='center', horizontalalignment='center',
             fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='white', 
             edgecolor='#667eea', linewidth=2, alpha=0.95), linespacing=1.1)
    
    # === SUBPLOT 5: Previsões vs Valores Reais ===
    ax5 = plt.subplot(2, 3, 5)
    ax5.set_facecolor('#ffffff')
    
    # Scatter plot com gradiente de densidade
    scatter = ax5.scatter(y_test, y_pred, c=y_pred, cmap='viridis', alpha=0.6, s=30, edgecolors='none')
    
    # Linha de perfeição
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax5.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Linha Ideal (y=x)', alpha=0.8)
    
    ax5.set_xlabel('Valores Reais (VL_FOB)', fontsize=10, fontweight='bold')
    ax5.set_ylabel('Previsões do Modelo', fontsize=10, fontweight='bold')
    ax5.set_title(' Previsões vs Valores Reais', fontsize=12, fontweight='bold', pad=10)
    ax5.legend(loc='upper left', framealpha=0.9)
    plt.colorbar(scatter, ax=ax5, label='Valor Previsto', fraction=0.046, pad=0.04)
    
    # === SUBPLOT 6: Análise de Resíduos ===
    ax6 = plt.subplot(2, 3, 6)
    ax6.set_facecolor('#ffffff')
    
    ax6.scatter(y_pred, residuos, alpha=0.5, color='#3498db', s=20)
    ax6.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax6.fill_between([y_pred.min(), y_pred.max()], [-mae, -mae], [mae, mae], 
                     alpha=0.2, color='green', label=f'±MAE ({mae:,.0f})')
    
    ax6.set_xlabel('Valores Previstos', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Resíduos (Real - Previsto)', fontsize=10, fontweight='bold')
    ax6.set_title(' Análise de Resíduos', fontsize=12, fontweight='bold', pad=10)
    ax6.legend(loc='upper right')
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    
    # Salva o gráfico com alta qualidade
    nome_arquivo = f'output/grafico_previsao_{produto_alvo}.png' if produto else 'output/grafico_previsao_completo.png'
    plt.savefig(nome_arquivo, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.show()
    print(f" Gráfico salvo em: {nome_arquivo}")
    
    return {
        'produto': produto_alvo,
        'mse': mse,
        'mae': mae,
        'registros_analisados': len(df_analise),
        'total_registros': len(df)
    }

def aplicar_regressao(df, produto):
    """Função legada para compatibilidade."""
    return aplicar_regressao_completa(df, produto)
