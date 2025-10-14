import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { summary, count } = await request.json();

    if (!summary || !summary.trim()) {
      return NextResponse.json({ error: 'Summary is required' }, { status: 400 });
    }

    // Generate sample MCQs
    const mcqs = [];
    for (let i = 0; i < count; i++) {
      mcqs.push({
        q: `Question ${i + 1}: What is the main concept discussed in the lecture?`,
        options: [
          'The fundamental principles and their applications',
          'Only theoretical concepts',
          'Unrelated topics',
          'No specific focus',
        ],
        correctIndex: 0,
        rationale: 'The lecture emphasized understanding fundamental principles and their practical applications in real-world scenarios.',
      });
    }

    return NextResponse.json({ mcqs });
  } catch (error) {
    console.error('Error generating MCQs:', error);
    return NextResponse.json({ error: 'Failed to generate MCQs' }, { status: 500 });
  }
}
