# LectureKit Setup Guide

This guide will help you set up LectureKit with all the new features including file upload, transcription, and AI-powered summarization.

## Prerequisites

1. **Node.js 20+** - Install from [nodejs.org](https://nodejs.org/)
2. **OpenAI API Key** - Get one from [platform.openai.com](https://platform.openai.com/)
3. **Git** - For cloning the repository

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd demo2_lecturekit
npm install
```

### 2. Configure Environment Variables

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

**Note**: The app works without the API key, but will use mock data instead of real AI features.

### 3. Start Development Server

```bash
npm run dev
```

Visit [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

## Features Overview

### 🎥 Recording
- Click "Start Recording" to record audio or video
- Browser will ask for permissions
- Recording data stays in browser (local preview)

### 📁 File Upload & Transcription
- Upload video, audio, or text files
- Audio/video files are automatically transcribed using OpenAI Whisper
- Transcribed content appears in lecture notes
- **Supported formats**:
  - Video: mp4, webm
  - Audio: mp3, wav, m4a, webm
  - Text: .txt
- **File size limit**: 25MB (Whisper API limit)

### 📝 Notes
- Type directly in the editor
- Auto-saves every second
- Content from uploads/recordings automatically added

### ✨ AI Summary
- Click "Summarize Lecture" to generate AI summary
- Uses OpenAI GPT-4 for real summaries (requires API key)
- Falls back to mock summary if no API key
- Streaming response shows text as it's generated

### 🎯 MCQ Generation
- Click "Generate MCQs" after creating a summary
- Choose number of questions (1-20) and difficulty
- Uses OpenAI GPT-4 for real questions (requires API key)
- Falls back to mock MCQs if no API key
- Edit questions, options, and answers as needed

### 📧 Email Distribution
- Enter comma-separated email addresses
- Send summaries or MCQs to students
- Currently simulated (console logs)
- Ready for Gmail OAuth integration in production

## Testing the Features

### Test 1: Upload a Text File
1. Create a test file with lecture content
2. Click on the upload area
3. Select your text file
4. Click "Upload & Process"
5. Content appears in notes immediately

### Test 2: Transcribe an Audio File
1. Record a short audio message on your phone
2. Transfer to your computer
3. Upload via the dashboard
4. Wait for transcription (requires OpenAI API key)
5. Transcribed text appears in notes

### Test 3: Generate Summary
1. Type or upload some lecture content
2. Click "Summarize Lecture"
3. Watch the AI-generated summary stream in
4. Scroll down to see email options

### Test 4: Create MCQs
1. Generate a summary first
2. Choose 5 questions, Mixed difficulty
3. Click "Generate MCQs"
4. Edit any questions you want to change
5. Test email sending with test addresses

## Using with OpenAI API

### Getting Your API Key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and paste into `.env.local`

### API Costs

- **Whisper (transcription)**: ~$0.006 per minute of audio
- **GPT-4o-mini (summaries/MCQs)**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Free tier**: $5 credit for new accounts

### Example Usage Costs

- 10-minute lecture transcription: ~$0.06
- Summary generation: ~$0.01
- 10 MCQs generation: ~$0.02
- **Total for typical lecture**: ~$0.09

## Deployment to Vercel

### 1. Prepare for Deployment

```bash
npm run build
```

Ensure no errors appear.

### 2. Deploy to Vercel

Option A: Using Vercel CLI
```bash
npm install -g vercel
vercel
```

Option B: Using GitHub Integration
1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy automatically on push

### 3. Configure Environment Variables

In Vercel dashboard, add:
- `OPENAI_API_KEY` - Your OpenAI API key

## Troubleshooting

### "OpenAI API key not configured" error
- Make sure `.env.local` exists and has `OPENAI_API_KEY=sk-...`
- Restart the development server after adding the key

### File upload fails
- Check file size (must be under 25MB)
- Verify file format is supported
- Check browser console for specific error

### Transcription taking long time
- Large files take longer to process
- Whisper API typically processes 1 minute of audio in 2-3 seconds
- Check network connection

### Summary generation is slow
- Streaming responses can take 10-30 seconds
- Depends on content length and OpenAI API load
- Mock summary is instant (when no API key)

### Email not sending
- Email is currently simulated (check browser console)
- For production, implement Gmail OAuth integration
- See `app/api/email/send/route.ts` for implementation

## Free Tools & Services

As requested in the problem statement, here are the free tools used:

1. **Vercel** - Free hosting for Next.js apps
2. **OpenAI Free Tier** - $5 credit for new accounts
3. **Browser APIs** - Free MediaRecorder, FileReader APIs
4. **Node.js/npm** - Free and open-source
5. **Next.js** - Free and open-source framework
6. **Tailwind CSS** - Free utility CSS framework

## Production Checklist

Before deploying to production:

- [ ] Set up proper OpenAI API key with billing
- [ ] Configure Gmail OAuth for email sending
- [ ] Set up Firebase for file storage (optional)
- [ ] Enable rate limiting on API routes
- [ ] Add user authentication
- [ ] Configure CORS policies
- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Add usage analytics
- [ ] Test with real lecture content
- [ ] Create backup strategy for user data

## Support

For issues or questions:
- Check the README.md for feature documentation
- Review IMPLEMENTATION.md for technical details
- Check browser console for error messages
- Verify API keys are correctly configured

## License

Part of the Academic_Demos collection - educational and demonstration purposes.
