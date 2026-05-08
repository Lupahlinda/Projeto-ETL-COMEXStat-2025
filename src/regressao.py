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
    
    # Configurar estilo profissional
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('#f8f9fa')
    
    # Título principal
    fig.suptitle(f'📊 Análise de Regressão - COMEX Stat 2025\n{produto_alvo}', 
                 fontsize=16, fontweight='bold', color='#2c3e50', y=0.98)
    
    # === SUBPLOT 1: Previsões vs Valores Reais ===
    ax1 = plt.subplot(2, 2, 1)
    ax1.set_facecolor('#ffffff')
    
    # Scatter plot com gradiente de densidade
    scatter = ax1.scatter(y_test, y_pred, c=y_pred, cmap='viridis', alpha=0.6, s=30, edgecolors='none')
    
    # Linha de perfeição
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Linha Ideal (y=x)', alpha=0.8)
    
    ax1.set_xlabel('Valores Reais (VL_FOB)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Previsões do Modelo', fontsize=10, fontweight='bold')
    ax1.set_title('Previsões vs Valores Reais', fontsize=12, fontweight='bold', pad=10)
    ax1.legend(loc='upper left', framealpha=0.9)
    plt.colorbar(scatter, ax=ax1, label='Valor Previsto')
    
    # === SUBPLOT 2: Resíduos ===
    ax2 = plt.subplot(2, 2, 2)
    ax2.set_facecolor('#ffffff')
    
    residuos = y_test - y_pred
    ax2.scatter(y_pred, residuos, alpha=0.5, color='#3498db', s=20)
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.fill_between([y_pred.min(), y_pred.max()], [-mae, -mae], [mae, mae], 
                     alpha=0.2, color='green', label=f'±MAE ({mae:,.0f})')
    
    ax2.set_xlabel('Valores Previstos', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Resíduos (Real - Previsto)', fontsize=10, fontweight='bold')
    ax2.set_title('Análise de Resíduos', fontsize=12, fontweight='bold', pad=10)
    ax2.legend(loc='upper right')
    
    # === SUBPLOT 3: Histograma dos Resíduos ===
    ax3 = plt.subplot(2, 2, 3)
    ax3.set_facecolor('#ffffff')
    
    n, bins, patches = ax3.hist(residuos, bins=50, color='#667eea', alpha=0.7, edgecolor='black', linewidth=0.5)
    ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Resíduo = 0')
    ax3.axvline(x=residuos.mean(), color='green', linestyle='-', linewidth=2, label=f'Média: {residuos.mean():,.0f}')
    
    ax3.set_xlabel('Valor do Resíduo', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Frequência', fontsize=10, fontweight='bold')
    ax3.set_title('Distribuição dos Resíduos', fontsize=12, fontweight='bold', pad=10)
    ax3.legend()
    
    # === SUBPLOT 4: Painel de Métricas ===
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    ax4.set_facecolor('#f8f9fa')
    
    # Criar cards de estatísticas
    stats_text = f'''
    ╔══════════════════════════════════════════════════════════════╗
    ║                    📈 ESTATÍSTICAS DO MODELO                  ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  🔢 Registros Analisados:    {len(df_analise):>15,}                  ║
    ║  📊 Total no Dataset:        {len(df):>15,}                  ║
    ║                                                               ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                    🎯 MÉTRICAS DE ERRO                        ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  📉 MAE (Erro Absoluto):     R$ {mae:>15,.2f}               ║
    ║  📉 RMSE:                    R$ {rmse:>15,.2f}               ║
    ║  📉 MSE:                     R$ {mse:>15,.2e}               ║
    ║                                                               ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                 📊 QUALIDADE DO MODELO                        ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  🎯 R² Score:                {r2:>16.4f}                 ║
    ║  ✅ Precisão:                {(r2*100):>15.2f}%                  ║
    ║                                                               ║
    ╚══════════════════════════════════════════════════════════════╝
    
    💡 INTERPRETAÇÃO:
    • R² = {r2:.4f} indica que {(r2*100):.2f}% da variância é explicada
    • Quanto mais próximo de 1.0, melhor o modelo
    • MAE médio de R$ {mae:,.2f} por previsão
    '''
    
    ax4.text(0.5, 0.5, stats_text, transform=ax4.transAxes, fontsize=9,
             verticalalignment='center', horizontalalignment='center',
             fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='white', 
             edgecolor='#667eea', linewidth=2, alpha=0.95), linespacing=1.1)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    
    # Salva o gráfico com alta qualidade
    nome_arquivo = f'output/grafico_previsao_{produto_alvo}.png' if produto else 'output/grafico_previsao_completo.png'
    plt.savefig(nome_arquivo, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.show()
    print(f"📁 Gráfico salvo em: {nome_arquivo}")
    
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
