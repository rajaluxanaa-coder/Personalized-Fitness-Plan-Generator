import streamlit as st
import pandas as pd
from datetime import datetime
from model_api import query_model  # Import your model function
from prompt_builder import build_prompt  # Import your prompt builder

# Page configuration
st.set_page_config(
    page_title="Fitness Profile & BMI Calculator",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS - UPDATED for better mobile responsiveness
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .stButton button {
            font-size: 14px;
            padding: 0.5rem;
        }
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.75rem;
        transition: all 0.3s;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .bmi-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
        word-wrap: break-word;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .category-underweight { color: #3498db; font-weight: bold; }
    .category-normal { color: #2ecc71; font-weight: bold; }
    .category-overweight { color: #f39c12; font-weight: bold; }
    .category-obese { color: #e74c3c; font-weight: bold; }
    .workout-plan {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-x: auto;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        line-height: 1.6;
        font-size: 16px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Mobile specific styles */
    @media (max-width: 768px) {
        .workout-plan {
            padding: 15px;
            font-size: 14px;
            margin: 10px -5px;
            border-radius: 8px;
        }
        h1, h2, h3 {
            word-wrap: break-word;
            font-size: 1.5rem;
        }
        .stExpander {
            border: none;
        }
        .streamlit-expanderHeader {
            font-size: 16px;
            padding: 12px !important;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .row-widget.stButton {
            margin-bottom: 10px;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            padding: 5px 0 !important;
        }
        .stTextInput, .stNumberInput, .stSelectbox, .stMultiselect {
            margin-bottom: 15px;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }
        .stRadio > div {
            flex-direction: column;
            align-items: flex-start;
        }
        .stRadio label {
            padding: 8px 0;
        }
    }
    /* Tablet specific styles */
    @media (min-width: 769px) and (max-width: 1024px) {
        .workout-plan {
            font-size: 15px;
            padding: 18px;
        }
    }
    /* Improve table responsiveness if any tables appear */
    table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        border-collapse: collapse;
        width: 100%;
        margin: 10px 0;
    }
    th, td {
        padding: 8px;
        text-align: left;
        border: 1px solid #ddd;
        min-width: 100px;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    /* Ensure cards don't overflow */
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    /* Style for download button */
    .stDownloadButton button {
        background-color: #2196F3 !important;
    }
    .stDownloadButton button:hover {
        background-color: #1976D2 !important;
    }
    /* Success and error message styling */
    .stAlert {
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    /* Sidebar styling for mobile */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
        }
    }
    /* Workout plan headings */
    .workout-plan h1 {
        font-size: 24px;
        color: #333;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .workout-plan h2 {
        font-size: 20px;
        color: #4CAF50;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    .workout-plan h3 {
        font-size: 18px;
        color: #666;
        margin-top: 12px;
        margin-bottom: 6px;
    }
    .workout-plan ul, .workout-plan ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    .workout-plan li {
        margin: 5px 0;
    }
    .workout-plan p {
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💪 Fitness Profile & AI Workout Planner")
st.markdown("Complete the form below to get a personalized AI-generated workout plan.")

# Initialize session state
if 'profile_created' not in st.session_state:
    st.session_state.profile_created = False
    st.session_state.profile_data = {}
    st.session_state.workout_plan = None

# Form validation function
def validate_inputs(name, age, height, weight, gender):
    errors = []
    
    if not name or not name.strip():
        errors.append("❌ Name is required")
    
    if not gender:
        errors.append("❌ Gender is required")
    
    if age is None or age <= 0 or age > 120:
        errors.append("❌ Please enter a valid age (1-120 years)")
    elif age < 18:
        errors.append("❌ You must be at least 18 years old to use this fitness planner")
    
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
        age = st.number_input("Age *", min_value=1, max_value=120, 
                             value=None, placeholder="Enter your age", step=1)
        weight = st.number_input("Weight (kg) *", min_value=0.1, max_value=500.0, 
                                value=None, placeholder="Enter weight", step=0.1)
    
    with col2:
        height = st.number_input("Height (cm) *", min_value=1.0, max_value=300.0, 
                                value=None, placeholder="Enter height", step=0.1)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
    
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
    submitted = st.form_submit_button("📊 Generate AI Workout Plan", use_container_width=True)
    
    if submitted:
        # Validate inputs
        errors = validate_inputs(name, age, height, weight, gender)
        
        if not equipment:
            errors.append("❌ Please select at least one equipment option")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            with st.spinner("🤖 AI is generating your personalized workout plan..."):
                try:
                    # Build the prompt
                    prompt, bmi, bmi_status = build_prompt(
                        name, age, gender, height, weight, 
                        fitness_goal, fitness_level, equipment
                    )
                    
                    # Query the AI model
                    workout_plan = query_model(prompt)
                    
                    # Store in session state
                    st.session_state.profile_created = True
                    st.session_state.profile_data = {
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'height_cm': height,
                        'weight': weight,
                        'bmi': bmi,
                        'bmi_status': bmi_status,
                        'fitness_goal': fitness_goal,
                        'fitness_level': fitness_level,
                        'equipment': equipment,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.workout_plan = workout_plan
                    
                    st.success("✅ Profile created and workout plan generated!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating workout plan: {str(e)}")

# Display Results
if st.session_state.profile_created:
    data = st.session_state.profile_data
    
    st.markdown("---")
    st.subheader("📄 Your Fitness Profile")
    
    # BMI Result Card
    st.markdown(f"""
    <div class="bmi-card">
        <h3>📊 BMI Result</h3>
        <h1 style="font-size: 48px; margin: 10px 0;">{data['bmi']:.2f}</h1>
        <p style="font-size: 20px;">
            <span class="category-{data['bmi_status'].lower().replace(' ', '')}">{data['bmi_status']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Details
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 👤 Personal Details")
        st.write(f"**Name:** {data['name']}")
        st.write(f"**Age:** {data['age']} years")
        st.write(f"**Gender:** {data['gender']}")
        st.write(f"**Height:** {data['height_cm']} cm")
        st.write(f"**Weight:** {data['weight']} kg")
    
    with col6:
        st.markdown("#### 🎯 Fitness Goals")
        st.write(f"**Primary Goal:** {data['fitness_goal']}")
        st.write(f"**Experience Level:** {data['fitness_level']}")
        st.write(f"**Equipment:** {', '.join(data['equipment'])}")
    
    # AI Generated Workout Plan
    st.markdown("---")
    st.subheader("🤖 AI-Generated Personalized Workout Plan")
    
    if st.session_state.workout_plan:
        # Simple success message without debug info
        st.success(f"✅ Your personalized workout plan is ready!")
        
        # Create tabs for different viewing options (removed Debug Info tab)
        tab1, tab2 = st.tabs(["📋 Formatted View", "📝 Raw Text"])
        
        with tab1:
            # Display with proper markdown formatting
            st.markdown("### Your 5-Day Workout Plan")
            st.markdown("---")
            
            # Use markdown to display the workout plan
            st.markdown(st.session_state.workout_plan)
            
            # Add download button for the plan
            st.download_button(
                label="📥 Download Workout Plan",
                data=st.session_state.workout_plan,
                file_name=f"workout_plan_{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with tab2:
            # Display in a text area for easy copying
            st.text_area(
                "Raw workout plan (select all and copy):", 
                st.session_state.workout_plan, 
                height=400,
                key="raw_plan"
            )
            st.caption("👆 Select all text above and copy (Ctrl+A, Ctrl+C or long press on mobile)")
    else:
        st.warning("⚠️ No workout plan generated yet. Please submit the form to generate a plan.")
    
    # Action buttons
    st.markdown("---")
    col9, col10, col11 = st.columns(3)
    
    with col9:
        if st.button("🔄 Create New Profile", use_container_width=True):
            st.session_state.profile_created = False
            st.session_state.profile_data = {}
            st.session_state.workout_plan = None
            st.rerun()
    
    with col10:
        # Export full profile data
        profile_text = f"""
FITNESS PROFILE REPORT
Generated: {data['timestamp']}

PERSONAL INFORMATION
Name: {data['name']}
Age: {data['age']} years
Gender: {data['gender']}
Height: {data['height_cm']} cm
Weight: {data['weight']} kg
BMI: {data['bmi']:.2f} ({data['bmi_status']})

FITNESS GOALS
Primary Goal: {data['fitness_goal']}
Experience Level: {data['fitness_level']}
Available Equipment: {', '.join(data['equipment'])}

WORKOUT PLAN:
{st.session_state.workout_plan if st.session_state.workout_plan else 'No plan generated'}
        """
        
        st.download_button(
            label="📥 Download Full Profile",
            data=profile_text,
            file_name=f"fitness_profile_{data['name'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col11:
        if st.button("🔄 Regenerate Plan", use_container_width=True):
            with st.spinner("🤖 Generating new plan..."):
                prompt, _, _ = build_prompt(
                    data['name'], data['age'], data['gender'], data['height_cm'], 
                    data['weight'], data['fitness_goal'], 
                    data['fitness_level'], data['equipment']
                )
                st.session_state.workout_plan = query_model(prompt)
                st.rerun()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3043/3043650.png", width=100)
    st.title("About This App")
    st.markdown("""
    This app combines:
    - 📊 BMI Calculation
    - 🤖 AI-Generated Workout Plans
    
    ### How it works:
    1. Fill in your details (including age)
    2. AI generates a personalized 5-day plan
    3. Download or regenerate as needed
    
    ### BMI Categories:
    - **Underweight:** < 18.5
    - **Normal:** 18.5 - 24.9
    - **Overweight:** 25 - 29.9
    - **Obese:** ≥ 30
    
    ### Age Note:
    This fitness planner is designed for adults (18+ years).
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🏋️‍♂️ Powered by AI - Your personal fitness trainer</p>
    <p style='font-size: 12px;'>* Plans are AI-generated suggestions. Consult a professional before starting.</p>
</div>
""", unsafe_allow_html=True)
