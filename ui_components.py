import customtkinter as ctk
from ui_base import UIBase
from components_ui import UIComponents
from ui_handlers import UIHandlers
from ui_dialogs import UIDialogs

class ProcessadorUI(UIBase):
    def __init__(self):
        super().__init__()
        
        self.components = UIComponents(self)
        self.handlers = UIHandlers(self)
        self.dialogs = UIDialogs(self)
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.components.create_header()
        self.components.create_main_area()
        self.components.create_footer()
    
    def selecionar_arquivo(self):
        self.handlers.selecionar_arquivo()
    
    def processar_arquivo_thread(self, filepath):
        self.handlers.processar_arquivo_thread(filepath)
    
    def mostrar_progresso(self):
        self.handlers.mostrar_progresso()
    
    def ocultar_progresso(self):
        self.handlers.ocultar_progresso()
    
    def atualizar_progresso(self, valor):
        self.handlers.atualizar_progresso(valor)
    
    def mostrar_sucesso(self, arquivos):
        self.dialogs.mostrar_sucesso(arquivos)
    
    def mostrar_erro(self, erro):
        self.dialogs.mostrar_erro(erro)
    
    def abrir_pasta(self, caminho: str):
        self.dialogs.abrir_pasta(caminho)
