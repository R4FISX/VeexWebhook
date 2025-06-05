import { FaMinus, FaTimes } from 'react-icons/fa'

const TitleBar = () => {
  const minimizeWindow = () => {
    window.electron.minimize()
  }

  const closeWindow = () => {
    window.electron.close()
  }

  return (
    <div className="titlebar h-8 bg-discord-darker flex items-center justify-between px-4 select-none">
      <div className="flex items-center gap-2">
        <img src="/discord.svg" alt="Discord" className="w-5 h-5" />
        <span className="text-sm font-medium">Discord Webhook</span>
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={minimizeWindow}
          className="p-1 hover:bg-discord-dark rounded-md transition-colors"
        >
          <FaMinus className="w-3 h-3" />
        </button>
        <button
          onClick={closeWindow}
          className="p-1 hover:bg-discord-red rounded-md transition-colors"
        >
          <FaTimes className="w-3 h-3" />
        </button>
      </div>
    </div>
  )
}

export default TitleBar 