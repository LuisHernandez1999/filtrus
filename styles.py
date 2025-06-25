"""
Configurações de estilo ultra profissional com cores bem variadas
"""

# Configurações do Matplotlib
MATPLOTLIB_CONFIG = {
    'font.family': ['Arial', 'DejaVu Sans', 'sans-serif'],
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 16,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '#d0d0d0',
    'axes.linewidth': 1,
    'grid.linewidth': 0.5,
    'lines.linewidth': 2,
    'patch.linewidth': 1,
    'patch.antialiased': True,
    'font.weight': 'normal',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold'
}

# Cores por tipo de alerta - MÁXIMA VARIAÇÃO (sem tons similares)
CORES_TIPO = {
    'EXCESSO_VELOCIDADE': '#DC2626',    # Vermelho forte
    'FREADA_BRUSCA': '#16A34A',         # Verde forte
    'ACELERACAO_BRUSCA': '#2563EB',     # Azul forte (apenas 1 azul)
    'CURVA_FECHADA': '#7C3AED',         # Roxo forte
    'FADIGA': '#EA580C',                # Laranja forte
    'OUTROS': '#6B7280'                 # Cinza neutro
}

# Cores por PA - MÁXIMA VARIAÇÃO (sem tons similares)
CORES_PA = {
    'PA1': '#DC2626',    # Vermelho
    'PA2': '#16A34A',    # Verde
    'PA3': '#7C3AED',    # Roxo
    'PA4': '#EA580C'     # Laranja
}

# Configurações do gráfico
GRAFICO_CONFIG = {
    'dpi': 300,
    'facecolor': 'white',
    'edgecolor': 'none',
    'figsize': (22, 16)
}

# Cores do tema clean
THEME_COLORS = {
    'primary': 'black',
    'secondary': 'black',
    'success': 'black',
    'warning': 'black',
    'error': 'black',
    'info': 'black',
    'text_primary': 'black',
    'text_secondary': 'black',
    'background': 'white',
    'surface': 'white',
    'border': '#d0d0d0'
}

# Meses em português
MESES_PT = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}
