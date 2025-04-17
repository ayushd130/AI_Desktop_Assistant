import os
import google.generativeai as genai
import datetime
import speech_recognition as sr
import webbrowser
from config import apikey
import pyautogui
import pyttsx3

# Initialize global variables
chatStr = ""

# Initialize the Generative AI configuration
genai.configure(api_key=apikey)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"Ayush: {query}")
            return query
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return "Sorry, there was an error with the request."
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return "Sorry, I didn't catch that."
        except Exception as e:
            print(f"Error: {e}")
            return "Some error occurred. Sorry from Jarvis."

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Ayush: {query}\nJarvis: "

    try:
        # Start a chat session with the model
        chat_session = model.start_chat(
            history=[{"role": "user", "parts": [query]}]
        )
        # Send user input to the model and get response
        response = chat_session.send_message(query)
        chatStr += f"{response.text}\n"
        print(response.text)
        say(response.text)
    except Exception as e:
        print(f"Error in chat function: {e}")
        chatStr += f"Error: {e}\n"
        return "Sorry, I encountered an error while processing your request."

def ai(prompt):
    text = f"Google AI response for Prompt: {prompt}\n*\n\n"
    try:
        # Start a chat session for AI
        chat_session = model.start_chat(history=[{"role": "user", "parts": [prompt]}])
        response = chat_session.send_message(prompt)
        text += response.text

        if not os.path.exists("GoogleAI"):
            os.mkdir("GoogleAI")
        with open(f"GoogleAI/{''.join(prompt.split()).strip()}.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        say(response.text)
    except Exception as e:
        print(f"Error in ai function: {e}")
        text += f"Error: {e}"

    return text

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def screenshot():
    try:
        img = pyautogui.screenshot()
        img_dir = os.path.join(os.path.dirname(os.path.abspath(file)), "pictureSS")
        img_path = os.path.join(img_dir, "ss.png")
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img.save(img_path)
        print(f"Screenshot saved at {img_path}")
    except pyautogui.PyAutoGUIException as e:
        print(f"An error occurred: {e}")

def wishme():
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        say("Good Morning Sir!!")
    elif 12 <= hour < 16:
        say("Good Afternoon Sir!!")
    elif 16 <= hour < 24:
        say("Good Evening Sir!!")
    else:
        say("Good Night Sir, See You Tomorrow")

    say("Jarvis at your service, please tell me how may I help you.")

if name == 'main':
    wishme()

    while True:
        query = takeCommand()

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
        ]

        site_opened = False
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                site_opened = True
                break

        if site_opened:
            continue

        if "open music" in query.lower():
            musicPath = r"C:\Users\Shorya\Music\song6.mp3"
            if os.name == 'nt':
                os.system(f"start {musicPath}")
            elif os.name == 'posix':
                os.system(f"open {musicPath}")

        elif "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {strfTime}")

        elif "search on google" in query.lower():
            try:
                say("What should I search?")
                search = takeCommand()
                search_url = f"https://www.google.com/search?q={search}"
                webbrowser.get('macosx').open_new_tab(search_url)
            except Exception as e:
                say("An error occurred while trying to search on Google.")
                print(f"Error: {e}")

        elif "who are you" in query.lower():
            say("I'm JARVIS created by Mr. Ayush and I'm a desktop voice assistant.")

        elif "how are you" in query.lower():
            say("I'm fine, sir. What about you?")

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "screenshot" in query:
            screenshot()
            say("I've taken a screenshot, please check it.")

        elif "jarvis quit" in query.lower():
            say("Goodbye, Sir.")
            engine.stop()  # Stop pyttsx3 engine before quitting
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            chat(query)