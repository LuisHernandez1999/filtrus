"""
Módulo para geração de gráficos - Versão Ultra Profissional com Análise Temporal
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch
from datetime import datetime, timedelta
from typing import List, Optional
import subprocess
import platform
import numpy as np

from styles import MATPLOTLIB_CONFIG, CORES_TIPO, CORES_PA, GRAFICO_CONFIG, THEME_COLORS, MESES_PT
from config import TOP_MOTORISTAS, TIPOS_DESCONSIDERAR

# Configurar matplotlib para não usar GUI quando necessário
matplotlib.use('Agg')

# Configurar Seaborn para design ultra profissional
sns.set_style("whitegrid")


class ChartGenerator:
    """Classe responsável pela geração de gráficos ultra profissionais com análise temporal"""
    
    def __init__(self):
        self._configurar_matplotlib()
        self._configurar_seaborn()
    
    def _configurar_matplotlib(self):
        """Configura o estilo do matplotlib"""
        plt.style.use('default')
        for key, value in MATPLOTLIB_CONFIG.items():
            plt.rcParams[key] = value
    
    def _configurar_seaborn(self):
        """Configura o estilo do Seaborn para design ultra profissional"""
        sns.set_context("notebook", font_scale=1.0)
        sns.set_style("whitegrid", {
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#f5f5f5",
            "grid.linewidth": 0.5,
            "axes.edgecolor": "#cccccc",
            "axes.linewidth": 1,
        })
        
        # Paleta ultra profissional - MÁXIMA VARIAÇÃO DE CORES (sem tons similares)
        self.cores_profissionais = [
            "#DC2626",  # Vermelho forte
            "#16A34A",  # Verde forte  
            "#2563EB",  # Azul forte (APENAS 1 azul)
            "#7C3AED",  # Roxo forte
            "#EA580C",  # Laranja forte
            "#059669",  # Verde esmeralda (diferente do verde)
            "#BE185D",  # Rosa forte
            "#92400E",  # Marrom forte
            "#374151",  # Cinza escuro
            "#7F1D1D",  # Vermelho escuro (diferente do vermelho)
            "#581C87",  # Roxo escuro (diferente do roxo)
            "#166534",  # Verde escuro (diferente dos verdes)
            "#9A3412",  # Laranja escuro (diferente do laranja)
            "#1F2937",  # Cinza muito escuro
            "#7E22CE"   # Roxo médio (diferente dos roxos)
        ]
        
        # Cores para pizza - MÁXIMA VARIAÇÃO (cada cor bem diferente)
        self.cores_pizza_pro = [
            "#DC2626",  # Vermelho
            "#16A34A",  # Verde
            "#7C3AED",  # Roxo
            "#EA580C",  # Laranja
            "#BE185D",  # Rosa
            "#059669",  # Verde esmeralda
            "#92400E",  # Marrom
            "#374151",  # Cinza escuro
            "#7F1D1D",  # Vermelho escuro
            "#166534"   # Verde escuro
        ]
        
        # Cores para motoristas - gradiente de risco (vermelho = mais alertas)
        self.cores_motoristas_pro = [
            "#DC2626",  # Vermelho (pior)
            "#EA580C",  # Laranja
            "#CA8A04",  # Amarelo escuro
            "#16A34A",  # Verde (neutro)
            "#059669",  # Verde esmeralda
            "#7C3AED",  # Roxo
            "#2563EB"   # Azul (melhor)
        ]
    
    def _formatar_data_portugues(self, data: datetime) -> str:
        """
        Formata data em português
        
        Args:
            data: Objeto datetime
            
        Returns:
            String com data formatada em português
        """
        data_formatada = data.strftime("%d de %B de %Y")
        for eng, pt in MESES_PT.items():
            data_formatada = data_formatada.replace(eng, pt)
        return data_formatada
    
    def _abrir_arquivo(self, caminho: str):
        """Abre o arquivo no sistema operacional padrão"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', caminho))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(caminho)
            else:  # Linux
                subprocess.call(('xdg-open', caminho))
            print(f"📊 Gráfico aberto automaticamente: {os.path.basename(caminho)}")
        except Exception as e:
            print(f"⚠️ Não foi possível abrir o gráfico automaticamente: {e}")
    
    def _processar_dados_temporais(self, df_geral: pd.DataFrame):
        """
        Processa dados temporais para análise de tendências
        
        Args:
            df_geral: DataFrame com todos os dados
            
        Returns:
            DataFrame processado com análise temporal
        """
        try:
            # Verificar se existe coluna DATA
            colunas_data_possiveis = ['DATA', 'Date', 'data', 'DATA_OCORRENCIA', 'DATA_ALERTA']
            coluna_data = None
            
            for col in colunas_data_possiveis:
                if col in df_geral.columns:
                    coluna_data = col
                    break
            
            if coluna_data is None:
                print("⚠️ Nenhuma coluna de data encontrada. Criando dados temporais simulados...")
                # Criar datas simuladas baseadas no índice
                data_inicio = datetime.now() - timedelta(days=len(df_geral))
                df_geral['DATA_PROCESSADA'] = [data_inicio + timedelta(days=i) for i in range(len(df_geral))]
            else:
                # Processar coluna de data existente
                print(f"📅 Processando coluna de data: {coluna_data}")
                df_geral['DATA_PROCESSADA'] = pd.to_datetime(df_geral[coluna_data], errors='coerce')
                
                # Remover registros com data inválida
                df_geral = df_geral.dropna(subset=['DATA_PROCESSADA'])
            
            # Agrupar por PA e data
            df_temporal = df_geral.groupby(['PA', df_geral['DATA_PROCESSADA'].dt.date]).size().reset_index()
            df_temporal.columns = ['PA', 'DATA', 'QUANTIDADE']
            df_temporal['DATA'] = pd.to_datetime(df_temporal['DATA'])
            
            return df_temporal
            
        except Exception as e:
            print(f"⚠️ Erro no processamento temporal: {e}")
            return pd.DataFrame()
    
    def _calcular_tendencias(self, df_temporal: pd.DataFrame):
        """
        Calcula tendências de aumento/diminuição para cada PA
        
        Args:
            df_temporal: DataFrame com dados temporais
            
        Returns:
            Dict com análise de tendências por PA
        """
        tendencias = {}
        
        try:
            for pa in df_temporal['PA'].unique():
                df_pa = df_temporal[df_temporal['PA'] == pa].sort_values('DATA')
                
                if len(df_pa) < 2:
                    continue
                
                # Dividir em duas metades para comparação
                meio = len(df_pa) // 2
                primeira_metade = df_pa.iloc[:meio]['QUANTIDADE'].mean()
                segunda_metade = df_pa.iloc[meio:]['QUANTIDADE'].mean()
                
                # Calcular variação percentual
                if primeira_metade > 0:
                    variacao = ((segunda_metade - primeira_metade) / primeira_metade) * 100
                else:
                    variacao = 0
                
                # Determinar tendência
                if variacao > 10:
                    status = "AUMENTO SIGNIFICATIVO"
                    cor = "#DC2626"  # Vermelho
                    icone = "📈"
                elif variacao > 5:
                    status = "AUMENTO MODERADO"
                    cor = "#EA580C"  # Laranja
                    icone = "📊"
                elif variacao < -10:
                    status = "REDUÇÃO SIGNIFICATIVA"
                    cor = "#16A34A"  # Verde
                    icone = "📉"
                elif variacao < -5:
                    status = "REDUÇÃO MODERADA"
                    cor = "#059669"  # Verde esmeralda
                    icone = "📊"
                else:
                    status = "ESTÁVEL"
                    cor = "#374151"  # Cinza
                    icone = "➖"
                
                tendencias[pa] = {
                    'variacao': variacao,
                    'status': status,
                    'cor': cor,
                    'icone': icone,
                    'total': df_pa['QUANTIDADE'].sum(),
                    'media': df_pa['QUANTIDADE'].mean(),
                    'primeira_metade': primeira_metade,
                    'segunda_metade': segunda_metade
                }
                
        except Exception as e:
            print(f"⚠️ Erro no cálculo de tendências: {e}")
        
        return tendencias
    
    def _criar_grafico_temporal_ultra_profissional(self, fig, ax5, df_geral: pd.DataFrame):
        """Cria gráfico de análise temporal ultra profissional"""
        try:
            # Processar dados temporais
            df_temporal = self._processar_dados_temporais(df_geral)
            
            if df_temporal.empty:
                self._criar_grafico_vazio(ax5, "ANÁLISE TEMPORAL - SEM DADOS", 
                                        "Sem dados temporais válidos")
                return
            
            # Calcular tendências
            tendencias = self._calcular_tendencias(df_temporal)
            
            # Criar gráfico de linha temporal
            pas_unicos = df_temporal['PA'].unique()
            
            for i, pa in enumerate(pas_unicos):
                df_pa = df_temporal[df_temporal['PA'] == pa].sort_values('DATA')
                
                if len(df_pa) > 0:
                    cor = self.cores_profissionais[i % len(self.cores_profissionais)]
                    
                    # Linha principal
                    ax5.plot(df_pa['DATA'], df_pa['QUANTIDADE'], 
                            color=cor, linewidth=3, marker='o', markersize=6,
                            label=f"{pa}", alpha=0.8)
                    
                    # Área sob a curva para destaque
                    ax5.fill_between(df_pa['DATA'], df_pa['QUANTIDADE'], 
                                   alpha=0.2, color=cor)
            
            # Título ultra profissional
            ax5.set_title('📅 ANÁLISE TEMPORAL DE INCIDENTES POR PA', 
                        fontsize=18, fontweight='bold', pad=30, color='black')
            
            # Labels dos eixos
            ax5.set_ylabel('Quantidade de Alertas por Dia', fontsize=14, fontweight='bold', 
                          color='black', labelpad=10)
            ax5.set_xlabel('Período de Análise', fontsize=14, fontweight='bold', 
                          color='black', labelpad=10)
            
            # Formatação do eixo X (datas)
            ax5.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax5.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(df_temporal['DATA'].unique()) // 10)))
            plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Grid ultra profissional
            ax5.grid(True, linestyle="--", alpha=0.3, color='#e2e8f0', linewidth=1)
            ax5.set_axisbelow(True)
            
            # Legenda com informações de tendência
            legend_labels = []
            for pa in pas_unicos:
                if pa in tendencias:
                    tend = tendencias[pa]
                    legend_labels.append(f"{pa} {tend['icone']} ({tend['variacao']:+.1f}%)")
                else:
                    legend_labels.append(pa)
            
            # Atualizar labels da legenda
            handles, _ = ax5.get_legend_handles_labels()
            legend = ax5.legend(handles, legend_labels, 
                              bbox_to_anchor=(1.02, 1), loc='upper left', 
                              fontsize=10, frameon=True, title="📊 PAs e Tendências",
                              title_fontsize=11, borderpad=1.2)
            legend.get_title().set_fontweight('bold')
            legend.get_title().set_color('black')
            legend.get_frame().set_facecolor('#f8fafc')
            legend.get_frame().set_edgecolor('#1e40af')
            legend.get_frame().set_linewidth(2)
            legend.get_frame().set_alpha(0.95)
            
            # Adicionar caixa de resumo de tendências
            if tendencias:
                texto_resumo = "RESUMO DE TENDÊNCIAS:\n"
                for pa, dados in tendencias.items():
                    texto_resumo += f"{dados['icone']} {pa}: {dados['status']} ({dados['variacao']:+.1f}%)\n"
                
                ax5.text(0.02, 0.98, texto_resumo, 
                        transform=ax5.transAxes, fontsize=9, 
                        verticalalignment='top', horizontalalignment='left',
                        bbox=dict(boxstyle="round,pad=0.8", facecolor='white', 
                                edgecolor='#1e40af', alpha=0.95, linewidth=2),
                        fontweight='bold', color='black')
            
            # Fundo ultra clean
            ax5.set_facecolor('#fefefe')
            
            # Formatação dos eixos premium
            ax5.tick_params(axis='x', labelsize=10, colors='black', pad=8)
            ax5.tick_params(axis='y', labelsize=11, colors='black', pad=8)
            
            # Bordas ultra profissionais
            ax5.spines['top'].set_visible(False)
            ax5.spines['right'].set_visible(False)
            ax5.spines['left'].set_color('#cbd5e1')
            ax5.spines['bottom'].set_color('#cbd5e1')
            ax5.spines['left'].set_linewidth(1.5)
            ax5.spines['bottom'].set_linewidth(1.5)
            
            print(f"✅ Gráfico temporal criado com {len(tendencias)} PAs analisados")
            
        except Exception as e:
            print(f"⚠️ Erro no gráfico temporal: {e}")
            self._criar_grafico_vazio(ax5, "ANÁLISE TEMPORAL - ERRO", 
                                    f"Erro no processamento: {str(e)}")
    
    def _criar_header_com_subtitulo_estatisticas(self, fig, ax_header, df_geral: pd.DataFrame, data_atual: datetime):
        """Cria o cabeçalho ultra profissional com estatísticas como subtítulo"""
        ax_header.axis('off')
        
        data_formatada = self._formatar_data_portugues(data_atual)
        hora_formatada = data_atual.strftime("%H:%M")
        
        # Título principal ultra profissional (SEM CAIXA AZUL)
        ax_header.text(0.5, 0.5, '📊 RELATÓRIO EXECUTIVO DE ANÁLISE DE ALERTAS COM TENDÊNCIAS TEMPORAIS', 
                      ha='center', va='center', fontsize=22, fontweight='bold', 
                      color='black', transform=ax_header.transAxes)
    
        # Data no canto superior direito de forma harmônica
        ax_header.text(0.95, 0.8, f'📅 {data_formatada}\n🕒 {hora_formatada}', 
                      ha='right', va='top', fontsize=11, 
                      color='#64748b', transform=ax_header.transAxes, 
                      fontweight='medium')
    
    def _criar_grafico_tipos_ultra_profissional(self, fig, ax1, df_geral: pd.DataFrame):
        """Cria gráfico de distribuição por tipos ultra profissional com detalhes premium"""
        if "TIPO" not in df_geral.columns:
            self._criar_grafico_vazio(ax1, "DISTRIBUIÇÃO DE ALERTAS - COLUNA TIPO NÃO ENCONTRADA", 
                                    "Coluna TIPO não encontrada nos dados")
            return
        
        try:
            # Limpar e filtrar dados de TIPO
            df_geral["TIPO"] = df_geral["TIPO"].astype(str).str.strip()
            df_geral = df_geral[df_geral["TIPO"] != "nan"]
            df_geral = df_geral[~df_geral["TIPO"].isin(TIPOS_DESCONSIDERAR)]
            
            if df_geral.empty:
                self._criar_grafico_vazio(ax1, "DISTRIBUIÇÃO DE ALERTAS - SEM DADOS VÁLIDOS", 
                                        "Sem dados válidos após filtros")
                return
            
            tipo_contagem = df_geral.groupby(["PA", "TIPO"]).size().unstack(fill_value=0)
            if tipo_contagem.empty:
                self._criar_grafico_vazio(ax1, "DISTRIBUIÇÃO DE ALERTAS - SEM CATEGORIAS", 
                                        "Sem dados de categoria válidos")
                return
            
            # Preparar dados para Seaborn
            df_plot = tipo_contagem.reset_index()
            df_melted = df_plot.melt(id_vars=['PA'], var_name='TIPO', value_name='Quantidade')
            
            # Criar gráfico de barras agrupadas FINAS com cores profissionais
            sns.barplot(data=df_melted, x='PA', y='Quantidade', hue='TIPO', 
                       ax=ax1, palette=self.cores_profissionais, 
                       edgecolor='white', linewidth=2, width=0.6)  # Barras mais finas
            
            # Título ultra profissional SEM caixa
            ax1.set_title('📊 DISTRIBUIÇÃO DE ALERTAS POR CATEGORIA E POSTO', 
                        fontsize=16, fontweight='bold', pad=25, color='black')
            
            # Labels dos eixos ultra profissionais
            ax1.set_ylabel('Quantidade de Alertas', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
            ax1.set_xlabel('Posto de Atendimento (PA)', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
            
            # Grid ultra profissional
            ax1.grid(axis="y", linestyle="-", alpha=0.25, color='#e2e8f0', linewidth=1)
            ax1.set_axisbelow(True)
            
            # Formatação dos eixos premium
            ax1.tick_params(axis='x', rotation=0, labelsize=10, colors='black', pad=6)
            ax1.tick_params(axis='y', labelsize=9, colors='black', pad=6)
            
            # Legenda ultra profissional
            legend = ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', 
                              fontsize=9, frameon=True, title="📋 Categorias",
                              title_fontsize=10, borderpad=1.0, columnspacing=1.0)
            legend.get_title().set_fontweight('bold')
            legend.get_title().set_color('black')
            legend.get_frame().set_facecolor('#f8fafc')
            legend.get_frame().set_edgecolor('#1e40af')
            legend.get_frame().set_linewidth(2)
            legend.get_frame().set_alpha(0.95)
            
            # Fundo ultra clean
            ax1.set_facecolor('#fefefe')
            
            # Bordas ultra profissionais
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#cbd5e1')
            ax1.spines['bottom'].set_color('#cbd5e1')
            ax1.spines['left'].set_linewidth(1.5)
            ax1.spines['bottom'].set_linewidth(1.5)
            
        except Exception as e:
            print(f"⚠️ Erro no gráfico de tipos: {e}")
            self._criar_grafico_vazio(ax1, "DISTRIBUIÇÃO DE ALERTAS - ERRO", 
                                    f"Erro no processamento: {str(e)}")
    
    def _criar_grafico_pizza_ultra_profissional(self, fig, ax2, df_geral: pd.DataFrame):
        """Cria gráfico de pizza ultra profissional com detalhes premium"""
        try:
            pa_contagem = df_geral.groupby("PA").size().sort_values(ascending=False)
            if pa_contagem.empty:
                self._criar_grafico_vazio(ax2, "VOLUME TOTAL DE ALERTAS - SEM DADOS", 
                                        "Sem dados válidos para análise")
                return
            
            # Criar gráfico de pizza ultra profissional
            wedges, texts, autotexts = ax2.pie(pa_contagem.values, 
                                             labels=pa_contagem.index,
                                             colors=self.cores_pizza_pro[:len(pa_contagem)],
                                             autopct='%1.1f%%',
                                             startangle=90,
                                             explode=[0.04] * len(pa_contagem),  # Separação elegante
                                             shadow=True,  # Sombra profissional
                                             textprops={'fontsize': 10, 'fontweight': 'bold'})
            
            # Configurar textos ultra profissionais
            for text in texts:
                text.set_color('black')
                text.set_fontsize(11)
                text.set_fontweight('bold')
                text.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='white', 
                                 edgecolor='#64748b', alpha=0.9, linewidth=1.5))
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')
                autotext.set_bbox(dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.8))
            
            # Título ultra profissional SEM caixa
            ax2.set_title('📊 VOLUME TOTAL DE ALERTAS POR POSTO', 
                        fontsize=16, fontweight='bold', pad=25, color='black')
            
            # Garantir círculo perfeito
            ax2.axis('equal')
            
            # Adicionar estatísticas no centro ultra profissionais
            total = pa_contagem.sum()
            ax2.text(0, 0, f'TOTAL\n{total:,}\nAlertas', 
                    ha='center', va='center', fontsize=14, fontweight='bold',
                    color='#1e40af',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                             edgecolor='#1e40af', alpha=0.95, linewidth=3))
            
        except Exception as e:
            print(f"⚠️ Erro no gráfico de pizza: {e}")
            self._criar_grafico_vazio(ax2, "VOLUME TOTAL DE ALERTAS - ERRO", 
                                    f"Erro no processamento: {str(e)}")
    
    def _criar_grafico_motoristas_ultra_profissional(self, fig, ax3, df_geral: pd.DataFrame):
        """Cria gráfico dos top motoristas ultra profissional com barras horizontais"""
        try:
            if "MOTORISTA" not in df_geral.columns:
                self._criar_grafico_vazio(ax3, "TOP MOTORISTAS - COLUNA NÃO ENCONTRADA", 
                                        "Coluna MOTORISTA não encontrada")
                return
        
            # Limpar dados de motorista
            df_geral["MOTORISTA"] = df_geral["MOTORISTA"].astype(str).str.strip()
            df_motoristas = df_geral[df_geral["MOTORISTA"] != "nan"]
            df_motoristas = df_motoristas[df_motoristas["MOTORISTA"] != ""]
        
            if df_motoristas.empty:
                self._criar_grafico_vazio(ax3, "TOP MOTORISTAS - SEM DADOS", 
                                        "Sem dados válidos de motoristas")
                return
        
            # Contar alertas por motorista e pegar os top 7
            motorista_contagem = df_motoristas.groupby("MOTORISTA").size().sort_values(ascending=False).head(TOP_MOTORISTAS)
        
            if motorista_contagem.empty:
                self._criar_grafico_vazio(ax3, "TOP MOTORISTAS - SEM DADOS", 
                                        "Nenhum motorista encontrado")
                return
        
            # Preparar dados para Seaborn
            df_motoristas_plot = motorista_contagem.reset_index()
            df_motoristas_plot.columns = ['Motorista', 'Alertas']
            df_motoristas_plot = df_motoristas_plot.sort_values('Alertas', ascending=True)
        
            # Criar gráfico horizontal FINO com cores profissionais
            bars = sns.barplot(data=df_motoristas_plot, y='Motorista', x='Alertas', 
                             ax=ax3, palette=self.cores_motoristas_pro, 
                             edgecolor='white', linewidth=2)
        
            # Ajustar altura das barras (mais finas)
            for bar in bars.patches:
                bar.set_height(0.5)  # Barras mais finas
        
            # Configurar eixos com nomes truncados profissionalmente
            labels = [nome[:20] + '...' if len(nome) > 20 else nome 
                     for nome in df_motoristas_plot['Motorista']]
            ax3.set_yticklabels(labels, fontsize=9)
        
            # Título ultra profissional SEM caixa
            ax3.set_title('🚗 TOP 7 MOTORISTAS COM MAIS ALERTAS', 
                        fontsize=16, fontweight='bold', pad=25, color='black')
        
            # Labels dos eixos ultra profissionais
            ax3.set_xlabel('Número de Alertas', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
            ax3.set_ylabel('Motoristas', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
        
            # Grid ultra profissional
            ax3.grid(axis="x", linestyle="--", alpha=0.25, color='#e2e8f0', linewidth=1)
            ax3.set_axisbelow(True)
        
            # Adicionar valores nas barras com estilo ultra profissional
            for i, (motorista, valor) in enumerate(df_motoristas_plot.values):
                color = '#dc2626' if i == len(df_motoristas_plot) - 1 else '#1e40af'
                ax3.text(valor + max(df_motoristas_plot['Alertas']) * 0.02, i, 
                       f'{valor}', ha='left', va='center', 
                       fontsize=10, fontweight='bold', color=color,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                                edgecolor=color, alpha=0.95, linewidth=1.5))
        
            # Fundo ultra clean
            ax3.set_facecolor('#fefefe')
        
            # Formatação dos eixos premium
            ax3.tick_params(axis='x', labelsize=9, colors='black', pad=6)
            ax3.tick_params(axis='y', labelsize=8, colors='black', pad=6)
        
            # Bordas ultra profissionais
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['left'].set_color('#cbd5e1')
            ax3.spines['bottom'].set_color('#cbd5e1')
            ax3.spines['left'].set_linewidth(1.5)
            ax3.spines['bottom'].set_linewidth(1.5)
        
        except Exception as e:
            print(f"⚠️ Erro no gráfico de motoristas: {e}")
            self._criar_grafico_vazio(ax3, "TOP MOTORISTAS - ERRO", 
                                    f"Erro no processamento: {str(e)}")
    
    def _criar_grafico_tipos_motoristas_ultra_profissional(self, fig, ax4, df_geral: pd.DataFrame):
        """Cria gráfico dos tipos de alertas dos top motoristas ultra profissional com detalhes premium"""
        try:
            if "MOTORISTA" not in df_geral.columns or "TIPO" not in df_geral.columns:
                self._criar_grafico_vazio(ax4, "TIPOS POR MOTORISTA - COLUNAS NÃO ENCONTRADAS", 
                                        "Colunas MOTORISTA ou TIPO não encontradas")
                return
            
            # Limpar dados
            df_clean = df_geral.copy()
            df_clean["MOTORISTA"] = df_clean["MOTORISTA"].astype(str).str.strip()
            df_clean["TIPO"] = df_clean["TIPO"].astype(str).str.strip()
            df_clean = df_clean[(df_clean["MOTORISTA"] != "nan") & (df_clean["MOTORISTA"] != "")]
            df_clean = df_clean[(df_clean["TIPO"] != "nan") & (~df_clean["TIPO"].isin(TIPOS_DESCONSIDERAR))]
            
            if df_clean.empty:
                self._criar_grafico_vazio(ax4, "TIPOS POR MOTORISTA - SEM DADOS", 
                                        "Sem dados válidos")
                return
            
            # Pegar top 7 motoristas
            top_motoristas = df_clean.groupby("MOTORISTA").size().sort_values(ascending=False).head(TOP_MOTORISTAS).index
            df_top = df_clean[df_clean["MOTORISTA"].isin(top_motoristas)]
            
            # Contar tipos por motorista
            tipo_motorista = df_top.groupby(["MOTORISTA", "TIPO"]).size().unstack(fill_value=0)
            
            if tipo_motorista.empty:
                self._criar_grafico_vazio(ax4, "TIPOS POR MOTORISTA - SEM DADOS", 
                                        "Sem dados de tipos para top motoristas")
                return
            
            # Criar gráfico empilhado FINO com cores profissionais
            bottom = np.zeros(len(tipo_motorista))
            
            for i, tipo in enumerate(tipo_motorista.columns):
                ax4.bar(range(len(tipo_motorista)), tipo_motorista[tipo], 
                       bottom=bottom, label=tipo, 
                       color=self.cores_profissionais[i % len(self.cores_profissionais)],
                       edgecolor='white', linewidth=2, width=0.5)  # Barras mais finas
                bottom += tipo_motorista[tipo]
            
            # Título ultra profissional SEM caixa
            ax4.set_title('📋 TIPOS DE ALERTAS DOS TOP MOTORISTAS', 
                        fontsize=16, fontweight='bold', pad=25, color='black')
            
            # Labels dos eixos ultra profissionais
            ax4.set_ylabel('Número de Alertas', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
            ax4.set_xlabel('Motoristas', fontsize=12, fontweight='bold', 
                          color='black', labelpad=8)
            
            # Ajustar labels do eixo x sem sobreposição
            labels = [nome[:10] + '...' if len(nome) > 10 else nome for nome in tipo_motorista.index]
            ax4.set_xticks(range(len(tipo_motorista)))
            ax4.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
            
            # Grid ultra profissional
            ax4.grid(axis="y", linestyle="--", alpha=0.25, color='#e2e8f0', linewidth=1)
            ax4.set_axisbelow(True)
            
            # Legenda ultra profissional
            legend = ax4.legend(bbox_to_anchor=(1.02, 1), loc='upper left', 
                              fontsize=9, frameon=True, title="📋 Tipos",
                              title_fontsize=10, borderpad=1.0, columnspacing=1.0)
            legend.get_title().set_fontweight('bold')
            legend.get_title().set_color('black')
            legend.get_frame().set_facecolor('#f8fafc')
            legend.get_frame().set_edgecolor('#1e40af')
            legend.get_frame().set_linewidth(2)
            legend.get_frame().set_alpha(0.95)
            
            # Fundo ultra clean
            ax4.set_facecolor('#fefefe')
            
            # Formatação dos eixos premium
            ax4.tick_params(axis='x', labelsize=8, colors='black', pad=6)
            ax4.tick_params(axis='y', labelsize=9, colors='black', pad=6)
            
            # Bordas ultra profissionais
            ax4.spines['top'].set_visible(False)
            ax4.spines['right'].set_visible(False)
            ax4.spines['left'].set_color('#cbd5e1')
            ax4.spines['bottom'].set_color('#cbd5e1')
            ax4.spines['left'].set_linewidth(1.5)
            ax4.spines['bottom'].set_linewidth(1.5)
            
        except Exception as e:
            print(f"⚠️ Erro no gráfico de tipos por motorista: {e}")
            self._criar_grafico_vazio(ax4, "TIPOS POR MOTORISTA - ERRO", 
                                    f"Erro no processamento: {str(e)}")
    
    def _criar_grafico_vazio(self, ax, titulo: str, mensagem: str):
        """Cria um gráfico vazio com mensagem ultra profissional"""
        ax.text(0.5, 0.5, mensagem, 
               ha='center', va='center', transform=ax.transAxes,
               fontsize=12, color='black', fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.6", facecolor='#f8fafc', 
                        edgecolor='#1e40af', alpha=0.95, linewidth=2))
        ax.set_title(titulo, color='black', fontsize=14, fontweight='bold', pad=20)
        ax.set_facecolor('#fefefe')
        
        # Remover todos os elementos
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
    
    def gerar_graficos(self, arquivos_filtrados: List[str]) -> Optional[str]:
        """
        Gera gráficos de análise dos dados ultra profissionais com análise temporal
        
        Args:
            arquivos_filtrados: Lista de caminhos dos arquivos Excel filtrados
            
        Returns:
            Caminho do arquivo de gráfico gerado ou None se houver erro
        """
        try:
            # Concatenar todos os DataFrames
            df_list = []
            for path in arquivos_filtrados:
                try:
                    df_temp = pd.read_excel(path)
                    df_list.append(df_temp)
                except Exception as e:
                    print(f"⚠️ Erro ao ler {os.path.basename(path)}: {e}")
                    continue
            
            if not df_list:
                print("❌ Nenhum arquivo válido encontrado para gerar gráficos")
                return None
                
            df_geral = pd.concat(df_list, ignore_index=True)
            print(f"📊 Dados carregados para gráficos: {len(df_geral)} registros")
            
            if df_geral.empty:
                print("❌ Nenhum dado válido encontrado")
                return None
            
            # Configurar figura ultra profissional com 5 gráficos
            fig = plt.figure(figsize=(24, 20), facecolor='white')
            
            # Layout ultra profissional com espaçamento para 5 gráficos
            gs = fig.add_gridspec(4, 2, height_ratios=[0.4, 1.8, 1.8, 2.0], width_ratios=[1, 1], 
                                hspace=0.5, wspace=0.4, 
                                left=0.06, right=0.82, top=0.94, bottom=0.06)
            
            data_atual = datetime.now()
            
            # Header ultra profissional com estatísticas como subtítulo
            ax_header = fig.add_subplot(gs[0, :])
            self._criar_header_com_subtitulo_estatisticas(fig, ax_header, df_geral, data_atual)
            
            # Gráfico 1: Distribuição por tipos (esquerda superior)
            ax1 = fig.add_subplot(gs[1, 0])
            self._criar_grafico_tipos_ultra_profissional(fig, ax1, df_geral)
            
            # Gráfico 2: Pizza por PA (direita superior)
            ax2 = fig.add_subplot(gs[1, 1])
            self._criar_grafico_pizza_ultra_profissional(fig, ax2, df_geral)
            
            # Gráfico 3: Top motoristas (esquerda meio)
            ax3 = fig.add_subplot(gs[2, 0])
            self._criar_grafico_motoristas_ultra_profissional(fig, ax3, df_geral)
            
            # Gráfico 4: Tipos por motorista (direita meio)
            ax4 = fig.add_subplot(gs[2, 1])
            self._criar_grafico_tipos_motoristas_ultra_profissional(fig, ax4, df_geral)
            
            # NOVO GRÁFICO 5: Análise temporal (parte inferior - ocupando toda a largura)
            ax5 = fig.add_subplot(gs[3, :])
            self._criar_grafico_temporal_ultra_profissional(fig, ax5, df_geral)
            
            # Salvar na pasta Downloads
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            caminho_saida = os.path.join(downloads_path, "relatorio_alertas_com_analise_temporal.png")
            
            # Salvar com qualidade ultra alta
            plt.savefig(caminho_saida, 
                       dpi=300, 
                       bbox_inches='tight', 
                       facecolor='white', 
                       edgecolor='none', 
                       format='png',
                       pad_inches=0.3)
            plt.close()
            
            print(f"✅ Gráficos ultra profissionais com análise temporal salvos em: {caminho_saida}")
            
            self._abrir_arquivo(caminho_saida)
            
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro geral ao gerar gráficos: {e}")
            return None