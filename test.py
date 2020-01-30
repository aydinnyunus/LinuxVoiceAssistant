import speech_recognition as sr  # recognise speech
import playsound  # to play an audio file
from PIL import ImageTk
from gtts import gTTS  # google text to speech
import random
from time import ctime  # get time details
import webbrowser  # open browser
import yfinance as yf  # to fetch financial data
import time
import os  # to remove created audio files
import pyautogui
import re
import tkinter as tk
import PIL
import importlib


class FullScreenApp(object):
    def __init__(self, root, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


# bind click event to image

# button with image binded to the same function

class Person:
    name = ''
    phone_number = ''
    messages = ''

    def setName(self, name):
        self.name = name

    def Target(self, phone_number):
        self.phone_number = phone_number

    def Messages(self, messages):
        self.messages = messages


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialise a recogniser


# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')  # text to speech(voice)
    r = random.randint(1, 20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    playsound.playsound(audio_file)  # play the audio file
    l1 = tk.Label(master, text=f"Kira: {audio_string}", bg="black", fg="white")

    canvas1.create_window(670, 635, window=l1)

    os.remove(audio_file)  # remove audio file


def respond(voice_data):
    global person_messages
    import time
    person_obj = Person()

    # 1: greeting
    if there_exists(['hey', 'hi', 'hello', "kira"]):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}",
                     f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        speak(greet)

    # 2: name
    elif there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            speak("my name is Kira")
        else:
            speak("my name is Kira. what's your name?")

    elif there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object

    # 3: greeting
    elif there_exists(["how are you", "how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    elif there_exists(["who creates you", "who create you"]):
        speak(f"My owner is Yunus AYDIN and God creates my owner.")

    elif there_exists(["can you make me laugh", "make me laugh"]):
        speak(f"Yeah of course")
        url = f"https://www.youtube.com/watch?v=Y9QfSKuTjxI"
        webbrowser.get().open(url)

    # 4: time
    elif there_exists(["what's the time", "tell me the time", "what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    # 5: search google
    elif there_exists(["search for"]) and 'youtube' not in voice_data and 'github' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    elif there_exists(["github"]) and 'youtube' not in voice_data and 'google' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://github.com/search?q=+{search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on github')

    # 6: search youtube
    elif there_exists(["youtube"]) and 'google' not in voice_data and 'google' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')
        time.sleep(5)
        pyautogui.click(x=333, y=333)

    # 7: get stock price
    elif there_exists(["price of"]):
        search_term = voice_data.lower().split(" of ")[
            -1].strip()  # strip removes whitespace after/before a term in string
        stocks = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "facebook": "FB",
            "tesla": "TSLA",
            "bitcoin": "BTC-USD"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            speak(f'price of {search_term} is {price} {stock.info["currency"]} {person_obj.name}')
        except:
            speak('oops, something went wrong')

    elif there_exists(["Message is", "message is", "messages is", "Messages is"]):
        person_messages = voice_data.split("is")[-1].strip()
        person_obj.Messages(person_messages)  # remember name in person object
        speak("Message received")
        # 905377672814

    elif there_exists(["Target is", "target is", "phone number is", "Phone number is"]):
        person_phone_number = voice_data.split("is")[-1].strip()
        person_phone_number = re.sub('-', '', person_phone_number, re.I)
        person_phone_number = person_phone_number.replace(" for", "4")
        speak(f"Okay message is sending.Do you want to enter text ?")
        time.sleep(3)
        person_obj.Target(person_phone_number)  # remember name in person object
        url = "https://web.whatsapp.com/send?phone={}&source=&data=#".format(person_obj.phone_number)
        time.sleep(3)
        webbrowser.get().open(url)
        time.sleep(5)
        speak("Whatsapp is opening")
        for i in range(10):
            pyautogui.moveTo(592, 696)
            pyautogui.click(x=592, y=696)
            pyautogui.typewrite(person_messages)
            pyautogui.press('enter')

    elif there_exists(["exit", "quit", "goodbye", "good bye", "bye"]):
        speak("going offline")
        exit()

    elif there_exists(["open"]):
        application = voice_data.split("the")[-1].strip()
        if application == "calculator":
            os.system("gnome-calculator")
        elif application == "calendar":
            os.system("gnome-calendar")
        elif application == ["terminal", "command line"]:
            os.system("gnome-terminal")

    elif there_exists(["screenshot", "ss"]):
        os.system("gnome-screenshot")

    elif there_exists(["video", "screen video"]):
        try:
            os.system("sudo apt install kazam")

        except SystemError:
            os.system("kazam")
        os.system("kazam")

    elif there_exists(["camera", "cam", "am i beautiful", "am i handsome"]):
        try:
            os.system("sudo apt install cheese")

        except SystemError:
            os.system("cheese")
        os.system("cheese")

    elif there_exists(["restart", "reboot"]):
        sure = record_audio('Are you sure ?')
        sure = record_audio()
        time.sleep(2)
        if 'yes' in sure:
            os.system("reboot")

    elif there_exists(["close", "shut down", "shutdown"]):
        sure = record_audio('Are you sure ?')
        sure = record_audio()
        time.sleep(2)
        if 'yes' in sure:
            os.system("reboot")

    elif there_exists(['watch', 'netflix']):
        watchs = voice_data.split("watch")[-1]
        url = f"https://google.com/search?q={watchs}"
        webbrowser.get().open(url)
        time.sleep(10)
        pyautogui.moveTo(200, 315)
        pyautogui.click(x=200, y=315)
        speak('Have a good time')

    elif there_exists(["set alarm", "alarm"]):
        try:
            os.system("sudo apt-get install vlc-bin")

        except SystemError:
            os.system("sudo apt-get install vlc-bin")
        alarm = voice_data.split("alarm")[-1]
        os.system("sleep {}h && vlc alarm.mp3".format(alarm))

    elif there_exists(["timer", "set timer"]) and "alarm" not in voice_data:
        time = voice_data.split("for")[-1].strip()
        os.system("sleep {} && vlc alarm.mp3".format(time))

    elif there_exists(["cancel alarm"]):
        pyautogui.hotkey('ctrlleft', 'c')

    elif there_exists(["roll a die"]):
        rand = random.randint(1, 6)
        speak("Result is {}".format(rand))

    elif there_exists(["flip a coin"]):
        coin = ['heads'] * 50 + ['tails'] * 50 + ['perpendicular'] * 1
        speak(random.choice(coin))

    elif voice_data == "what time is it in":
        location = voice_data.split("in")[-1].strip()
        url = "https://www.google.com/search?q=what+time+is+it+in+{}".format(location)
        webbrowser.get().open(url)

    elif "how much is" in voice_data:
        convert = voice_data.split("is")[-1].strip()  # 5 dollar in euros
        url = f"https://www.google.com/search?q=how+much+is+{convert}"
        webbrowser.get().open(url)

    elif there_exists(["calculate"]):
        search = voice_data.split("calculate")[-1].strip()
        url = f"https://www.google.com/search?q=how+much+is+{search}"
        webbrowser.get().open(url)

    elif there_exists(["what is"]):
        search = voice_data.split("is")[-1].strip()
        url = f"https://www.google.com/search?q=how+much+is+{search}"
        webbrowser.get().open(url)

    elif there_exists(["pip"]):
        package = voice_data.split("install")[-1]

        try:
            os.system("pip install {}".format(package))
            importlib.import_module(package)
        except ImportError:
            speak("Import ERROR")

    elif there_exists(["update", "update the system"]):
        os.system("sudo -S apt update")
        os.system("sudo -S apt upgrade")

    elif there_exists(["take note", "note"]):
        text_file = open("sample.txt", "w")
        note = record_audio('Are you sure ?')
        note = record_audio()
        text_file.write(note)
        text_file.close()

    elif "count to" in voice_data:
        count = voice_data.split("to")[-1].strip()
        for i in range(int(count)):
            speak(str(i+1))

    elif there_exists(["telegram message to"]):
        data = voice_data.split("to")[-1].strip()
        url = "https://web.telegram.org/#/im?p=@{}".format(data)
        time.sleep(3)
        webbrowser.get().open(url)

    elif there_exists(["call me"]):
        nickname = voice_data.split("me")[-1].strip()
        person_obj.setName(nickname)

    elif there_exists(["increase sound", "incrase volume"]):
        os.system("pactl -- set-sink-volume 0 +10%")

    elif there_exists(["decrease sound", "decrease volume"]):
        os.system("pactl -- set-sink-volume 0 -10%")

    elif there_exists(["find location"]):
        location = record_audio('Which location you want to search for')
        location = record_audio()
        url = 'https://google.nl/maps/place' + str(location)
        webbrowser.get().open(url)
        speak("here is your location" + str(location) + '/&amp;')

    elif there_exists(["search for viki", "vikipedia"]):
        concept = record_audio('Which concept you want to search for')
        concept = record_audio()
        url = 'https://wikipedia.org/wiki/' + str(concept)
        webbrowser.get().open(url)

    elif there_exists(["translate"]):
        words = record_audio('Which word you want to translate for')
        words = record_audio()
        url = 'https://translate.google.com/?hl=tr#view=home&op=translate&sl=auto&tl=tr&text=' + str(words)
        webbrowser.get().open(url)

    elif there_exists(["increase brigh", "brighter"]):
        os.system("xrandr --output VGA1 --brightness 1")
        os.system("xrandr --output Virtual1 --brightness 1")

    elif there_exists(["decrease brigh"]):
        os.system("xrandr --output VGA1 --brightness 0.1")
        os.system("xrandr --output Virtual1 --brightness 0.1")

    elif there_exists(["enable bluetooth"]):
        os.system("sudo service bluetooth start")

    elif there_exists(["disable bluetooth"]):
        os.system("sudo service bluetooth stop")

    elif there_exists(["lock"]):
        pyautogui.hotkey('ctrlleft', 'altleft', 'l')

    elif there_exists(["ping to"]):
        site = voice_data.split("to")[-1].strip()
        os.system("ping {}".format(site))

    elif there_exists(["calendar"]):
        os.system("cal")

    elif there_exists(["who is"]):
        os.system("sudo apt install whois")
        who = record_audio('Which word you want to translate for')
        who = record_audio()
        os.system("whois {}".format(who))

    elif there_exists(["pycharm", "code with python"]):
        os.system("charm")

    elif there_exists(["install sublime text"]):
        os.system("wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -")
        os.system('echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee '
                  '/etc/apt/sources.list.d/sublime-text.list')
        os.system("sudo apt-get install sublime-text")
        os.system("sublime-text")

    elif there_exists(["summarize"]):
        subject = voice_data.split("summarize")[-1].strip()
        url = f"https://google.com/search?q={subject}summarize"
        webbrowser.get().open(url)
        # TODO : ADD BETTER SOLUTION

    elif there_exists(["what’s the weather like today?", "do I need an umbrella today?", "what’s the weather going to "
                                                                                         "be like", "what’s the "
                                                                                                    "temperature "
                                                                                                    "outside?",
                       "is there a chance of rain on"]):
        url = f"https://google.com/search?q=weather"
        webbrowser.get().open(url)

    elif there_exists(["to do"]):
        os.system("sudo add-apt-repository ppa:mank319/go-for-it")
        os.system("sudo apt update && sudo apt install go-for-it")
        # TODO : ADD TO DO LIST WITH SPEECH

    elif there_exists(["remind me"]):
        os.system("sudo add-apt-repository ppa:umang/indicator-stickynotes")
        os.system("sudo apt-get install indicator-stickynotes")
        os.system("indicator-stickynotes")
        # TODO : ADD TO DO LIST WITH SPEECH

    elif there_exists(["what’s the traffic like on the way to work"]):
        url = f"https://www.google.com/search?q=what%E2%80%99s+the+traffic+like+on+the+way+to+work"
        webbrowser.get().open(url)

    elif there_exists(["find my phone"]):
        url = f"https://www.google.com/android/find"
        webbrowser.get().open(url)


master = tk.Tk()
app = FullScreenApp(master)
master.title("Linux Assistant")
width = 1280
height = 800

# load the .gif image file
# canvas1.create_line(15, 25, 200, 25)

# canvas1.create_line(55, 85, 155, 85, 105, 180, 55, 85)
# canvas1.create_text(400, 10, fill="black", font="Times 20 italic bold",
#                  text="Whatsapp Bot")

canvas1 = tk.Canvas(master, width=width, height=height, relief='raised', bg='white')
canvas1.pack()
# load image
photo = ImageTk.PhotoImage(file="photo5875314613397074278.jpg")
canvas1.create_image(width / 2, height / 2, image=photo)

# label with image

while True:
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond
    master.mainloop()


