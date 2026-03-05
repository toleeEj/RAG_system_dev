// src/App.jsx
import { useState, useRef, useEffect } from 'react'
import './index.css'

function App() {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      text: 'Hello! I can help you with questions about savings accounts, loans, interest rates, branch locations, and more.\n\nWhat would you like to know?',
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = { type: 'user', text: input.trim() }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const res = await fetch('http://127.0.0.1:8000/api/query/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input.trim() }),
      })

      if (!res.ok) throw new Error(`HTTP ${res.status}`)

      const data = await res.json()
      const aiReply = {
        type: 'assistant',
        text: data.answer || "I don't have an answer for that right now.",
      }

      setMessages((prev) => [...prev, aiReply])
    } catch (err) {
      console.error(err)
      setMessages((prev) => [
        ...prev,
        { type: 'assistant', text: 'Sorry, something went wrong. Please try again.' },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-blue-700 text-white p-4 text-center font-semibold text-lg shadow">
        Bank AI Assistant
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-24">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`
                max-w-[80%] px-4 py-3 rounded-2xl shadow-sm
                ${msg.type === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'}
              `}
            >
              {msg.text.split('\n').map((line, idx) => (
                <p key={idx} className={idx > 0 ? 'mt-1' : ''}>
                  {line}
                </p>
              ))}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-600 px-4 py-3 rounded-2xl shadow-sm animate-pulse">
              Thinking...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-4 bg-white border-t flex gap-3 sticky bottom-0"
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about our banking services..."
          className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none h-12 max-h-32"
          rows={1}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className={`
            px-6 py-3 rounded-lg font-medium text-white transition
            ${isLoading || !input.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'}
          `}
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default App