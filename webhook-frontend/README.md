# Discord Webhook Frontend

Interface moderna para envio de webhooks do Discord, construída com React, TypeScript e TailwindCSS.

## Tecnologias Utilizadas

- React
- TypeScript
- TailwindCSS
- Vite
- React Icons

## Requisitos

- Node.js 16.x ou superior
- npm ou yarn

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
npm install
# ou
yarn
```

## Desenvolvimento

Para iniciar o servidor de desenvolvimento:

```bash
npm run dev
# ou
yarn dev
```

O aplicativo estará disponível em `http://localhost:3000`

## Build

Para criar uma versão de produção:

```bash
npm run build
# ou
yarn build
```

Os arquivos de build serão gerados na pasta `dist`

## Preview da Build

Para visualizar a versão de produção localmente:

```bash
npm run preview
# ou
yarn preview
```

## Estrutura do Projeto

```
src/
  ├── components/     # Componentes reutilizáveis
  ├── pages/         # Páginas da aplicação
  ├── hooks/         # Custom hooks
  ├── services/      # Serviços e APIs
  ├── types/         # Definições de tipos TypeScript
  ├── utils/         # Funções utilitárias
  ├── App.tsx        # Componente principal
  └── main.tsx       # Ponto de entrada
```

## Licença

MIT
