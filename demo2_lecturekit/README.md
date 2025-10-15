# 📚 LectureKit

A production-grade, teacher-facing web application for lecture recording, note-taking, AI-powered summarization, MCQ generation, and student email distribution.

![LectureKit Dashboard](https://via.placeholder.com/800x400?text=LectureKit+Dashboard)

## ✨ Features

### 🎥 Session Recording
- Browser-based audio and video recording using MediaRecorder API
- Real-time duration tracking and file size monitoring
- Permission state management
- Preview thumbnails for recorded content
- Firebase Storage integration with signed upload URLs

### 📁 File Upload & Processing
- Upload video files (mp4, webm)
- Upload audio files (mp3, wav, m4a, webm)
- Upload text files (.txt)
- Automatic transcription of audio and video files using OpenAI Whisper API
- File size validation (max 25MB for transcription)
- Real-time upload status tracking
- Automatic content addition to lecture notes

### 📝 Lecture Notes
- Rich-text note editor with Markdown support
- Auto-save functionality (saves every 1 second)
- Timestamp insertion linked to recording position
- Real-time character count
- Support for typed text, uploaded files, and transcribed content

### ✨ AI-Powered Summarization
- OpenAI GPT-4 integration for lecture summarization
- Streaming responses for real-time feedback
- Persistent summary storage
- Token usage tracking
- Works with typed notes, uploaded files, and transcribed recordings
- Fallback to mock summaries when API key not configured

### 🎯 MCQ Generation
- Automated multiple-choice question generation from summaries using OpenAI
- Configurable question count (1-20) and difficulty levels (easy/medium/hard/mixed)
- Zod validation for strict JSON structure
- Editable table UI with add/edit/delete functionality
- Four options per question with exactly one correct answer
- Rationale for each correct answer
- Fallback to mock MCQs when API key not configured

### 📧 Email Distribution
- Send summaries to students via email
- Send MCQs to students via email
- Support for multiple recipients (comma-separated)
- HTML email formatting
- Optional CSV attachment support
- Send status tracking
- Gmail OAuth2 integration ready (simulated in demo mode)

## 🛠️ Tech Stack

- **Framework:** Next.js 14+ with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Authentication & Database:** Firebase Auth, Firestore
- **Storage:** Firebase Storage
- **LLM:** OpenAI API with streaming
- **Email:** Nodemailer with Gmail OAuth2
- **Validation:** Zod
- **UI Components:** Radix UI
- **Testing:** Playwright
- **Code Quality:** ESLint, Prettier, Husky

## 🚀 Quick Start

### Prerequisites

- Node.js 20+ and npm
- Firebase project with Auth, Firestore, and Storage enabled
- OpenAI API key
- Google Cloud project with Gmail API enabled

### Installation

1. **Clone the repository:**
```bash
cd demo2_lecturekit
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment variables:**

Copy `.env.example` to `.env.local` and fill in your credentials:

```bash
cp .env.example .env.local
```

Required environment variables:
- Firebase Client SDK credentials
- Firebase Admin SDK credentials
- OpenAI API key
- Google OAuth credentials
- Gmail OAuth refresh token

4. **Run the development server:**
```bash
npm run dev
```

5. **Open your browser:**

Navigate to [http://localhost:3000](http://localhost:3000)

## 📋 How to Use

### Recording a Lecture

1. Go to the Dashboard
2. Select recording type (video or audio)
3. Grant browser permissions for camera/microphone
4. Click "Start Recording"
5. Use Pause/Resume as needed
6. Click "Stop" when finished
7. Recording automatically uploads to Firebase Storage

### Uploading Files

1. Go to the "Upload Files" section
2. Click on the upload area to select a file
3. Choose a video, audio, or text file
4. Click "Upload & Process"
5. For audio/video files: The file will be automatically transcribed using OpenAI Whisper
6. For text files: The content will be directly added to your notes
7. Transcribed or uploaded content appears in the lecture notes section

### Taking Notes

1. Type in the notes editor (auto-save enabled)
2. Click "Insert Timestamp" to add time markers
3. Notes are saved automatically every second
4. Upload files or transcribe recordings to add content automatically

### Generating a Summary

1. Complete your lecture notes (by typing, recording, or uploading files)
2. Click "Summarize Lecture"
3. Watch as the AI streams the summary in real-time
4. Summary is automatically persisted
5. Note: Requires OpenAI API key; uses mock summary if not configured

### Creating MCQs

1. Generate a summary first
2. Select number of questions (1-20) and difficulty level
3. Click "Generate MCQs"
4. Edit questions, options, and rationales as needed
5. Add or delete questions manually
6. Note: Requires OpenAI API key; uses mock MCQs if not configured

### Sending to Students

**Sending Summaries:**
1. Generate a summary first
2. Scroll to "Email Summary" section
3. Enter student email addresses (comma-separated)
4. Click "Send Summary"

**Sending MCQs:**
1. Generate MCQs first
2. Scroll to "Email Distribution" section in MCQs panel
3. Enter student email addresses (comma-separated)
4. Click "Send to Students"

Note: Email sending is simulated in demo mode. Configure Gmail OAuth for production use.

## 🧪 Testing

Run the Playwright test suite:

```bash
npm run test
```

Run tests in UI mode:

```bash
npx playwright test --ui
```

## 📊 Project Structure

```
demo2_lecturekit/
├── app/
│   ├── api/              # API routes
│   │   ├── summary/      # Summary generation with OpenAI
│   │   ├── mcqs/         # MCQ generation with OpenAI
│   │   ├── email/        # Email sending (summaries & MCQs)
│   │   └── transcribe/   # Audio/video transcription with Whisper
│   ├── dashboard/        # Dashboard page
│   └── page.tsx          # Homepage
├── components/           # React components
│   ├── RecordingPanel.tsx
│   ├── FileUploadPanel.tsx   # NEW: File upload & transcription
│   ├── NotesEditor.tsx
│   ├── SummaryPanel.tsx      # Enhanced with email feature
│   └── MCQPanel.tsx
├── lib/                  # Utilities and configurations
│   ├── types.ts          # TypeScript interfaces
│   ├── openai.ts         # OpenAI integration (Whisper, GPT-4, etc.)
│   ├── firebaseClient.ts # Firebase client SDK (optional)
│   ├── firebaseAdmin.ts  # Firebase Admin SDK (optional)
│   └── gmail.ts          # Gmail OAuth utilities (optional)
└── tests/                # Playwright tests
```

## 🔧 Configuration

### Firebase Setup

1. Create a Firebase project
2. Enable Authentication, Firestore, and Storage
3. Download service account credentials
4. Add credentials to `.env.local`

### OpenAI Setup

1. Get API key from OpenAI
2. Add to `.env.local` as `OPENAI_API_KEY`

### Gmail OAuth Setup

1. Create OAuth 2.0 credentials in Google Cloud Console
2. Enable Gmail API
3. Generate refresh token
4. Add credentials to `.env.local`

## 📈 Data Model

TypeScript interfaces defined in `lib/types.ts`:

- **UserProfile:** User information and consent flags
- **Course:** Course metadata
- **SessionRec:** Recording session details
- **Summary:** AI-generated summaries
- **MCQ:** Multiple-choice questions
- **Assessment:** Collection of MCQs
- **Mailout:** Email distribution tracking
- **LectureNotes:** Notes with timestamps

## 🤝 Contributing

This is a demonstration project showcasing production-grade educational technology. Feel free to extend with:

- Additional LLM providers
- Enhanced rich-text editing
- Real-time collaboration
- Student-facing quiz interface
- Analytics dashboard
- LMS integration

## 📄 License

Part of the Academic_Demos collection - educational and demonstration purposes.

## 🔐 Security Notes

- Never commit `.env.local` to version control
- Use environment variables for all sensitive data
- Implement proper authentication before production use
- Enable Firebase security rules for Firestore and Storage
- Rotate OAuth tokens regularly
