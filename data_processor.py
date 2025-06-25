"""
Módulo para processamento de dados
"""

import os
import pandas as pd
import time
from datetime import datetime
from typing import List, Callable, Optional

from config import PREFIXOS, COLUNAS_REMOVER, ENCODING_CSV, PASTA_EXPORTADOS, TIPOS_DESCONSIDERAR
from excel_formatter import ExcelFormatter


class DataProcessor:
    
    def __init__(self):
        self.formatter = ExcelFormatter()
    
    def filtrar_dataframe_por_prefixo(self, df: pd.DataFrame, prefixos: set, pa: str) -> pd.DataFrame:
        df_filtrado = df[df["PREFIXO"].isin(prefixos)].copy()
        if "TIPO" in df_filtrado.columns:
            df_filtrado = df_filtrado[~df_filtrado["TIPO"].isin(TIPOS_DESCONSIDERAR)]

        cols_para_remover = [col for col in COLUNAS_REMOVER if col in df_filtrado.columns]
        if cols_para_remover:
            df_filtrado.drop(columns=cols_para_remover, inplace=True)
        df_filtrado.insert(0, "PA", pa)
        return df_filtrado
    
    def processar_arquivo(self, filepath: str, progress_callback: Optional[Callable] = None) -> List[str]:
        
        try:
            print(f"📂 Processando arquivo: {os.path.basename(filepath)}")
            
            
            df = pd.read_csv(filepath, encoding=ENCODING_CSV, sep=None, engine="python")
            print(f"📊 Dados carregados: {len(df)} registros")
            
            
            pasta_exportados = os.path.join(os.path.dirname(filepath), PASTA_EXPORTADOS)
            os.makedirs(pasta_exportados, exist_ok=True)

            arquivos_gerados = []
            total_grupos = len(PREFIXOS)

            
            for i, (pa, prefixos) in enumerate(PREFIXOS.items(), start=1):
                try:
                    print(f"🔄 Processando {pa}... ({i}/{total_grupos})")
                    
                    
                    df_filtrado = self.filtrar_dataframe_por_prefixo(df, prefixos, pa)
                    
                    if df_filtrado.empty:
                        continue
                    
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:21]
                    nome_arquivo = f"veiculos_{pa.lower()}_filtrado_{timestamp}.xlsx"
                    caminho_saida = os.path.join(pasta_exportados, nome_arquivo)

                    
                    df_filtrado.to_excel(caminho_saida, index=False)
                    self.formatter.formatar_arquivo(caminho_saida)
                    arquivos_gerados.append(caminho_saida)
                    
                    print(f"✅ {pa}: {len(df_filtrado)} registros salvos")

                   
                    if progress_callback:
                        try:
                            progress_callback(i / total_grupos)
                        except Exception as callback_error:
                            print(f"⚠️ Erro no callback de progresso: {callback_error}")

                    time.sleep(0.1)  
                    
                except Exception as pa_error:
                    print(f"❌ Erro ao processar {pa}: {pa_error}")
                    continue

            print(f"🎉 Processamento concluído! {len(arquivos_gerados)} arquivos gerados")
            return arquivos_gerados
            
        except Exception as e:
            print(f"❌ Erro geral no processamento: {e}")
            return []
