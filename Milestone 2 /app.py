import streamlit as st
import pandas as pd
from datetime import datetime
from prompt_builder import build_prompt
from model_api import query_model
import re

# Page configuration
st.set_page_config(
    page_title="Fitness Profile & BMI Calculator",
    page_icon="💪",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .bmi-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    .category-underweight { color: #3498db; font-weight: bold; }
    .category-normal { color: #2ecc71; font-weight: bold; }
    .category-overweight { color: #f39c12; font-weight: bold; }
    .category-obese { color: #e74c3c; font-weight: bold; }
    .workout-plan {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin: 20px 0;
        white-space: pre-wrap;
        font-family: 'Arial', sans-serif;
        line-height: 1.8;
    }
    .day-header {
        color: #4CAF50;
        font-size: 1.4em;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 8px;
    }
    .section-header {
        color: #2196F3;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .exercise-item {
        margin-left: 20px;
        margin-bottom: 8px;
    }
    .warning-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        margin: 15px 0;
    }
    .exercise-details {
        margin-left: 30px;
        color: #555;
        font-size: 0.95em;
    }
    /* Fix for calendar icon */
    .custom-calendar {
        display: flex;
        align-items: center;
        margin: 20px 0;
    }
    .custom-calendar span {
        font-size: 32px;
        margin-right: 10px;
    }
    .custom-calendar h2 {
        margin: 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💪 Fitness Profile & BMI Calculator")
st.markdown("Complete the form below to calculate your BMI and create your fitness profile.")

# Initialize session state for profile data
if 'profile_created' not in st.session_state:
    st.session_state.profile_created = False
    st.session_state.profile_data = {}
if 'workout_plan' not in st.session_state:
    st.session_state.workout_plan = None
if 'generation_attempts' not in st.session_state:
    st.session_state.generation_attempts = 0

# BMI Calculation Function
def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from weight and height"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2), height_m

def get_bmi_category(bmi):
    """Classify BMI into standard health categories"""
    if bmi < 18.5:
        return "Underweight", "category-underweight"
    elif 18.5 <= bmi < 25:
        return "Normal", "category-normal"
    elif 25 <= bmi < 30:
        return "Overweight", "category-overweight"
    else:
        return "Obese", "category-obese"

def get_bmi_description(category):
    """Get health description based on BMI category"""
    descriptions = {
        "Underweight": "Consider consulting a healthcare provider about healthy weight gain strategies.",
        "Normal": "Great job! Maintain your healthy lifestyle with balanced diet and regular exercise.",
        "Overweight": "Focus on gradual weight management through diet and increased physical activity.",
        "Obese": "Consult healthcare providers for personalized weight management plans."
    }
    return descriptions.get(category, "")

def clean_markdown(text):
    """Remove markdown symbols like # and * from text"""
    if not text:
        return text
    
    # Remove markdown headers (# symbols)
    text = re.sub(r'#{1,6}\s*', '', text)
    
    # Remove markdown bold/italic (* and **)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *italic*
    
    # Remove markdown bullets
    text = re.sub(r'^\s*[-*+]\s+', '  • ', text, flags=re.MULTILINE)
    
    # Remove markdown links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    return text

def format_workout_plan(plan):
    """Format the workout plan with clean styling (no markdown symbols)"""
    if not plan:
        return plan
    
    # First clean markdown symbols
    plan = clean_markdown(plan)
    
    lines = plan.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('')
            continue
        
        # Check if line contains day header
        upper_line = line.upper()
        is_day_header = False
        
        for i in range(1, 6):
            if (f"DAY {i}" in upper_line or 
                f"DAY {i}:" in upper_line or 
                f"DAY {i} -" in upper_line):
                # Add separator before each day (except first)
                if i > 1:
                    formatted_lines.append('')
                    formatted_lines.append('─' * 60)
                formatted_lines.append(f'📅 {line}')
                formatted_lines.append('─' * 60)
                is_day_header = True
                break
        
        if not is_day_header:
            # Format workout sections
            if "WARM-UP" in upper_line:
                formatted_lines.append('')
                formatted_lines.append(f'🔥 {line}')
                formatted_lines.append('')
            elif "MAIN WORKOUT" in upper_line:
                formatted_lines.append('')
                formatted_lines.append(f'💪 {line}')
                formatted_lines.append('')
            elif "COOL-DOWN" in upper_line:
                formatted_lines.append('')
                formatted_lines.append(f'🧘 {line}')
                formatted_lines.append('')
            elif "REST DAY" in upper_line:
                formatted_lines.append('')
                formatted_lines.append(f'😴 {line}')
                formatted_lines.append('')
            elif "SETS" in upper_line or "REPS" in upper_line or "REST" in upper_line:
                formatted_lines.append(f'   {line}')
            elif line.startswith('•') or line.startswith('-'):
                formatted_lines.append(f'  {line}')
            else:
                formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def count_days_in_plan(plan):
    """Count how many days are present in the workout plan"""
    if not plan:
        return 0
    plan_upper = plan.upper()
    days = 0
    for i in range(1, 6):
        if (f"DAY {i}" in plan_upper or 
            f"DAY {i}:" in plan_upper or 
            f"DAY {i} -" in plan_upper):
            days += 1
    return days

# Form validation function
def validate_inputs(name, height, weight):
    """Validate all required inputs"""
    errors = []
    
    if not name or not name.strip():
        errors.append("❌ Name is required")
    
    if height is None or height <= 0:
        errors.append("❌ Height must be greater than 0")
    
    if weight is None or weight <= 0:
        errors.append("❌ Weight must be greater than 0")
    
    return errors

# Main Form
with st.form("fitness_form"):
    st.subheader("📋 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        weight = st.number_input("Weight (kg) *", min_value=0.1, max_value=500.0, 
                                value=None, placeholder="Enter weight", step=0.1)
    
    with col2:
        height = st.number_input("Height (cm) *", min_value=1.0, max_value=300.0, 
                                value=None, placeholder="Enter height", step=0.1)
    
    st.subheader("💪 Fitness Details")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fitness_goal = st.selectbox(
            "Fitness Goal *",
            ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"]
        )
        
        fitness_level = st.radio(
            "Fitness Level *",
            ["Beginner", "Intermediate", "Advanced"],
            horizontal=True
        )
    
    with col4:
        equipment_options = ["Dumbbells", "Resistance Band", "Yoga Mat", "Kettlebells", 
                           "Barbell", "Treadmill", "Exercise Bike", "No Equipment"]
        equipment = st.multiselect(
            "Available Equipment *",
            equipment_options,
            help="Select all equipment you have access to"
        )
    
    # Submit button
    submitted = st.form_submit_button("📊 Calculate BMI & Generate Profile", use_container_width=True)
    
    if submitted:
        # Validate inputs
        errors = validate_inputs(name, height, weight)
        
        if not equipment:
            errors.append("❌ Please select at least one equipment option")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Calculate BMI
            bmi, height_m = calculate_bmi(weight, height)
            category, css_class = get_bmi_category(bmi)
            description = get_bmi_description(category)
            
            # Store profile data in session state
            st.session_state.profile_created = True
            st.session_state.profile_data = {
                'name': name,
                'gender': gender,
                'height_cm': height,
                'height_m': height_m,
                'weight': weight,
                'bmi': bmi,
                'category': category,
                'css_class': css_class,
                'description': description,
                'fitness_goal': fitness_goal,
                'fitness_level': fitness_level,
                'equipment': equipment,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.workout_plan = None
            st.session_state.generation_attempts = 0
            
            st.success("✅ Profile created successfully!")
            st.rerun()

# Display Profile Results
if st.session_state.profile_created:
    data = st.session_state.profile_data
    
    st.markdown("---")
    st.subheader("📄 Your Fitness Profile")
    
    # BMI Result Card
    st.markdown(f"""
    <div class="bmi-card">
        <h3>📊 BMI Result</h3>
        <h1 style="font-size: 48px; margin: 10px 0;">{data['bmi']}</h1>
        <p style="font-size: 20px;">
            <span class="{data['css_class']}">{data['category']}</span>
        </p>
        <p style="color: #666;">{data['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Details Card
    with st.container():
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown("#### 👤 Personal Details")
            st.write(f"**Name:** {data['name']}")
            st.write(f"**Gender:** {data['gender']}")
            st.write(f"**Height:** {data['height_cm']} cm ({data['height_m']:.2f} m)")
            st.write(f"**Weight:** {data['weight']} kg")
        
        with col6:
            st.markdown("#### 🎯 Fitness Goals")
            st.write(f"**Primary Goal:** {data['fitness_goal']}")
            st.write(f"**Experience Level:** {data['fitness_level']}")
            st.write(f"**Equipment:** {', '.join(data['equipment'])}")
    
    # Health Recommendations
    st.markdown("#### 💡 Recommendations")
    
    col7, col8 = st.columns(2)
    
    with col7:
        if data['category'] == "Underweight":
            st.info("🍽️ Focus on nutrient-dense foods and strength training")
        elif data['category'] == "Normal":
            st.success("🌟 Maintain balanced diet and regular exercise routine")
        elif data['category'] == "Overweight":
            st.warning("🏃 Combine cardio with strength training for best results")
        else:
            st.error("🏥 Consider professional guidance for safe weight management")
    
    with col8:
        # Goal-specific tips
        if data['fitness_goal'] == "Build Muscle":
            st.info("💪 Increase protein intake and focus on progressive overload")
        elif data['fitness_goal'] == "Weight Loss":
            st.info("🔥 Maintain calorie deficit and incorporate HIIT workouts")
        elif data['fitness_goal'] == "Strength Gain":
            st.info("🏋️ Focus on compound lifts and proper form")
        elif data['fitness_goal'] == "Abs Building":
            st.info("🧘 Combine core work with overall fat loss strategies")
        else:
            st.info("🧘‍♀️ Include dynamic stretching and mobility work")
    
    # Profile Summary Table
    st.markdown("#### 📋 Profile Summary")
    summary_df = pd.DataFrame({
        'Metric': ['BMI', 'Category', 'Goal', 'Level', 'Equipment Count'],
        'Value': [
            data['bmi'],
            data['category'],
            data['fitness_goal'],
            data['fitness_level'],
            len(data['equipment'])
        ]
    })
    st.table(summary_df)
    
    # AI Workout Plan Generator
    st.markdown("---")
    st.subheader("🤖 AI-Powered Workout Plan Generator")
    st.markdown("Click the button below to get a personalized 5-day workout plan based on your profile!")
    
    col9, col10 = st.columns([1, 1])
    
    with col9:
        if st.button("🎯 Generate 5-Day Workout Plan", use_container_width=True):
            with st.spinner("Creating your personalized 5-day workout plan... This may take a few seconds..."):
                try:
                    # Build the prompt with profile data
                    prompt, bmi_value, bmi_cat = build_prompt(
                        name=data['name'],
                        gender=data['gender'],
                        height=data['height_cm'],
                        weight=data['weight'],
                        goal=data['fitness_goal'],
                        fitness_level=data['fitness_level'],
                        equipment=data['equipment']
                    )
                    
                    # Get the workout plan from the model
                    workout_plan = query_model(prompt)
                    
                    # Store in session state
                    st.session_state.workout_plan = workout_plan
                    st.session_state.generation_attempts += 1
                    
                    st.success("✅ Workout plan generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating workout plan: {str(e)}")
                    st.info("Please check your internet connection and HF_TOKEN, then try again.")
    
    with col10:
        if st.button("🔄 Create New Profile", use_container_width=True):
            st.session_state.profile_created = False
            st.session_state.profile_data = {}
            st.session_state.workout_plan = None
            st.session_state.generation_attempts = 0
            st.rerun()
    
    # Display Workout Plan if generated
    if st.session_state.workout_plan:
        st.markdown("---")
        
        # Custom header without date
        st.markdown("""
        <div class="custom-calendar">
            <span>📅</span>
            <h2>Your Personalized 5-Day Workout Schedule</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if the plan contains all 5 days
        days_count = count_days_in_plan(st.session_state.workout_plan)
        
        if days_count < 5:
            st.markdown(f"""
            <div class="warning-box">
                <strong>⚠️ Warning:</strong> The generated plan shows only {days_count} out of 5 days. 
                Click "Generate Again" for a complete 5-day plan.
                <br><br>
                <strong>Tips for better results:</strong>
                <ul style="margin-top: 5px; margin-bottom: 0;">
                    <li>Try generating again - sometimes the model needs multiple attempts</li>
                    <li>Make sure you have a stable internet connection</li>
                    <li>If problem persists, check your HF_TOKEN</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Display generation attempt info
        if st.session_state.generation_attempts > 1:
            st.info(f"🔄 Generation attempt #{st.session_state.generation_attempts}")
        
        # Format and clean the workout plan (remove markdown symbols)
        cleaned_plan = clean_markdown(st.session_state.workout_plan)
        formatted_plan = format_workout_plan(cleaned_plan)
        
        with st.container():
            st.markdown('<div class="workout-plan">', unsafe_allow_html=True)
            st.text(formatted_plan)  # Using st.text to ensure no markdown rendering
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons for workout plan
        st.markdown("### 📋 Plan Actions")
        col11, col12, col13, col14 = st.columns(4)
        
        with col11:
            if st.button("🔄 Generate Again", use_container_width=True):
                st.session_state.workout_plan = None
                st.rerun()
        
        with col12:
            # Download workout plan only
            st.download_button(
                label="📥 Download Plan",
                data=st.session_state.workout_plan,
                file_name=f"workout_plan_{data['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col13:
            # Download complete report
            profile_text = f"""
FITNESS PROFILE REPORT
Generated: {data['timestamp']}

PERSONAL INFORMATION
Name: {data['name']}
Gender: {data['gender']}
Height: {data['height_cm']} cm ({data['height_m']:.2f} m)
Weight: {data['weight']} kg

BMI ANALYSIS
BMI Value: {data['bmi']}
Category: {data['category']}
Status: {data['description']}

FITNESS GOALS
Primary Goal: {data['fitness_goal']}
Experience Level: {data['fitness_level']}
Available Equipment: {', '.join(data['equipment'])}

{"="*60}
PERSONALIZED 5-DAY WORKOUT PLAN
{"="*60}

{st.session_state.workout_plan}
            """
            
            st.download_button(
                label="📥 Complete Report",
                data=profile_text,
                file_name=f"complete_report_{data['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col14:
            if st.button("🏠 Back to Top", use_container_width=True):
                st.rerun()
        
        # Add tips for getting better results
        with st.expander("💡 Tips for better workout plans"):
            st.markdown("""
            - Be specific with your available equipment
            - Try multiple generations - each plan is slightly different
            - Regenerate after 4-6 weeks as you progress
            - Combine goals if you have multiple focuses
            - Always consult a fitness professional before starting
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🏋️‍♂️ Your fitness journey starts here! Complete the form to get personalized insights and AI-generated workout plans.</p>
    <p style='font-size: 12px;'>* Required fields | BMI is a screening tool, not a diagnostic measure | AI-generated plans should be reviewed by a professional</p>
</div>
""", unsafe_allow_html=True)
# Sidebar with additional information
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3043/3043650.png", width=100)
    st.title("About BMI")
    st.markdown("""
    **Body Mass Index (BMI)** is a simple measure that uses your height and weight to estimate body fat.
    
    BMI Categories:
    - Underweight: < 18.5
    - Normal: 18.5 - 24.9
    - Overweight: 25 - 29.9
    - Obese: ≥ 30
    
    Tips for Accuracy:
    - Measure height without shoes
    - Weigh yourself in the morning
    - Use consistent units
    """)
    
    st.markdown("---")
    st.markdown("### 🤖 About AI Workout Plans")
    st.markdown("""
    Our AI-powered workout plans are:
    - 🎯 Personalized to your goals
    - 📅 5-day structured schedules
    - 💪 Based on your fitness level
    - 🏋️ Adapted to available equipment
    - 🔄 Regenerate for variety
    
    Note: If you don't get all 5 days, click "Generate Again"
    """)
    
    # Show generation stats if plan exists
    if st.session_state.workout_plan:
        days = count_days_in_plan(st.session_state.workout_plan)
        st.markdown("---")
        st.markdown("### 📊 Current Plan Stats")
        st.markdown(f"- Days included: {days}/5")
        st.markdown(f"- Generation attempts: {st.session_state.generation_attempts}")
        if days < 5:
            st.markdown("⚠️ Tip: Click 'Generate Again' for more days")
    
    st.markdown("---")
    st.markdown("### 📝 Quick Example")
    st.markdown("""
    Try this example:
    - Name: Sarah Johnson
    - Gender: Female
    - Height: 165 cm
    - Weight: 58 kg
    - Goal: Weight Loss
    - Equipment: Dumbbells, Yoga Mat
    - Level: Intermediate
    
    BMI: 21.3 (Normal)
    """)
    
