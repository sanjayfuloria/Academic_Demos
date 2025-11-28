"""
Trainer Simulation Game - Core Logic

A simulation game that helps trainers practice classroom management,
student engagement, and teaching decision-making in various scenarios.
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class StudentPersonality(Enum):
    """Different student personality types that affect their behavior"""
    ENGAGED = "engaged"
    QUIET = "quiet"
    STRUGGLING = "struggling"
    DISRUPTIVE = "disruptive"
    OVERACHIEVER = "overachiever"


class ActionType(Enum):
    """Types of actions a trainer can take"""
    LECTURE = "lecture"
    GROUP_ACTIVITY = "group_activity"
    INDIVIDUAL_HELP = "individual_help"
    QUIZ = "quiz"
    DISCUSSION = "discussion"
    BREAK = "break"


@dataclass
class Student:
    """Represents a student in the simulation"""
    name: str
    personality: StudentPersonality
    engagement: float  # 0.0 to 1.0
    understanding: float  # 0.0 to 1.0
    energy: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "personality": self.personality.value,
            "engagement": round(self.engagement, 2),
            "understanding": round(self.understanding, 2),
            "energy": round(self.energy, 2)
        }


@dataclass
class ScenarioOption:
    """An option for the trainer to choose in a scenario"""
    id: str
    description: str
    action_type: ActionType
    effects: Dict[str, float]  # personality_type -> engagement_modifier


@dataclass
class Scenario:
    """A teaching scenario the trainer must respond to"""
    id: str
    title: str
    description: str
    options: List[ScenarioOption]
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "options": [
                {"id": o.id, "description": o.description, "action_type": o.action_type.value}
                for o in self.options
            ]
        }


class TrainerSimulation:
    """Main simulation game engine for trainer practice"""
    
    # Student first names for generation
    STUDENT_NAMES = [
        "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
        "Parker", "Drew", "Sage", "Reese", "Charlie", "Sam", "Jamie", "Blake"
    ]
    
    def __init__(self, num_students: int = 8, difficulty: str = "normal"):
        """Initialize the simulation with a class of students
        
        Args:
            num_students: Number of students in the class (4-16)
            difficulty: Game difficulty ("easy", "normal", "hard")
        """
        self.num_students = max(4, min(16, num_students))
        self.difficulty = difficulty
        self.students: List[Student] = []
        self.session_time: int = 0  # Minutes elapsed
        self.max_session_time: int = 90  # 90-minute session
        self.trainer_energy: float = 1.0
        self.session_score: int = 0
        self.actions_taken: List[Dict] = []
        self.current_scenario: Optional[Scenario] = None
        self.scenario_history: List[str] = []
        
        # Initialize students
        self._generate_students()
        
        # Generate scenarios
        self.scenarios = self._generate_scenarios()
    
    def _generate_students(self) -> None:
        """Generate a diverse class of students"""
        personalities = list(StudentPersonality)
        names = random.sample(self.STUDENT_NAMES, self.num_students)
        
        # Ensure a mix of personalities based on difficulty
        if self.difficulty == "easy":
            weights = [0.4, 0.2, 0.2, 0.05, 0.15]  # More engaged students
        elif self.difficulty == "hard":
            weights = [0.15, 0.2, 0.25, 0.25, 0.15]  # More challenging students
        else:
            weights = [0.25, 0.2, 0.2, 0.15, 0.2]  # Balanced
        
        for name in names:
            personality = random.choices(personalities, weights=weights)[0]
            
            # Initial stats based on personality
            base_engagement = self._get_base_stat(personality, "engagement")
            base_understanding = self._get_base_stat(personality, "understanding")
            base_energy = self._get_base_stat(personality, "energy")
            
            self.students.append(Student(
                name=name,
                personality=personality,
                engagement=base_engagement,
                understanding=base_understanding,
                energy=base_energy
            ))
    
    def _get_base_stat(self, personality: StudentPersonality, stat: str) -> float:
        """Get base stat value based on personality"""
        base_stats = {
            StudentPersonality.ENGAGED: {"engagement": 0.8, "understanding": 0.7, "energy": 0.8},
            StudentPersonality.QUIET: {"engagement": 0.4, "understanding": 0.6, "energy": 0.5},
            StudentPersonality.STRUGGLING: {"engagement": 0.5, "understanding": 0.3, "energy": 0.6},
            StudentPersonality.DISRUPTIVE: {"engagement": 0.6, "understanding": 0.5, "energy": 0.9},
            StudentPersonality.OVERACHIEVER: {"engagement": 0.9, "understanding": 0.8, "energy": 0.7},
        }
        # Add some randomness
        base = base_stats[personality][stat]
        variation = random.uniform(-0.1, 0.1)
        return max(0.1, min(1.0, base + variation))
    
    def _generate_scenarios(self) -> List[Scenario]:
        """Generate teaching scenarios"""
        return [
            Scenario(
                id="intro_engagement",
                title="Low Class Energy",
                description="You notice the class seems tired and disengaged at the start of the session. "
                           "Several students are yawning and looking at their phones.",
                options=[
                    ScenarioOption(
                        id="energizer",
                        description="Start with a quick energizer activity to wake everyone up",
                        action_type=ActionType.GROUP_ACTIVITY,
                        effects={
                            "engaged": 0.1, "quiet": 0.15, "struggling": 0.1,
                            "disruptive": 0.2, "overachiever": 0.05
                        }
                    ),
                    ScenarioOption(
                        id="straight_lecture",
                        description="Push through and start your planned lecture immediately",
                        action_type=ActionType.LECTURE,
                        effects={
                            "engaged": 0.0, "quiet": -0.1, "struggling": -0.15,
                            "disruptive": -0.2, "overachiever": 0.1
                        }
                    ),
                    ScenarioOption(
                        id="ask_students",
                        description="Ask students what would help them focus today",
                        action_type=ActionType.DISCUSSION,
                        effects={
                            "engaged": 0.15, "quiet": 0.05, "struggling": 0.1,
                            "disruptive": 0.1, "overachiever": 0.1
                        }
                    ),
                ]
            ),
            Scenario(
                id="struggling_student",
                title="Student Falling Behind",
                description="You notice one student looking confused and not participating. "
                           "They seem reluctant to ask for help.",
                options=[
                    ScenarioOption(
                        id="public_help",
                        description="Address the class and explain the concept again for everyone",
                        action_type=ActionType.LECTURE,
                        effects={
                            "engaged": -0.05, "quiet": 0.1, "struggling": 0.15,
                            "disruptive": -0.1, "overachiever": -0.15
                        }
                    ),
                    ScenarioOption(
                        id="private_help",
                        description="Walk over discreetly and offer one-on-one assistance",
                        action_type=ActionType.INDIVIDUAL_HELP,
                        effects={
                            "engaged": 0.0, "quiet": 0.1, "struggling": 0.25,
                            "disruptive": -0.05, "overachiever": 0.0
                        }
                    ),
                    ScenarioOption(
                        id="peer_help",
                        description="Pair them with a stronger student for peer support",
                        action_type=ActionType.GROUP_ACTIVITY,
                        effects={
                            "engaged": 0.1, "quiet": 0.15, "struggling": 0.2,
                            "disruptive": 0.05, "overachiever": 0.15
                        }
                    ),
                ]
            ),
            Scenario(
                id="disruptive_behavior",
                title="Classroom Disruption",
                description="A student keeps interrupting others and making off-topic comments. "
                           "The class is getting distracted.",
                options=[
                    ScenarioOption(
                        id="redirect",
                        description="Acknowledge their energy and redirect it to the topic",
                        action_type=ActionType.DISCUSSION,
                        effects={
                            "engaged": 0.05, "quiet": 0.05, "struggling": 0.0,
                            "disruptive": 0.2, "overachiever": 0.05
                        }
                    ),
                    ScenarioOption(
                        id="private_talk",
                        description="Ask to speak with them privately after class",
                        action_type=ActionType.INDIVIDUAL_HELP,
                        effects={
                            "engaged": 0.0, "quiet": 0.1, "struggling": 0.05,
                            "disruptive": 0.1, "overachiever": 0.0
                        }
                    ),
                    ScenarioOption(
                        id="ignore",
                        description="Ignore the behavior and continue with the lesson",
                        action_type=ActionType.LECTURE,
                        effects={
                            "engaged": -0.1, "quiet": -0.1, "struggling": -0.1,
                            "disruptive": -0.15, "overachiever": -0.05
                        }
                    ),
                ]
            ),
            Scenario(
                id="knowledge_check",
                title="Time for Assessment",
                description="You're halfway through the session and want to check understanding. "
                           "How do you assess what students have learned?",
                options=[
                    ScenarioOption(
                        id="formal_quiz",
                        description="Give a short formal quiz to assess knowledge",
                        action_type=ActionType.QUIZ,
                        effects={
                            "engaged": 0.0, "quiet": 0.05, "struggling": -0.1,
                            "disruptive": -0.1, "overachiever": 0.15
                        }
                    ),
                    ScenarioOption(
                        id="group_discussion",
                        description="Have students discuss key concepts in small groups",
                        action_type=ActionType.GROUP_ACTIVITY,
                        effects={
                            "engaged": 0.15, "quiet": 0.1, "struggling": 0.15,
                            "disruptive": 0.1, "overachiever": 0.1
                        }
                    ),
                    ScenarioOption(
                        id="open_questions",
                        description="Ask open-ended questions to the whole class",
                        action_type=ActionType.DISCUSSION,
                        effects={
                            "engaged": 0.1, "quiet": -0.05, "struggling": 0.0,
                            "disruptive": 0.15, "overachiever": 0.2
                        }
                    ),
                ]
            ),
            Scenario(
                id="energy_drop",
                title="Post-Lunch Slump",
                description="It's right after lunch and students are showing signs of fatigue. "
                           "Energy levels are dropping fast.",
                options=[
                    ScenarioOption(
                        id="short_break",
                        description="Give a 5-minute stretch break",
                        action_type=ActionType.BREAK,
                        effects={
                            "engaged": 0.1, "quiet": 0.15, "struggling": 0.15,
                            "disruptive": 0.1, "overachiever": 0.05
                        }
                    ),
                    ScenarioOption(
                        id="interactive_activity",
                        description="Switch to a hands-on interactive activity",
                        action_type=ActionType.GROUP_ACTIVITY,
                        effects={
                            "engaged": 0.2, "quiet": 0.1, "struggling": 0.1,
                            "disruptive": 0.15, "overachiever": 0.1
                        }
                    ),
                    ScenarioOption(
                        id="push_through",
                        description="Continue with the lecture as planned",
                        action_type=ActionType.LECTURE,
                        effects={
                            "engaged": -0.1, "quiet": -0.15, "struggling": -0.2,
                            "disruptive": -0.15, "overachiever": 0.0
                        }
                    ),
                ]
            ),
            Scenario(
                id="advanced_student",
                title="Advanced Student Bored",
                description="An overachieving student has finished early and seems bored. "
                           "They're starting to distract others.",
                options=[
                    ScenarioOption(
                        id="challenge_task",
                        description="Give them a challenging extension activity",
                        action_type=ActionType.INDIVIDUAL_HELP,
                        effects={
                            "engaged": 0.05, "quiet": 0.0, "struggling": 0.0,
                            "disruptive": 0.0, "overachiever": 0.25
                        }
                    ),
                    ScenarioOption(
                        id="peer_tutor",
                        description="Ask them to help struggling classmates",
                        action_type=ActionType.GROUP_ACTIVITY,
                        effects={
                            "engaged": 0.1, "quiet": 0.1, "struggling": 0.2,
                            "disruptive": 0.05, "overachiever": 0.15
                        }
                    ),
                    ScenarioOption(
                        id="wait",
                        description="Ask them to wait quietly for others to catch up",
                        action_type=ActionType.LECTURE,
                        effects={
                            "engaged": -0.05, "quiet": 0.0, "struggling": 0.0,
                            "disruptive": 0.0, "overachiever": -0.2
                        }
                    ),
                ]
            ),
        ]
    
    def get_next_scenario(self) -> Optional[Scenario]:
        """Get the next scenario based on game state"""
        # Filter out already seen scenarios
        available = [s for s in self.scenarios if s.id not in self.scenario_history]
        
        if not available:
            return None
        
        # Weight scenarios based on current class state
        scenario = random.choice(available)
        self.current_scenario = scenario
        return scenario
    
    def make_decision(self, option_id: str) -> Dict:
        """Process trainer's decision and update simulation state
        
        Args:
            option_id: The ID of the chosen option
            
        Returns:
            Dictionary containing the results of the action
        """
        if not self.current_scenario:
            return {"error": "No active scenario"}
        
        # Find the selected option
        option = None
        for opt in self.current_scenario.options:
            if opt.id == option_id:
                option = opt
                break
        
        if not option:
            return {"error": f"Invalid option: {option_id}"}
        
        # Apply effects to students
        results = []
        for student in self.students:
            personality_key = student.personality.value
            modifier = option.effects.get(personality_key, 0.0)
            
            # Apply difficulty modifiers
            if self.difficulty == "hard":
                modifier *= 0.7  # Reduced positive effects
            elif self.difficulty == "easy":
                modifier *= 1.3  # Enhanced positive effects
            
            # Update student stats
            old_engagement = student.engagement
            student.engagement = max(0.0, min(1.0, student.engagement + modifier))
            
            # Understanding improves based on engagement and action type
            if option.action_type in [ActionType.LECTURE, ActionType.DISCUSSION, ActionType.QUIZ]:
                understanding_gain = modifier * 0.5 * student.engagement
                student.understanding = max(0.0, min(1.0, student.understanding + understanding_gain))
            
            # Energy depletes over time, restored by breaks
            if option.action_type == ActionType.BREAK:
                student.energy = min(1.0, student.energy + 0.2)
            else:
                student.energy = max(0.1, student.energy - 0.05)
            
            results.append({
                "student": student.name,
                "engagement_change": round(student.engagement - old_engagement, 2),
                "new_engagement": round(student.engagement, 2)
            })
        
        # Update trainer energy
        if option.action_type == ActionType.BREAK:
            self.trainer_energy = min(1.0, self.trainer_energy + 0.1)
        else:
            self.trainer_energy = max(0.1, self.trainer_energy - 0.08)
        
        # Advance time
        time_costs = {
            ActionType.LECTURE: 15,
            ActionType.GROUP_ACTIVITY: 20,
            ActionType.INDIVIDUAL_HELP: 10,
            ActionType.QUIZ: 15,
            ActionType.DISCUSSION: 12,
            ActionType.BREAK: 5,
        }
        self.session_time += time_costs.get(option.action_type, 10)
        
        # Calculate score for this action
        avg_engagement = sum(s.engagement for s in self.students) / len(self.students)
        action_score = int(avg_engagement * 100)
        self.session_score += action_score
        
        # Record action
        self.actions_taken.append({
            "scenario_id": self.current_scenario.id,
            "option_id": option_id,
            "action_type": option.action_type.value,
            "time": self.session_time,
            "score": action_score
        })
        
        # Mark scenario as seen
        self.scenario_history.append(self.current_scenario.id)
        self.current_scenario = None
        
        return {
            "success": True,
            "action_type": option.action_type.value,
            "student_results": results,
            "time_elapsed": self.session_time,
            "time_remaining": self.max_session_time - self.session_time,
            "action_score": action_score,
            "total_score": self.session_score,
            "trainer_energy": round(self.trainer_energy, 2)
        }
    
    def get_class_status(self) -> Dict:
        """Get current status of the class"""
        avg_engagement = sum(s.engagement for s in self.students) / len(self.students)
        avg_understanding = sum(s.understanding for s in self.students) / len(self.students)
        avg_energy = sum(s.energy for s in self.students) / len(self.students)
        
        return {
            "students": [s.to_dict() for s in self.students],
            "averages": {
                "engagement": round(avg_engagement, 2),
                "understanding": round(avg_understanding, 2),
                "energy": round(avg_energy, 2)
            },
            "session_time": self.session_time,
            "time_remaining": self.max_session_time - self.session_time,
            "trainer_energy": round(self.trainer_energy, 2),
            "total_score": self.session_score,
            "actions_taken": len(self.actions_taken)
        }
    
    def is_session_over(self) -> bool:
        """Check if the training session is complete"""
        return self.session_time >= self.max_session_time
    
    def get_final_report(self) -> Dict:
        """Generate final report for the training session"""
        status = self.get_class_status()
        
        # Calculate performance grade
        avg_engagement = status["averages"]["engagement"]
        avg_understanding = status["averages"]["understanding"]
        
        overall_performance = (avg_engagement * 0.4 + avg_understanding * 0.4 + 
                             self.trainer_energy * 0.2)
        
        if overall_performance >= 0.8:
            grade = "A - Excellent"
            feedback = "Outstanding session! You effectively engaged students and maintained energy throughout."
        elif overall_performance >= 0.65:
            grade = "B - Good"
            feedback = "Good session with solid engagement. Some areas for improvement in energy management."
        elif overall_performance >= 0.5:
            grade = "C - Satisfactory"
            feedback = "Adequate session. Consider varying your teaching strategies more."
        elif overall_performance >= 0.35:
            grade = "D - Needs Improvement"
            feedback = "Session had challenges. Focus on reading student cues and adapting your approach."
        else:
            grade = "F - Poor"
            feedback = "Significant improvement needed. Consider reviewing engagement techniques."
        
        # Identify strongest and weakest areas
        personality_engagement = {}
        for student in self.students:
            p = student.personality.value
            if p not in personality_engagement:
                personality_engagement[p] = []
            personality_engagement[p].append(student.engagement)
        
        avg_by_personality = {
            p: sum(e) / len(e) for p, e in personality_engagement.items()
        }
        
        strongest = max(avg_by_personality.items(), key=lambda x: x[1])
        weakest = min(avg_by_personality.items(), key=lambda x: x[1])
        
        return {
            "session_complete": True,
            "total_time": self.session_time,
            "final_score": self.session_score,
            "grade": grade,
            "overall_performance": round(overall_performance, 2),
            "feedback": feedback,
            "class_averages": status["averages"],
            "strongest_with": f"{strongest[0]} students (avg engagement: {strongest[1]:.0%})",
            "needs_work_with": f"{weakest[0]} students (avg engagement: {weakest[1]:.0%})",
            "actions_summary": {
                "total_actions": len(self.actions_taken),
                "action_types": self._summarize_actions()
            },
            "tips": self._generate_tips(avg_by_personality)
        }
    
    def _summarize_actions(self) -> Dict[str, int]:
        """Summarize actions taken by type"""
        summary = {}
        for action in self.actions_taken:
            action_type = action["action_type"]
            summary[action_type] = summary.get(action_type, 0) + 1
        return summary
    
    def _generate_tips(self, engagement_by_personality: Dict[str, float]) -> List[str]:
        """Generate personalized improvement tips"""
        tips = []
        
        if engagement_by_personality.get("struggling", 1.0) < 0.5:
            tips.append("💡 Try using more peer support activities for struggling students")
        
        if engagement_by_personality.get("disruptive", 1.0) < 0.5:
            tips.append("💡 Consider channeling disruptive energy into positive contributions")
        
        if engagement_by_personality.get("quiet", 1.0) < 0.5:
            tips.append("💡 Create more small group activities to help quiet students participate")
        
        if engagement_by_personality.get("overachiever", 1.0) < 0.6:
            tips.append("💡 Provide extension challenges for advanced students")
        
        action_summary = self._summarize_actions()
        if action_summary.get("lecture", 0) > 2 and action_summary.get("group_activity", 0) < 2:
            tips.append("💡 Balance lectures with more interactive activities")
        
        if action_summary.get("break", 0) == 0:
            tips.append("💡 Consider including short breaks to maintain energy levels")
        
        if not tips:
            tips.append("🌟 Great job varying your teaching strategies!")
        
        return tips
