import requests
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import colorchooser
import re
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request

class DiscordWebhookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Webhook Sender - VeexMC")
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
        
        self.url_entry = ttk.Entry(url_input_frame, width=80)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Simple message tab
        self.simple_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.simple_frame, text="Simple Message")
        
        ttk.Label(self.simple_frame, text="Message Content:").pack(anchor=tk.W, pady=(0, 5))
        
        self.simple_message = tk.Text(self.simple_frame, height=10, width=70, 
                                      font=("Segoe UI", 10), bg="#40444B", fg="white")
        self.simple_message.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Embed tab
        self.embed_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.embed_frame, text="Embed Message")
        
        # Left side - embed settings
        settings_frame = ttk.Frame(self.embed_frame)
        settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title
        ttk.Label(settings_frame, text="Title:").pack(anchor=tk.W, pady=(0, 5))
        self.titulo_entry = ttk.Entry(settings_frame, width=50)
        self.titulo_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Description
        ttk.Label(settings_frame, text="Description:").pack(anchor=tk.W, pady=(0, 5))
        self.descricao_text = tk.Text(settings_frame, height=6, width=50, 
                                      font=("Segoe UI", 10), bg="#40444B", fg="white")
        self.descricao_text.pack(fill=tk.X, pady=(0, 10))
        
        # Color picker
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT, padx=(0, 5))
        self.color_preview = tk.Canvas(color_frame, width=20, height=20, bg="#FF0000", highlightthickness=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cor_entry = ttk.Entry(color_frame, width=10)
        self.cor_entry.insert(0, "FF0000")
        self.cor_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.cor_entry.bind("<KeyRelease>", self.update_color_preview)
        
        color_btn = ttk.Button(color_frame, text="Choose Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT, padx=5)
        
        # Image URL
        ttk.Label(settings_frame, text="Image URL:").pack(anchor=tk.W, pady=(0, 5))
        self.imagem_entry = ttk.Entry(settings_frame, width=50)
        self.imagem_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Footer
        ttk.Label(settings_frame, text="Footer Text:").pack(anchor=tk.W, pady=(0, 5))
        self.footer_entry = ttk.Entry(settings_frame, width=50)
        self.footer_entry.insert(0, "Equipe de administração VeexMC")
        self.footer_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Send button
        send_button = ttk.Button(main_frame, text="Send Webhook", command=self.enviar_webhook, style="Send.TButton")
        send_button.pack(pady=15, ipadx=10, ipady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to send")
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
            messagebox.showerror("Error", "Please enter a webhook URL!")
            return
            
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            messagebox.showerror("Error", "Invalid Discord webhook URL format!")
            return
        
        data = {}
        
        # Process based on selected tab
        if current_tab == 0:  # Simple message
            mensagem_simples = self.simple_message.get("1.0", tk.END).strip()
            if not mensagem_simples:
                messagebox.showerror("Error", "Please enter a message to send!")
                return
            data = {"content": mensagem_simples}
        else:  # Embed message
            titulo = self.titulo_entry.get()
            descricao = self.descricao_text.get("1.0", tk.END).strip()
            cor = self.cor_entry.get()
            imagem_url = self.imagem_entry.get()
            footer = self.footer_entry.get()
            
            if not titulo and not descricao:
                messagebox.showerror("Error", "Title or description is required for embeds!")
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
                
            data = {"embeds": [embed]}
            
        # Update status
        self.status_var.set("Sending webhook...")
        self.root.update_idletasks()
        
        # Send the webhook
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                self.status_var.set("Webhook sent successfully!")
                messagebox.showinfo("Success", "Message sent successfully!")
            else:
                self.status_var.set(f"Error: Status code {response.status_code}")
                messagebox.showerror("Error", f"Failed to send message. Status code: {response.status_code}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordWebhookApp(root)
    root.mainloop()
