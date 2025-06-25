from tkinter import filedialog
import threading
import os

class UIHandlers:
    def __init__(self, parent):
        self.parent = parent
    
    def selecionar_arquivo(self):
        if self.parent.processando:
            return
            
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if filepath:
            self.parent.arquivo_selecionado = filepath
            thread = threading.Thread(target=self.processar_arquivo_thread, args=(filepath,))
            thread.daemon = True
            thread.start()
    
    def processar_arquivo_thread(self, filepath):
        self.parent.processando = True
        
        self.parent.after(0, self.mostrar_progresso)
        
        try:
            arquivos_gerados = self.parent.data_processor.processar_arquivo(
                filepath, 
                progress_callback=self.atualizar_progresso
            )
            
            if arquivos_gerados:
                self.parent.chart_generator.gerar_graficos(arquivos_gerados)
            
            self.parent.after(0, lambda: self.parent.dialogs.mostrar_sucesso(arquivos_gerados))
            
        except Exception as e:
            self.parent.after(0, lambda: self.parent.dialogs.mostrar_erro(str(e)))
        
        finally:
            self.parent.processando = False
            self.parent.after(2000, self.ocultar_progresso)
    
    def mostrar_progresso(self):
        self.parent.upload_frame.pack_forget()
        self.parent.progress_frame.pack(fill="x", padx=30, pady=20)
        self.parent.progress_bar.set(0)
        self.parent.progress_percent.configure(text="0%")

        self.parent.select_button.configure(
            state="disabled", 
            text="🔄 Processando...",
            width=280,  
            height=50   
        )

        self.parent.status_label.configure(
            text="⚡ Processamento em andamento...",
            text_color="#0d6efd"
        )
    
    def ocultar_progresso(self):
        self.parent.progress_frame.pack_forget()
        self.parent.upload_frame.pack(fill="x", padx=30, pady=30)
        
        self.parent.select_button.configure(
            state="normal", 
            text="📂 Selecionar Arquivo CSV",
            width=280,  
            height=50  
        )
        
        self.parent.status_label.configure(
            text="💡 Dica: Certifique-se de que seu arquivo CSV contém os dados de alertas",
            text_color="#6c757d"
        )
    
    def atualizar_progresso(self, valor):
        def update():
            self.parent.progress_bar.set(valor)
            percent = int(valor * 100)
            self.parent.progress_percent.configure(text=f"{percent}%")

            if percent < 25:
                self.parent.progress_label.configure(text="🔍 Analisando arquivo...")
            elif percent < 50:
                self.parent.progress_label.configure(text="📊 Processando dados...")
            elif percent < 75:
                self.parent.progress_label.configure(text="📁 Organizando por grupos...")
            else:
                self.parent.progress_label.configure(text="✅ Finalizando...")
        
        self.parent.after(0, update)
