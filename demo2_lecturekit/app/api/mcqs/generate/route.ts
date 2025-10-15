import { NextRequest, NextResponse } from 'next/server';
import { generateMCQs } from '@/lib/openai';

export async function POST(request: NextRequest) {
  try {
    const { summary, count = 5, difficulty = 'medium' } = await request.json();

    if (!summary || !summary.trim()) {
      return NextResponse.json({ error: 'Summary is required' }, { status: 400 });
    }

    // Check if OpenAI API key is configured
    if (!process.env.OPENAI_API_KEY) {
      // Fallback to mock MCQs if API key not configured
      const mcqs = [];
      for (let i = 0; i < count; i++) {
        mcqs.push({
          id: `mcq-${Date.now()}-${i}`,
          question: `Question ${i + 1}: What is the main concept discussed in the lecture?`,
          options: [
            'The fundamental principles and their applications',
            'Only theoretical concepts',
            'Unrelated topics',
            'No specific focus',
          ],
          correctAnswer: 0,
          rationale: 'The lecture emphasized understanding fundamental principles and their practical applications in real-world scenarios.',
          difficulty: difficulty,
        });
      }
      return NextResponse.json({ mcqs });
    }

    // Use real OpenAI API for MCQ generation
    const mcqs = await generateMCQs(summary, count, difficulty);

    return NextResponse.json({ mcqs });
  } catch (error) {
    console.error('Error generating MCQs:', error);
    return NextResponse.json({ error: 'Failed to generate MCQs' }, { status: 500 });
  }
}
