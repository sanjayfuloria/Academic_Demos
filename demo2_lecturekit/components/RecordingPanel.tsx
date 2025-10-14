'use client';

import { useState, useRef, useEffect } from 'react';

interface RecordingPanelProps {
  onRecordingComplete: (url: string) => void;
}

export default function RecordingPanel({ onRecordingComplete }: RecordingPanelProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [duration, setDuration] = useState(0);
  const [permissionState, setPermissionState] = useState<'granted' | 'denied' | 'prompt'>('prompt');
  const [fileSize, setFileSize] = useState(0);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [recordingType, setRecordingType] = useState<'video' | 'audio'>('video');
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const videoPreviewRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const requestPermissions = async () => {
    try {
      const constraints = recordingType === 'video'
        ? { video: true, audio: true }
        : { audio: true };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;
      setPermissionState('granted');

      if (recordingType === 'video' && videoPreviewRef.current) {
        videoPreviewRef.current.srcObject = stream;
      }

      return stream;
    } catch (error) {
      console.error('Permission denied:', error);
      setPermissionState('denied');
      return null;
    }
  };

  const startRecording = async () => {
    const stream = streamRef.current || await requestPermissions();
    if (!stream) return;

    chunksRef.current = [];
    const mimeType = recordingType === 'video' ? 'video/webm' : 'audio/webm';

    const mediaRecorder = new MediaRecorder(stream, { mimeType });

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
        setFileSize((prev) => prev + event.data.size);
      }
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: mimeType });
      const url = URL.createObjectURL(blob);
      setPreviewUrl(url);
      await uploadRecording(blob);
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start(1000);
    setIsRecording(true);

    timerRef.current = setInterval(() => {
      setDuration((prev) => prev + 1);
    }, 1000);
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.pause();
      setIsPaused(true);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const resumeRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'paused') {
      mediaRecorderRef.current.resume();
      setIsPaused(false);
      timerRef.current = setInterval(() => {
        setDuration((prev) => prev + 1);
      }, 1000);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  };

  const uploadRecording = async (blob: Blob) => {
    try {
      setUploadStatus('uploading');
      
      // For demo purposes, create a local URL
      const url = URL.createObjectURL(blob);
      setUploadStatus('success');
      onRecordingComplete(url);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-4 items-center">
        <label className="text-sm font-medium text-gray-700">Recording Type:</label>
        <div className="flex gap-2">
          <button
            onClick={() => setRecordingType('video')}
            disabled={isRecording}
            className={`px-4 py-2 rounded-md ${recordingType === 'video' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'} disabled:opacity-50`}
          >
            🎥 Video
          </button>
          <button
            onClick={() => setRecordingType('audio')}
            disabled={isRecording}
            className={`px-4 py-2 rounded-md ${recordingType === 'audio' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'} disabled:opacity-50`}
          >
            🎤 Audio
          </button>
        </div>
      </div>

      {recordingType === 'video' && (
        <div className="relative bg-black rounded-lg overflow-hidden" style={{ maxHeight: '400px' }}>
          <video ref={videoPreviewRef} autoPlay muted className="w-full h-auto" style={{ maxHeight: '400px' }} />
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-xs text-gray-600 mb-1">Duration</p>
          <p className="text-lg font-semibold text-gray-900">{formatDuration(duration)}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-xs text-gray-600 mb-1">File Size</p>
          <p className="text-lg font-semibold text-gray-900">{formatFileSize(fileSize)}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-xs text-gray-600 mb-1">Permission</p>
          <p className={`text-sm font-semibold ${permissionState === 'granted' ? 'text-green-600' : permissionState === 'denied' ? 'text-red-600' : 'text-yellow-600'}`}>
            {permissionState === 'granted' ? '✓ Granted' : permissionState === 'denied' ? '✗ Denied' : '⋯ Pending'}
          </p>
        </div>
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-xs text-gray-600 mb-1">Upload Status</p>
          <p className={`text-sm font-semibold ${uploadStatus === 'success' ? 'text-green-600' : uploadStatus === 'error' ? 'text-red-600' : uploadStatus === 'uploading' ? 'text-blue-600' : 'text-gray-600'}`}>
            {uploadStatus === 'success' ? '✓ Uploaded' : uploadStatus === 'error' ? '✗ Failed' : uploadStatus === 'uploading' ? '⋯ Uploading' : '◯ Idle'}
          </p>
        </div>
      </div>

      <div className="flex gap-2">
        {!isRecording ? (
          <button onClick={startRecording} className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-md transition-colors">
            ● Start Recording
          </button>
        ) : (
          <>
            {!isPaused ? (
              <button onClick={pauseRecording} className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-3 px-6 rounded-md transition-colors">
                ⏸ Pause
              </button>
            ) : (
              <button onClick={resumeRecording} className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-md transition-colors">
                ▶ Resume
              </button>
            )}
            <button onClick={stopRecording} className="flex-1 bg-gray-800 hover:bg-gray-900 text-white font-semibold py-3 px-6 rounded-md transition-colors">
              ⏹ Stop
            </button>
          </>
        )}
      </div>

      {previewUrl && (
        <div className="mt-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Preview</h3>
          {recordingType === 'video' ? (
            <video src={previewUrl} controls className="w-full rounded-md" style={{ maxHeight: '300px' }} />
          ) : (
            <audio src={previewUrl} controls className="w-full" />
          )}
        </div>
      )}
    </div>
  );
}
