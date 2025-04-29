import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from mini_project.settings import GENERATIVE_AI_KEY
from chatbot.models import ChatMessage
import google.generativeai as genai
import json
from django.utils.html import escape


# Import training functions from train_chatbot.py
from .train_chatbot import load_and_preprocess_data, train_kmeans_model, main, predict_cluster

# Load pre-trained model and vectorizer
kmeans_model, vectorizer = main()

def home(request):
    return render(request, 'chatbot/home.html')

programming_keywords = ["code", "programming", "language", "python", "java", "c++"]  # Ensure all items are strings

def is_programming_query(message):
    return any(keyword in message.lower() for keyword in programming_keywords)



import logging

logger = logging.getLogger(__name__)


def send_message(request):
    if request.method == 'POST':
        genai.configure(api_key=GENERATIVE_AI_KEY)
        model = genai.GenerativeModel("gemini-pro")

        data = json.loads(request.body)
        user_message = data.get('user_message')

        logger.info(f"Received user message: {user_message}")

        if is_general_greeting(user_message):
            bot_response = get_general_response(user_message)
            logger.info(f"General greeting response: {bot_response}")
        elif is_programming_query(user_message):
            context_programming = "Provide a relevant code snippet or programming advice."
            programming_response = model.generate_content(f"{user_message}\n\n{context_programming}")
            bot_response = escape(programming_response.text).replace("\n", "<br>")
            logger.info(f"Programming response: {bot_response}")
        else:
            # Handle other general queries
            context_0 = "Provide a detailed guide on how to begin with the project, using HTML formatting for clarity."
            context_1 = "Suggest advanced techniques, integrations, and features, using HTML formatting for clarity."
            context_2 = "Provide alternative project ideas and explain their benefits, using HTML formatting for clarity."

            detailed_guide_response = model.generate_content(f"{user_message}\n\n{context_0}")
            advanced_techniques_response = model.generate_content(f"{user_message}\n\n{context_1}")
            alternative_projects_response = model.generate_content(f"{user_message}\n\n{context_2}")

            bot_response = (
                "<strong>0: A detailed guide on how to begin with the project:</strong><br><br>"
                + escape(detailed_guide_response.text).replace("\n", "<br>")
                + "<br><br><strong>1: Suggestions for advanced techniques, integrations, and features:</strong><br><br>"
                + escape(advanced_techniques_response.text).replace("\n", "<br>")
                + "<br><br><strong>2: Alternative project ideas and their benefits:</strong><br><br>"
                + escape(alternative_projects_response.text).replace("\n", "<br>")
            )
            logger.info(f"General query response: {bot_response}")

        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        return JsonResponse({'response': bot_response})

    return JsonResponse({'error': 'Invalid request'}, status=400)

general_responses = {
    'greetings': ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Good morning! How can I help?"],
    'thanks': ["You're welcome!", "No problem!", "Glad to help!"]
}

def is_general_greeting(message):
    greetings = ["hi", "hello", "good morning", "thanks", "thats good", "satisfying"]
    return message.lower() in greetings

def get_general_response(message):
    if message.lower() in ["hi", "hello", "good morning"]:
        return random.choice(general_responses['greetings'])
    elif message.lower() in ["thanks", "thats good", "satisfying"]:
        return random.choice(general_responses['thanks'])
    return None

def list_messages(request):
    messages = ChatMessage.objects.all()
    return render(request, 'chatbot/list_messages.html', { 'messages': messages })

def train_chatbot(request):
    if request.method == 'POST':
        csv_file_path = r'C:\Users\SHAFIA SABA\OneDrive\Desktop\chatbot_query.csv'  # Update this path
        data, vectorizer, feature_vectors = load_and_preprocess_data(csv_file_path)
        kmeans_model = train_kmeans_model(feature_vectors)
        return JsonResponse({'message': 'Chatbot trained successfully!'})

    return JsonResponse({'message': 'Send a POST request to train the chatbot'})