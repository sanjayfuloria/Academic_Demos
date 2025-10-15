import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { recipients, mcqs, summary, subject } = await request.json();

    if (!recipients || recipients.length === 0) {
      return NextResponse.json({ error: 'Recipients are required' }, { status: 400 });
    }

    // Support sending either MCQs or summary or both
    if (!mcqs && !summary) {
      return NextResponse.json({ error: 'Either MCQs or summary is required' }, { status: 400 });
    }

    // Simulate email sending
    console.log('Sending email to:', recipients);
    console.log('Subject:', subject);
    if (mcqs) console.log('MCQ Count:', mcqs.length);
    if (summary) console.log('Summary Length:', summary.length);

    // In production, this would use the Gmail API or another email service
    await new Promise(resolve => setTimeout(resolve, 1000));

    return NextResponse.json({
      success: true,
      message: `Email sent to ${recipients.length} recipient(s)`,
      mailoutId: `mailout-${Date.now()}`,
    });
  } catch (error) {
    console.error('Error sending email:', error);
    return NextResponse.json({ error: 'Failed to send email' }, { status: 500 });
  }
}
