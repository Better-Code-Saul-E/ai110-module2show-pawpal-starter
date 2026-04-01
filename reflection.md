# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
classDiagram
    class PawPalApp {
        - planner: Planner
        + create_task(name, duration, priority)
        + read_tasks() : List~Task~
        + update_task(task_id, new_data)
        + delete_task(task_id)
        + render_ui()
    }

    class Owner {
        - name: String
        - time_available_mins: int
        - preferences: List~String~
        + update_availability(mins: int)
        + get_available_time() : int
    }

    class Pet {
        - name: String
        - species: String
        - hunger_level: int  %% 0-100 scale
        - energy_level: int  %% 0-100 scale
        - hygiene_level: int %% 0-100 scale
        - needs_meds: bool
        + feed(food_amount: int)
        + provide_enrichment(duration: int)
        + groom()
        + simulate_time_passing(hours: int)
    }

    class Task {
        - id: int
        - name: String
        - duration_mins: int
        - priority: int
        - category: String   %% e.g., "Food", "Exercise", "Grooming"
        - is_completed: bool
        + mark_completed()
    }

    class Planner {
        - task_pool: List~Task~
        - owner: Owner
        - pet: Pet
        + add_to_pool(task: Task)
        - calculate_dynamic_priority(task: Task) : int
        + generate_daily_plan() : List~Task~
        + generate_reasoning() : String
    }

    PawPalApp --> Planner : Uses
    Planner "1" *-- "many" Task : Manages
    Planner "1" *-- "1" Owner : Considers constraints of
    Planner "1" *-- "1" Pet : Plans for

- What classes did you include, and what responsibilities did you assign to each?
Owner: This will hold how much time the user has for their pet.
Pet: The pet itself it will hold the pets tasks like getting fe
Task: Keeps information of a single task
Planner: This is plan the schedule
PawPalApp/app: The streamlit interface 

**b. Design changes**

- Did your design change during implementation?
Yes, alot. Their is so much to consider with tracking the pets status.

- If yes, describe at least one change and why you made it.
Adding internal states for the pet like hunger_level and energy_level. It made sense to add it because if the app only tracked when your feeding it, how would you know how much you fed your pet 1 scoop or 2 scoops. Pets could also get a long walk in or a short one. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time limits like the owners availible time vs the time it takes to complete a task
The time of day to make sure that a task isnt scheduled for morning when listed for the evening 
- How did you decide which constraints mattered most?
The owners time is the most important, since it is the owner how is making the schedule. If they dont have time then it wont be scheduled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The is that my scheduler is sorted by value per minute. It grabs the highest rank that fits in the remaning time and schedules it. It will no look ahead to see if a combination of three smaller taks could fill a 30 minute block better than a 25 minute task.

- Why is that tradeoff reasonable for this scenario?
A task such as feeding should be the most important. Without food your pet will obviously die.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
