import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, Owais!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Owais!")   
    else:
        speak("Good Evening, Owais!")  
    speak("I am Jarvis, Owais. Please tell me how may I help you.")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

def getWeather(city):
    api_key = '3663dcf79813a8eb81cce073a1d3c999' # Your actual API key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    if data['cod'] == 200:
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        speak(f"Sorry, I couldn't find the weather for {city}. Error: {data['message']}")

def getNews():
    api_key = '15c3cd563c534ea297ef931ff8625994'  # Your actual API key
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    news = response.json()
    articles = news['articles']
    headlines = [article['title'] for article in articles]
    for i, headline in enumerate(headlines[:5]):
        speak(f"News {i+1}: {headline}")

def setReminder(reminder):
    with open('reminders.txt', 'a') as file:
        file.write(reminder + '\n')
    speak("Reminder has been set.")

def getReminders():
    if os.path.exists('reminders.txt'):
        with open('reminders.txt', 'r') as file:
            reminders = file.readlines()
        if reminders:
            speak("Here are your reminders:")
            for reminder in reminders:
                speak(reminder.strip())
        else:
            speak("You have no reminders set.")
    else:
        speak("You have no reminders set.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        print(f"Query received: {query}") 
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any results for your query.")
                print("PageError: No results found.")  
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for your query. Please be more specific.")
                print(f"DisambiguationError: {e.options}")  
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open instagram' in query:
            webbrowser.open("instagram.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open whatsapp' in query:
            webbrowser.open("whatsapp.com")   
        elif 'play music' in query:
            music_dir = "C:\\Users\\admin\\Music"  # Update with your music directory
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Owais, the time is {strTime}.")
        elif 'open code folder' in query:
            codePath = "D:\\Python"  # Update with your code folder path
            os.startfile(codePath)
        elif 'news' in query:
            getNews()
        elif 'set reminder' in query:
            speak("What should I remind you about?")
            reminder = takeCommand()
            setReminder(reminder)
        elif 'show my reminders' in query:
            getReminders()
        elif 'what is the weather in' in query:
            city = query.replace("what is the weather in", "").strip()
            print(f"City to check: {city}")  # Debugging output
            getWeather(city)
        else:
            print("No query matched")
