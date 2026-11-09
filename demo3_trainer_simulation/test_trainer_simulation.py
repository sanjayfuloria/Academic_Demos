"""
Test suite for Trainer Simulation Game

Tests cover:
- Simulation initialization
- Student generation
- Scenario management
- Decision making and effects
- Scoring and reporting
"""

import unittest
from trainer_simulation import (
    TrainerSimulation,
    Student,
    StudentPersonality,
    ActionType,
    Scenario,
    ScenarioOption
)


class TestStudentGeneration(unittest.TestCase):
    """Tests for student generation"""
    
    def test_correct_number_of_students(self):
        """Test that correct number of students are generated"""
        sim = TrainerSimulation(num_students=8)
        self.assertEqual(len(sim.students), 8)
    
    def test_min_students_enforced(self):
        """Test minimum student count is enforced"""
        sim = TrainerSimulation(num_students=1)
        self.assertEqual(len(sim.students), 4)  # Min is 4
    
    def test_max_students_enforced(self):
        """Test maximum student count is enforced"""
        sim = TrainerSimulation(num_students=100)
        self.assertEqual(len(sim.students), 16)  # Max is 16
    
    def test_students_have_unique_names(self):
        """Test that all students have unique names"""
        sim = TrainerSimulation(num_students=10)
        names = [s.name for s in sim.students]
        self.assertEqual(len(names), len(set(names)))
    
    def test_students_have_valid_personalities(self):
        """Test all students have valid personality types"""
        sim = TrainerSimulation(num_students=8)
        for student in sim.students:
            self.assertIsInstance(student.personality, StudentPersonality)
    
    def test_student_stats_in_valid_range(self):
        """Test student stats are within valid range"""
        sim = TrainerSimulation(num_students=8)
        for student in sim.students:
            self.assertGreaterEqual(student.engagement, 0.0)
            self.assertLessEqual(student.engagement, 1.0)
            self.assertGreaterEqual(student.understanding, 0.0)
            self.assertLessEqual(student.understanding, 1.0)
            self.assertGreaterEqual(student.energy, 0.0)
            self.assertLessEqual(student.energy, 1.0)


class TestSimulationInitialization(unittest.TestCase):
    """Tests for simulation initialization"""
    
    def test_default_initialization(self):
        """Test default simulation initialization"""
        sim = TrainerSimulation()
        self.assertEqual(sim.num_students, 8)
        self.assertEqual(sim.difficulty, "normal")
        self.assertEqual(sim.session_time, 0)
        self.assertEqual(sim.max_session_time, 90)
        self.assertEqual(sim.trainer_energy, 1.0)
        self.assertEqual(sim.session_score, 0)
    
    def test_custom_initialization(self):
        """Test custom simulation initialization"""
        sim = TrainerSimulation(num_students=10, difficulty="hard")
        self.assertEqual(sim.num_students, 10)
        self.assertEqual(sim.difficulty, "hard")
    
    def test_scenarios_generated(self):
        """Test scenarios are generated on init"""
        sim = TrainerSimulation()
        self.assertGreater(len(sim.scenarios), 0)
        for scenario in sim.scenarios:
            self.assertIsInstance(scenario, Scenario)


class TestScenarioManagement(unittest.TestCase):
    """Tests for scenario management"""
    
    def test_get_next_scenario(self):
        """Test getting next scenario"""
        sim = TrainerSimulation()
        scenario = sim.get_next_scenario()
        self.assertIsInstance(scenario, Scenario)
        self.assertIsNotNone(scenario.id)
        self.assertIsNotNone(scenario.title)
        self.assertIsNotNone(scenario.description)
        self.assertGreater(len(scenario.options), 0)
    
    def test_scenario_not_repeated(self):
        """Test that scenarios are not immediately repeated"""
        sim = TrainerSimulation()
        seen_ids = set()
        
        for _ in range(3):
            scenario = sim.get_next_scenario()
            if scenario:
                self.assertNotIn(scenario.id, seen_ids)
                seen_ids.add(scenario.id)
                # Make a decision to complete the scenario
                sim.make_decision(scenario.options[0].id)
    
    def test_scenario_to_dict(self):
        """Test scenario serialization"""
        sim = TrainerSimulation()
        scenario = sim.get_next_scenario()
        scenario_dict = scenario.to_dict()
        
        self.assertIn("id", scenario_dict)
        self.assertIn("title", scenario_dict)
        self.assertIn("description", scenario_dict)
        self.assertIn("options", scenario_dict)


