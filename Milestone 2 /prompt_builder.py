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

    # Pre-defined workout templates for each day (this forces the model to follow structure)
    day1_template = f"""
DAY 1: [FOCUS AREA - Based on {goal}]

WARM-UP (5-10 minutes):
• [Warm-up exercise 1] - [duration]
• [Warm-up exercise 2] - [duration]
• [Warm-up exercise 3] - [duration]

MAIN WORKOUT:
1. [Exercise 1] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
2. [Exercise 2] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
3. [Exercise 3] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
4. [Exercise 4] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds

COOL-DOWN (5-10 minutes):
• [Stretch 1] - [duration]
• [Stretch 2] - [duration]
• [Stretch 3] - [duration]
"""

    # Create the complete 5-day structure with placeholders
    complete_plan = f"""
====================================================
COMPLETE 5-DAY WORKOUT PLAN FOR {name.upper()}
====================================================

CLIENT: {name} | GOAL: {goal} | LEVEL: {fitness_level}

====================================================
{day1_template}

====================================================
DAY 2: [FOCUS AREA - Based on {goal}]

WARM-UP (5-10 minutes):
• [Warm-up exercise 1] - [duration]
• [Warm-up exercise 2] - [duration]
• [Warm-up exercise 3] - [duration]

MAIN WORKOUT:
1. [Exercise 1] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
2. [Exercise 2] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
3. [Exercise 3] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
4. [Exercise 4] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds

COOL-DOWN (5-10 minutes):
• [Stretch 1] - [duration]
• [Stretch 2] - [duration]
• [Stretch 3] - [duration]

====================================================
DAY 3: [FOCUS AREA - Based on {goal}]

WARM-UP (5-10 minutes):
• [Warm-up exercise 1] - [duration]
• [Warm-up exercise 2] - [duration]
• [Warm-up exercise 3] - [duration]

MAIN WORKOUT:
1. [Exercise 1] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
2. [Exercise 2] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
3. [Exercise 3] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
4. [Exercise 4] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds

COOL-DOWN (5-10 minutes):
• [Stretch 1] - [duration]
• [Stretch 2] - [duration]
• [Stretch 3] - [duration]

====================================================
DAY 4: [FOCUS AREA - Based on {goal}]

WARM-UP (5-10 minutes):
• [Warm-up exercise 1] - [duration]
• [Warm-up exercise 2] - [duration]
• [Warm-up exercise 3] - [duration]

MAIN WORKOUT:
1. [Exercise 1] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
2. [Exercise 2] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
3. [Exercise 3] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
4. [Exercise 4] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds

COOL-DOWN (5-10 minutes):
• [Stretch 1] - [duration]
• [Stretch 2] - [duration]
• [Stretch 3] - [duration]

====================================================
DAY 5: [FOCUS AREA - Based on {goal}]

WARM-UP (5-10 minutes):
• [Warm-up exercise 1] - [duration]
• [Warm-up exercise 2] - [duration]
• [Warm-up exercise 3] - [duration]

MAIN WORKOUT:
1. [Exercise 1] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
2. [Exercise 2] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
3. [Exercise 3] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds
4. [Exercise 4] - {fitness_level} level
   • Sets: [X] | Reps: [Y] | Rest: [Z] seconds

COOL-DOWN (5-10 minutes):
• [Stretch 1] - [duration]
• [Stretch 2] - [duration]
• [Stretch 3] - [duration]

====================================================
DAY 6: REST DAY (Active recovery - light walking, stretching)
DAY 7: REST DAY (Complete rest or light activity)
====================================================
"""

    prompt = f"""You are a certified professional fitness trainer. Your task is to create a COMPLETE 5-DAY WORKOUT PLAN.

ABSOLUTELY CRITICAL INSTRUCTION: You MUST fill in ALL 5 DAYS (Day 1 through Day 5) completely. DO NOT stop after Day 1 or Day 2. The response MUST include all 5 days.

CLIENT INFORMATION:
- Name: {name}
- Gender: {gender}
- Height: {height}cm
- Weight: {weight}kg
- BMI: {bmi:.1f} ({bmi_status})
- Primary Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}

SPECIAL CONSIDERATIONS:
- {bmi_considerations.get(bmi_status, "")}
- {goal_focus.get(goal, "")}

Here is the COMPLETE STRUCTURE you MUST follow. Fill in ALL the bracketed information [like this] with actual exercises, sets, reps, and rest times:

{complete_plan}

REQUIREMENTS:
1. Replace ALL [bracketed text] with actual exercises and numbers
2. Choose exercises appropriate for {fitness_level} level
3. Use only exercises that can be done with: {equipment_list}
4. Consider the client's BMI ({bmi_status}) when selecting exercises
5. Make each day different with appropriate focus areas
6. Include specific sets, reps, and rest periods
7. Ensure exercises are safe and effective

DAY FOCUS SUGGESTIONS (based on {goal}):
"""
    
    # Add specific day focus suggestions based on goal
    if goal == "Build Muscle":
        prompt += """
- Day 1: Chest and Triceps
- Day 2: Back and Biceps  
- Day 3: Legs and Core
- Day 4: Shoulders and Arms
- Day 5: Full Body Compound"""
    elif goal == "Weight Loss":
        prompt += """
- Day 1: Full Body HIIT
- Day 2: Upper Body Strength + Cardio
- Day 3: Lower Body Strength + Cardio
- Day 4: Core and Cardio
- Day 5: Full Body Endurance"""
    elif goal == "Strength Gain":
        prompt += """
- Day 1: Push Day (Chest, Shoulders, Triceps)
- Day 2: Pull Day (Back, Biceps)
- Day 3: Leg Day (Quads, Hamstrings, Glutes)
- Day 4: Accessory and Core Work
- Day 5: Full Body Strength"""
    elif goal == "Abs Building":
        prompt += """
- Day 1: Core and Cardio
- Day 2: Upper Body and Core
- Day 3: Lower Body and Core
- Day 4: Core Specialization
- Day 5: Full Body and Core"""
    else:  # Flexible
        prompt += """
- Day 1: Full Body Mobility
- Day 2: Upper Body Flexibility
- Day 3: Lower Body Stretching
- Day 4: Dynamic Movement
- Day 5: Recovery and Flexibility"""

    prompt += """

FINAL REMINDER: You MUST provide a complete 5-day plan. Do not stop early. Fill in every section for all 5 days. The response should be long and detailed, covering Monday through Friday workouts.

Begin your response with "COMPLETE 5-DAY WORKOUT PLAN FOR {name}" and then fill in all the sections above."""
    
    return prompt, bmi, bmi_status
