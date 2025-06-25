"""
Configurações e constantes do sistema
"""

# Configurações dos prefixos por PA
PREFIXOS = {
    "PA1": {"CC13", "CC21", "CL2005", "CL3008", "CL3010", "CL3012", "CL3013", "CL3014",
            "CL3016", "CL3017", "CL3021", "CL3022", "CL3024", "CL3035", "CL3037",
            "CC02", "CC03", "CC09"},
    "PA2": {"CL19", "CL2002", "CL2004", "CL3002", "CL3003", "CL3004", "CL3005",
            "CL3006", "CL3009", "CL3015", "CL3036", "CL3039", "CL3042", "CL3043", "CL206"},
    "PA3": {"C11", "CL2001", "CL2003", "CL2006", "CL2018", "CL3001", "CL3011",
            "CL3018", "CL3023", "CL3025", "CL3027", "CL3030", "CL3032", "CL3033",
            "CL3024", "CL2013", "CL2014", "CL2015"},
    "PA4": {"CC04", "CC10", "CC14", "CL2007", "CL2008", "CL3007", "CL3019", "CL3020",
            "CL3026", "CL3028", "CL3029", "CL3031", "CL3038", "CL3040", "CL3041",
            "CC16", "CC17", "SL001"}
}

# Colunas a serem removidas do processamento
COLUNAS_REMOVER = [
    "CIDADE", "ESTADO", "LATITUDE", "LONGITUDE", "LIMIAR", "UO", "PONTO_REFERENCIA",
    "USUARIO FEEDBACK", "FEEDBACK VIDEO", "ULTIMO_COMENTARIO", "ATRIBUIDO",
    "CATEGORIA", "CERCA ELETRÔNICA", "INTEGRADOR", "GRUPO", "VISUALIZADO POR",
    "NIVEL", "RÓTULO"
]

# Adicionar configuração para tipos a serem desconsiderados
TIPOS_DESCONSIDERAR = {"EXCESSO_RPM", "BOCEJO"}

# Configurações de arquivo
ENCODING_CSV = "latin1"
PASTA_EXPORTADOS = "exportados"

# Configurações de interface melhoradas
WINDOW_TITLE = "🚛 Processador de Dados de Alertas - Sistema Avançado"
WINDOW_SIZE = "800x600"

# Configurações de gráficos
TOP_MOTORISTAS = 7

# Configurações CustomTkinter
CTK_THEME = "blue"  # blue, green, dark-blue
CTK_APPEARANCE = "dark"  # light, dark, system

# Cores personalizadas para CustomTkinter
CTK_COLORS = {
    'primary': "#1f538d",
    'primary_hover': "#14375e", 
    'secondary': "#2cc985",
    'secondary_hover': "#25a085",
    'accent': "#ff6b35",
    'background': "#212121",
    'surface': "#2b2b2b",
    'card': "#363636",
    'text': "#ffffff",
    'text_secondary': "#b0b0b0",
    'success': "#4caf50",
    'warning': "#ff9800",
    'error': "#f44336"
}