class TestDecisionMaking(unittest.TestCase):
    """Tests for decision making"""
    
    def test_valid_decision(self):
        """Test making a valid decision"""
        sim = TrainerSimulation()
        scenario = sim.get_next_scenario()
        option_id = scenario.options[0].id
        
        result = sim.make_decision(option_id)
        
        self.assertTrue(result["success"])
        self.assertIn("action_type", result)
        self.assertIn("student_results", result)
        self.assertIn("time_elapsed", result)
        self.assertIn("action_score", result)
    
    def test_invalid_decision(self):
        """Test making an invalid decision"""
        sim = TrainerSimulation()
        sim.get_next_scenario()
        
        result = sim.make_decision("invalid_option")
        self.assertIn("error", result)
    
    def test_decision_without_scenario(self):
        """Test making decision without active scenario"""
        sim = TrainerSimulation()
        result = sim.make_decision("some_option")
        self.assertIn("error", result)
    
    def test_decision_advances_time(self):
        """Test that decisions advance session time"""
        sim = TrainerSimulation()
        initial_time = sim.session_time
        
        scenario = sim.get_next_scenario()
        sim.make_decision(scenario.options[0].id)
        
        self.assertGreater(sim.session_time, initial_time)
    
    def test_decision_affects_students(self):
        """Test that decisions affect student stats"""
        sim = TrainerSimulation()
        
        # Store initial engagements
        initial_engagements = [s.engagement for s in sim.students]
        
        scenario = sim.get_next_scenario()
        sim.make_decision(scenario.options[0].id)
        
        final_engagements = [s.engagement for s in sim.students]
        
        # At least some students should have different engagement
        changes = sum(1 for i, f in zip(initial_engagements, final_engagements) if i != f)
        self.assertGreater(changes, 0)
    
    def test_decision_affects_trainer_energy(self):
        """Test that decisions affect trainer energy"""
        sim = TrainerSimulation()
        initial_energy = sim.trainer_energy
        
        scenario = sim.get_next_scenario()
        sim.make_decision(scenario.options[0].id)
        
        # Energy should change after a decision
        self.assertNotEqual(sim.trainer_energy, initial_energy)


class TestDifficultyLevels(unittest.TestCase):
    """Tests for different difficulty levels"""
    
    def test_easy_difficulty(self):
        """Test easy difficulty has more engaged students"""
        sim = TrainerSimulation(num_students=12, difficulty="easy")
        engaged_count = sum(1 for s in sim.students 
                          if s.personality == StudentPersonality.ENGAGED)
        # Easy should tend to have more engaged students
        self.assertGreaterEqual(len(sim.students), 4)
    
    def test_hard_difficulty(self):
        """Test hard difficulty simulation works"""
        sim = TrainerSimulation(num_students=8, difficulty="hard")
        self.assertEqual(sim.difficulty, "hard")
        # Should still have valid students
        self.assertEqual(len(sim.students), 8)


