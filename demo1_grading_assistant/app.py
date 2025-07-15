import streamlit as st
import pandas as pd
import plotly.express as px
from grading_assistant import GradingAssistant

def main():
    st.set_page_config(
        page_title="Assignment Feedback Generator", 
        page_icon="📝",
        layout="wide"
    )
    
    st.title("📝 Assignment Feedback Generator")
    st.markdown("*Intelligent automated grading with detailed feedback*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        assignment_type = st.selectbox(
            "Assignment Type",
            ["short_answer", "essay", "explanation", "analysis"],
            help="Select the type of assignment for optimized grading"
        )
        
        show_detailed_scores = st.checkbox(
            "Show Detailed Scores", 
            value=True,
            help="Display breakdown of individual criteria scores"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Grading Criteria")
        st.markdown("""
        - **Content Accuracy (40%)**: How well the answer matches expected content
        - **Completeness (30%)**: Coverage of key points and concepts  
        - **Clarity (20%)**: How clearly the ideas are expressed
        - **Structure (10%)**: Grammar, organization, and presentation
        """)
    
    # Initialize grading assistant
    grader = GradingAssistant()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Assignment Setup")
        
        # Input reference answer
        reference_answer = st.text_area(
            "Reference Answer / Model Response",
            placeholder="Enter the correct or model answer here...",
            height=150,
            help="This will be used as the benchmark for grading student responses"
        )
        
        # Input assignment context
        assignment_context = st.text_area(
            "Assignment Context (Optional)",
            placeholder="Provide context about the assignment, question, or topic...",
            height=100,
            help="Additional context can help improve grading accuracy"
        )
    
    with col2:
        st.header("🎓 Student Responses")
        
        # Input student answers
        num_students = st.number_input(
            "Number of student responses",
            min_value=1,
            max_value=10,
            value=3,
            help="Select how many student responses you want to grade"
        )
        
        student_answers = []
        for i in range(num_students):
            answer = st.text_area(
                f"Student {i+1} Response",
                placeholder=f"Enter student {i+1}'s response here...",
                height=100,
                key=f"student_{i}"
            )
            student_answers.append(answer)
    
    # Grading section
    st.markdown("---")
    
    if st.button("🔍 Grade Responses", type="primary", use_container_width=True):
        if reference_answer and all(answer.strip() for answer in student_answers):
            with st.spinner("Analyzing responses..."):
                results = grader.grade_multiple_responses(
                    student_answers,
                    reference_answer,
                    assignment_type
                )
            
            st.header("📊 Grading Results")
            
            # Create summary statistics
            grades = [result[0] for result in results]
            avg_grade = sum(grades) / len(grades)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Grade", f"{avg_grade:.1f}/5")
            with col2:
                st.metric("Highest Grade", f"{max(grades)}/5")
            with col3:
                st.metric("Lowest Grade", f"{min(grades)}/5")
            with col4:
                st.metric("Total Responses", len(grades))
            
            # Grade distribution chart
            if len(grades) > 1:
                grade_counts = pd.Series(grades).value_counts().sort_index()
                fig = px.bar(
                    x=grade_counts.index, 
                    y=grade_counts.values,
                    title="Grade Distribution",
                    labels={'x': 'Grade', 'y': 'Number of Students'},
                    color=grade_counts.values,
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed results for each student
            st.subheader("📝 Individual Student Results")
            
            for i, (grade, feedback, scores) in enumerate(results):
                with st.expander(f"Student {i+1} - Grade: {grade}/5", expanded=True):
                    
                    # Display the student's response
                    st.markdown("**Student Response:**")
                    st.info(student_answers[i])
                    
                    # Display grade and feedback
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Grade display with color coding
                        if grade >= 4:
                            st.success(f"**Grade: {grade}/5**")
                        elif grade >= 3:
                            st.warning(f"**Grade: {grade}/5**")
                        else:
                            st.error(f"**Grade: {grade}/5**")
                    
                    with col2:
                        st.markdown("**Feedback:**")
                        st.markdown(feedback)
                    
                    # Show detailed scores if enabled
                    if show_detailed_scores:
                        st.markdown("**Detailed Criteria Scores:**")
                        score_data = {
                            'Criteria': ['Content Accuracy', 'Completeness', 'Clarity', 'Structure'],
                            'Score': [
                                scores['content_accuracy'],
                                scores['completeness'], 
                                scores['clarity'],
                                scores['structure']
                            ],
                            'Weight': ['40%', '30%', '20%', '10%']
                        }
                        
                        score_df = pd.DataFrame(score_data)
                        score_df['Score (%)'] = (score_df['Score'] * 100).round(1)
                        
                        # Display as a bar chart
                        fig = px.bar(
                            score_df, 
                            x='Criteria', 
                            y='Score',
                            title=f"Student {i+1} - Criteria Breakdown",
                            color='Score',
                            color_continuous_scale='RdYlGn',
                            range_y=[0, 1]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display as table
                        st.dataframe(score_df[['Criteria', 'Score (%)', 'Weight']], hide_index=True)
        
        else:
            st.error("⚠️ Please provide a reference answer and ensure all student responses are filled in.")

    # Help section
    with st.expander("❓ How to Use This Tool"):
        st.markdown("""
        ### Getting Started:
        1. **Enter Reference Answer**: Provide the correct or model answer for the assignment
        2. **Add Student Responses**: Input the student responses you want to grade
        3. **Select Assignment Type**: Choose the appropriate assignment type for optimized grading
        4. **Click Grade Responses**: The system will analyze and grade each response
        
        ### Understanding the Results:
        - **Grades**: Scored on a 0-5 scale (5 being the highest)
        - **Feedback**: Detailed constructive feedback for improvement
        - **Criteria Scores**: Breakdown showing performance in different areas
        
        ### Tips for Best Results:
        - Provide clear, comprehensive reference answers
        - Ensure student responses are complete
        - Use assignment context for better accuracy
        """)

if __name__ == "__main__":
    main()