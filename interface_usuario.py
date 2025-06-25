import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from io import StringIO
from datetime import datetime

# Importar módulos locais
from processador_dados import processar_arquivo
from gerador_relatorios import gerar_graficos


class ProcessadorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Processamento de Alertas - v2.0")
        self.root.geometry("650x450")
        
        self.arquivo_selecionado = None
        self.processando = False
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título da aplicação
        titulo = ttk.Label(main_frame, text="Sistema de Processamento de Alertas", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Seleção de arquivo
        ttk.Label(main_frame, text="Selecione o arquivo CSV para processamento:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        frame_arquivo = ttk.Frame(main_frame)
        frame_arquivo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_arquivo = ttk.Label(frame_arquivo, text="Nenhum arquivo selecionado", 
                                      foreground="gray", font=("Arial", 9))
        self.label_arquivo.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(frame_arquivo, text="Procurar Arquivo", 
                  command=self.selecionar_arquivo).grid(row=0, column=1, padx=(10, 0))
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Barra de progresso
        ttk.Label(main_frame, text="Progresso do processamento:").grid(
            row=4, column=0, sticky=tk.W, pady=(5, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=450)
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_status = ttk.Label(main_frame, text="Aguardando arquivo para processar", 
                                     font=("Arial", 9))
        self.label_status.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Botões de ação
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.btn_processar = ttk.Button(frame_botoes, text="🚀 Iniciar Processamento", 
                                       command=self.iniciar_processamento)
        self.btn_processar.grid(row=0, column=0, padx=5)
        
        ttk.Button(frame_botoes, text="🧹 Limpar Tudo", 
                  command=self.limpar).grid(row=0, column=1, padx=5)
        
        ttk.Button(frame_botoes, text="❓ Ajuda", 
                  command=self.mostrar_ajuda).grid(row=0, column=2, padx=5)
        
        # Área de log
        ttk.Label(main_frame, text="Registro de atividades:").grid(
            row=8, column=0, sticky=tk.W, pady=(20, 5))
        
        frame_log = ttk.Frame(main_frame)
        frame_log.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.text_log = tk.Text(frame_log, height=12, width=75, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(frame_log, orient=tk.VERTICAL, command=self.text_log.yview)
        self.text_log.configure(yscrollcommand=scrollbar.set)
        
        self.text_log.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
        frame_log.columnconfigure(0, weight=1)
        frame_log.rowconfigure(0, weight=1)
    
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo CSV para processamento",
            filetypes=[
                ("Arquivos CSV", "*.csv"), 
                ("Arquivos de texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.arquivo_selecionado = arquivo
            nome_arquivo = os.path.basename(arquivo)
            self.label_arquivo.config(text=f"📄 {nome_arquivo}", foreground="black")
            self.log(f"📁 Arquivo selecionado: {nome_arquivo}")
            self.label_status.config(text="Arquivo carregado - Pronto para processar")
    
    def log(self, mensagem):
        """Adiciona mensagem ao log de forma thread-safe"""
        def _log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.text_log.insert(tk.END, f"[{timestamp}] {mensagem}\n")
            self.text_log.see(tk.END)
        
        if threading.current_thread() == threading.main_thread():
            _log()
        else:
            self.root.after(0, _log)
    
    def atualizar_progresso(self, valor):
        """Atualiza a barra de progresso de forma thread-safe"""
        def _atualizar():
            self.progress_var.set(valor * 100)
            self.label_status.config(text=f"Processando dados... {valor*100:.1f}% concluído")
        
        if threading.current_thread() == threading.main_thread():
            _atualizar()
        else:
            self.root.after(0, _atualizar)
    
    def mostrar_erro(self, mensagem):
        """Mostra erro de forma thread-safe"""
        def _mostrar():
            messagebox.showerror("❌ Erro no Processamento", mensagem)
            self.finalizar_processamento()
        
        if threading.current_thread() == threading.main_thread():
            _mostrar()
        else:
            self.root.after(0, _mostrar)
    
    def mostrar_sucesso(self, mensagem):
        """Mostra sucesso de forma thread-safe"""
        def _mostrar():
            messagebox.showinfo("✅ Processamento Concluído", mensagem)
            self.finalizar_processamento()
        
        if threading.current_thread() == threading.main_thread():
            _mostrar()
        else:
            self.root.after(0, _mostrar)
    
    def mostrar_ajuda(self):
        """Mostra janela de ajuda"""
        ajuda_texto = """
🔧 COMO USAR O SISTEMA:

1️⃣ Clique em "Procurar Arquivo" e selecione um arquivo CSV
2️⃣ Clique em "Iniciar Processamento" para começar
3️⃣ Aguarde o processamento ser concluído
4️⃣ Os arquivos serão salvos na pasta "exportados"
5️⃣ Um gráfico será gerado na pasta Downloads

📋 FUNCIONALIDADES:
• Filtragem automática por PA (PA1, PA2, PA3, PA4)
• Geração de arquivos Excel formatados
• Criação de relatórios gráficos profissionais
• Log detalhado de todas as operações

⚠️ REQUISITOS:
• Arquivo CSV com coluna "PREFIXO"
• Dados válidos para processamento
        """
        messagebox.showinfo("Ajuda do Sistema", ajuda_texto)
    
    def iniciar_processamento(self):
        if not self.arquivo_selecionado:
            messagebox.showwarning("⚠️ Atenção", "Por favor, selecione um arquivo CSV primeiro!")
            return
        
        if self.processando:
            messagebox.showwarning("⚠️ Atenção", "Já existe um processamento em andamento!")
            return
        
        self.processando = True
        self.btn_processar.config(state="disabled", text="⏳ Processando...")
        self.progress_var.set(0)
        self.label_status.config(text="Iniciando processamento dos dados...")
        self.log("🚀 === INICIANDO NOVO PROCESSAMENTO ===")
        
        # Executar processamento em thread separada
        thread = threading.Thread(target=self.processar_arquivo_thread)
        thread.daemon = True
        thread.start()
    
    def processar_arquivo_thread(self):
        """Executa o processamento em thread separada"""
        try:
            # Capturar output do processamento
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            try:
                # Processar arquivo
                arquivos_gerados = processar_arquivo(
                    self.arquivo_selecionado, 
                    progress_callback=self.atualizar_progresso
                )
                
                # Gerar gráficos se houver arquivos
                if arquivos_gerados:
                    self.log("📊 Iniciando geração de relatórios gráficos...")
                    gerar_graficos(arquivos_gerados)
                
                # Restaurar stdout
                sys.stdout = old_stdout
                output_messages = captured_output.getvalue()
                
                # Exibir mensagens capturadas no log
                for linha in output_messages.strip().split('\n'):
                    if linha.strip():
                        self.log(linha)
                
                if arquivos_gerados:
                    mensagem = (f"Processamento concluído com sucesso!\n\n"
                              f"📊 {len(arquivos_gerados)} arquivos Excel gerados\n"
                              f"📈 Relatório gráfico criado\n"
                              f"📁 Arquivos salvos na pasta 'exportados'")
                    self.log(f"✅ Processamento finalizado com sucesso!")
                    self.mostrar_sucesso(mensagem)
                else:
                    mensagem = ("Nenhum arquivo foi gerado durante o processamento.\n\n"
                              "Verifique se o arquivo CSV contém dados válidos\n"
                              "e se possui a coluna 'PREFIXO' necessária.")
                    self.log(f"⚠️ Processamento finalizado sem gerar arquivos")
                    self.mostrar_erro(mensagem)
                    
            finally:
                # Garantir que stdout seja restaurado
                sys.stdout = old_stdout
                
        except Exception as e:
            # Tratar erros durante o processamento
            mensagem_erro = f"Erro durante o processamento:\n\n{str(e)}"
            self.log(f"❌ ERRO: {str(e)}")
            # Usar after para mostrar erro na thread principal
            self.root.after(0, lambda erro=e: self.mostrar_erro(str(erro)))
    
    def finalizar_processamento(self):
        """Finaliza o processamento e restaura interface"""
        self.processando = False
        self.btn_processar.config(state="normal", text="🚀 Iniciar Processamento")
        self.progress_var.set(0)
        self.label_status.config(text="Processamento finalizado - Pronto para novo arquivo")
        self.log("🏁 === PROCESSAMENTO FINALIZADO ===\n")
    
    def limpar(self):
        if self.processando:
            messagebox.showwarning("⚠️ Atenção", 
                                 "Não é possível limpar durante o processamento!")
            return
        
        self.arquivo_selecionado = None
        self.label_arquivo.config(text="Nenhum arquivo selecionado", foreground="gray")
        self.progress_var.set(0)
        self.label_status.config(text="Aguardando arquivo para processar")
        self.text_log.delete(1.0, tk.END)
        self.log("🧹 Interface limpa - Sistema pronto para uso")


def main():
    """Função principal para executar a aplicação"""
    root = tk.Tk()
    
    # Configurar ícone da janela (se disponível)
    try:
        root.iconbitmap('icon.ico')  # Opcional: adicione um ícone
    except:
        pass
    
    app = ProcessadorUI(root)
    
    # Centralizar janela na tela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
