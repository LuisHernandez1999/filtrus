"""
Arquivo principal da aplicação - Versão Moderna
"""

try:
    # Tentar importar CustomTkinter
    import customtkinter as ctk
    from ui_components import main as modern_main
    
    def main():
        """Função principal que executa a interface moderna"""
        print("🚀 Iniciando interface moderna com CustomTkinter...")
        modern_main()

except ImportError:
    # Fallback para tkinter tradicional se CustomTkinter não estiver disponível
    print("⚠️ CustomTkinter não encontrado. Usando interface tradicional...")
    from ui_components import ProcessadorUI
    import tkinter as tk
    
    def main():
        """Função principal que executa a interface tradicional"""
        root = tk.Tk()
        app = ProcessadorUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()