import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from datetime import datetime

matplotlib.use('Agg')


def gerar_graficos(arquivos_filtrados: list):
    """
    Gera gráficos de análise dos dados com design profissional
    
    Args:
        arquivos_filtrados: Lista de caminhos para arquivos Excel filtrados
        
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
        
        # Configurar estilo do matplotlib
        plt.style.use('default')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        
        # Configurar figura com subplots
        fig = plt.figure(figsize=(18, 14))
        gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 2, 2], hspace=0.4)
        
        # Header com informações
        ax_header = fig.add_subplot(gs[0])
        ax_header.axis('off')
        
        # Data atual formatada
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d de %B de %Y")
        hora_formatada = data_atual.strftime("%H:%M")
        
        # Meses em português
        meses = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        
        for eng, pt in meses.items():
            data_formatada = data_formatada.replace(eng, pt)
        
        # Header com fundo verde claro
        header_rect = Rectangle((0, 0), 1, 1, transform=ax_header.transAxes, 
                               facecolor='#f0f8f0', edgecolor='#c8e6c9', linewidth=1.5)
        ax_header.add_patch(header_rect)
        
        # Título principal
        ax_header.text(0.5, 0.7, 'RELATÓRIO EXECUTIVO DE ANÁLISE DE ALERTAS', 
                      ha='center', va='center', fontsize=20, fontweight='bold', 
                      color='#000000', transform=ax_header.transAxes)
        
        # Subtítulo com data
        ax_header.text(0.5, 0.3, f'Gerado em {data_formatada} às {hora_formatada}', 
                      ha='center', va='center', fontsize=12, 
                      color='#333333', transform=ax_header.transAxes)
        
        # Cores profissionais
        cores_tipo = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        cores_pa = ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']

        # Gráfico 1: Contagem de ocorrências por TIPO por PA
        ax1 = fig.add_subplot(gs[1])
        if "TIPO" in df_geral.columns:
            try:
                # Limpar dados de TIPO
                df_geral["TIPO"] = df_geral["TIPO"].astype(str).str.strip()
                df_geral = df_geral[df_geral["TIPO"] != "nan"]
                
                if not df_geral.empty:
                    tipo_contagem = df_geral.groupby(["PA", "TIPO"]).size().unstack(fill_value=0)
                    if not tipo_contagem.empty:
                        # Criar gráfico de barras agrupadas
                        bars = tipo_contagem.plot(kind="bar", ax=ax1, 
                                                color=cores_tipo[:len(tipo_contagem.columns)],
                                                edgecolor='white', linewidth=1.5, width=0.8)
                        
                        ax1.set_title('DISTRIBUIÇÃO DE ALERTAS POR CATEGORIA E POSTO', 
                                    fontsize=16, fontweight='bold', pad=25, color='#000000')
                        ax1.set_ylabel('Quantidade de Alertas', fontsize=13, fontweight='bold', color='#000000')
                        ax1.set_xlabel('Posto de Atendimento (PA)', fontsize=13, fontweight='bold', color='#000000')
                        
                        # Grid profissional
                        ax1.grid(axis="y", linestyle="-", alpha=0.2, color='#cccccc')
                        ax1.set_axisbelow(True)
                        
                        # Formatação dos eixos
                        ax1.tick_params(axis='x', rotation=0, labelsize=11, colors='#000000')
                        ax1.tick_params(axis='y', labelsize=10, colors='#000000')
                        
                        # Legenda profissional
                        legend = ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', 
                                          fontsize=10, frameon=True, fancybox=True, 
                                          shadow=True, title="Categorias de Alerta",
                                          title_fontsize=11)
                        legend.get_title().set_fontweight('bold')
                        legend.get_title().set_color('#000000')
                        
                        # Adicionar valores nas barras
                        for container in ax1.containers:
                            ax1.bar_label(container, fmt='%d', fontsize=9, 
                                        fontweight='bold', color='white')
                        
                        ax1.set_facecolor('#fafafa')
                        
                    else:
                        ax1.text(0.5, 0.5, 'Sem dados de categoria válidos', 
                               ha='center', va='center', transform=ax1.transAxes,
                               fontsize=14, color='#d32f2f')
                        ax1.set_title("DISTRIBUIÇÃO DE ALERTAS - SEM DADOS", color='#000000')
                else:
                    ax1.text(0.5, 0.5, 'Sem dados válidos após processamento', 
                           ha='center', va='center', transform=ax1.transAxes,
                           fontsize=14, color='#d32f2f')
                    ax1.set_title("DISTRIBUIÇÃO DE ALERTAS - SEM DADOS", color='#000000')
            except Exception as e:
                print(f"⚠️ Erro no gráfico de tipos: {e}")
                ax1.text(0.5, 0.5, f'Erro no processamento: {str(e)}', 
                       ha='center', va='center', transform=ax1.transAxes,
                       fontsize=12, color='#d32f2f')
                ax1.set_title("DISTRIBUIÇÃO DE ALERTAS - ERRO", color='#000000')

        # Gráfico 2: Total por PA
        ax2 = fig.add_subplot(gs[2])
        try:
            pa_contagem = df_geral.groupby("PA").size().sort_values(ascending=False)
            if not pa_contagem.empty:
                # Criar gráfico com cores verdes suaves
                bars = ax2.bar(pa_contagem.index, pa_contagem.values, 
                             color=cores_pa[:len(pa_contagem)], 
                             edgecolor='white', linewidth=2.5, width=0.7,
                             alpha=0.8)
                
                # Destacar a barra com maior valor
                for i, bar in enumerate(bars):
                    if i == 0:  # Primeira barra (maior valor)
                        bar.set_facecolor('#4caf50')
                        bar.set_edgecolor('#2e7d32')
                        bar.set_linewidth(3)
                        bar.set_alpha(0.9)
                
                ax2.set_title('VOLUME TOTAL DE ALERTAS POR POSTO DE ATENDIMENTO', 
                            fontsize=16, fontweight='bold', pad=25, color='#000000')
                ax2.set_ylabel('Total de Alertas', fontsize=13, fontweight='bold', color='#000000')
                ax2.set_xlabel('Posto de Atendimento (PA)', fontsize=13, fontweight='bold', color='#000000')
                
                # Grid profissional
                ax2.grid(axis="y", linestyle="-", alpha=0.2, color='#cccccc')
                ax2.set_axisbelow(True)
                
                # Formatação dos eixos
                ax2.tick_params(axis='x', rotation=0, labelsize=12, colors='#000000')
                ax2.tick_params(axis='y', labelsize=11, colors='#000000')
                
                # Adicionar valores nas barras
                for i, (pa, valor) in enumerate(pa_contagem.items()):
                    fontsize = 13 if i == 0 else 11
                    ax2.text(i, valor + max(pa_contagem.values) * 0.02, 
                           f'{valor:,}', ha='center', va='bottom', 
                           fontsize=fontsize, fontweight='bold', color='#000000')
                
                ax2.set_facecolor('#fafafa')
                
                # Linha de média
                media = pa_contagem.mean()
                ax2.axhline(y=media, color='#ff9800', linestyle='--', 
                          linewidth=2, alpha=0.7, label=f'Média: {media:.0f} alertas')
                
                # Legenda da média
                legend = ax2.legend(loc='upper right', fontsize=11, frameon=True, 
                                  fancybox=True, shadow=True)
                legend.get_frame().set_facecolor('#ffffff')
                legend.get_frame().set_alpha(0.9)
                
            else:
                ax2.text(0.5, 0.5, 'Sem dados válidos para análise', 
                       ha='center', va='center', transform=ax2.transAxes,
                       fontsize=14, color='#d32f2f')
                ax2.set_title("VOLUME TOTAL DE ALERTAS - SEM DADOS", color='#000000')
        except Exception as e:
            print(f"⚠️ Erro no gráfico de contagem: {e}")
            ax2.text(0.5, 0.5, f'Erro no processamento: {str(e)}', 
                   ha='center', va='center', transform=ax2.transAxes,
                   fontsize=12, color='#d32f2f')
            ax2.set_title("VOLUME TOTAL DE ALERTAS - ERRO", color='#000000')

        # Footer profissional
        footer_y = 0.02
        footer_rect = Rectangle((0.05, footer_y), 0.9, 0.06, transform=fig.transFigure, 
                               facecolor='#f0f8f0', edgecolor='#c8e6c9', linewidth=1)
        fig.patches.append(footer_rect)
        
        # Informações do footer
        total_registros = len(df_geral)
        total_pas = df_geral['PA'].nunique()
        
        footer_text = (f'Sistema de Monitoramento de Alertas | '
                      f'Total de Registros: {total_registros:,} | '
                      f'Postos Analisados: {total_pas} | '
                      f'Período de Análise: {data_formatada}')
        
        fig.text(0.5, footer_y + 0.03, footer_text, 
                ha='center', va='center', fontsize=10, 
                color='#000000', fontweight='bold')
        
        # Ajustar layout
        plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.12)
        
        # Salvar na pasta Downloads
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        caminho_saida = os.path.join(downloads_path, "grafico_alertas.png")
        
        # Salvar com alta qualidade
        plt.savefig(caminho_saida, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', format='png',
                   pad_inches=0.2)
        plt.close()
        
        print(f"✅ Gráficos salvos em: {caminho_saida}")
        return caminho_saida
        
    except Exception as e:
        print(f"❌ Erro geral ao gerar gráficos: {e}")
        return None
