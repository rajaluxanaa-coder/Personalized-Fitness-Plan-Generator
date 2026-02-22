from huggingface_hub import InferenceClient
import os

def query_model(prompt):
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")

        client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=HF_TOKEN
        )

        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a certified professional fitness trainer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
