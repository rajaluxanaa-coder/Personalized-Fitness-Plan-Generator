"""
Build structured prompts for AI workout generation
"""

def build_workout_prompt(user, goal, level, equipment):
    """Build a structured prompt for workout generation"""
    
    goal_focus = {
        'weight_loss': 'HIIT, cardio, and circuits',
        'muscle_gain': 'progressive overload, hypertrophy',
        'strength': 'compound lifts, power movements',
        'endurance': 'higher reps, shorter rest',
        'general': 'balanced approach'
    }
    
    focus = goal_focus.get(goal, goal_focus['general'])
    
    return f"""Create a 5-day workout schedule for {user.name}.

USER PROFILE:
- Age: {user.age}
- Weight: {user.weight}kg
- Height: {user.height}cm
- Level: {level}
- Goal: {goal} - {focus}
- Equipment: {equipment}

FORMAT:
DAY 1: [Focus]
1. [Exercise] - [sets]x[reps]
2. [Exercise] - [sets]x[reps]
3. [Exercise] - [sets]x[reps]
4. [Exercise] - [sets]x[reps]
5. [Exercise] - [sets]x[reps]

Repeat for DAYS 2-5. Make each day different."""
