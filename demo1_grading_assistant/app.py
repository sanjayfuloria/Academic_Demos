import streamlit as st
from grading_assistant import GradingAssistant

def main():
    st.title("Automated Grading Assistant")
    
    # Initialize grading assistant
    grader = GradingAssistant()
    
    # Input reference answer
    reference_answer = st.text_area(
        "Reference Answer",
        "Enter the correct answer here..."
    )
    
    # Input student answers
    student_answers = []
    num_students = st.number_input(
        "Number of student answers to grade",
        min_value=1,
        max_value=10,
        value=3
    )
    
    for i in range(num_students):
        answer = st.text_area(
            f"Student Answer {i+1}",
            f"Enter student {i+1}'s answer here..."
        )
        student_answers.append(answer)
    
    if st.button("Grade Answers"):
        if reference_answer and all(student_answers):
            results = grader.grade_multiple_responses(
                student_answers,
                reference_answer
            )
            
            st.header("Grading Results")
            for i, (grade, feedback) in enumerate(results):
                st.subheader(f"Student {i+1}")
                st.write(f"Grade: {grade}/5")
                st.write(f"Feedback: {feedback}")
        else:
            st.error("Please fill in all answers before grading.")

if __name__ == "__main__":
    main()