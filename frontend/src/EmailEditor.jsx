import React, { useState } from 'react';
import { ImagePlus, Text, Heading3 } from 'lucide-react';

export default function EmailEditor() {
  const [blocks, setBlocks] = useState([]);
  const [to, setTo] = useState('');
  const [subject, setSubject] = useState('');

  const addBlock = (type) => {
    setBlocks([...blocks, { id: Date.now(), type, content: '' }]);
  };

  const updateContent = (id, newContent) => {
    setBlocks(blocks.map(b => b.id === id ? { ...b, content: newContent } : b));
  };

  const renderBlock = (block) => {
    switch (block.type) {
      case 'title':
        return (
          <input
            className="w-full border p-2 rounded"
            placeholder="Email Title"
            value={block.content}
            onChange={e => updateContent(block.id, e.target.value)}
          />
        );
      case 'text':
        return (
          <textarea
            className="w-full border p-2 rounded"
            placeholder="Paragraph text"
            value={block.content}
            onChange={e => updateContent(block.id, e.target.value)}
          />
        );
      case 'image':
        return (
          <input
            className="w-full border p-2 rounded"
            placeholder="Image URL"
            value={block.content}
            onChange={e => updateContent(block.id, e.target.value)}
          />
        );
      default:
        return null;
    }
  };

  const generateHtml = () => {
    return blocks.map(b => {
      if (b.type === 'title') return `<h1>${b.content}</h1>`;
      if (b.type === 'text') return `<p>${b.content}</p>`;
      if (b.type === 'image') return `<img src='${b.content}' style='max-width:100%' />`;
      return '';
    }).join('\n');
  };

  const handleCopy = () => {
    const html = generateHtml();
    navigator.clipboard.writeText(html);
    alert('HTML copied to clipboard!');
  };

  const handleSend = async () => {
    const html = generateHtml();
    if (!to) return alert("Missing recipient email");

    try {
      const res = await fetch('http://127.0.0.1:5000/send-html', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ html, to, subject })
      });
      const data = await res.json();
      if (res.ok) {
        alert("✅ Email sent successfully!");
      } else {
        alert("❌ Error: " + data.error);
      }
    } catch (err) {
      alert("❌ Request failed: " + err.message);
    }
  };

  return (
    <div className="p-6 space-y-4 max-w-3xl mx-auto font-sans">
      <h1 className="text-2xl font-bold">📧 Drag-and-Drop Email Editor</h1>

      {/* Block Buttons */}
      <div className="flex gap-4">
        <button onClick={() => addBlock('title')} className="bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-2">
          <Heading3 className="w-4 h-4" /> Title
        </button>
        <button onClick={() => addBlock('text')} className="bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-2">
          <Text className="w-4 h-4" /> Text
        </button>
        <button onClick={() => addBlock('image')} className="bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-2">
          <ImagePlus className="w-4 h-4" /> Image
        </button>
      </div>

      {/* Editor Blocks */}
      <div className="space-y-4">
        {blocks.map(block => (
          <div key={block.id} className="border p-4 rounded shadow bg-white">
            {renderBlock(block)}
          </div>
        ))}
      </div>

      {/* Email Inputs */}
      <div className="space-y-2 pt-4">
        <input
          className="w-full border p-2 rounded"
          placeholder="Recipient email"
          value={to}
          onChange={e => setTo(e.target.value)}
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Email Subject"
          value={subject}
          onChange={e => setSubject(e.target.value)}
        />
        <button onClick={handleSend} className="bg-green-600 text-white px-4 py-2 rounded">
          🚀 Send Email
        </button>
        <button onClick={handleCopy} className="border px-4 py-2 rounded">
          📋 Copy HTML
        </button>
      </div>
    </div>
  );
}
