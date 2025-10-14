# Academic_Demos

A collection of production-grade educational technology demonstrations showcasing AI-powered tools for educators.

## 🚀 Demos

### 📚 LectureKit - Lecture Recording & Management Platform

A modern, production-grade web application for teachers to record lectures, take notes, generate AI summaries, create MCQs, and distribute content to students.

![LectureKit Homepage](https://github.com/user-attachments/assets/c50a0166-e314-4928-ad98-93fd09007d40)
![LectureKit Dashboard](https://github.com/user-attachments/assets/d4d4fedf-3be2-48ec-93f5-ffe15ef1e3e3)
![LectureKit Features](https://github.com/user-attachments/assets/beff97e6-35d4-406a-9a04-ab6e31607f8b)

**Tech Stack:** Next.js 14+, TypeScript, Tailwind CSS, Firebase, OpenAI, Gmail OAuth2

**Key Features:**
- 🎥 Browser-based audio/video recording with MediaRecorder API
- 📝 Rich-text notes with autosave and timestamp linking
- ✨ AI-powered lecture summarization with streaming
- 🎯 Automated MCQ generation with Zod validation
- 📧 Email distribution via Gmail OAuth2

[**→ View LectureKit Documentation**](demo2_lecturekit/README.md)

---

## 📝 Assignment Feedback Generator

An intelligent automated grading system that evaluates student responses using advanced natural language processing and provides comprehensive feedback across multiple criteria.

![Assignment Feedback Generator Interface](https://github.com/user-attachments/assets/c02c1d3e-55bb-4844-a851-723732e06dce)

### ✨ Features

- **Multi-Criteria Grading**: Evaluates responses across four key dimensions:
  - Content Accuracy (40%) - How well the answer matches expected content
  - Completeness (30%) - Coverage of key points and concepts  
  - Clarity (20%) - How clearly ideas are expressed
  - Structure (10%) - Grammar, organization, and presentation

- **Professional Dashboard**: Clean, intuitive Streamlit interface with:
  - Real-time grade distribution visualization
  - Detailed individual student breakdowns
  - Interactive charts and metrics
  - Configurable assignment types

- **Comprehensive Feedback**: Provides constructive feedback with:
  - Overall grades (0-5 scale)
  - Detailed criteria scores
  - Specific improvement suggestions
  - Visual progress indicators

- **Multiple Assignment Types**: Optimized for different assessment formats:
  - Short answers
  - Essays  
  - Explanations
  - Analysis responses

![Grading Results Dashboard](https://github.com/user-attachments/assets/92f9fecf-15de-40ea-9aa6-b7822a258b16)

### 🚀 Quick Start

1. **Navigate to the demo directory:**
```bash
cd demo1_grading_assistant
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run tests:**
```bash
python -m unittest test_grading_assistant.py
```

5. **Start the application:**
```bash
streamlit run app.py
```

6. **Open your browser:** Go to http://localhost:8501

### 📋 How to Use

1. **Setup**: Enter a reference answer and select assignment type
2. **Input**: Add student responses (up to 10 supported)
3. **Grade**: Click "Grade Responses" to analyze submissions
4. **Review**: Examine detailed feedback and scores for each student

### 🛠️ Technical Implementation

- **Backend**: Python with semantic similarity analysis
- **NLP Processing**: Sentence transformers with fallback algorithms
- **Frontend**: Streamlit with Plotly visualizations
- **Testing**: Comprehensive unit test coverage
- **Architecture**: Modular design for easy extension

### 📊 Grading Algorithm

The system uses a weighted scoring approach:

1. **Content Accuracy**: Semantic similarity to reference answer
2. **Completeness**: Coverage of key concepts and terms
3. **Clarity**: Sentence structure and readability analysis  
4. **Structure**: Grammar, punctuation, and organization

### 🔧 Configuration

- Assignment types can be customized for different subjects
- Grading criteria weights are configurable
- Supports both transformer-based and fallback similarity methods
- Detailed scoring can be toggled on/off

### 🧪 Testing

Run the comprehensive test suite:
```bash
python -m unittest test_grading_assistant.py -v
```

Tests cover:
- Similarity calculations
- Individual criteria assessment
- Multi-response grading
- Feedback generation
- Edge cases and error handling

### 📈 Example Results

The system provides rich analytics including:
- Average class performance (e.g., 3.3/5)
- Grade distribution charts
- Individual student breakdowns
- Criteria-specific scoring
- Actionable improvement feedback

### 🤝 Contributing

This demo showcases automated educational assessment capabilities. Feel free to extend with:
- Additional assignment types
- Custom grading rubrics
- Integration with LMS systems
- Advanced NLP models

### 📄 License

Part of the Academic_Demos collection - educational and demonstration purposes.