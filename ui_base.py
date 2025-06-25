import customtkinter as ctk
from tkinter import filedialog
import threading
import os
from typing import Optional, Callable

from config import WINDOW_TITLE, CTK_THEME, CTK_APPEARANCE, CTK_COLORS, PASTA_EXPORTADOS
from data_processor import DataProcessor
from chart_generator import ChartGenerator

class UIBase(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Processador de Dados de Alertas")
        self.geometry("600x500")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.configure(fg_color="white")
        
        self.arquivo_selecionado = None
        self.processando = False
        
        self.data_processor = DataProcessor()
        self.chart_generator = ChartGenerator()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def executar(self):
        self.mainloop()
