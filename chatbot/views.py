import openai
import os
import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Load API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

print("OpenAI API Key loaded:", bool(openai.api_key))  # For debugging; remove in production

def get_ai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        print("OpenAI ChatCompletion API error:", e)
        traceback.print_exc()
        return "Sorry, I couldn't process your question at the moment."

@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()
            if not user_input:
                return JsonResponse({'response': 'Please enter a valid question.'})

            reply = get_ai_response(user_input)
            return JsonResponse({'response': reply})
        except Exception as e:
            print("Error in chat_response view:", e)
            traceback.print_exc()
            return JsonResponse({'response': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'response': 'Invalid request method.'}, status=400)

def chat_page(request):
    return render(request, 'chatbot/chat.html')
