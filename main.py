import requests
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import re
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder, color='grey', **kw):
        super().__init__(master, **kw)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self['foreground']
        self.bind('<FocusIn>', self._clear)
        self.bind('<FocusOut>', self._add)
        self._add()

    def _clear(self, _):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['foreground'] = self.default_fg

    def _add(self, _=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['foreground'] = self.placeholder_color

class ToolTip:
    def __init__(self, widget, text):
        self.widget, self.text = widget, text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _):
        if self.tip or not self.text: return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx()+25
        y += self.widget.winfo_rooty()+20
        self.tip = tk.Toplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")
        tk.Label(self.tip, text=self.text, bg="#ffffe0", relief='solid', bd=1).pack()

    def hide(self, _):
        if self.tip:
            self.tip.destroy()
            self.tip = None

class DiscordWebhookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Webhook Sender - ReisPixelmon")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#2C2F33")  # Discord-like dark background
        
        self.setup_styles()
        self.create_ui()
        
    def setup_styles(self):
        # Configure ttk styles for a more modern look
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # Configure colors similar to Discord's theme
        self.style.configure('TFrame', background='#2C2F33')
        self.style.configure('TNotebook', background='#2C2F33', tabmargins=[2, 5, 2, 0])
        self.style.configure('TNotebook.Tab', background='#23272A', foreground='white', 
                             padding=[10, 5], font=('Segoe UI', 9))
        self.style.map('TNotebook.Tab', background=[('selected', '#7289DA')], 
                        foreground=[('selected', 'white')])
        
        self.style.configure('TLabel', background='#2C2F33', foreground='white', font=('Segoe UI', 10))
        self.style.configure('TButton', background='#7289DA', foreground='white', font=('Segoe UI', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#677BC4')])
        self.style.configure('TCheckbutton', background='#2C2F33', foreground='white', font=('Segoe UI', 10))
        self.style.map('TCheckbutton', background=[('active', '#2C2F33')])
        self.style.configure('TEntry', font=('Segoe UI', 10))
        
        # Special button styles
        self.style.configure('Send.TButton', background='#43B581', font=('Segoe UI', 10, 'bold'))
        self.style.map('Send.TButton', background=[('active', '#3CA374')])
        
        self.style.configure('ColorPicker.TButton', background='#FF0000')
        
    def create_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Webhook URL section
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="Discord Webhook URL:").pack(anchor=tk.W, pady=(0, 5))
        
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.pack(fill=tk.X)
        
        self.url_entry = PlaceholderEntry(
            url_input_frame,
            "https://discord.com/api/webhooks/ID/TOKEN",
            width=80
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        ToolTip(self.url_entry, "Cole aqui sua URL de webhook do Discord")

        # Após a seção URL e antes do notebook
        mention_frame = ttk.Frame(main_frame)
        mention_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(mention_frame, text="Mencionar Cargos (IDs separados por vírgula):").pack(anchor=tk.W, pady=(0, 5))
        
        self.mention_entry = ttk.Entry(mention_frame, width=50)
        self.mention_entry.pack(fill=tk.X, ipady=3)
        ToolTip(self.mention_entry, "Insira IDs de cargos para mencioná-los (ex: 123456789,987654321)")
    
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Simple message tab
        self.simple_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.simple_frame, text="Mensagem Simples")
        
        ttk.Label(self.simple_frame, text="Conteúdo da Mensagem:").pack(anchor=tk.W, pady=(0, 5))
        
        self.simple_message = tk.Text(self.simple_frame, height=10, width=70, 
                                      font=("Segoe UI", 10), bg="#40444B", fg="white")
        self.simple_message.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Embed tab
        self.embed_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.embed_frame, text="Mensagem Embed")
        
        # Left side - embed settings
        settings_frame = ttk.Frame(self.embed_frame)
        settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title
        ttk.Label(settings_frame, text="Título:").pack(anchor=tk.W, pady=(0, 5))
        self.titulo_entry = ttk.Entry(settings_frame, width=50)
        self.titulo_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Description
        ttk.Label(settings_frame, text="Descrição:").pack(anchor=tk.W, pady=(0, 5))
        self.descricao_text = tk.Text(settings_frame, height=6, width=50, 
                                      font=("Segoe UI", 10), bg="#40444B", fg="white")
        self.descricao_text.pack(fill=tk.X, pady=(0, 10))
        
        # Color picker
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_frame, text="Cor:").pack(side=tk.LEFT, padx=(0, 5))
        self.color_preview = tk.Canvas(color_frame, width=20, height=20, bg="#FF0000", highlightthickness=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cor_entry = ttk.Entry(color_frame, width=10)
        self.cor_entry.insert(0, "FF0000")
        self.cor_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.cor_entry.bind("<KeyRelease>", self.update_color_preview)
        
        color_btn = ttk.Button(color_frame, text="Escolher Cor", command=self.choose_color)
        color_btn.pack(side=tk.LEFT, padx=5)
        
        # Image URL
        ttk.Label(settings_frame, text="Image URL:").pack(anchor=tk.W, pady=(0, 5))
        self.imagem_entry = ttk.Entry(settings_frame, width=50)
        self.imagem_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Footer
        ttk.Label(settings_frame, text="Footer Text:").pack(anchor=tk.W, pady=(0, 5))
        self.footer_entry = ttk.Entry(settings_frame, width=50)
        self.footer_entry.insert(0, "Equipe de administração ReisPixelmon")
        self.footer_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Send button
        send_button = ttk.Button(
            main_frame,
            text="Enviar Webhook",
            command=self.enviar_webhook,
            style="Send.TButton"
        )
        send_button.pack(pady=15, ipadx=10, ipady=5)
        ToolTip(send_button, "Clique para enviar sua mensagem")

        # +++ Nova barra de progresso +++
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5,0))
        self.progress.pack_forget()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para enviar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
    def update_color_preview(self, event=None):
        try:
            color = f"#{self.cor_entry.get()}"
            self.color_preview.config(bg=color)
        except:
            pass
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=f"#{self.cor_entry.get()}")
        if color[1]:
            hex_color = color[1][1:]  # Remove the # from the hex value
            self.cor_entry.delete(0, tk.END)
            self.cor_entry.insert(0, hex_color.upper())
            self.color_preview.config(bg=color[1])
    
    def validate_webhook_url(self, url):
        # Basic Discord webhook URL validation
        pattern = r'^https://discord\.com/api/webhooks/\d+/[\w-]+$'
        return re.match(pattern, url) is not None
    
    def enviar_webhook(self):
        webhook_url = self.url_entry.get().strip()
        current_tab = self.notebook.index(self.notebook.select())
        
        # Basic URL validation
        if not webhook_url:
            messagebox.showerror("Erro", "Por favor, insira uma URL de webhook!")
            return
            
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            messagebox.showerror("Erro", "Formato de URL de webhook do Discord inválido!")
            return
        
        data = {}
        
        # Processa as menções de cargos
        role_mentions = ""
        roles_ids = self.mention_entry.get().strip()
        if roles_ids:
            role_ids_list = [role.strip() for role in roles_ids.split(",")]
            for role_id in role_ids_list:
                if role_id.isdigit():  # Verifica se é um número
                    role_mentions += f"<@&{role_id}> "
    
        # Process based on selected tab
        if current_tab == 0:  # Simple message
            mensagem_simples = self.simple_message.get("1.0", tk.END).strip()
            if not mensagem_simples:
                messagebox.showerror("Erro", "Por favor, insira uma mensagem para enviar!")
                return
            
            # Adiciona menções ao início da mensagem simples
            content = role_mentions + mensagem_simples if role_mentions else mensagem_simples
            data = {"content": content}
        else:  # Embed message
            titulo = self.titulo_entry.get()
            descricao = self.descricao_text.get("1.0", tk.END).strip()
            cor = self.cor_entry.get()
            imagem_url = self.imagem_entry.get()
            footer = self.footer_entry.get()
            
            if not titulo and not descricao:
                messagebox.showerror("Erro", "Título ou descrição são necessários para embeds!")
                return
                
            # Build embed
            embed = {
                "title": titulo,
                "description": descricao,
                "color": int(cor, 16) if cor else 16711680,  # Default red color
            }
            
            if imagem_url:
                embed["image"] = {"url": imagem_url}
                
            if footer:
                embed["footer"] = {"text": footer}
                
            # Adiciona as menções no campo content, separado do embed
            data = {
                "content": role_mentions if role_mentions else "",
                "embeds": [embed]
            }
    
        # Inicia animação
        self.progress.pack(fill=tk.X, pady=(5,0))
        self.progress.start(20)
        self.status_var.set("Enviando webhook...")
        self.root.update_idletasks()

        # Update status
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                self.status_var.set("Webhook enviado com sucesso!")
                messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
            else:
                self.status_var.set(f"Erro: Código de status {response.status_code}")
                messagebox.showerror("Erro", f"Falha ao enviar mensagem. Código de status: {response.status_code}")
        except Exception as e:
            self.status_var.set(f"Erro: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        finally:
            # Para animação
            self.progress.stop()
            self.progress.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordWebhookApp(root)
    root.mainloop()
