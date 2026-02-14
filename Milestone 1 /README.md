# Personalized-Fitness-Plan-Generator - Milestone 1: Fitness Profile & BMI Calculator

## 📌 Objective
The objective of this milestone is to create an interactive **Fitness Profile & BMI Calculator** application that allows users to:
- Input their personal and fitness details
- Calculate their Body Mass Index (BMI)
- Receive personalized health recommendations based on BMI category
- Generate and download a comprehensive fitness profile

## 📊 BMI Formula Explanation

BMI (Body Mass Index) is calculated using the following formula:

BMI = weight(kg) / (height(m))²


Where:
- **Weight** is measured in kilograms (kg)
- **Height** is measured in meters (m)

### BMI Categories:
| Category | BMI Range |
|----------|-----------|
| Underweight | < 18.5 |
| Normal | 18.5 - 24.9 |
| Overweight | 25 - 29.9 |
| Obese | ≥ 30 |

## 🚀 Steps Performed

### 1. **Form Creation**
- Designed a user-friendly form using Streamlit's form components
- Implemented input fields for:
  - Personal Information (Name, Height, Weight)
  - Fitness Details (Goal, Level, Available Equipment)
- Used columns layout for better visual organization

### 2. **Input Validation**
- Implemented comprehensive validation checks:
  - Required fields validation
  - Numeric value validation (positive numbers only)
  - Equipment selection validation
- Displayed user-friendly error messages
- Prevented form submission with invalid data

### 3. **BMI Logic Implementation**
- Created functions for:
  - `calculate_bmi()`: Computes BMI from weight and height
  - `get_bmi_category()`: Classifies BMI into health categories
  - `get_bmi_description()`: Provides health recommendations
- Real-time BMI calculation upon form submission

### 4. **Deployment on Hugging Face Spaces**
- Prepared the application for deployment
- Created necessary configuration files
- Deployed on Hugging Face Spaces platform
- Tested functionality in production environment

## 💻 Technologies Used

- **Python 3.9+**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and display
- **Hugging Face Spaces**: Deployment platform
- **Git**: Version control

## 🌐 Live Application

Access the live application here: [Hugging Face Space Link](https://huggingface.co/spaces/Rajaluxanaa/FitPlan_AI)
