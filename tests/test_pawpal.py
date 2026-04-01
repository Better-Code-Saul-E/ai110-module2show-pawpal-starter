import unittest
from pawpal_system import Task, Pet, Owner, Planner, PawPalApp

class TestPawPalSystem(unittest.TestCase):

    def test_task_completion(self):
        """Task Completion: Verify calling mark_completed() changes the status."""
        # Arrange: Create a new task
        task = Task(id=1, name="Afternoon Walk", duration_mins=30, priority=3, category="Exercise")
        
        # Assert initial state is False
        self.assertFalse(task.is_completed, "Task should initially be incomplete.")
        
        # Act: Call the method
        task.mark_completed()
        
        # Assert new state is True
        self.assertTrue(task.is_completed, "Task should be marked as complete after calling mark_completed().")

    def test_task_addition(self):
        """Task Addition: Verify adding a task increases the system's task count."""
        # Arrange: Set up the app environment
        owner = Owner(name="Alex", time_available_mins=60)
        pet = Pet(name="Buddy", species="Dog")
        planner = Planner(owner=owner, pet=pet)
        app = PawPalApp(planner=planner)
        
        # Assert initial state is 0
        self.assertEqual(len(app.read_tasks()), 0, "App task database should initially be empty.")
        self.assertEqual(len(planner.task_pool), 0, "Planner task pool should initially be empty.")
        
        # Act: Create a new task through the app
        app.create_task(name="Feed Buddy", duration=5, priority=5, category="Food")
        
        # Assert new state is 1
        self.assertEqual(len(app.read_tasks()), 1, "App task database should increase to 1.")
        self.assertEqual(len(planner.task_pool), 1, "Planner task pool should increase to 1.")

if __name__ == '__main__':
    unittest.main()