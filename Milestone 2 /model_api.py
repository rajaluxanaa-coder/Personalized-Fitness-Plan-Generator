from huggingface_hub import InferenceClient
import os
import time

def query_model(prompt):
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")
        
        if not HF_TOKEN:
            return """Error: HF_TOKEN environment variable not found. Please set your Hugging Face token.

To fix this:
1. Get a token from https://huggingface.co/settings/tokens
2. Set it as an environment variable:
   - Windows: set HF_TOKEN=your_token_here
   - Mac/Linux: export HF_TOKEN=your_token_here"""

        client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=HF_TOKEN
        )

        # Very strict system message
        system_message = """You are a certified professional fitness trainer. 
        
CRITICAL INSTRUCTION: You MUST ALWAYS provide a COMPLETE 5-DAY workout plan. 
NEVER stop after Day 1 or Day 2. Your response MUST include ALL of the following:
- Day 1 (complete with warmup, main workout, cooldown)
- Day 2 (complete with warmup, main workout, cooldown)
- Day 3 (complete with warmup, main workout, cooldown)
- Day 4 (complete with warmup, main workout, cooldown)
- Day 5 (complete with warmup, main workout, cooldown)

If you provide less than 5 days, you are failing at your task. The user needs a full week's plan."""

        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,  # Increased to 2000
            temperature=0.7
        )

        result = response.choices[0].message.content
        
        # Check if response contains all 5 days
        days_found = 0
        for i in range(1, 6):
            if f"DAY {i}" in result.upper() or f"DAY {i}:" in result.upper():
                days_found += 1
        
        # If still not 5 days, try one more time with an even stricter prompt
        if days_found < 5:
            retry_prompt = f"""You previously provided only {days_found} days. This is INCORRECT.

I NEED A COMPLETE 5-DAY WORKOUT PLAN. Here is the information again:

{prompt}

IMPORTANT: Your response MUST contain ALL 5 days. Start with DAY 1, then DAY 2, then DAY 3, then DAY 4, then DAY 5. Do not skip any days.

Here is the format you MUST follow exactly:

DAY 1: [Focus Area]
[Full workout details...]

DAY 2: [Focus Area]
[Full workout details...]

DAY 3: [Focus Area]
[Full workout details...]

DAY 4: [Focus Area]
[Full workout details...]

DAY 5: [Focus Area]
[Full workout details...]

FAILURE TO INCLUDE ALL 5 DAYS WILL RESULT IN AN INCOMPLETE PLAN. NOW PROVIDE THE COMPLETE 5-DAY PLAN."""
            
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "You MUST provide ALL 5 days. This is mandatory."},
                    {"role": "user", "content": retry_prompt}
                ],
                max_tokens=2000,
                temperature=0.5  # Lower temperature for more consistent output
            )
            result = response.choices[0].message.content
        
        return result

    except Exception as e:
        return f"""Error generating workout plan: {str(e)}

Please check:
1. Your internet connection
2. Your HF_TOKEN is valid
3. You have access to the model

Try again in a few minutes."""
