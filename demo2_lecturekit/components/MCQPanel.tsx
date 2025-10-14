'use client';

import { useState } from 'react';

import { MCQ } from '@/lib/types';

interface MCQPanelProps {
  sessionId: string;
  summary: string;
  mcqs: MCQ[];
  onMcqsChange: (mcqs: MCQ[]) => void;
}

export default function MCQPanel({ sessionId, summary, mcqs, onMcqsChange }: MCQPanelProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [count, setCount] = useState(5);
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard' | 'mixed'>('mixed');
  const [error, setError] = useState('');

  const [isSending, setIsSending] = useState(false);
  const [emailRecipients, setEmailRecipients] = useState('');

  const generateMCQs = async () => {
    if (!summary.trim()) {
      setError('Please generate a summary first.');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch('/api/mcqs/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, summary, count, difficulty }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate MCQs');
      }

      const data = await response.json();
      onMcqsChange(data.mcqs);
    } catch (err) {
      console.error('Error generating MCQs:', err);
      setError('Failed to generate MCQs. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const updateMCQ = (index: number, field: string, value: string | number) => {
    const updated = [...mcqs];
    updated[index] = { ...updated[index], [field]: value };
    onMcqsChange(updated);
  };

  const updateOption = (mcqIndex: number, optionIndex: number, value: string) => {
    const updated = [...mcqs];
    updated[mcqIndex].options[optionIndex] = value;
    onMcqsChange(updated);
  };

  const deleteMCQ = (index: number) => {
    const updated = mcqs.filter((_, i) => i !== index);
    onMcqsChange(updated);
  };

  const addNewMCQ = () => {
    const newMCQ: MCQ = {
      q: 'New question',
      options: ['Option A', 'Option B', 'Option C', 'Option D'],
      correctIndex: 0,
      rationale: 'Explanation...',
    };
    onMcqsChange([...mcqs, newMCQ]);
  };

  const sendEmail = async () => {
    if (!emailRecipients.trim()) {
      setError('Please enter email recipients.');
      return;
    }

    if (mcqs.length === 0) {
      setError('Please generate MCQs first.');
      return;
    }

    setIsSending(true);
    setError('');

    try {
      const recipients = emailRecipients.split(',').map((email) => email.trim());
      const response = await fetch('/api/email/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          recipients,
          mcqs,
          subject: 'Quiz Questions from Recent Lecture',
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send email');
      }

      alert('Email sent successfully!');
      setEmailRecipients('');
    } catch (err) {
      console.error('Error sending email:', err);
      setError('Failed to send email. Please try again.');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Generation Controls */}
      <div className="flex flex-wrap gap-4 items-end">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Number of Questions</label>
          <input
            type="number"
            min="1"
            max="20"
            value={count}
            onChange={(e) => setCount(parseInt(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value as 'easy' | 'medium' | 'hard' | 'mixed')}
            className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
            <option value="mixed">Mixed</option>
          </select>
        </div>
        <button
          onClick={generateMCQs}
          disabled={isGenerating || !summary.trim()}
          className="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isGenerating ? '🎯 Generating...' : '🎯 Generate MCQs'}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-700">
          {error}
        </div>
      )}

      {/* MCQ List */}
      {mcqs.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-800">Questions ({mcqs.length})</h3>
            <button
              onClick={addNewMCQ}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-md transition-colors"
            >
              ➕ Add Question
            </button>
          </div>

          {mcqs.map((mcq, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4 bg-white">
              <div className="flex justify-between items-start mb-3">
                <h4 className="font-semibold text-gray-800">Question {index + 1}</h4>
                <button
                  onClick={() => deleteMCQ(index)}
                  className="text-red-600 hover:text-red-800 text-sm font-medium"
                >
                  🗑️ Delete
                </button>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Question</label>
                  <input
                    type="text"
                    value={mcq.q}
                    onChange={(e) => updateMCQ(index, 'q', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {mcq.options.map((option: string, optIndex: number) => (
                    <div key={optIndex} className="flex items-center gap-2">
                      <input
                        type="radio"
                        name={`correct-${index}`}
                        checked={mcq.correctIndex === optIndex}
                        onChange={() => updateMCQ(index, 'correctIndex', optIndex)}
                        className="text-blue-600"
                      />
                      <input
                        type="text"
                        value={option}
                        onChange={(e) => updateOption(index, optIndex, e.target.value)}
                        placeholder={`Option ${String.fromCharCode(65 + optIndex)}`}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  ))}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Rationale</label>
                  <textarea
                    value={mcq.rationale}
                    onChange={(e) => updateMCQ(index, 'rationale', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={2}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Email Distribution */}
      {mcqs.length > 0 && (
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📧 Email Distribution</h3>
          <div className="flex flex-wrap gap-4 items-end">
            <div className="flex-1 min-w-64">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Student Email Addresses (comma-separated)
              </label>
              <input
                type="text"
                value={emailRecipients}
                onChange={(e) => setEmailRecipients(e.target.value)}
                placeholder="student1@example.com, student2@example.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={sendEmail}
              disabled={isSending || !emailRecipients.trim()}
              className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSending ? '📧 Sending...' : '📧 Send to Students'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
