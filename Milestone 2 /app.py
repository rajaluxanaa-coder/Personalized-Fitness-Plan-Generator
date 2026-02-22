import streamlit as st
import pandas as pd
from datetime import datetime
from prompt_builder import build_prompt
from model_api import query_model

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
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 20px 0;
        white-space: pre-wrap;
        font-family: monospace;
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
            st.session_state.workout_plan = None  # Reset workout plan when new profile is created
            
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
                    
                    st.success("✅ Workout plan generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating workout plan: {str(e)}")
                    st.info("Please check your internet connection and HF_TOKEN, then try again.")
    
    with col10:
        if st.button("🔄 Create New Profile", use_container_width=True):
            st.session_state.profile_created = False
            st.session_state.profile_data = {}
            st.session_state.workout_plan = None
            st.rerun()
    
    # Display Workout Plan if generated
    if st.session_state.workout_plan:
        st.markdown("### 📅 Your Personalized 5-Day Workout Schedule")
        st.markdown("---")
        
        # Display the workout plan in a nice container
        with st.container():
            st.markdown('<div class="workout-plan">', unsafe_allow_html=True)
            st.markdown(st.session_state.workout_plan)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Download buttons for both profile and workout plan
        col11, col12 = st.columns(2)
        
        with col11:
            # Export profile data
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

WORKOUT PLAN
{st.session_state.workout_plan}
            """
            
            st.download_button(
                label="📥 Download Complete Report",
                data=profile_text,
                file_name=f"fitness_report_{data['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col12:
            # Download only workout plan
            st.download_button(
                label="📥 Download Workout Plan Only",
                data=st.session_state.workout_plan,
                file_name=f"workout_plan_{data['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

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
    
    ### BMI Categories:
    - **Underweight:** < 18.5
    - **Normal:** 18.5 - 24.9
    - **Overweight:** 25 - 29.9
    - **Obese:** ≥ 30
    
    ### Tips for Accuracy:
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
    - 🔒 Private and secure
    
    *Always consult with a fitness professional before starting any new exercise routine.*
    """)
    
    st.markdown("---")
    st.markdown("### 📝 Quick Example")
    st.markdown("""
    **Try this example:**
    - Name: Sarah Johnson
    - Gender: Female
    - Height: 165 cm
    - Weight: 58 kg
    - Goal: Weight Loss
    - Equipment: Dumbbells, Yoga Mat
    - Level: Intermediate
    
    BMI: 21.3 (Normal)
    """)
