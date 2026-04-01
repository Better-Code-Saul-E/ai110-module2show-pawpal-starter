from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Task:
    id: int
    name: str
    duration_mins: int
    priority: int
    category: str
    is_completed: bool = False
    is_recurring: bool = False        
    time_of_day: str = "Any"          

    def mark_completed(self) -> None:
        """Marks the task as completed by setting is_completed to True."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    hunger_level: int = 50   
    energy_level: int = 50   
    hygiene_level: int = 50  
    needs_meds: bool = False

    def feed(self, food_amount: int) -> None:
        """Decreases the pet's hunger level by the specified food amount."""
        self.hunger_level = max(0, self.hunger_level - food_amount)

    def provide_enrichment(self, duration: int) -> None:
        """Decreases the pet's energy level by the specified duration."""
        self.energy_level = max(0, self.energy_level - duration)

    def groom(self) -> None:
        """Resets the pet's hygiene level to 0 (perfectly clean)."""
        self.hygiene_level = 0

    def simulate_time_passing(self, hours: int) -> None:
        """Increases hunger, energy, and hygiene levels based on hours passed."""
        self.hunger_level = min(100, self.hunger_level + (hours * 10))
        self.energy_level = min(100, self.energy_level + (hours * 5))
        self.hygiene_level = min(100, self.hygiene_level + (hours * 2))


@dataclass
class Owner:
    name: str
    time_available_mins: int
    preferences: List[str] = field(default_factory=list)

    def update_availability(self, mins: int) -> None:
        """Updates the owner's available time in minutes."""
        self.time_available_mins = max(0, mins)

    def get_available_time(self) -> int:
        """Returns the owner's currently available time in minutes."""
        return self.time_available_mins


class Planner:
    def __init__(self, owner: Owner, pet: Pet):
        self.task_pool: List[Task] = []
        self.owner: Owner = owner
        self.pet: Pet = pet
        self._last_reasoning: str = "No plan generated yet."

    def add_to_pool(self, task: Task) -> None:
        """Adds a new task to the planner's available task pool."""
        self.task_pool.append(task)

    def _calculate_dynamic_priority(self, task: Task) -> int:
        """Calculates task priority based on base priority and the pet's current state."""
        dynamic_priority = task.priority

        if task.category.lower() == "medical" and self.pet.needs_meds:
            return 999 

        if task.category.lower() == "food" and self.pet.hunger_level > 75:
            dynamic_priority += 50
            
        if task.category.lower() in ["exercise", "enrichment"]:
            if self.pet.energy_level > 80:
                dynamic_priority += 30
            elif self.pet.energy_level < 30:
                dynamic_priority -= 20

        if task.category.lower() == "grooming" and self.pet.hygiene_level > 90:
            dynamic_priority += 20

        return dynamic_priority

    def generate_daily_plan(self, current_time_of_day: str = "Any") -> List[Task]:
        """Generates a daily schedule prioritizing urgent pet needs within available time."""
        
        pending_tasks = []
        
        for t in self.task_pool:
            if not t.is_completed:
                if t.time_of_day == "Any" or current_time_of_day == "Any" or t.time_of_day == current_time_of_day:
                    pending_tasks.append(t)
        
        # UPGRADE: Sorting by value-per-minute
        sorted_tasks = sorted(
            pending_tasks, 
            key=lambda t: self._calculate_dynamic_priority(t) / max(1, t.duration_mins), 
            reverse=True
        )

        schedule = []
        time_left = self.owner.get_available_time()
        tasks_scheduled_count = 0

        for task in sorted_tasks:
            # UPGRADE: Time Conflict Detection
            # If a task takes longer than the time we have left, skip it!
            if task.duration_mins <= time_left:
                schedule.append(task)
                time_left -= task.duration_mins
                tasks_scheduled_count += 1

        time_used = self.owner.get_available_time() - time_left
        self._last_reasoning = (
            f"Scheduled {tasks_scheduled_count} {current_time_of_day} tasks taking {time_used} mins. "
            f"Prioritized by value-per-minute based on {self.pet.name}'s current needs "
            f"(Hunger: {self.pet.hunger_level}, Energy: {self.pet.energy_level})."
        )

        return schedule

    def generate_reasoning(self) -> str:
        """Returns a text summary explaining how the daily plan was generated."""
        return self._last_reasoning


class PawPalApp:
    def __init__(self, planner: Planner):
        self.planner: Planner = planner
        self.tasks_db: Dict[int, Task] = {} 
        self._next_id: int = 1

    def create_task(self, name: str, duration: int, priority: int, category: str, is_recurring: bool = False, time_of_day: str = "Any") -> Task:
        """Creates a new task, saves it to the database, and adds it to the planner."""
        safe_duration = max(1, duration)
        safe_priority = max(1, min(10, priority))
        
        new_task = Task(
            id=self._next_id,
            name=name,
            duration_mins=safe_duration,
            priority=safe_priority,
            category=category,
            is_recurring=is_recurring,
            time_of_day=time_of_day
        )
        self.tasks_db[self._next_id] = new_task
        self.planner.add_to_pool(new_task)
        self._next_id += 1
        return new_task

    def start_new_day(self) -> None:
        """NEW: Handles recurring tasks by resetting them for the next day."""
        for task in self.tasks_db.values():
            if task.is_recurring:
                task.is_completed = False

    def read_tasks(self) -> List[Task]:
        """Returns a list of all tasks currently in the database."""
        return list(self.tasks_db.values())

    def update_task(self, task_id: int, new_data: Dict[str, Any]) -> None:
        """Updates specific attributes of an existing task by its ID."""
        if task_id in self.tasks_db:
            task = self.tasks_db[task_id]
            for key, value in new_data.items():
                if hasattr(task, key):
                    setattr(task, key, value)

    def delete_task(self, task_id: int) -> None:
        """Deletes a task from the database and the planner's pool by its ID."""
        if task_id in self.tasks_db:
            task_to_remove = self.tasks_db[task_id]
            del self.tasks_db[task_id]
            
            if task_to_remove in self.planner.task_pool:
                self.planner.task_pool.remove(task_to_remove)

    def render_ui(self) -> None:
        """Placeholder for rendering the Streamlit user interface."""
        pass