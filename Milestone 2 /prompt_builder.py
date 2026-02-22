def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def build_prompt(name, gender, height, weight, goal, fitness_level, equipment):
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)
    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    # BMI-specific considerations
    bmi_considerations = {
        "Underweight": "Focus on muscle building and nutrient-dense foods. Avoid excessive cardio.",
        "Normal Weight": "Maintain balanced approach with focus on specific goals.",
        "Overweight": "Include cardio for fat loss, start with low-impact exercises to protect joints.",
        "Obese": "Focus on low-impact exercises, prioritize consistency over intensity, consult doctor before starting."
    }

    # Goal-specific focus
    goal_focus = {
        "Build Muscle": "Focus on hypertrophy with moderate weights and higher reps. Include compound exercises.",
        "Weight Loss": "Combine strength training with cardio. Focus on full-body workouts and HIIT.",
        "Strength Gain": "Focus on compound lifts with lower reps and heavier weights. Include progressive overload.",
        "Abs Building": "Combine core-specific exercises with overall fat loss strategies.",
        "Flexible": "Include dynamic stretching, mobility work, and flexibility training."
    }

    prompt = f"""As a certified professional fitness trainer, create a DETAILED 5-day workout plan for the following client:

CLIENT PROFILE:
- Name: {name}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.1f} ({bmi_status})
- Primary Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}

SPECIAL CONSIDERATIONS:
- BMI Consideration: {bmi_considerations.get(bmi_status, "")}
- Goal Focus: {goal_focus.get(goal, "")}

REQUIREMENTS FOR THE WORKOUT PLAN:
1. Create a COMPLETE 5-day schedule (Monday to Friday)
2. For EACH day, provide:
   - Warm-up (5-10 minutes)
   - Main workout (include ALL these details for each exercise):
     * Exercise name
     * Sets and reps (e.g., 3x12)
     * Rest period between sets
   - Cool-down (5-10 minutes)
3. Adjust exercise intensity and complexity based on fitness level ({fitness_level})
4. Ensure exercises are safe and appropriate for the equipment available
5. Include rest days on weekends
6. Format the response with clear headings for each day

Please provide the complete 5-day plan in this exact format:

DAY 1 (Focus: [focus area])
WARM-UP:
- [exercise] - [duration/reps]

MAIN WORKOUT:
1. [exercise] - [sets]x[reps] - Rest: [time]
2. [exercise] - [sets]x[reps] - Rest: [time]
3. [exercise] - [sets]x[reps] - Rest: [time]
4. [exercise] - [sets]x[reps] - Rest: [time]

COOL-DOWN:
- [stretch] - [duration]

[Repeat this exact format for Days 2, 3, 4, and 5]

Ensure the plan is practical, achievable, and tailored to the client's specific needs and available equipment."""
    
    return prompt, bmi, bmi_status
