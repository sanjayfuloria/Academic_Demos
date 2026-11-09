"""
Trainer Simulation Game - Streamlit Application

An interactive training simulation game for educators to practice
classroom management and student engagement strategies.
"""

import streamlit as st
from trainer_simulation import (
    TrainerSimulation, 
    StudentPersonality, 
    ActionType
)


def get_personality_emoji(personality: str) -> str:
    """Get emoji for personality type"""
    emojis = {
        "engaged": "🌟",
        "quiet": "🤫",
        "struggling": "😓",
        "disruptive": "🎭",
        "overachiever": "🚀"
    }
    return emojis.get(personality, "👤")


def get_engagement_color(engagement: float) -> str:
    """Get color based on engagement level"""
    if engagement >= 0.7:
        return "🟢"
    elif engagement >= 0.4:
        return "🟡"
    else:
        return "🔴"


def display_student_card(student: dict, col):
    """Display a student card with their stats"""
    with col:
        emoji = get_personality_emoji(student["personality"])
        eng_color = get_engagement_color(student["engagement"])
        
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            background-color: #f9f9f9;
        ">
            <h4 style="margin: 0;">{emoji} {student["name"]}</h4>
            <p style="font-size: 0.8em; color: #666; margin: 2px 0;">
                {student["personality"].title()}
            </p>
            <p style="margin: 5px 0;">
                {eng_color} Engagement: {student["engagement"]:.0%}
            </p>
            <p style="margin: 5px 0;">
                📚 Understanding: {student["understanding"]:.0%}
            </p>
            <p style="margin: 5px 0;">
                ⚡ Energy: {student["energy"]:.0%}
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Trainer Simulation Game",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Trainer Simulation Game")
    st.markdown("*Practice your teaching skills in realistic classroom scenarios*")
    
    # Initialize session state
    if "game" not in st.session_state:
        st.session_state.game = None
        st.session_state.game_started = False
        st.session_state.current_scenario = None
        st.session_state.last_result = None
        st.session_state.game_over = False
    
    # Sidebar for game setup
    with st.sidebar:
        st.header("⚙️ Game Settings")
        
        if not st.session_state.game_started:
            num_students = st.slider(
                "Number of Students",
                min_value=4,
                max_value=12,
                value=8,
                help="Choose how many students will be in your virtual classroom"
            )
            
            difficulty = st.selectbox(
                "Difficulty",
                ["easy", "normal", "hard"],
                index=1,
                help="Easy: More engaged students. Hard: More challenging behaviors."
            )
            
            if st.button("🎮 Start New Game", type="primary", use_container_width=True):
                st.session_state.game = TrainerSimulation(
                    num_students=num_students,
                    difficulty=difficulty
                )
                st.session_state.game_started = True
                st.session_state.current_scenario = None
                st.session_state.last_result = None
                st.session_state.game_over = False
                st.rerun()
        
        else:
            # Show game stats
            if st.session_state.game:
                status = st.session_state.game.get_class_status()
                
                st.markdown("### 📊 Session Stats")
                st.metric("Time Elapsed", f"{status['session_time']} min")
                st.metric("Time Remaining", f"{status['time_remaining']} min")
                st.metric("Score", status['total_score'])
                st.metric("Your Energy", f"{status['trainer_energy']:.0%}")
                
                st.markdown("---")
                st.markdown("### 📈 Class Averages")
                st.progress(status['averages']['engagement'], text=f"Engagement: {status['averages']['engagement']:.0%}")
                st.progress(status['averages']['understanding'], text=f"Understanding: {status['averages']['understanding']:.0%}")
                st.progress(status['averages']['energy'], text=f"Energy: {status['averages']['energy']:.0%}")
            
            st.markdown("---")
            if st.button("🔄 Reset Game", use_container_width=True):
                st.session_state.game = None
                st.session_state.game_started = False
                st.session_state.current_scenario = None
                st.session_state.last_result = None
                st.session_state.game_over = False
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎭 Student Personalities")
        st.markdown("""
        - 🌟 **Engaged**: Active participants
        - 🤫 **Quiet**: Reserved but attentive  
        - 😓 **Struggling**: Need extra support
        - 🎭 **Disruptive**: High energy, distractible
        - 🚀 **Overachiever**: Fast learners
        """)
    
    # Main game area
    if not st.session_state.game_started:
        # Welcome screen
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("Welcome to the Trainer Simulation!")
            st.markdown("""
            ### 🎯 Objective
            Lead a successful 90-minute training session by making smart decisions
            about how to engage and teach your virtual students.
            
            ### 📋 How to Play
            1. **Set up your class** - Choose number of students and difficulty
            2. **Face scenarios** - Respond to realistic classroom situations
            3. **Make decisions** - Choose the best teaching approach
            4. **Track progress** - Monitor student engagement and understanding
            5. **Complete the session** - Get your performance report!
            
            ### 🏆 Scoring
            - Keep students engaged for higher scores
            - Balance different teaching methods
            - Manage your own energy
            - Adapt to different student personalities
            """)
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                color: white;
            ">
                <div style="font-size: 4em;">🎓</div>
                <p style="font-size: 1.2em; margin-top: 10px;">Practice makes perfect!</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        game = st.session_state.game
        
        # Check if game is over
        if game.is_session_over():
            st.session_state.game_over = True
        
        if st.session_state.game_over:
            # Show final report
            st.header("📊 Session Complete!")
            
            report = game.get_final_report()
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Final Score", report['final_score'])
            with col2:
                st.metric("Grade", report['grade'].split(' - ')[0])
            with col3:
                st.metric("Time Used", f"{report['total_time']} min")
            with col4:
                st.metric("Performance", f"{report['overall_performance']:.0%}")
            
            st.markdown("---")
            
            # Detailed feedback
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Feedback")
                st.info(report['feedback'])
                
                st.subheader("💪 Strengths & Weaknesses")
                st.success(f"**Strongest with:** {report['strongest_with']}")
                st.warning(f"**Needs work with:** {report['needs_work_with']}")
            
            with col2:
                st.subheader("📈 Final Class Averages")
                st.metric("Engagement", f"{report['class_averages']['engagement']:.0%}")
                st.metric("Understanding", f"{report['class_averages']['understanding']:.0%}")
                st.metric("Energy", f"{report['class_averages']['energy']:.0%}")
                
                st.subheader("🎬 Actions Summary")
                for action_type, count in report['actions_summary']['action_types'].items():
                    st.write(f"• {action_type.replace('_', ' ').title()}: {count}")
            
            st.markdown("---")
            st.subheader("💡 Tips for Next Time")
            for tip in report['tips']:
                st.markdown(tip)
            
            if st.button("🎮 Play Again", type="primary", use_container_width=True):
                st.session_state.game = None
                st.session_state.game_started = False
                st.session_state.current_scenario = None
                st.session_state.last_result = None
                st.session_state.game_over = False
                st.rerun()
        
        else:
            # Active game
            st.markdown("---")
            
            # Display last action result if available
            if st.session_state.last_result:
                result = st.session_state.last_result
                with st.expander("📋 Last Action Results", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Action", result['action_type'].replace('_', ' ').title())
                    with col2:
                        st.metric("Action Score", f"+{result['action_score']}")
                    with col3:
                        st.metric("Your Energy", f"{result['trainer_energy']:.0%}")
                    
                    st.write("**Student Impact:**")
                    for sr in result['student_results'][:5]:  # Show top 5
                        change = sr['engagement_change']
                        icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                        st.write(f"{icon} {sr['student']}: {change:+.0%}")
            
            # Show classroom view
            st.header("👥 Your Classroom")
            status = game.get_class_status()
            
            # Create grid of student cards
            students = status['students']
            cols = st.columns(4)
            for i, student in enumerate(students):
                display_student_card(student, cols[i % 4])
            
            st.markdown("---")
            
            # Scenario section
            st.header("🎬 Current Scenario")
            
            # Get or create scenario
            if st.session_state.current_scenario is None:
                scenario = game.get_next_scenario()
                if scenario:
                    st.session_state.current_scenario = scenario
                else:
                    st.session_state.game_over = True
                    st.rerun()
            
            scenario = st.session_state.current_scenario
            
            if scenario:
                st.subheader(f"📌 {scenario.title}")
                st.markdown(f"*{scenario.description}*")
                
                st.markdown("### 🤔 What do you do?")
                
                for option in scenario.options:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{option.description}**")
                        st.caption(f"Action type: {option.action_type.value.replace('_', ' ').title()}")
                    with col2:
                        if st.button("Choose", key=f"opt_{option.id}", use_container_width=True):
                            result = game.make_decision(option.id)
                            st.session_state.last_result = result
                            st.session_state.current_scenario = None
                            st.rerun()
                    st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Trainer Simulation Game - Part of the Academic_Demos collection. "
        "Practice makes perfect!*"
    )


if __name__ == "__main__":
    main()
