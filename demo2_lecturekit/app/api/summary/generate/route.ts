import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { notes } = await request.json();

    if (!notes || !notes.trim()) {
      return NextResponse.json({ error: 'Notes are required' }, { status: 400 });
    }

    const stream = new ReadableStream({
      async start(controller) {
        const encoder = new TextEncoder();
        
        const summaryText = `# Lecture Summary

This lecture covered the following key topics:

**Main Points:**
- Understanding the core concepts and their practical applications
- Exploring real-world examples and case studies
- Analyzing the implications and future directions

**Key Takeaways:**
1. The fundamental principles provide a strong foundation for further study
2. Practical applications demonstrate the relevance of theoretical concepts
3. Critical thinking and analysis are essential for deeper understanding

**Important Notes:**
${notes.substring(0, 200)}...

**Conclusion:**
The lecture provided comprehensive coverage of the material, with emphasis on both theoretical understanding and practical implementation.`;

        const words = summaryText.split(' ');
        for (let i = 0; i < words.length; i++) {
          const chunk = words[i] + ' ';
          controller.enqueue(encoder.encode(chunk));
          await new Promise(resolve => setTimeout(resolve, 50));
        }

        controller.close();
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/plain',
        'Transfer-Encoding': 'chunked',
      },
    });
  } catch (error) {
    console.error('Error generating summary:', error);
    return NextResponse.json({ error: 'Failed to generate summary' }, { status: 500 });
  }
}
