import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { recipients, mcqs, subject } = await request.json();

    if (!recipients || recipients.length === 0) {
      return NextResponse.json({ error: 'Recipients are required' }, { status: 400 });
    }

    if (!mcqs || mcqs.length === 0) {
      return NextResponse.json({ error: 'MCQs are required' }, { status: 400 });
    }

    // Simulate email sending
    console.log('Sending email to:', recipients);
    console.log('Subject:', subject);
    console.log('MCQ Count:', mcqs.length);

    // In production, this would use the Gmail API
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
