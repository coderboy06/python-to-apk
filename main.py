# Import necessary libraries
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import platform
# from firebase_admin import credentials, initialize_app, db
import pyrebase
import speech_recognition as sr
import pyttsx3

Config = {
"apiKey": "AIzaSyBhEvZbXvc6f5_fw8FVX-DHkekSdtcByC4",
"authDomain": "rpi1-28441.firebaseapp.com",
"databaseURL": "https://rpi1-28441-default-rtdb.firebaseio.com",
"projectId": "rpi1-28441",
"storageBucket": "rpi1-28441.appspot.com",
"messagingSenderId": "1033614972637",
"appId": "1:1033614972637:web:842b0f41c17cf62c102d34",
"measurementId": "G-KD8SNQ7WKW"
}

firebase = pyrebase.initialize_app(Config)
ref = firebase.database()

# Initialize Firebase
# cred = credentials.Certificate('C:\\Users\\Aslam Guddad\\wipod\\rpi1-28441-firebase-adminsdk-0qkos-8fef145d5a.json')
# firebase_app = initialize_app(cred, {
#     'databaseURL': 'https://rpi1-28441-default-rtdb.firebaseio.com/'
# })
# ref = db.reference('/')

# Define the main app class
class VoiceAssistantApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Button to trigger voice assistant
        self.button = Button(text='Hit And Ask', on_press=self.start_voice_command)
        layout.add_widget(self.button)

        # Label to display responses
        self.response_label = Label(text='', size_hint_y=1)
        layout.add_widget(self.response_label)

        return layout

    # Function to start voice command
    def start_voice_command(self, instance):
        self.button.text = "Listening..."
        Clock.schedule_once(self.listen_for_command, 0.5)  # Wait for 1 second

    # Function to listen for voice command
    def listen_for_command(self, dt):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            user_query = recognizer.recognize_google(audio)
            self.fetch_response_from_firebase(user_query)
        except sr.UnknownValueError:
            self.response_label.text = "Sorry, I didn't catch that."
        except sr.RequestError:
            self.response_label.text = "Sorry, I couldn't reach the recognition service."
        finally:
            self.button.text = "Hit And Ask"

    # Function to fetch response from Firebase
    def fetch_response_from_firebase(self, user_query):
        response = "Sorry, I couldn't find a response."

        # Access data from Firebase
        try:
            
            if "voltage" in user_query:
                response = ref.child('canbus').child('data').child('voltage').get()
                self.response_label.text = response
                self.speak_out(response)
                
            if "current" in user_query:
                response = ref.child('canbus').child('data').child('current').get()
                self.response_label.text = response
                self.speak_out(response)
                
            if "soc" in user_query:
                response = ref.child('canbus').child('data').child('soc').get()
                self.response_label.text = response
                self.speak_out(response)
            if "steering angle" in user_query:
                response = ref.child('canbus').child('data').child('steerfb').get()
                self.response_label.text = response
                self.speak_out(response)
            if "turn the steering right" in user_query:
                response = ref.child('canbus').child('data').child('TRsteer').set(750)
                self.response_label.text = "please move aside steering is moving right side"                
                self.speak_out('please move aside steering is moving right side..')
            if "turn the steering left" in user_query:
                response = ref.child('canbus').child('data').child('TLsteer').set(350)
                self.response_label.text = "please move aside steering is moving right side"
                self.speak_out('please move aside steering is moving left side..')
                
            if "turn on lights" in user_query:
                response = ref.child('canbus').child('data').child('lights').set('on')
                self.response_label.text = "the lights are turning on."
                self.speak_out('The lights are turing on..')
                
            
            if "turn of lights" in user_query:
                response = ref.child('canbus').child('data').child('lights').set('off')
                self.response_label.text = "the lights are turning off"
                self.speak_out('The lights are turing off..')
                
            if "open the windows" in user_query:
                response = ref.child('canbus').child('data').child('window').set('open')
                self.response_label.text = "please be aware the windows are opening.."
                self.speak_out('please be aware the windows are opening..')
                
            if "close the windows" in user_query:
                response = ref.child('canbus').child('data').child('window').set('close')
                self.response_label.text = "please be aware the windows are closing.."
                self.speak_out('please be aware the windows are closing..')
                
            if "open the doors" in user_query:
                response = ref.child('canbus').child('data').child('doors').set('open')
                self.response_label.text = "please be aside door is opening.."
                self.speak_out("please be aside door is opening..")
                
            if "close the doors" in user_query:
                response = ref.child('canbus').child('data').child('doors').set('close')
                self.response_label.text = "please be aside door is closing.."
                self.speak_out('please be aside door is closing..')
            
            if "go back" in user_query:
                response = ref.child('canbus').child('data').child('reverse').set(200)
                self.response_label.text = "please be aside wipod 2.0 is moving back.."
                self.speak_out('please be aside wipod 2.0 is moving back..')
                
            if "press the brake" in user_query:
                response = ref.child('canbus').child('data').child('brake').set(250)
                self.response_label.text = "please hold the seat the wipod 2.0 is  applying brake now .."
                self.speak_out('please be hold your seat the wipod 2.0 is applying brake now..')
                
            if "release the brake" in user_query:
                response = ref.child('canbus').child('data').child('brake').set(0)
                self.response_label.text = "please hold the seat the wipod 2.0 is  releasing brake now .."
                self.speak_out('please be hold your seat the wipod 2.0 is releasing brake now..')
                
            if "go forward" in user_query:
                response = ref.child('canbus').child('data').child('forward').set(200)
                self.response_label.text = "please be aside wipod 2.0 is moving forward.."
                self.speak_out('please be aside wipod 2.0 is moving forward..')
                
            
            # if response:
            #     self.speak_out(response)
            # else:
            #     self.response_label.text = "Sorry, I couldn't find a response."
        except Exception as e:
            self.speak_out("Error fetching response from Firebase")
            print("Error fetching response from Firebase:", e)

    # Function to speak out the response
    def speak_out(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()

# Run the app
if __name__ == '__main__':
    VoiceAssistantApp().run()
