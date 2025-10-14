'use client';

import { useState } from 'react';
import RecordingPanel from '@/components/RecordingPanel';
import NotesEditor from '@/components/NotesEditor';
import SummaryPanel from '@/components/SummaryPanel';
import MCQPanel from '@/components/MCQPanel';
import { v4 as uuidv4 } from 'uuid';
import { MCQ } from '@/lib/types';

export default function Dashboard() {
  const [sessionId] = useState(() => uuidv4());
  const [notes, setNotes] = useState('');
  const [summary, setSummary] = useState('');
  const [mcqs, setMcqs] = useState<MCQ[]>([]);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">📚 LectureKit Dashboard</h1>
          <p className="text-sm text-gray-600">Session ID: {sessionId}</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid gap-6">
          {/* Recording Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">🎥 Session Recording</h2>
            <RecordingPanel
              onRecordingComplete={(url) => console.log('Recording complete:', url)}
            />
          </div>

          {/* Notes Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">📝 Lecture Notes</h2>
            <NotesEditor
              notes={notes}
              onNotesChange={setNotes}
            />
          </div>

          {/* Summary Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">✨ Lecture Summary</h2>
            <SummaryPanel
              sessionId={sessionId}
              notes={notes}
              onSummaryGenerated={setSummary}
            />
          </div>

          {/* MCQ Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">🎯 Generated MCQs</h2>
            <MCQPanel
              sessionId={sessionId}
              summary={summary}
              mcqs={mcqs}
              onMcqsChange={setMcqs}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
