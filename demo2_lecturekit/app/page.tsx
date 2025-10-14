import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            📚 LectureKit
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Production-grade lecture recording and management platform for educators
          </p>
        </div>

        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-3xl font-semibold mb-6 text-gray-800">Features</h2>
          
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold mb-3 text-blue-600">🎥 Session Recording</h3>
              <p className="text-gray-600">
                Record audio and video lectures in the browser with real-time duration tracking, 
                permission management, and automatic Firebase Storage uploads.
              </p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold mb-3 text-green-600">📝 Lecture Notes</h3>
              <p className="text-gray-600">
                Rich-text notes with autosave functionality and timestamp insertion 
                linked to recording positions for seamless review.
              </p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold mb-3 text-purple-600">✨ AI Summarization</h3>
              <p className="text-gray-600">
                Generate comprehensive lecture summaries using OpenAI with 
                real-time streaming to see results as they&apos;re created.
              </p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold mb-3 text-orange-600">🎯 MCQ Generation</h3>
              <p className="text-gray-600">
                Automatically create multiple-choice questions with validated JSON structure, 
                complete with rationales and an editable table interface.
              </p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow md:col-span-2">
              <h3 className="text-xl font-semibold mb-3 text-red-600">📧 Email Distribution</h3>
              <p className="text-gray-600">
                Send MCQs to students via Gmail OAuth2 with HTML formatting and optional CSV attachments, 
                with comprehensive send status tracking.
              </p>
            </div>
          </div>

          <div className="text-center">
            <Link
              href="/dashboard"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors shadow-md hover:shadow-lg"
            >
              Get Started →
            </Link>
          </div>
        </div>

        <div className="mt-12 text-center text-gray-600">
          <p className="mb-2">Built with Next.js 14, TypeScript, Tailwind CSS, Firebase, and OpenAI</p>
          <p className="text-sm">Part of the Academic_Demos collection</p>
        </div>
      </main>
    </div>
  );
}
