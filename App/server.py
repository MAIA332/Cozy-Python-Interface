import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Cozy:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Flow Module")
        self.root.geometry("1404x700")
        self.root.configure(bg="#292827")
        #self.root.overrideredirect(True)

        # frm = ttk.Frame(self.root, padding=10)
        # frm.grid()

        #self.create_custom_title_bar()

        # tk.Label(self.root, text="Hello World!",font=("Arial", 16), bg="#292827", fg="#b6a587")
        #self.button_factory(self.root,"#292827","#b6a587","Quit",self.root.destroy,"#453b2a",2,"Arial",12,"flat")
        #self.build_menu()
        
        self.build_banner()
        self.create_main_section()
        self.root.mainloop()

    def button_factory(self,local,bg,fg,text,command,bd_color,bd_wd,font_family,font_size,relief):
        """
        Cria um botão personalizado dentro de uma borda.
        """
        
        # Criação da borda para o botão
        bord = tk.Frame(local, bg=bd_color, padx=bd_wd, pady=bd_wd)
        bord.pack()

        # Verifique se o Frame foi criado corretamente
        if bord is None:
            raise ValueError("Erro ao criar a borda (Frame)!")

        # Criação do botão
        button = tk.Button(
            bord,
            text=text,
            command=command,
            font=(font_family, font_size),
            bg=bg,
            fg=fg,
            relief=relief
        )

        # Verifique se o botão foi criado corretamente
        if button is None:
            raise ValueError("Erro ao criar o botão!")

        button.pack()
        
        return button  # Retorna o botão criado

    def build_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        file_menu = tk.Menu(menu)
        
        # menu.add_cascade(label="File", menu=file_menu)
        # file_menu.add_command(label="New")
        # file_menu.add_command(label="Open")
        # file_menu.add_command(label="Save")

    def build_banner(self):
        # Carrega a imagem
        header_image = Image.open("App/Assets/banner.jpg").resize((800, 250))
        self.header_photo = ImageTk.PhotoImage(header_image)

        # Frame do cabeçalho
        header_frame = tk.Frame(self.root, bg="#292827")
        header_frame.pack(fill="x")

        # Label com imagem
        header_label = tk.Label(header_frame, image=self.header_photo)
        header_label.pack()

        # Texto sobre a imagem
        text_label = tk.Label(header_frame, text="Organize your Life.",font=("Arial", 24, "bold"), fg="#b6a587", bg="#292827")
        text_label.place(relx=0.5, rely=0.5, anchor="center")

    def create_main_section(self):

        # Container central
        container = tk.Frame(self.root, bg="#2b2b2b")
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.7)

        # Canvas para rolagem
        self.canvas = tk.Canvas(container, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar_y.pack(side="right", fill="y")

        # Configurações do Canvas
        self.canvas.configure(yscrollcommand=scrollbar_y.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)  # Scroll para Windows
        self.canvas.bind_all("<Button-4>", self.on_mouse_scroll)   # Scroll para Linux/Mac
        self.canvas.bind_all("<Button-5>", self.on_mouse_scroll)

        # Frame scrollável
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2b2b2b")
        self.canvas.create_window((0, 10), window=self.scrollable_frame, anchor="nw")

        # Título e descrição
        title = tk.Label(self.scrollable_frame, text="Lofi Style", font=("Arial", 18, "bold"), fg="white", bg="#2b2b2b")
        title.pack(pady=(0, 10))

        subtitle = tk.Label(self.scrollable_frame, text="All your thoughts in one place.",
                            font=("Arial", 12), fg="#b6a587", bg="#2b2b2b")
        subtitle.pack(pady=(0, 20))

        # Cards
        cards = [
            {"title": "Daily", "image": "App/Assets/banner.jpg"},
            {"title": "Planners", "image": "App/Assets/banner.jpg"},
            {"title": "Personal", "image": "App/Assets/banner.jpg"},
            {"title": "Goals", "image": "App/Assets/banner.jpg"},
        ]

        card_frame = tk.Frame(self.scrollable_frame, bg="#2b2b2b")
        card_frame.pack()

        for i, card in enumerate(cards):
            self.create_card(card_frame, card, row=i // 2, column=i % 2)
    

    def create_card(self, parent, card, row, column):

        # Carrega imagem
        image = Image.open(card["image"]).resize((180, 100))
        photo = ImageTk.PhotoImage(image)

        # Card frame
        card_frame = tk.Frame(parent, bg="#292827", bd=2, relief="groove")
        card_frame.grid(row=row, column=column, padx=10, pady=10)

        # Imagem
        img_label = tk.Label(card_frame, image=photo, bg="#292827")
        img_label.image = photo  # Para evitar garbage collection
        img_label.pack()

        # Título do card
        title_label = tk.Label(card_frame, text=card["title"], fg="#b6a587", bg="#292827",
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=5)

        # Botão de ação
        btn = self.button_factory(card_frame,"#292827","#b6a587","Open",lambda: self.open_card(card["title"]),"#453b2a",0,"Arial",12,"flat")
        btn.pack(pady=5)

    def open_card(self, title):

        # Abre uma nova janela ao clicar no botão
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("400x300")
        tk.Label(new_window, text=f"Welcome to {title} Section", 
                 font=("Arial", 16)).pack(pady=50)
        
    def on_mouse_scroll(self, event):
        """Configura o scroll do mouse para o Canvas"""
        if event.num == 4 or event.delta > 0:  # Scroll para cima
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll para baixo
            self.canvas.yview_scroll(1, "units")
        
if __name__ == "__main__":
    Cozy()