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

    def mark_completed(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    hunger_level: int = 50   # Assuming a default 0-100 scale starting at 50
    energy_level: int = 50   # Assuming a default 0-100 scale starting at 50
    hygiene_level: int = 50  # Assuming a default 0-100 scale starting at 50
    needs_meds: bool = False

    def feed(self, food_amount: int) -> None:
        pass

    def provide_enrichment(self, duration: int) -> None:
        pass

    def groom(self) -> None:
        pass

    def simulate_time_passing(self, hours: int) -> None:
        pass


@dataclass
class Owner:
    name: str
    time_available_mins: int
    preferences: List[str] = field(default_factory=list)

    def update_availability(self, mins: int) -> None:
        pass

    def get_available_time(self) -> int:
        pass


class Planner:
    def __init__(self, owner: Owner, pet: Pet):
        self.task_pool: List[Task] = []
        self.owner: Owner = owner
        self.pet: Pet = pet

    def add_to_pool(self, task: Task) -> None:
        pass

    def _calculate_dynamic_priority(self, task: Task) -> int:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass

    def generate_reasoning(self) -> str:
        pass


class PawPalApp:
    def __init__(self, planner: Planner):
        self.planner: Planner = planner

    def create_task(self, name: str, duration: int, priority: int) -> None:
        pass

    def read_tasks(self) -> List[Task]:
        pass

    def update_task(self, task_id: int, new_data: Dict[str, Any]) -> None:
        pass

    def delete_task(self, task_id: int) -> None:
        pass

    def render_ui(self) -> None:
        pass