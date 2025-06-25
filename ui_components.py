"""
Interface moderna usando CustomTkinter - Estilo idêntico ao app de referência
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from typing import Optional, Callable
from io import StringIO
import sys
from datetime import datetime

from config import WINDOW_TITLE, CTK_THEME, CTK_APPEARANCE, CTK_COLORS, PASTA_EXPORTADOS
from data_processor import DataProcessor
from chart_generator import ChartGenerator

class ModernProcessadorUI(ctk.CTk):
    """Interface gráfica moderna usando CustomTkinter"""
    
    def __init__(self):
        super().__init__()
        
        # Configurar janela principal
        self.title("Processador de Dados de Alertas")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Fundo branco
        self.configure(fg_color="white")
        
        # Variáveis de controle
        self.arquivo_selecionado = None
        self.processando = False
        
        # Inicializar processadores
        self.data_processor = DataProcessor()
        self.chart_generator = ChartGenerator()
        
        # Criar interface
        self.setup_ui()
        
        # Centralizar janela
        self.center_window()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Container principal
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_header()
        self.create_main_area()
        self.create_footer()
    
    def create_header(self):
        """Cria o cabeçalho"""
        header_frame = ctk.CTkFrame(
            self.main_container, 
            height=120, 
            corner_radius=15,
            fg_color=("#f8f9fa", "#f8f9fa"),
            border_width=1,
            border_color=("#e9ecef", "#e9ecef")
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🚛 Processador de Dados de Alertas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title_label.pack(pady=(20, 5))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sistema avançado de análise e relatórios de alertas",
            font=ctk.CTkFont(size=14),
            text_color="#6c757d"
        )
        subtitle_label.pack(pady=(0, 20))
    
    def create_main_area(self):
        """Cria a área principal"""
        # Card principal
        self.main_card = ctk.CTkFrame(
            self.main_container, 
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color=("#dee2e6", "#dee2e6")
        )
        self.main_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Criar áreas
        self.create_upload_area()
        self.create_progress_area()
        self.create_status_area()
    
    def create_upload_area(self):
        """Cria área de upload"""
        self.upload_frame = ctk.CTkFrame(
            self.main_card, 
            corner_radius=10, 
            fg_color=("#f8f9fa", "#f8f9fa"),
            border_width=2,
            border_color=("#e9ecef", "#e9ecef")
        )
        self.upload_frame.pack(fill="x", padx=30, pady=30)
        
        # Ícone
        upload_icon = ctk.CTkLabel(
            self.upload_frame,
            text="📁",
            font=ctk.CTkFont(size=48)
        )
        upload_icon.pack(pady=(30, 10))
        
        # Instrução principal
        instruction_label = ctk.CTkLabel(
            self.upload_frame,
            text="Selecione seu arquivo CSV para processamento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#212529"
        )
        instruction_label.pack(pady=(0, 5))
        
        # Instrução secundária
        secondary_label = ctk.CTkLabel(
            self.upload_frame,
            text="Formatos suportados: .csv",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        secondary_label.pack(pady=(0, 20))
        
        # Botão de seleção
        self.select_button = ctk.CTkButton(
            self.upload_frame,
            text="📂 Selecionar Arquivo CSV",
            command=self.selecionar_arquivo,
            width=280,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0d6efd",
            hover_color="#0b5ed7"
        )
        self.select_button.pack(pady=(0, 30))
        self.select_button.pack_propagate(False)
    
    def create_progress_area(self):
        """Cria área de progresso"""
        self.progress_frame = ctk.CTkFrame(
            self.main_card, 
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color=("#dee2e6", "#dee2e6")
        )
        # Não fazer pack inicialmente
        
        # Label de progresso
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Processando arquivo...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#212529"
        )
        self.progress_label.pack(pady=(20, 10))
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=400,
            height=20,
            corner_radius=10,
            fg_color="#e9ecef",
            progress_color="#0d6efd"
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Porcentagem
        self.progress_percent = ctk.CTkLabel(
            self.progress_frame,
            text="0%",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        self.progress_percent.pack(pady=(0, 20))
    
    def create_status_area(self):
        """Cria área de status"""
        self.status_frame = ctk.CTkFrame(
            self.main_card, 
            height=60, 
            corner_radius=10, 
            fg_color="white"
        )
        self.status_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="💡 Dica: Certifique-se de que seu arquivo CSV contém os dados de alertas",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        self.status_label.pack(expand=True)
    
    def create_footer(self):
        """Cria rodapé"""
        footer_frame = ctk.CTkFrame(
            self.main_container, 
            height=50, 
            corner_radius=10,
            fg_color=("#f8f9fa", "#f8f9fa"),
            border_width=1,
            border_color=("#e9ecef", "#e9ecef")
        )
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="✨ Sistema de Processamento de Dados de Alertas | Versão 2.0",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6c757d"
        )
        footer_label.pack(expand=True)
    
    def selecionar_arquivo(self):
        """Seleciona arquivo para processamento"""
        if self.processando:
            return
            
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if filepath:
            self.arquivo_selecionado = filepath
            # Iniciar processamento em thread separada
            thread = threading.Thread(target=self.processar_arquivo_thread, args=(filepath,))
            thread.daemon = True
            thread.start()
    
    def processar_arquivo_thread(self, filepath):
        """Processa arquivo em thread separada"""
        self.processando = True
        
        # Mostrar progresso
        self.after(0, self.mostrar_progresso)
        
        try:
            # Processar dados
            arquivos_gerados = self.data_processor.processar_arquivo(
                filepath, 
                progress_callback=self.atualizar_progresso
            )
            
            # Gerar gráficos se houver arquivos
            if arquivos_gerados:
                self.chart_generator.gerar_graficos(arquivos_gerados)
            
            # Mostrar sucesso
            self.after(0, lambda: self.mostrar_sucesso(arquivos_gerados))
            
        except Exception as e:
            # Mostrar erro
            self.after(0, lambda: self.mostrar_erro(str(e)))
        
        finally:
            self.processando = False
            # Ocultar progresso após 2 segundos
            self.after(2000, self.ocultar_progresso)
    
    def mostrar_progresso(self):
        """Mostra área de progresso"""
        # Ocultar upload e mostrar progresso
        self.upload_frame.pack_forget()
        self.progress_frame.pack(fill="x", padx=30, pady=20)
        self.progress_bar.set(0)
        self.progress_percent.configure(text="0%")

        # Desabilitar botão
        self.select_button.configure(
            state="disabled", 
            text="🔄 Processando...",
            width=280,  
            height=50   
        )

        # Atualizar status
        self.status_label.configure(
            text="⚡ Processamento em andamento...",
            text_color="#0d6efd"
        )
    
    def ocultar_progresso(self):
        """Oculta área de progresso"""
        # Ocultar progresso e mostrar upload
        self.progress_frame.pack_forget()
        self.upload_frame.pack(fill="x", padx=30, pady=30)
        
        # Reabilitar botão
        self.select_button.configure(
            state="normal", 
            text="📂 Selecionar Arquivo CSV",
            width=280,  
            height=50  
        )
        
        # Restaurar status
        self.status_label.configure(
            text="💡 Dica: Certifique-se de que seu arquivo CSV contém os dados de alertas",
            text_color="#6c757d"
        )
    
    def atualizar_progresso(self, valor):
        """Atualiza barra de progresso"""
        def update():
            self.progress_bar.set(valor)
            percent = int(valor * 100)
            self.progress_percent.configure(text=f"{percent}%")

            # Atualizar mensagem baseada no progresso
            if percent < 25:
                self.progress_label.configure(text="🔍 Analisando arquivo...")
            elif percent < 50:
                self.progress_label.configure(text="📊 Processando dados...")
            elif percent < 75:
                self.progress_label.configure(text="📁 Organizando por grupos...")
            else:
                self.progress_label.configure(text="✅ Finalizando...")
        
        self.after(0, update)
    
    def mostrar_sucesso(self, arquivos):
        """Mostra diálogo de sucesso"""
        if not arquivos:
            self.mostrar_erro("Nenhum arquivo foi gerado")
            return
            
        diretorio = os.path.dirname(arquivos[0])

        # Criar janela de sucesso
        success_window = ctk.CTkToplevel(self)
        success_window.title("Processamento Concluído")
        success_window.geometry("400x250")
        success_window.resizable(False, False)
        success_window.transient(self)
        success_window.grab_set()
        success_window.configure(fg_color="white")

        # Centralizar
        success_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 125
        success_window.geometry(f"400x250+{x}+{y}")

        # Frame principal
        success_frame = ctk.CTkFrame(
            success_window,
            fg_color="white",
            border_width=1,
            border_color="#dee2e6"
        )
        success_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Ícone de sucesso
        success_icon = ctk.CTkLabel(success_frame, text="✅", font=ctk.CTkFont(size=48))
        success_icon.pack(pady=(20, 10))

        # Título
        success_title = ctk.CTkLabel(
            success_frame,
            text="Processamento Concluído!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#198754"
        )
        success_title.pack(pady=(0, 10))

        # Mensagem
        success_msg = ctk.CTkLabel(
            success_frame,
            text=f"Arquivos salvos em:\n{diretorio}",
            font=ctk.CTkFont(size=12),
            justify="center",
            text_color="#212529"
        )
        success_msg.pack(pady=(0, 20))

        # Botões
        button_frame = ctk.CTkFrame(success_frame, fg_color="white")
        button_frame.pack(fill="x", pady=(0, 20))
        
        open_button = ctk.CTkButton(
            button_frame,
            text="📂 Abrir Pasta",
            command=lambda: [self.abrir_pasta(diretorio), success_window.destroy()],
            width=120,
            fg_color="#198754",
            hover_color="#157347"
        )
        open_button.pack(side="left", padx=(20, 10))
        
        ok_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=success_window.destroy,
            width=120,
            fg_color="#6c757d",
            hover_color="#5c636a"
        )
        ok_button.pack(side="right", padx=(10, 20))
        
        # Atualizar status
        self.status_label.configure(
            text="✅ Processamento concluído com sucesso!",
            text_color="#198754"
        )
    
    def mostrar_erro(self, erro):
        """Mostra diálogo de erro"""
        # Criar janela de erro
        error_window = ctk.CTkToplevel(self)
        error_window.title("Erro no Processamento")
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        error_window.transient(self)
        error_window.grab_set()
        error_window.configure(fg_color="white")
        
        # Centralizar
        error_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 100
        error_window.geometry(f"400x200+{x}+{y}")
        
        # Frame principal
        error_frame = ctk.CTkFrame(
            error_window,
            fg_color="white",
            border_width=1,
            border_color="#dee2e6"
        )
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone de erro
        error_icon = ctk.CTkLabel(error_frame, text="❌", font=ctk.CTkFont(size=48))
        error_icon.pack(pady=(20, 10))
        
        # Título
        error_title = ctk.CTkLabel(
            error_frame,
            text="Erro no Processamento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#dc3545"
        )
        error_title.pack(pady=(0, 10))
        
        # Mensagem
        error_msg = ctk.CTkLabel(
            error_frame,
            text=erro,
            font=ctk.CTkFont(size=12),
            justify="center",
            wraplength=350,
            text_color="#212529"
        )
        error_msg.pack(pady=(0, 20))
        
        # Botão OK
        ok_button = ctk.CTkButton(
            error_frame,
            text="OK",
            command=error_window.destroy,
            width=120,
            fg_color="#dc3545",
            hover_color="#bb2d3b"
        )
        ok_button.pack(pady=(0, 20))
        
        # Atualizar status
        self.status_label.configure(
            text="❌ Erro durante o processamento",
            text_color="#dc3545"
        )
    
    def abrir_pasta(self, caminho: str):
        """Abre a pasta no explorador de arquivos"""
        try:
            import subprocess
            import platform
            
            if platform.system() == 'Windows':
                os.startfile(caminho)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', caminho])
            else:  # Linux
                subprocess.run(['xdg-open', caminho])
        except Exception as e:
            pass
    
    def executar(self):
        """Executa a aplicação"""
        self.mainloop()


def main():
    """Função principal da aplicação moderna"""
    app = ModernProcessadorUI()
    app.executar()


if __name__ == "__main__":
    main()