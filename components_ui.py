import customtkinter as ctk

class UIComponents:
    def __init__(self, parent):
        self.parent = parent
    
    def create_header(self):
        header_frame = ctk.CTkFrame(
            self.parent.main_container, 
            height=120, 
            corner_radius=15,
            fg_color=("#f8f9fa", "#f8f9fa"),
            border_width=1,
            border_color=("#e9ecef", "#e9ecef")
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🚛 Processador de Dados de Alertas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1f538d"
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sistema avançado de análise e relatórios de alertas",
            font=ctk.CTkFont(size=14),
            text_color="#6c757d"
        )
        subtitle_label.pack(pady=(0, 20))
    
    def create_main_area(self):
        self.parent.main_card = ctk.CTkFrame(
            self.parent.main_container, 
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color=("#dee2e6", "#dee2e6")
        )
        self.parent.main_card.pack(fill="both", expand=True, pady=(0, 20))
        
        self.create_upload_area()
        self.create_progress_area()
        self.create_status_area()
    
    def create_upload_area(self):
        self.parent.upload_frame = ctk.CTkFrame(
            self.parent.main_card, 
            corner_radius=10, 
            fg_color=("#f8f9fa", "#f8f9fa"),
            border_width=2,
            border_color=("#e9ecef", "#e9ecef")
        )
        self.parent.upload_frame.pack(fill="x", padx=30, pady=30)
        
        upload_icon = ctk.CTkLabel(
            self.parent.upload_frame,
            text="📁",
            font=ctk.CTkFont(size=48)
        )
        upload_icon.pack(pady=(30, 10))
        
        instruction_label = ctk.CTkLabel(
            self.parent.upload_frame,
            text="Selecione seu arquivo CSV para processamento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#212529"
        )
        instruction_label.pack(pady=(0, 5))
        
        secondary_label = ctk.CTkLabel(
            self.parent.upload_frame,
            text="Formatos suportados: .csv",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        secondary_label.pack(pady=(0, 20))
        
        self.parent.select_button = ctk.CTkButton(
            self.parent.upload_frame,
            text="📂 Selecionar Arquivo CSV",
            command=self.parent.selecionar_arquivo,
            width=280,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0d6efd",
            hover_color="#0b5ed7"
        )
        self.parent.select_button.pack(pady=(0, 30))
        self.parent.select_button.pack_propagate(False)
    
    def create_progress_area(self):
        self.parent.progress_frame = ctk.CTkFrame(
            self.parent.main_card, 
            corner_radius=10,
            fg_color="white",
            border_width=1,
            border_color=("#dee2e6", "#dee2e6")
        )
        
        self.parent.progress_label = ctk.CTkLabel(
            self.parent.progress_frame,
            text="Processando arquivo...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#212529"
        )
        self.parent.progress_label.pack(pady=(20, 10))
        
        self.parent.progress_bar = ctk.CTkProgressBar(
            self.parent.progress_frame,
            width=400,
            height=20,
            corner_radius=10,
            fg_color="#e9ecef",
            progress_color="#0d6efd"
        )
        self.parent.progress_bar.pack(pady=(0, 10))
        
        self.parent.progress_percent = ctk.CTkLabel(
            self.parent.progress_frame,
            text="0%",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        self.parent.progress_percent.pack(pady=(0, 20))
    
    def create_status_area(self):
        self.parent.status_frame = ctk.CTkFrame(
            self.parent.main_card, 
            height=60, 
            corner_radius=10, 
            fg_color="white"
        )
        self.parent.status_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.parent.status_frame.pack_propagate(False)
        
        self.parent.status_label = ctk.CTkLabel(
            self.parent.status_frame,
            text="💡 Dica: Certifique-se de que seu arquivo CSV contém os dados de alertas",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        self.parent.status_label.pack(expand=True)
    
    def create_footer(self):
        footer_frame = ctk.CTkFrame(
            self.parent.main_container, 
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
