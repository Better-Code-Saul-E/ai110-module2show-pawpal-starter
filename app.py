import streamlit as st
from pawpal_system import Owner, Pet, Planner, PawPalApp

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "pawpal" not in st.session_state:
    default_owner = Owner(name="Jordan", time_available_mins=60)
    default_pet = Pet(name="Mochi", species="Dog", hunger_level=50, energy_level=50)
    default_planner = Planner(owner=default_owner, pet=default_pet)
    st.session_state.pawpal = PawPalApp(planner=default_planner)

app: PawPalApp = st.session_state.pawpal

st.title("🐾 PawPal+")

with st.expander("Scenario & System Status", expanded=False):
    st.markdown("### System Loaded Successfully!")
    st.write(f"**Current Owner:** {app.planner.owner.name} (Time available: {app.planner.owner.time_available_mins} mins)")
    st.write(f"**Current Pet:** {app.planner.pet.name} the {app.planner.pet.species}")
    st.write(f"  - Hunger: {app.planner.pet.hunger_level}/100")
    st.write(f"  - Energy: {app.planner.pet.energy_level}/100")

st.divider()

st.subheader("1. Update Pet & Owner Settings")
col_o, col_p = st.columns(2)

with col_o:
    new_time = st.number_input("Time Available Today (mins)", min_value=0, max_value=300, value=app.planner.owner.time_available_mins)
    app.planner.owner.update_availability(new_time)

with col_p:
    new_hunger = st.slider("Mochi's Hunger Level", 0, 100, app.planner.pet.hunger_level)
    new_energy = st.slider("Mochi's Energy Level", 0, 100, app.planner.pet.energy_level)
    app.planner.pet.hunger_level = new_hunger
    app.planner.pet.energy_level = new_energy

st.divider()

st.subheader("2. Manage Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.number_input("Base Priority (1-10)", min_value=1, max_value=10, value=5)

col4, col5, col6 = st.columns(3)
with col4:
    category = st.selectbox("Category", ["Exercise", "Food", "Grooming", "Medical", "Other"])
with col5:
    time_of_day = st.selectbox("Time of Day", ["Any", "Morning", "Afternoon", "Evening"])
with col6:
    st.write("") # Spacing to align the checkbox
    st.write("") 
    is_recurring = st.checkbox("Is Recurring?")

if st.button("Add task"):
    app.create_task(
        name=task_title, 
        duration=int(duration), 
        priority=int(priority), 
        category=category,
        is_recurring=is_recurring,
        time_of_day=time_of_day
    )
    st.success(f"Added {task_title}!")

current_tasks = app.read_tasks()
if current_tasks:
    st.write("### Current Task Pool:")
    for t in current_tasks:
        recurring_badge = "🔁" if t.is_recurring else "1️⃣"
        st.write(f"- {recurring_badge} **{t.name}** | {t.duration_mins}m | Pri: {t.priority} | Cat: {t.category} | Time: {t.time_of_day}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("3. Build Schedule")
plan_time = st.selectbox("Plan for which time of day?", ["Any", "Morning", "Afternoon", "Evening"])

if st.button("Generate schedule"):
    schedule = app.planner.generate_daily_plan(current_time_of_day=plan_time)
    
    if not schedule:
        st.warning(f"No tasks could fit in the {plan_time} schedule, or the task pool is empty!")
    else:
        st.success("Schedule Generated Successfully!")
        
        st.markdown(f"### 📋 Today's {plan_time} Plan:")
        for i, task in enumerate(schedule):
            st.markdown(f"{i+1}. **{task.name}** ({task.duration_mins} mins)")
            
        st.info(f"**Planner Reasoning:** {app.planner.generate_reasoning()}")
        
        # Mark tasks as completed after scheduling them
        for task in schedule:
            task.mark_completed()

st.divider()

st.subheader("4. End of Day Simulation")
st.caption("Press this to test your recurring task logic!")
if st.button("Simulate Next Day"):
    app.start_new_day()
    st.success("A new day has started! All recurring tasks are back in the pending pool.")