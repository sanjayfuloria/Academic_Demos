import streamlit as st
import os
from grading_assistant import GradingAssistant

def main():
    st.title("Automated Grading Assistant")
    
    # Configuration sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Username input
        username = st.text_input("Username", value="sanjayfuloria")
        
        # Offline mode toggle
        offline_mode = st.checkbox("Offline Mode", value=False, help="Use offline mode with local models only")
        
        # SSL settings
        with st.expander("SSL Settings"):
            verify_ssl = st.checkbox("Verify SSL Certificates", value=False)
            if verify_ssl:
                os.environ["ACADEMIC_DEMOS_VERIFY_SSL"] = "true"
            else:
                os.environ["ACADEMIC_DEMOS_VERIFY_SSL"] = "false"
    
    # Initialize grading assistant with error handling
    try:
        if 'grader' not in st.session_state or st.session_state.get('username') != username:
            with st.spinner("Initializing grading system..."):
                st.session_state.grader = GradingAssistant(username=username, offline_mode=offline_mode)
                st.session_state.username = username
            
            # Show model information
            model_info = st.session_state.grader.get_model_info()
            with st.expander("Model Information"):
                for key, value in model_info.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                
                if model_info["model_type"] == "dummy":
                    st.warning("⚠️ Using offline dummy model. Accuracy may be reduced.")
                else:
                    st.success("✅ Using full sentence transformer model.")
        
        grader = st.session_state.grader
        
    except Exception as e:
        st.error(f"Failed to initialize grading system: {str(e)}")
        st.error("Please check your internet connection, SSL settings, or try offline mode.")
        
        # Show troubleshooting tips
        with st.expander("Troubleshooting Tips"):
            st.write("1. Try enabling 'Offline Mode' in the sidebar")
            st.write("2. Check if SSL certificate verification is causing issues")
            st.write("3. Ensure you have sufficient disk space for model caching")
            st.write("4. Check your internet connection if downloading models")
        
        return
    
    # Input reference answer
    reference_answer = st.text_area(
        "Reference Answer",
        "Enter the correct answer here...",
        help="This is the model answer that student responses will be compared against."
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
            f"Enter student {i+1}'s answer here...",
            key=f"student_answer_{i}"
        )
        student_answers.append(answer)
    
    # Grade answers button
    if st.button("Grade Answers", type="primary"):
        if not reference_answer.strip():
            st.error("Please provide a reference answer.")
            return
            
        if not any(answer.strip() for answer in student_answers):
            st.error("Please provide at least one student answer.")
            return
        
        # Filter out empty answers
        valid_answers = [(i, answer) for i, answer in enumerate(student_answers) if answer.strip()]
        
        if not valid_answers:
            st.error("No valid student answers found.")
            return
        
        # Grade the answers
        with st.spinner("Grading answers..."):
            try:
                results = grader.grade_multiple_responses(
                    [answer for _, answer in valid_answers],
                    reference_answer
                )
                
                # Display results
                st.header("Grading Results")
                
                # Summary statistics
                grades = [grade for grade, _ in results]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Grade", f"{sum(grades)/len(grades):.1f}/5")
                with col2:
                    st.metric("Highest Grade", f"{max(grades)}/5")
                with col3:
                    st.metric("Lowest Grade", f"{min(grades)}/5")
                
                # Individual results
                for (student_idx, _), (grade, feedback) in zip(valid_answers, results):
                    with st.container():
                        st.subheader(f"Student {student_idx + 1}")
                        
                        # Grade with color coding
                        if grade >= 4:
                            st.success(f"**Grade: {grade}/5**")
                        elif grade >= 3:
                            st.info(f"**Grade: {grade}/5**")
                        elif grade >= 2:
                            st.warning(f"**Grade: {grade}/5**")
                        else:
                            st.error(f"**Grade: {grade}/5**")
                        
                        st.write(f"**Feedback:** {feedback}")
                        st.divider()
                        
            except Exception as e:
                st.error(f"Error during grading: {str(e)}")
                st.error("Please try again or check the application logs.")

if __name__ == "__main__":
    main()