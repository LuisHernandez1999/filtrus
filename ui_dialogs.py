import customtkinter as ctk
import os
import subprocess
import platform

class UIDialogs:
    def __init__(self, parent):
        self.parent = parent
    
    def mostrar_sucesso(self, arquivos):
        if not arquivos:
            self.mostrar_erro("Nenhum arquivo foi gerado")
            return
            
        diretorio = os.path.dirname(arquivos[0])

        success_window = ctk.CTkToplevel(self.parent)
        success_window.title("Processamento Concluído")
        success_window.geometry("400x250")
        success_window.resizable(False, False)
        success_window.transient(self.parent)
        success_window.grab_set()
        success_window.configure(fg_color="white")

        success_window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 125
        success_window.geometry(f"400x250+{x}+{y}")

        success_frame = ctk.CTkFrame(
            success_window,
            fg_color="white",
            border_width=1,
            border_color="#dee2e6"
        )
        success_frame.pack(fill="both", expand=True, padx=20, pady=20)

        success_icon = ctk.CTkLabel(success_frame, text="✅", font=ctk.CTkFont(size=48))
        success_icon.pack(pady=(20, 10))

        success_title = ctk.CTkLabel(
            success_frame,
            text="Processamento Concluído!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#198754"
        )
        success_title.pack(pady=(0, 10))

        success_msg = ctk.CTkLabel(
            success_frame,
            text=f"Arquivos salvos em:\n{diretorio}",
            font=ctk.CTkFont(size=12),
            justify="center",
            text_color="#212529"
        )
        success_msg.pack(pady=(0, 20))

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
        
        self.parent.status_label.configure(
            text="✅ Processamento concluído com sucesso!",
            text_color="#198754"
        )
    
    def mostrar_erro(self, erro):
        error_window = ctk.CTkToplevel(self.parent)
        error_window.title("Erro no Processamento")
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        error_window.transient(self.parent)
        error_window.grab_set()
        error_window.configure(fg_color="white")
        
        error_window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 100
        error_window.geometry(f"400x200+{x}+{y}")
        
        error_frame = ctk.CTkFrame(
            error_window,
            fg_color="white",
            border_width=1,
            border_color="#dee2e6"
        )
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        error_icon = ctk.CTkLabel(error_frame, text="❌", font=ctk.CTkFont(size=48))
        error_icon.pack(pady=(20, 10))
        
        error_title = ctk.CTkLabel(
            error_frame,
            text="Erro no Processamento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#dc3545"
        )
        error_title.pack(pady=(0, 10))
        
        error_msg = ctk.CTkLabel(
            error_frame,
            text=erro,
            font=ctk.CTkFont(size=12),
            justify="center",
            wraplength=350,
            text_color="#212529"
        )
        error_msg.pack(pady=(0, 20))
        
        ok_button = ctk.CTkButton(
            error_frame,
            text="OK",
            command=error_window.destroy,
            width=120,
            fg_color="#dc3545",
            hover_color="#bb2d3b"
        )
        ok_button.pack(pady=(0, 20))
        
        self.parent.status_label.configure(
            text="❌ Erro durante o processamento",
            text_color="#dc3545"
        )
    
    def abrir_pasta(self, caminho: str):
        try:
            if platform.system() == 'Windows':
                os.startfile(caminho)
            elif platform.system() == 'Darwin': 
                subprocess.run(['open', caminho])
            else: 
                subprocess.run(['xdg-open', caminho])
        except Exception as e:
            pass
