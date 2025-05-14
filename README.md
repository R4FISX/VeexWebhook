```markdown
# Discord Webhook Sender - ReisPixelmon

Uma aplicação desktop em Python com interface gráfica (Tkinter) para facilitar o envio de mensagens e embeds para webhooks do Discord, com recursos avançados como menção de cargos, preview de embed em tempo real, gerenciamento de webhooks salvos e interface inspirada no Discord.

---

## Recursos

- **Envio de mensagens simples ou embeds para webhooks do Discord**
- **Menção de cargos**: insira IDs de cargos para notificar membros
- **Preview em tempo real** do embed (título, descrição, cor, imagem, footer)
- **Gerenciamento de webhooks salvos**: salve, edite, exclua e carregue URLs de webhooks
- **Barra de progresso e status** durante o envio
- **Atalhos de teclado**:  
  - `Ctrl+Enter` para enviar  
  - `Ctrl+S` para salvar webhook
- **Interface amigável** e responsiva, com tooltips e placeholders

---

## Instalação

1. **Clone ou baixe este repositório**

2. **Instale as dependências:**
   ```bash
   pip install requests pillow
   ```

3. **Execute o aplicativo:**
   ```bash
   python main.py
   ```

---

## Como Usar

### 1. **URL do Webhook**
- Cole a URL do webhook do Discord no campo indicado (exemplo: `https://discord.com/api/webhooks/ID/TOKEN`).

### 2. **Mencionar Cargos**
- Insira os IDs dos cargos que deseja mencionar, separados por vírgula (ex: `123456789,987654321`).  
- Os membros desses cargos serão notificados.

### 3. **Mensagem Simples**
- Clique na aba "Mensagem Simples" para enviar apenas texto.

### 4. **Mensagem Embed**
- Clique na aba "Mensagem Embed" para criar um embed customizado:
  - **Título** e **Descrição**
  - **Cor** (hexadecimal, ex: `FF0000`)
  - **Imagem** (URL)
  - **Footer** (texto de rodapé)
- Veja o preview em tempo real à direita.

### 5. **Enviar**
- Clique em "Enviar Webhook" ou pressione `Ctrl+Enter`.

### 6. **Gerenciar Webhooks**
- Salve URLs de webhooks para uso futuro (`Ctrl+S` ou botão 💾).
- Carregue, edite ou exclua webhooks salvos pelo menu apropriado.

---

## Estrutura do Projeto

```
VeexWebhook/
│
├── main.py
├── .veexwebhook/
│   └── webhooks.json   # (criado automaticamente para armazenar webhooks salvos)
```

---

## Dicas

- **IDs de cargos**: Ative o modo desenvolvedor no Discord, clique com o botão direito no cargo e selecione "Copiar ID".
- **Imagens**: Use apenas URLs diretas de imagens (terminando em .png, .jpg, etc).
- **Webhooks salvos**: São armazenados em uma pasta oculta na sua home (`~/.veexwebhook/webhooks.json`).

---

## Requisitos

- Python 3.7+
- Bibliotecas: `requests`, `pillow`

---

## Licença

MIT

---

## Créditos

Desenvolvido por Rafael Rodrigues