class TestClassStatus(unittest.TestCase):
    """Tests for class status reporting"""
    
    def test_get_class_status(self):
        """Test getting class status"""
        sim = TrainerSimulation()
        status = sim.get_class_status()
        
        self.assertIn("students", status)
        self.assertIn("averages", status)
        self.assertIn("session_time", status)
        self.assertIn("time_remaining", status)
        self.assertIn("trainer_energy", status)
        self.assertIn("total_score", status)
    
    def test_averages_calculation(self):
        """Test that averages are calculated correctly"""
        sim = TrainerSimulation()
        status = sim.get_class_status()
        
        # Manually calculate expected averages
        expected_engagement = sum(s.engagement for s in sim.students) / len(sim.students)
        
        self.assertAlmostEqual(
            status["averages"]["engagement"], 
            round(expected_engagement, 2),
            places=2
        )


class TestSessionCompletion(unittest.TestCase):
    """Tests for session completion"""
    
    def test_session_not_over_initially(self):
        """Test session is not over at start"""
        sim = TrainerSimulation()
        self.assertFalse(sim.is_session_over())
    
    def test_session_over_after_max_time(self):
        """Test session ends after max time"""
        sim = TrainerSimulation()
        sim.session_time = 90
        self.assertTrue(sim.is_session_over())
    
    def test_final_report_generation(self):
        """Test final report is generated correctly"""
        sim = TrainerSimulation()
        
        # Play through some scenarios
        for _ in range(3):
            scenario = sim.get_next_scenario()
            if scenario:
                sim.make_decision(scenario.options[0].id)
        
        report = sim.get_final_report()
        
        self.assertIn("session_complete", report)
        self.assertIn("total_time", report)
        self.assertIn("final_score", report)
        self.assertIn("grade", report)
        self.assertIn("feedback", report)
        self.assertIn("tips", report)
    
    def test_grade_calculation(self):
        """Test that grades are assigned correctly"""
        sim = TrainerSimulation()
        
        # Force high engagement for A grade test
        for student in sim.students:
            student.engagement = 0.9
            student.understanding = 0.9
        sim.trainer_energy = 0.9
        
        report = sim.get_final_report()
        self.assertIn("A", report["grade"])


class TestStudentModel(unittest.TestCase):
    """Tests for Student data model"""
    
    def test_student_to_dict(self):
        """Test student serialization"""
        student = Student(
            name="Alex",
            personality=StudentPersonality.ENGAGED,
            engagement=0.8,
            understanding=0.7,
            energy=0.9
        )
        
        student_dict = student.to_dict()
        
        self.assertEqual(student_dict["name"], "Alex")
        self.assertEqual(student_dict["personality"], "engaged")
        self.assertEqual(student_dict["engagement"], 0.8)
        self.assertEqual(student_dict["understanding"], 0.7)
        self.assertEqual(student_dict["energy"], 0.9)


class TestActionTypes(unittest.TestCase):
    """Tests for action types"""
    
    def test_all_action_types_have_time_cost(self):
        """Test that all action types advance time"""
        sim = TrainerSimulation()
        
        action_types_seen = set()
        
        # Go through scenarios to see different action types
        for scenario in sim.scenarios:
            for option in scenario.options:
                action_types_seen.add(option.action_type)
        
        # All major action types should be represented
        self.assertIn(ActionType.LECTURE, action_types_seen)
        self.assertIn(ActionType.GROUP_ACTIVITY, action_types_seen)
        self.assertIn(ActionType.DISCUSSION, action_types_seen)


class TestScenarioOptions(unittest.TestCase):
    """Tests for scenario options"""
    
    def test_options_have_effects(self):
        """Test that scenario options have effects defined"""
        sim = TrainerSimulation()
        
        for scenario in sim.scenarios:
            for option in scenario.options:
                self.assertIsInstance(option.effects, dict)
                self.assertGreater(len(option.effects), 0)
    
    def test_options_have_action_types(self):
        """Test that scenario options have action types"""
        sim = TrainerSimulation()
        
        for scenario in sim.scenarios:
            for option in scenario.options:
                self.assertIsInstance(option.action_type, ActionType)


if __name__ == "__main__":
    unittest.main(verbosity=2)
