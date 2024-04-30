import os
import requests
import wikipedia
import pywhatkit as kit
import openai
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

load_dotenv()

openai.api_key = "sk-******8"  # Replace with your OpenAI API key

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def find_my_ip():
    ip_address = requests.get('https://www.ipify.org/').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    try:
        wiki_pages = wikipedia.search(query)
        if not wiki_pages:
            return "Sorry, no results found on Wikipedia for that query."
        page = wikipedia.page(wiki_pages[0])
        results = page.content[:500] + "..."
        return results
    except wikipedia.exceptions.PageError as e:
        return f"Sorry, an error occurred while searching Wikipedia: {e}"
    except Exception as e:
        return f"Sorry, an unexpected error occurred: {e}"


def search_on_chatgpt(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    result = response.choices[0].message.content
    return result


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def open_browser(url_to_open=None):
    if url_to_open:
        kit.open_web(f"https://{url_to_open}")
    else:
        kit.open_web()


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Authentication error: {e}")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


def get_news():
    news_headline = []
    api_key = "pub_4272186a9fbec7360df67943ac1a1ef54c4be"  # Your API key
    country = "ke"  # Replace with the desired country code
    api_url = f"https://newsdata.io/api/1/news?apikey={api_key}&country={country}"
    result = requests.get(api_url).json()
    articles = result["results"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]



