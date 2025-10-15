'use client';

import { useState, useRef } from 'react';

interface FileUploadPanelProps {
  onFileUploaded: (content: string, fileName: string, fileType: 'video' | 'audio' | 'text') => void;
}

export default function FileUploadPanel({ onFileUploaded }: FileUploadPanelProps) {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'transcribing' | 'success' | 'error'>('idle');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus('idle');
      setErrorMessage('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploadStatus('uploading');
      setUploadProgress(0);
      setErrorMessage('');

      // Determine file type
      let fileType: 'video' | 'audio' | 'text';
      if (selectedFile.type.startsWith('video/')) {
        fileType = 'video';
      } else if (selectedFile.type.startsWith('audio/')) {
        fileType = 'audio';
      } else if (selectedFile.type.startsWith('text/') || selectedFile.name.endsWith('.txt')) {
        fileType = 'text';
      } else {
        throw new Error('Unsupported file type');
      }

      // Handle text files directly
      if (fileType === 'text') {
        const text = await selectedFile.text();
        setUploadProgress(100);
        setUploadStatus('success');
        onFileUploaded(text, selectedFile.name, fileType);
        return;
      }

      // For audio/video files, transcribe them
      setUploadStatus('transcribing');
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Transcription failed');
      }

      const data = await response.json();
      setUploadProgress(100);
      setUploadStatus('success');
      onFileUploaded(data.transcription, selectedFile.name, fileType);
    } catch (error) {
      console.error('Upload/transcription error:', error);
      setUploadStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Failed to process file');
    }
  };

  const getStatusText = () => {
    switch (uploadStatus) {
      case 'uploading':
        return '📤 Uploading...';
      case 'transcribing':
        return '🎙️ Transcribing...';
      case 'success':
        return '✓ Success';
      case 'error':
        return '✗ Error';
      default:
        return '◯ Ready';
    }
  };

  const getStatusColor = () => {
    switch (uploadStatus) {
      case 'uploading':
      case 'transcribing':
        return 'text-blue-600';
      case 'success':
        return 'text-green-600';
      case 'error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-4">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*,audio/*,.txt,text/plain"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center space-y-2"
        >
          <div className="text-4xl">📁</div>
          <div className="text-sm text-gray-600">
            {selectedFile ? (
              <span className="font-medium text-gray-900">{selectedFile.name}</span>
            ) : (
              <span>Click to select a file</span>
            )}
          </div>
          <div className="text-xs text-gray-500">
            Supports: Video (mp4, webm), Audio (mp3, wav, m4a, webm), Text (.txt)
          </div>
        </label>
      </div>

      {selectedFile && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">File size:</span>
            <span className="font-medium">
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Status:</span>
            <span className={`font-semibold ${getStatusColor()}`}>
              {getStatusText()}
            </span>
          </div>

          {(uploadStatus === 'uploading' || uploadStatus === 'transcribing') && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          )}

          {errorMessage && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-700">
              {errorMessage}
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={uploadStatus === 'uploading' || uploadStatus === 'transcribing'}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploadStatus === 'uploading' || uploadStatus === 'transcribing'
              ? 'Processing...'
              : 'Upload & Process'}
          </button>
        </div>
      )}

      {uploadStatus === 'success' && (
        <div className="bg-green-50 border border-green-200 rounded-md p-3 text-sm text-green-700">
          File processed successfully! The content has been added to your notes.
        </div>
      )}
    </div>
  );
}
