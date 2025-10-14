'use client';

import { useState, useEffect, useRef } from 'react';

interface NotesEditorProps {
  notes: string;
  onNotesChange: (notes: string) => void;
}

export default function NotesEditor({ notes, onNotesChange }: NotesEditorProps) {
  const [localNotes, setLocalNotes] = useState(notes);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    setLocalNotes(notes);
  }, [notes]);

  useEffect(() => {
    const saveNotesAsync = async (content: string) => {
      setIsSaving(true);
      try {
        await new Promise((resolve) => setTimeout(resolve, 500));
        onNotesChange(content);
        setLastSaved(new Date());
      } catch (error) {
        console.error('Failed to save notes:', error);
      } finally {
        setIsSaving(false);
      }
    };

    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setTimeout(() => {
      saveNotesAsync(localNotes);
    }, 1000);

    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, [localNotes, onNotesChange]);



  const insertTimestamp = () => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString();
    const newContent = `${localNotes}\n[${timestamp}] `;
    setLocalNotes(newContent);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600">
          {isSaving ? (
            <span className="text-blue-600">💾 Saving...</span>
          ) : lastSaved ? (
            <span className="text-green-600">✓ Saved at {lastSaved.toLocaleTimeString()}</span>
          ) : (
            <span>Auto-save enabled</span>
          )}
        </div>
        <button
          onClick={insertTimestamp}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md transition-colors"
        >
          🕒 Insert Timestamp
        </button>
      </div>

      <textarea
        value={localNotes}
        onChange={(e) => setLocalNotes(e.target.value)}
        placeholder="Start taking notes... Click 'Insert Timestamp' to add a timestamp linked to the recording."
        className="w-full h-64 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
      />

      <div className="text-xs text-gray-500">
        {localNotes.length} characters • Markdown supported
      </div>
    </div>
  );
}
