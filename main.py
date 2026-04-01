from pawpal_system import Owner, Pet, Planner, PawPalApp

def main():
    print("🐾 Welcome to the PawPal+ Terminal Test 🐾\n")

    # 1. Create an Owner with limited time (60 minutes)
    owner = Owner(name="Alex", time_available_mins=60)

    # 2. Create at least two Pets
    # Buddy is very hungry and has high energy!
    pet1 = Pet(name="Buddy", species="Dog", hunger_level=85, energy_level=90) 
    # Luna is a very chill, recently fed cat.
    pet2 = Pet(name="Luna", species="Cat", hunger_level=20, energy_level=30)  

    # 3. Initialize the Planner and App (We'll plan for Buddy today)
    planner = Planner(owner=owner, pet=pet1)
    app = PawPalApp(planner=planner)

    # 4. Add at least three Tasks with different times and base priorities
    # Notice how we give the walk a lower base priority than grooming, 
    # but the dynamic planner should boost it because Buddy's energy is at 90!
    app.create_task(name="Feed Buddy", duration=5, priority=5, category="Food")
    app.create_task(name="Long Walk", duration=45, priority=2, category="Exercise")
    app.create_task(name="Brush Fur", duration=20, priority=3, category="Grooming")
    
    # Let's throw in a medical task and flag that Buddy needs meds
    pet1.needs_meds = True
    app.create_task(name="Give Heartworm Pill", duration=2, priority=5, category="Medical")

    # 5. Generate and print "Today's Schedule"
    print(f"--- Generating Schedule for {pet1.name} ---")
    print(f"Owner Time Available: {owner.get_available_time()} mins\n")
    
    schedule = app.planner.generate_daily_plan()
    
    print("✅ Today's Schedule:")
    for task in schedule:
        print(f"  - {task.name} ({task.duration_mins} mins) [Category: {task.category}]")
        
    print("\n🧠 Planner Reasoning:")
    print(f"  {app.planner.generate_reasoning()}")

if __name__ == "__main__":
    main()