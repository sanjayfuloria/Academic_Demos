# Academic_Demos

## Automated Grading Assistant Demo

This demo implements an automated grading system that evaluates student short-answer responses using natural language processing techniques.

### Setup

1. Navigate to the demo directory:
```bash
cd demo1_grading_assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Demo

1. Run tests:
```bash
python -m unittest test_grading_assistant.py
```

2. Start the web interface:
```bash
streamlit run app.py
```

3. Open your browser and go to http://localhost:8501

### Usage

1. Enter a reference (correct) answer
2. Enter student answers (up to 10)
3. Click "Grade Answers" to see results

## SSL Troubleshooting

If you encounter SSL certificate issues while downloading the model, try these solutions:

1. Update your certificates:
   ```bash
   pip install --upgrade certifi
   ```

2. For macOS, run:
   ```bash
   /Applications/Python\ 3.x/Install\ Certificates.command
   ```

3. For Linux:
   ```bash
   sudo update-ca-certificates
   ```

4. If issues persist, the code will automatically try alternative approaches:
   - Using an alternative model
   - Temporarily disabling SSL verification (not recommended for production)