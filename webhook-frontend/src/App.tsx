import { useState } from 'react'
import { FaDiscord, FaPaperPlane } from 'react-icons/fa'
import TitleBar from './components/TitleBar'

interface WebhookData {
  url: string
  username: string
  avatar_url: string
  content: string
  embeds: Array<{
    title: string
    description: string
    color: string
    fields: Array<{
      name: string
      value: string
      inline: boolean
    }>
  }>
}

function App() {
  const [webhookData, setWebhookData] = useState<WebhookData>({
    url: '',
    username: '',
    avatar_url: '',
    content: '',
    embeds: [{
      title: '',
      description: '',
      color: '#5865F2',
      fields: []
    }]
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(webhookData),
      })
      if (response.ok) {
        alert('Webhook enviado com sucesso!')
      } else {
        alert('Erro ao enviar webhook')
      }
    } catch (error) {
      console.error('Erro:', error)
      alert('Erro ao enviar webhook')
    }
  }

  return (
    <div className="min-h-screen bg-discord-dark text-white flex flex-col">
      <TitleBar />
      <div className="flex-1 container mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2 flex items-center justify-center gap-2">
            <FaDiscord className="text-discord-blue" />
            Discord Webhook
          </h1>
          <p className="text-discord-light">Envie mensagens para seu servidor Discord</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Formulário */}
          <div className="bg-discord-darker p-6 rounded-lg shadow-lg">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">URL do Webhook</label>
                <input
                  type="text"
                  value={webhookData.url}
                  onChange={(e) => setWebhookData({ ...webhookData, url: e.target.value })}
                  className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue"
                  placeholder="https://discord.com/api/webhooks/..."
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nome do Bot</label>
                  <input
                    type="text"
                    value={webhookData.username}
                    onChange={(e) => setWebhookData({ ...webhookData, username: e.target.value })}
                    className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue"
                    placeholder="Nome do Bot"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Avatar URL</label>
                  <input
                    type="text"
                    value={webhookData.avatar_url}
                    onChange={(e) => setWebhookData({ ...webhookData, avatar_url: e.target.value })}
                    className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue"
                    placeholder="https://..."
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Mensagem</label>
                <textarea
                  value={webhookData.content}
                  onChange={(e) => setWebhookData({ ...webhookData, content: e.target.value })}
                  className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue h-24"
                  placeholder="Digite sua mensagem aqui..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Título do Embed</label>
                <input
                  type="text"
                  value={webhookData.embeds[0].title}
                  onChange={(e) => setWebhookData({
                    ...webhookData,
                    embeds: [{ ...webhookData.embeds[0], title: e.target.value }]
                  })}
                  className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue"
                  placeholder="Título do Embed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Descrição do Embed</label>
                <textarea
                  value={webhookData.embeds[0].description}
                  onChange={(e) => setWebhookData({
                    ...webhookData,
                    embeds: [{ ...webhookData.embeds[0], description: e.target.value }]
                  })}
                  className="w-full px-4 py-2 bg-discord-dark border border-discord-light rounded-md focus:outline-none focus:ring-2 focus:ring-discord-blue h-24"
                  placeholder="Descrição do Embed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Cor do Embed</label>
                <input
                  type="color"
                  value={webhookData.embeds[0].color}
                  onChange={(e) => setWebhookData({
                    ...webhookData,
                    embeds: [{ ...webhookData.embeds[0], color: e.target.value }]
                  })}
                  className="w-full h-10 bg-discord-dark border border-discord-light rounded-md cursor-pointer"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-discord-blue hover:bg-discord-blue/90 text-white font-medium py-3 px-4 rounded-md transition-colors flex items-center justify-center gap-2"
              >
                <FaPaperPlane />
                Enviar Webhook
              </button>
            </form>
          </div>

          {/* Preview */}
          <div className="bg-discord-darker p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-4">Preview</h2>
            <div className="bg-discord-dark p-4 rounded-md">
              {webhookData.username && (
                <div className="flex items-center gap-3 mb-4">
                  {webhookData.avatar_url && (
                    <img
                      src={webhookData.avatar_url}
                      alt="Avatar"
                      className="w-10 h-10 rounded-full"
                    />
                  )}
                  <span className="font-medium">{webhookData.username}</span>
                </div>
              )}
              
              {webhookData.content && (
                <p className="mb-4">{webhookData.content}</p>
              )}

              {webhookData.embeds[0].title && (
                <div
                  className="border-l-4 p-4 rounded-r-md"
                  style={{ borderColor: webhookData.embeds[0].color }}
                >
                  {webhookData.embeds[0].title && (
                    <h3 className="font-bold mb-2">{webhookData.embeds[0].title}</h3>
                  )}
                  {webhookData.embeds[0].description && (
                    <p className="text-discord-light">{webhookData.embeds[0].description}</p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
