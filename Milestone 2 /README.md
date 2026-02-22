# Personalized-Fitness-Plan-Generator - Milestone 2: AI-Powered 5-Day Workout Plan Generator

## 📌 Objective

The objective of this milestone is to enhance the Fitness Profile & BMI Calculator by integrating an AI-powered 5-day workout plan generator that creates personalized exercise schedules based on user profiles, BMI categories, fitness goals, and available equipment.

---

## 📊 BMI Formula Explanation

BMI (Body Mass Index) is calculated using the following formula:
Where:
- Weight is measured in kilograms (kg)
- Height is measured in meters (m)

---

### BMI Categories:

| Category | BMI Range | Health Recommendation |
|----------|-----------|----------------------|
| Underweight | < 18.5 | Focus on muscle building & nutrient-dense foods |
| Normal Weight | 18.5 - 24.9 | Maintain balanced diet & regular exercise |
| Overweight | 25 - 29.9 | Combine cardio with strength training |
| Obese | ≥ 30 | Consult healthcare providers for safe weight management |

---

## ✨ Features Implemented

### 1. Comprehensive User Profile Creation
- **Personal Information:** Name, Gender, Height (cm), Weight (kg)
- **Fitness Details:**
  - Fitness Goal (Build Muscle, Weight Loss, Strength Gain, Abs Building, Flexible)
  - Fitness Level (Beginner, Intermediate, Advanced)
  - Available Equipment (Multi-select from 8+ equipment options)

### 2. BMI Calculation & Health Classification
- Real-time BMI calculation with automatic height conversion
- Color-coded BMI categories for visual identification
- Personalized health recommendations based on BMI category
- Detailed health tips and suggestions

### 3. AI-Powered 5-Day Workout Plan Generator
- Complete 5-day structured schedules (Monday to Friday)
- Day-specific focus areas based on fitness goals:

| Goal | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |
|------|-------|-------|-------|-------|-------|
| Build Muscle | Chest/Triceps | Back/Biceps | Legs/Core | Shoulders/Arms | Full Body |
| Weight Loss | Full Body HIIT | Cardio/Core | Upper Body | Lower Body | Endurance |
| Strength Gain | Push Day | Pull Day | Leg Day | Accessory Work | Full Body |
| Abs Building | Core/Cardio | Upper Body | Lower Body | Core Specialization | Full Body |
| Flexible | Mobility | Upper Body Flexibility | Lower Body Stretching | Dynamic Movement | Recovery |

### 4. Comprehensive Workout Details

Each day's workout includes:
- 🔥 **Warm-up Exercises** (5-10 minutes)
- 💪 **Main Workout** with:
  - Exercise names
  - Sets and repetitions
  - Rest periods between sets
  - Form tips for proper execution
- 🧘 **Cool-down Stretches** (5-10 minutes)
- 😴 **Rest Days** (Weekend recovery recommendations)

### 5. Smart Adaptations
- **BMI-based exercise selection:** Low-impact options for overweight/obese users
- **Fitness level adjustments:** Beginner to Advanced difficulty scaling
- **Equipment-aware planning:** Exercises limited to available equipment
- **Goal-specific focus:** Tailored exercises for each fitness objective

### 6. Profile Management & Export
- Session-based profile storage
- Profile summary with key metrics table
- Dual download options:
  - 📥 Complete Report (Profile + BMI + Workout Plan)
  - 📥 Workout Plan Only (Just the exercise schedule)
- Generation attempt tracking with status indicators

### 7. User-Friendly Interface
- Clean, responsive design with custom CSS styling
- Visual progress indicators and warning messages
- One-click plan regeneration
- Back to Top navigation for easy scrolling
- Sidebar with BMI information and quick example

---

## 🛠️ Technology Stack

- **Frontend & Backend:** Streamlit (Python)
- **Data Processing:** Pandas
- **AI Integration:** Hugging Face Inference API
- **AI Model:** mistralai/Mistral-7B-Instruct-v0.2
- **Environment Management:** python-dotenv
- **Additional Libraries:** re (regex for text cleaning)

---

## 🌐 Live Application

Access the live application here: [Hugging Face Space Link](https://huggingface.co/spaces/Rajaluxanaa/FitPlan_AI22)
