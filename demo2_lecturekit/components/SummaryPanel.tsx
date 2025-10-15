'use client';

import { useState } from 'react';

interface SummaryPanelProps {
  sessionId: string;
  notes: string;
  onSummaryGenerated: (summary: string) => void;
}

export default function SummaryPanel({ sessionId, notes, onSummaryGenerated }: SummaryPanelProps) {
  const [summary, setSummary] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [emailRecipients, setEmailRecipients] = useState('');

  const generateSummary = async () => {
    if (!notes.trim()) {
      setError('Please add some notes before generating a summary.');
      return;
    }

    setIsGenerating(true);
    setError('');
    setSummary('');

    try {
      const response = await fetch('/api/summary/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, notes }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate summary');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('No response body');
      }

      let accumulatedSummary = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        accumulatedSummary += chunk;
        setSummary(accumulatedSummary);
      }

      onSummaryGenerated(accumulatedSummary);
    } catch (err) {
      console.error('Error generating summary:', err);
      setError('Failed to generate summary. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const sendSummaryEmail = async () => {
    if (!emailRecipients.trim()) {
      setError('Please enter email recipients.');
      return;
    }

    if (!summary.trim()) {
      setError('Please generate a summary first.');
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
          summary,
          subject: 'Lecture Summary',
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send email');
      }

      alert('Summary sent successfully!');
      setEmailRecipients('');
    } catch (err) {
      console.error('Error sending email:', err);
      setError('Failed to send email. Please try again.');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <button
          onClick={generateSummary}
          disabled={isGenerating || !notes.trim()}
          className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isGenerating ? '✨ Generating Summary...' : '✨ Summarize Lecture'}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-700">
          {error}
        </div>
      )}

      {summary && (
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-md">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Generated Summary</h3>
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap text-gray-700">{summary}</p>
          </div>
        </div>
      )}

      {isGenerating && !summary && (
        <div className="flex items-center justify-center p-8">
          <div className="animate-pulse text-gray-600">Generating summary with AI...</div>
        </div>
      )}

      {/* Email Distribution for Summary */}
      {summary && (
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📧 Email Summary</h3>
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
              onClick={sendSummaryEmail}
              disabled={isSending || !emailRecipients.trim()}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSending ? '📧 Sending...' : '📧 Send Summary'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
