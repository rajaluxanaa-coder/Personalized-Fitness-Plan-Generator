# In prompt_builder.py, update the function signature and add age to the prompt:

def build_prompt(name, age, gender, height_cm, weight, fitness_goal, fitness_level, equipment):
    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    # Determine BMI status
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"
    
    # Build prompt with age included
    prompt = f"""
    Create a 5-day workout plan for:
    - Name: {name}
    - Age: {age}
    - Gender: {gender}
    - Height: {height_cm} cm
    - Weight: {weight} kg
    - BMI: {bmi:.1f} ({bmi_status})
    - Fitness Goal: {fitness_goal}
    - Fitness Level: {fitness_level}
    - Available Equipment: {', '.join(equipment)}
    
    Please provide a detailed day-by-day workout plan considering age and fitness level.
    """
    
    return prompt, bmi, bmi_status
