import unittest
from pawpal_system import Task, Pet, Owner, Planner, PawPalApp

class TestPawPalSystem(unittest.TestCase):

    def setUp(self):
        """This runs before EVERY test to give us a fresh app state."""
        self.owner = Owner(name="Alex", time_available_mins=60)
        self.pet = Pet(name="Buddy", species="Dog", hunger_level=50, energy_level=50)
        self.planner = Planner(owner=self.owner, pet=self.pet)
        self.app = PawPalApp(planner=self.planner)

    def test_task_completion(self):
        """Task Completion: Verify calling mark_completed() changes the status."""
        task = self.app.create_task("Walk", 30, 5, "Exercise")
        self.assertFalse(task.is_completed)
        task.mark_completed()
        self.assertTrue(task.is_completed)

    def test_task_addition(self):
        """Task Addition: Verify adding a task increases the system's task count."""
        self.assertEqual(len(self.app.read_tasks()), 0)
        self.app.create_task("Feed", 5, 5, "Food")
        self.assertEqual(len(self.app.read_tasks()), 1)

    def test_sorting_correctness(self):
        """Sorting Correctness: Verify tasks are sorted by highest value-per-minute."""
        task_a = self.app.create_task("Medium Value", 10, 10, "Other")
        task_b = self.app.create_task("Low Value", 10, 5, "Other")
        task_c = self.app.create_task("High Value", 5, 10, "Other")

        schedule = self.app.planner.generate_daily_plan()
        
        self.assertEqual(schedule[0].name, "High Value")
        self.assertEqual(schedule[1].name, "Medium Value")
        self.assertEqual(schedule[2].name, "Low Value")

    def test_recurrence_logic(self):
        """Recurrence Logic: Confirm start_new_day() resets completed recurring tasks."""
        recurring_task = self.app.create_task("Daily Meds", 2, 10, "Medical", is_recurring=True)
        one_time_task = self.app.create_task("Go to Vet", 60, 10, "Medical", is_recurring=False)
        
        recurring_task.mark_completed()
        one_time_task.mark_completed()
        
        self.app.start_new_day()
        
        self.assertFalse(recurring_task.is_completed, "Recurring task should be reset to False.")
        self.assertTrue(one_time_task.is_completed, "One-time task should remain True.")

    def test_conflict_detection(self):
        """Conflict Detection: Verify Planner flags/rejects time and time-of-day conflicts."""
        self.app.planner.owner.update_availability(60)
        
        task_a = self.app.create_task("High Value Walk", 30, 10, "Exercise", time_of_day="Morning")
        task_b = self.app.create_task("Low Value Grooming", 45, 5, "Grooming", time_of_day="Morning")
        task_c = self.app.create_task("Evening Feed", 5, 10, "Food", time_of_day="Evening")

        schedule = self.app.planner.generate_daily_plan(current_time_of_day="Morning")
        
        self.assertIn(task_a, schedule, "Task A should be scheduled because it has highest value/min.")
        self.assertNotIn(task_b, schedule, "Task B should be excluded due to lack of time (Conflict).")
        self.assertNotIn(task_c, schedule, "Task C should be excluded due to wrong time of day (Conflict).")


if __name__ == '__main__':
    unittest.main()