"""
AI model integration with fallback mechanisms
"""

import requests
import os
import time

def generate_workout_with_ai(prompt, user, goal, level, equipment):
    """Generate workout with multiple model fallbacks"""
    
    groq_key = os.getenv('GROQ_API_KEY')
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]
    
    for model in models:
        try:
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a professional fitness trainer."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1500
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                schedule = result['choices'][0]['message']['content']
                if "DAY 5" in schedule and len(schedule) > 300:
                    return schedule
                    
        except Exception as e:
            print(f"Model {model} failed: {str(e)}")
            time.sleep(1)
            continue
    
    # Fallback to template
    return generate_fallback_template(user, goal, level, equipment)

def generate_fallback_template(user, goal, level, equipment):
    """Generate fallback template when AI fails"""
    sets = 3 if level == 'beginner' else 4
    reps = "10-12" if level == 'beginner' else "8-10" if level == 'intermediate' else "6-8"
    
    return f"""5-DAY WORKOUT PLAN (Template)
For: {user.name} | Goal: {goal} | Level: {level}

DAY 1: Upper Body
1. Push-ups - {sets} x {reps}
2. Rows - {sets} x {reps}
3. Shoulder Press - {sets} x {reps}
4. Bicep Curls - {sets} x {reps}
5. Tricep Dips - {sets} x {reps}

DAY 2: Lower Body
1. Squats - {sets} x {reps}
2. Lunges - {sets} x {reps}
3. Glute Bridges - {sets} x {reps}
4. Calf Raises - {sets} x 15
5. Step-ups - {sets} x {reps}

DAY 3: Core & Cardio
1. Planks - 3 x 45 sec
2. Mountain Climbers - 3 x 30 sec
3. Crunches - 3 x 15
4. Leg Raises - 3 x 12
5. Jumping Jacks - 3 x 30 sec

DAY 4: Full Body
1. Burpees - 3 x 8
2. Squat to Press - {sets} x {reps}
3. Lunges - {sets} x {reps}
4. Push-ups - {sets} x {reps}
5. Plank - 3 x 45 sec

DAY 5: Active Recovery
1. Light walking - 20 min
2. Full body stretching - 15 min
3. Deep breathing - 5 min
"""
