# 🎓 Trainer Simulation Game

An interactive simulation game for trainers and educators to practice classroom management, student engagement, and teaching decision-making in realistic scenarios.

## 🎯 Overview

This simulation game helps trainers develop their teaching skills by:
- Managing a virtual classroom of diverse student personalities
- Responding to realistic teaching scenarios
- Making decisions that affect student engagement and learning
- Receiving feedback on their training effectiveness

## 🚀 Quick Start

1. **Navigate to the demo directory:**
```bash
cd demo3_trainer_simulation
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
python -m unittest test_trainer_simulation.py -v
```

5. **Start the application:**
```bash
streamlit run app.py
```

6. **Open your browser:** Go to http://localhost:8501

## 📋 How to Play

### Setting Up
1. Choose the number of students (4-12)
2. Select difficulty level (easy, normal, hard)
3. Click "Start New Game"

### Gameplay
1. **View your classroom** - See all students with their personalities and current stats
2. **Face scenarios** - Realistic teaching situations will appear
3. **Make decisions** - Choose how to respond from multiple options
4. **Track progress** - Monitor student engagement, understanding, and energy
5. **Complete the session** - Play through a 90-minute virtual training session

### Winning
- Keep students engaged throughout the session
- Maintain good understanding levels
- Manage your own energy as a trainer
- Balance different teaching approaches

## 🎭 Student Personalities

Each student has a unique personality that affects how they respond to your teaching:

| Personality | Emoji | Description |
|-------------|-------|-------------|
| **Engaged** | 🌟 | Active participants who respond well to most activities |
| **Quiet** | 🤫 | Reserved but attentive, benefit from small group activities |
| **Struggling** | 😓 | Need extra support and patience |
| **Disruptive** | 🎭 | High energy, can be challenging but respond to redirection |
| **Overachiever** | 🚀 | Fast learners who need extra challenges |

## 🎬 Action Types

Your decisions involve different teaching approaches:

- **Lecture** - Direct instruction
- **Group Activity** - Collaborative learning
- **Individual Help** - One-on-one support
- **Quiz** - Knowledge assessment
- **Discussion** - Open dialogue
- **Break** - Rest and recharge

## 📊 Metrics Tracked

### Student Metrics
- **Engagement** - How involved students are in the learning
- **Understanding** - Comprehension of the material
- **Energy** - Student alertness and focus

### Session Metrics
- **Time** - Progress through the 90-minute session
- **Score** - Points earned based on student engagement
- **Trainer Energy** - Your own energy level

## 🏆 Grading

At the end of each session, you receive:
- **Overall Grade** (A-F)
- **Performance Score** (percentage)
- **Strengths & Weaknesses** - Which personalities you worked best with
- **Improvement Tips** - Personalized suggestions

## 🔧 Difficulty Levels

| Level | Description |
|-------|-------------|
| **Easy** | More engaged students, greater impact from positive actions |
| **Normal** | Balanced mix of personalities |
| **Hard** | More challenging students, reduced effectiveness of actions |

## 🛠️ Technical Details

### Architecture
- `trainer_simulation.py` - Core game engine and logic
- `app.py` - Streamlit web interface
- `test_trainer_simulation.py` - Comprehensive test suite

### Key Classes
- `TrainerSimulation` - Main game controller
- `Student` - Individual student model with stats
- `Scenario` - Teaching situations with options
- `ScenarioOption` - Choices with effects on students

### Testing
```bash
# Run all tests
python -m unittest test_trainer_simulation.py -v

# Run specific test class
python -m unittest test_trainer_simulation.TestDecisionMaking -v
```

## 📈 Extending the Game

### Adding New Scenarios
Add scenarios to the `_generate_scenarios()` method in `trainer_simulation.py`:

```python
Scenario(
    id="your_scenario_id",
    title="Scenario Title",
    description="What's happening in the classroom...",
    options=[
        ScenarioOption(
            id="option1",
            description="First choice",
            action_type=ActionType.DISCUSSION,
            effects={
                "engaged": 0.1,
                "quiet": 0.05,
                "struggling": 0.1,
                "disruptive": 0.0,
                "overachiever": 0.1
            }
        ),
        # Add more options...
    ]
)
```

### Adding New Personalities
1. Add to `StudentPersonality` enum
2. Add base stats in `_get_base_stat()`
3. Add effects in scenario options

## 🤝 Contributing

Feel free to extend with:
- Additional teaching scenarios
- New student personality types
- More action types
- Integration with learning management systems
- Multiplayer/competitive modes

## 📄 License

Part of the Academic_Demos collection - educational and demonstration purposes.
