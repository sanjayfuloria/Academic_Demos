import { NextRequest, NextResponse } from 'next/server';
import { transcribeAudio } from '@/lib/openai';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'File is required' }, { status: 400 });
    }

    // Validate file type
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/webm', 'video/webm', 'video/mp4', 'audio/mp3', 'audio/m4a'];
    if (!validTypes.some(type => file.type.includes(type.split('/')[1]))) {
      return NextResponse.json(
        { error: 'Invalid file type. Supported: audio (mp3, wav, webm, m4a) and video (webm, mp4)' },
        { status: 400 }
      );
    }

    // Check file size (max 25MB for Whisper API)
    const maxSize = 25 * 1024 * 1024;
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size exceeds 25MB limit' },
        { status: 400 }
      );
    }

    // Transcribe the audio/video
    const transcription = await transcribeAudio(file);

    return NextResponse.json({
      success: true,
      transcription,
    });
  } catch (error) {
    console.error('Transcription error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to transcribe file' },
      { status: 500 }
    );
  }
}
