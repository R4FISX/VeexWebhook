import requests
import tkinter as tk
from tkinter import messagebox, ttk


def enviar_webhook():
    webhook_url = url_entry.get()
    mensagem_simples = mensagem_text.get("1.0", tk.END).strip()
    usar_embed = embed_var.get()


    if not webhook_url.startswith(""):
        messagebox.showerror("Erro", "Insira uma URL válida do webhook!")
        return


    data = {}


    if usar_embed:
        titulo = titulo_entry.get()
        descricao = descricao_text.get("1.0", tk.END).strip()
        cor = cor_entry.get()
        imagem_url = imagem_entry.get()


        if not titulo or not descricao:
            messagebox.showerror("Erro", "Título e Descrição são obrigatórios para embeds!")
            return

        data = {
            "embeds": [
                {
                    "title": titulo,
                    "description": descricao,
                    "color": int(cor, 16) if cor else 16711680,  # Cor padrão vermelha
                    "image": {"url": imagem_url} if imagem_url else {},
                    "footer": {"text": "Equipe de adminstração Veexmc"}
                }
            ]
        }
    else:
        if not mensagem_simples:
            messagebox.showerror("Erro", "Insira uma mensagem simples para enviar!")
            return
        data = {"content": mensagem_simples}

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
        else:
            messagebox.showerror("Erro", f"Falha ao enviar mensagem. Código: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

app = tk.Tk()
app.title("App de Envio de Webhooks")
app.geometry("600x600")

tk.Label(app, text="URL do Webhook:").pack(anchor=tk.W, padx=10, pady=5)
url_entry = tk.Entry(app, width=60)
url_entry.pack(padx=10, pady=5)

tk.Label(app, text="Mensagem Simples:").pack(anchor=tk.W, padx=10, pady=5)
mensagem_text = tk.Text(app, height=5, width=60)
mensagem_text.pack(padx=10, pady=5)

embed_var = tk.BooleanVar()
tk.Checkbutton(app, text="Usar Embed", variable=embed_var).pack(anchor=tk.W, padx=10, pady=5)

embed_frame = tk.Frame(app)
embed_frame.pack(padx=10, pady=10, fill=tk.X)

tk.Label(embed_frame, text="Título:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
titulo_entry = tk.Entry(embed_frame, width=50)
titulo_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(embed_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
descricao_text = tk.Text(embed_frame, height=5, width=50)
descricao_text.grid(row=1, column=1, padx=5, pady=5)

tk.Label(embed_frame, text="Cor (Hexadecimal):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
cor_entry = tk.Entry(embed_frame, width=20)
cor_entry.insert(0, "FF0000")  # Cor padrão vermelha
cor_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(embed_frame, text="URL da Imagem:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
imagem_entry = tk.Entry(embed_frame, width=50)
imagem_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(app, text="Enviar Webhook", command=enviar_webhook, bg="green", fg="white").pack(pady=20)

app.mainloop()
