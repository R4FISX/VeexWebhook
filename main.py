import requests
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import re
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request
import json
import os

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
        
        # Armazenar webhooks recentes
        self.recent_webhooks = []
        self.load_saved_webhooks()

        # Bind keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.enviar_webhook())
        self.root.bind('<Control-s>', lambda e: self.save_current_webhook())

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Moderno e clean

        # Cores base
        bg = '#23272A'
        fg = '#FFFFFF'
        accent = '#7289DA'
        button_bg = '#5865F2'
        button_fg = '#FFFFFF'
        entry_bg = '#2C2F33'

        self.root.configure(bg=bg)
        self.style.configure('TFrame', background=bg)
        self.style.configure('TNotebook', background=bg, tabmargins=[2, 5, 2, 0])
        self.style.configure('TNotebook.Tab', background=bg, foreground=fg, padding=[12, 8], font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', accent)], foreground=[('selected', fg)])

        self.style.configure('TLabel', background=bg, foreground=fg, font=('Segoe UI', 11))
        self.style.configure('TButton', background=button_bg, foreground=button_fg, font=('Segoe UI', 11, 'bold'), padding=8)
        self.style.map('TButton', background=[('active', accent)])
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg, font=('Segoe UI', 10), padding=6)
        self.style.configure('TCheckbutton', background=bg, foreground=fg, font=('Segoe UI', 10))

        # Botão de envio destacado
        self.style.configure('Send.TButton', background='#43B581', foreground='white', font=('Segoe UI', 12, 'bold'), padding=10)
        self.style.map('Send.TButton', background=[('active', '#3CA374'), ('pressed', '#2D7A59')])

        self.style.configure('ColorPicker.TButton', background='#FF0000')
        
    def create_ui(self):
        # Main container com scrollbar, ocupando toda a janela
        main_canvas = tk.Canvas(self.root, bg="#2C2F33", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        main_frame = ttk.Frame(main_canvas)

        main_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        canvas_frame = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def configure_scroll(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Ajusta largura do main_frame para sempre ocupar toda a largura do canvas
            main_canvas.itemconfig(canvas_frame, width=main_canvas.winfo_width())
        main_frame.bind("<Configure>", configure_scroll)
        main_canvas.bind("<Configure>", configure_scroll)
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Função para forçar fundo escuro nos LabelFrames
        def set_dark_labelframe(widget):
            try:
                widget.configure(style="Dark.TLabelframe")
            except:
                pass

        # Estilo escuro para LabelFrame
        self.style.configure("Dark.TLabelframe", background="#23272A", foreground="#FFFFFF", borderwidth=1)
        self.style.configure("Dark.TLabelframe.Label", background="#23272A", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"))

        # Webhook URL section
        url_frame = ttk.LabelFrame(main_frame, text="Webhook do Discord", padding="15 10 15 10", style="Dark.TLabelframe")
        url_frame.pack(fill=tk.X, pady=(0, 15), expand=True)
        set_dark_labelframe(url_frame)
        ttk.Label(url_frame, text="URL:", font=("Segoe UI", 10, "bold"), background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        url_input_frame = ttk.Frame(url_frame, style="TFrame")
        url_input_frame.pack(fill=tk.X, expand=True)
        self.url_entry = PlaceholderEntry(url_input_frame, "https://discord.com/api/webhooks/ID/TOKEN", width=80)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        ToolTip(self.url_entry, "Cole aqui sua URL de webhook do Discord")

        # Menções
        mention_frame = ttk.LabelFrame(main_frame, text="Menção de Cargos", padding="15 10 15 10", style="Dark.TLabelframe")
        mention_frame.pack(fill=tk.X, pady=(0, 15), expand=True)
        set_dark_labelframe(mention_frame)
        ttk.Label(mention_frame, text="IDs separados por vírgula:", background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.mention_entry = ttk.Entry(mention_frame, width=50)
        self.mention_entry.pack(fill=tk.X, ipady=3, expand=True)
        ToolTip(self.mention_entry, "Insira IDs de cargos para mencioná-los (ex: 123456789,987654321)")

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aba Mensagem Simples
        self.simple_frame = ttk.Frame(self.notebook, padding=15, style="TFrame")
        self.notebook.add(self.simple_frame, text="Mensagem Simples")
        ttk.Label(self.simple_frame, text="Conteúdo da Mensagem:", font=("Segoe UI", 10, "bold"), background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.simple_message = tk.Text(self.simple_frame, height=10, width=70, font=("Segoe UI", 10), bg="#40444B", fg="white")
        self.simple_message.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Aba Embed
        self.embed_frame = ttk.Frame(self.notebook, padding=15, style="TFrame")
        self.notebook.add(self.embed_frame, text="Mensagem Embed")
        embed_content = ttk.Frame(self.embed_frame, style="TFrame")
        embed_content.pack(fill=tk.BOTH, expand=True)
        # Esquerda: configurações do embed
        settings_frame = ttk.LabelFrame(embed_content, text="Configurações do Embed", padding="15 10 15 10", style="Dark.TLabelframe")
        settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=5)
        set_dark_labelframe(settings_frame)
        ttk.Label(settings_frame, text="Título:", background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.titulo_entry = ttk.Entry(settings_frame, width=50)
        self.titulo_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        ttk.Label(settings_frame, text="Descrição:", background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.descricao_text = tk.Text(settings_frame, height=10, width=50, font=("Segoe UI", 10), bg="#40444B", fg="white", wrap=tk.WORD)
        self.descricao_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        color_frame = ttk.Frame(settings_frame, style="TFrame")
        color_frame.pack(fill=tk.X, pady=(0, 10), expand=True)
        ttk.Label(color_frame, text="Cor:", background="#23272A").pack(side=tk.LEFT, padx=(0, 5))
        self.color_preview = tk.Canvas(color_frame, width=20, height=20, bg="#FF0000", highlightthickness=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        self.cor_entry = ttk.Entry(color_frame, width=10)
        self.cor_entry.insert(0, "FF0000")
        self.cor_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.cor_entry.bind("<KeyRelease>", self.update_color_preview)
        color_btn = ttk.Button(color_frame, text="Escolher Cor", command=self.choose_color)
        color_btn.pack(side=tk.LEFT, padx=5)
        ttk.Label(settings_frame, text="Image URL:", background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.imagem_entry = ttk.Entry(settings_frame, width=50)
        self.imagem_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        ttk.Label(settings_frame, text="Footer Text:", background="#23272A").pack(anchor=tk.W, pady=(0, 5))
        self.footer_entry = ttk.Entry(settings_frame, width=50)
        self.footer_entry.insert(0, "Equipe de administração ReisPixelmon")
        self.footer_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)

        # Direita: preview do embed
        preview_frame = ttk.LabelFrame(embed_content, text="Preview do Embed", padding="15 10 15 10", style="Dark.TLabelframe")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)
        set_dark_labelframe(preview_frame)
        self.preview_frame = ttk.Frame(preview_frame, padding=20, relief="solid", borderwidth=3, style="Preview.TFrame")
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_title = ttk.Label(self.preview_frame, text="", font=("Segoe UI", 13, "bold"), background="#36393F")
        self.preview_title.pack(anchor=tk.W, pady=(0, 8))
        self.preview_desc = ttk.Label(self.preview_frame, text="", wraplength=300, font=("Segoe UI", 10), background="#36393F")
        self.preview_desc.pack(anchor=tk.W, fill=tk.X, pady=(0, 8))
        self.preview_img = ttk.Label(self.preview_frame, background="#36393F")
        self.preview_img.pack(anchor=tk.W, pady=(5, 8))
        self.preview_footer = ttk.Label(self.preview_frame, text="", font=("Segoe UI", 8), background="#36393F")
        self.preview_footer.pack(anchor=tk.W, side=tk.BOTTOM)

        # Vincular eventos para atualização em tempo real
        self.titulo_entry.bind("<KeyRelease>", self.update_preview)
        self.descricao_text.bind("<KeyRelease>", self.update_preview)
        self.cor_entry.bind("<KeyRelease>", self.update_preview)
        self.imagem_entry.bind("<KeyRelease>", self.update_preview)
        self.footer_entry.bind("<KeyRelease>", self.update_preview)

        # Botão de envio centralizado
        send_button_frame = ttk.Frame(main_frame, style="TFrame")
        send_button_frame.pack(pady=25, fill=tk.X, expand=True)
        send_button = ttk.Button(
            send_button_frame,
            text="Enviar Webhook",
            command=self.enviar_webhook,
            style="Send.TButton",
            width=22
        )
        send_button.pack(ipadx=12, ipady=10)
        ToolTip(send_button, "Clique para enviar sua mensagem (Ctrl+Enter)")
        def button_click_effect(event):
            send_button.state(['pressed'])
            self.root.after(100, lambda: send_button.state(['!pressed']))
            self.enviar_webhook()
        send_button.bind('<Button-1>', button_click_effect)

        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5,0))
        self.progress.pack_forget()

        # Status bar discreto
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para enviar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9), background="#23272A", foreground="#AAAAAA")
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
    
    def validate_image_url(self):
        """Tenta validar e carregar uma imagem da URL especificada"""
        img_url = self.imagem_entry.get().strip()
        if not img_url:
            return False
            
        if not img_url.startswith(("http://", "https://")):
            messagebox.showwarning("URL de Imagem", "URLs de imagem devem começar com http:// ou https://")
            return False
            
        try:
            with urllib.request.urlopen(img_url) as u:
                raw_data = u.read()
            img = Image.open(io.BytesIO(raw_data))
            return True
        except Exception as e:
            messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem: {str(e)}")
            return False
    
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

    def update_preview(self, event=None):
        """Atualiza o preview do embed em tempo real"""
        # Estilo baseado na cor selecionada
        cor = self.cor_entry.get()
        try:
            color_hex = f"#{cor}"
            self.style.configure("Preview.TFrame", background="#36393F", bordercolor=color_hex)
            self.preview_frame.configure(style="Preview.TFrame")
            
            # Atualizar borda colorida
            self.preview_frame.configure(borderwidth=3)
            
            # Atualizar título
            titulo = self.titulo_entry.get()
            self.preview_title.configure(text=titulo, foreground=color_hex if titulo else "white")
            
            # Atualizar descrição
            desc = self.descricao_text.get("1.0", tk.END).strip()
            self.preview_desc.configure(text=desc)
            
            # Atualizar imagem
            img_url = self.imagem_entry.get().strip()
            if img_url and img_url.startswith(("http://", "https://")):
                try:
                    with urllib.request.urlopen(img_url) as u:
                        raw_data = u.read()
                    img = Image.open(io.BytesIO(raw_data))
                    img = img.resize((200, int(200 * img.height / img.width)), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    self.preview_img.configure(image=img_tk)
                    self.preview_img.image = img_tk  # Manter referência
                except Exception:
                    self.preview_img.configure(image="")
            else:
                self.preview_img.configure(image="")
                
            # Atualizar footer
            footer = self.footer_entry.get()
            self.preview_footer.configure(text=footer)
            
        except Exception as e:
            print(f"Erro ao atualizar preview: {e}")

    def save_current_webhook(self):
        """Salva o webhook atual na lista de recentes"""
        current_url = self.url_entry.get().strip()
        if not current_url or current_url == self.url_entry.placeholder:
            messagebox.showwarning("Salvar Webhook", "Digite uma URL válida primeiro")
            return
            
        # Perguntar por um nome amigável
        name = tk.simpledialog.askstring("Salvar Webhook", "Nome para este webhook:")
        if not name:
            return
            
        # Verificar se já existe
        for i, (saved_name, saved_url) in enumerate(self.recent_webhooks):
            if saved_url == current_url:
                self.recent_webhooks[i] = (name, current_url)
                self.save_webhooks_to_file()
                messagebox.showinfo("Webhook Salvo", "Webhook atualizado com sucesso")
                return
        
        # Adicionar novo
        self.recent_webhooks.append((name, current_url))
        self.save_webhooks_to_file()
        messagebox.showinfo("Webhook Salvo", "Webhook salvo com sucesso")
        
    def save_webhooks_to_file(self):
        """Salva webhooks em um arquivo de configuração"""
        config_dir = os.path.join(os.path.expanduser("~"), ".veexwebhook")
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, "webhooks.json"), "w") as f:
            json.dump(self.recent_webhooks, f)
            
    def load_saved_webhooks(self):
        """Carrega webhooks salvos do arquivo de configuração"""
        config_file = os.path.join(os.path.expanduser("~"), ".veexwebhook", "webhooks.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    self.recent_webhooks = json.load(f)
            except Exception:
                self.recent_webhooks = []

    def show_saved_webhooks(self):
        """Mostra uma janela com webhooks salvos"""
        if not self.recent_webhooks:
            messagebox.showinfo("Webhooks Salvos", "Nenhum webhook salvo")
            return
            
        popup = tk.Toplevel(self.root)
        popup.title("Webhooks Salvos")
        popup.geometry("400x300")
        popup.transient(self.root)
        popup.grab_set()
        
        # Lista de webhooks
        frame = ttk.Frame(popup, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Selecione um webhook:").pack(anchor=tk.W, pady=(0, 10))
        
        listbox = tk.Listbox(frame, bg="#40444B", fg="white", font=("Segoe UI", 10))
        listbox.pack(fill=tk.BOTH, expand=True)
        
        for name, _ in self.recent_webhooks:
            listbox.insert(tk.END, name)
        
        # CRIE O btn_frame ANTES DE USAR OS BOTÕES!
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        def load_selected():
            selected = listbox.curselection()
            if selected:
                index = selected[0]
                _, url = self.recent_webhooks[index]
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url)
                self.url_entry['foreground'] = self.url_entry.default_fg
                popup.destroy()
        
        def delete_selected():
            selected = listbox.curselection()
            if selected:
                index = selected[0]
                del self.recent_webhooks[index]
                self.save_webhooks_to_file()
                listbox.delete(index)

        def edit_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showinfo("Editar Webhook", "Selecione um webhook para editar.")
                return
            index = selected[0]
            old_name, old_url = self.recent_webhooks[index]

            edit_win = tk.Toplevel(popup)
            edit_win.title("Editar Webhook")
            edit_win.geometry("350x150")
            edit_win.transient(popup)
            edit_win.grab_set()

            ttk.Label(edit_win, text="Nome:").pack(anchor=tk.W, padx=10, pady=(10, 0))
            name_entry = ttk.Entry(edit_win)
            name_entry.pack(fill=tk.X, padx=10)
            name_entry.insert(0, old_name)

            ttk.Label(edit_win, text="URL:").pack(anchor=tk.W, padx=10, pady=(10, 0))
            url_entry = ttk.Entry(edit_win)
            url_entry.pack(fill=tk.X, padx=10)
            url_entry.insert(0, old_url)

            def save_edit():
                new_name = name_entry.get().strip()
                new_url = url_entry.get().strip()
                if not new_name or not new_url:
                    messagebox.showerror("Erro", "Nome e URL não podem ser vazios.")
                    return
                self.recent_webhooks[index] = (new_name, new_url)
                self.save_webhooks_to_file()
                listbox.delete(index)
                listbox.insert(index, new_name)
                edit_win.destroy()

            ttk.Button(edit_win, text="Salvar", command=save_edit).pack(pady=10)
            ttk.Button(edit_win, text="Cancelar", command=edit_win.destroy).pack()

        # Agora sim, adicione os botões:
        ttk.Button(btn_frame, text="Carregar", command=load_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Editar", command=edit_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Excluir", command=delete_selected).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Fechar", command=popup.destroy).pack(side=tk.RIGHT)

        # Estilo da janela
        style = ttk.Style(popup)
        style.configure("TButton", padding=6, relief="flat",
                        background="#7289DA", foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#677BC4")])

        # Configurações da listbox
        listbox.configure(borderwidth=0, highlightthickness=0)
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

# Adicione isso ao final do arquivo:
if __name__ == "__main__":
    try:
        import tkinter.simpledialog  # Necessário para o method askstring
        root = tk.Tk()
        app = DiscordWebhookApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Erro ao iniciar a aplicação: {e}")
        traceback.print_exc()
        # Mostrar uma mensagem de erro se a interface não iniciar
        try:
            messagebox.showerror("Erro de Inicialização", f"Erro ao iniciar: {e}")
        except:
            pass
        # Manter o console aberto se estiver executando como .py
        input("Pressione Enter para fechar...")
