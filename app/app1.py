import sys
import os
import random
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QCalendarWidget, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, QLocale
from playsound import playsound

class MeditationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meditation App')
        self.setGeometry(100, 100, 400, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        self.instruction_label = QLabel('Welcome to Meditation App')
        layout.addWidget(self.instruction_label)
        
        self.audio_combobox = QComboBox()
        self.audio_combobox.addItems(['Select Audio', 'Rain Sounds', 'Forest Sounds', 'Ocean Waves'])
        layout.addWidget(self.audio_combobox)
        
        self.duration_combobox = QComboBox()
        self.duration_combobox.addItems(['Select Duration', '5 minutes', '10 minutes', '30 minutes', '1 hour'])
        layout.addWidget(self.duration_combobox)
        
        self.start_button = QPushButton('Start Meditation')
        self.start_button.clicked.connect(self.start_meditation)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_audio)
        layout.addWidget(self.stop_button)
        self.stop_button.setVisible(False)
        
        self.animation_label = QLabel()
        layout.addWidget(self.animation_label)
        self.animation_label.setVisible(False)
        
        self.audio_files = {
            'Rain Sounds': 'rain.wav',
            'Forest Sounds': 'forest.wav',
            'Ocean Waves': 'ocean.wav'
        }
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_picture)
        self.animation_step = 0
        
    def start_meditation(self):
        selected_audio = self.audio_combobox.currentText()
        selected_duration = self.duration_combobox.currentText()
        
        if selected_audio == 'Select Audio':
            self.instruction_label.setText('Please select an audio')
            return
        elif selected_duration == 'Select Duration':
            self.instruction_label.setText('Please select a duration')
            return
        
        self.instruction_label.setText('Meditation in progress...')
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.animation_label.setVisible(True)
        
        # Set the pixmap to display the calming image
        calming_image_path = '1.jpg'  # Replace 'calming_image.jpg' with the path to your calming image
        pixmap = QPixmap(calming_image_path)
        self.animation_label.setPixmap(pixmap)
        
        # Start animation timer
        self.animation_timer.start(100)  # Set interval for animation update
        
        audio_file = self.audio_files[selected_audio]
        audio_path = os.path.join('audio', audio_file)
        
        duration_mapping = {'5 minutes': 300, '10 minutes': 600, '30 minutes': 1800, '1 hour': 3600}
        duration = duration_mapping[selected_duration]
        
        start_time = time.time()
        while time.time() - start_time < duration:
            playsound(audio_path)
        
        self.instruction_label.setText('Meditation completed')
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.animation_label.setVisible(False)
        
        # Stop animation timer
        self.animation_timer.stop()
        
    def stop_audio(self):
        playsound(False)  # Stops currently playing audio
        self.instruction_label.setText('Meditation stopped')
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.animation_label.setVisible(False)
        
        # Stop animation timer
        self.animation_timer.stop()
        
    def animate_picture(self):
        # Move the picture
        self.animation_step += 1
        dx = 5  # Change in x-coordinate for each step
        dy = 2  # Change in y-coordinate for each step
        new_pos = self.animation_label.pos() + QPoint(dx, dy)
        self.animation_label.move(new_pos)

class JournalApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Journal Application")
        layout = QVBoxLayout()

        self.language_label = QLabel("Select Language:")
        layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Swedish", "Japanese", "Chinese", "Greek", "Italian", "Spanish"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)

        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.setLayout(layout)

        self.calendar.clicked.connect(self.date_selected)  # Connect clicked signal to date_selected method

    def change_language(self, index):
        language = self.language_combo.currentText()
        if language == "English":
            self.calendar.setLocale(QLocale(QLocale.English))
        elif language == "Swedish":
            self.calendar.setLocale(QLocale(QLocale.Swedish))
        elif language == "Japanese":
            self.calendar.setLocale(QLocale(QLocale.Japanese))
        elif language == "Chinese":
            self.calendar.setLocale(QLocale(QLocale.Chinese))
        elif language == "Greek":
            self.calendar.setLocale(QLocale(QLocale.Greek))
        elif language == "Italian":
            self.calendar.setLocale(QLocale(QLocale.Italian))
        elif language == "Spanish":
            self.calendar.setLocale(QLocale(QLocale.Spanish))

    def date_selected(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        window = JournalPage(selected_date)
        window.exec_()


class JournalPage(QDialog):
    def __init__(self, selected_date):
        super().__init__()
        self.setWindowTitle("Journal")
        self.selected_date = selected_date
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_entry)
        layout.addWidget(self.btn_clear)

        self.btn_modify = QPushButton("Modify")
        self.btn_modify.clicked.connect(self.modify_entry)
        layout.addWidget(self.btn_modify)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_entry)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

        # Load existing entry if available
        filename = selected_date + ".txt"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                content = f.read()
                self.text_edit.setPlainText(content)

    def clear_entry(self):
        self.text_edit.clear()

    def modify_entry(self):
        self.text_edit.setReadOnly(False)

    def save_entry(self):
        content = self.text_edit.toPlainText()
        create_or_update_entry(self.selected_date, content)
        self.accept()


def create_or_update_entry(selected_date, content):
    filename = selected_date + ".txt"
    with open(filename, "w") as f:
        f.write(content)


class MoodTracker(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mood Tracker")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.mood_label = QLabel("Select Mood:")
        layout.addWidget(self.mood_label)

        self.mood_combo = QComboBox()
        self.mood_combo.addItems(['Select Mood', 'Happy', 'Sad', 'Anxious', 'Calm', 'Stressed'])
        layout.addWidget(self.mood_combo)

        self.symptoms_label = QLabel("Enter Symptoms:")
        layout.addWidget(self.symptoms_label)

        self.symptoms_edit = QTextEdit()
        layout.addWidget(self.symptoms_edit)

        self.triggers_label = QLabel("Enter Triggers:")
        layout.addWidget(self.triggers_label)

        self.triggers_edit = QTextEdit()
        layout.addWidget(self.triggers_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_entry)  # Connect save_button to save_entry method
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_entry(self):
        mood = self.mood_combo.currentText()
        symptoms = self.symptoms_edit.toPlainText()
        triggers = self.triggers_edit.toPlainText()

        # Save mood entry to file or database
        # Here you can implement your logic to save the mood entry with symptoms and triggers
        filename = "mood_entries.txt"
        with open(filename, "a") as f:
            f.write(f"Mood: {mood}\nSymptoms: {symptoms}\nTriggers: {triggers}\n\n")

        self.close()  # Close the Mood Tracker dialog after saving

class TherapistMatching(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Therapist Matching")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.btn_search = QPushButton("Search Therapists")
        layout.addWidget(self.btn_search)
        
class Chatbot(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_message(self):
        message = self.input_field.text()
        self.input_field.clear()
        self.chat_history.append(f"You: {message}")

        # Implement chatbot logic here to generate a response
        # For now, let's just echo the user's message as a response
        self.chat_history.append("Chatbot: " + message)
        
class PeerSupport(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Peer Support and Community")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_message(self):
        message = self.input_field.text()
        self.input_field.clear()
        self.chat_history.append(f"You: {message}")

        # Implement peer support and community chat logic here
        # For now, let's just echo the user's message as a response
        self.chat_history.append("Peer: " + message)
        
        
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        layout = QVBoxLayout()

        self.btn_meditation = QPushButton("Meditation")
        self.btn_meditation.clicked.connect(self.open_meditation)
        layout.addWidget(self.btn_meditation)

        self.btn_journal = QPushButton("Journal")
        self.btn_journal.clicked.connect(self.open_journal)
        layout.addWidget(self.btn_journal)

        self.btn_mood_tracker = QPushButton("Mood Tracker")  # Add Mood Tracker button
        self.btn_mood_tracker.clicked.connect(self.open_mood_tracker)
        layout.addWidget(self.btn_mood_tracker)

        self.btn_therapist_matching = QPushButton("Therapist Matching")  # Add Therapist Matching button
        self.btn_therapist_matching.clicked.connect(self.open_therapist_matching)  # Connect button to method
        layout.addWidget(self.btn_therapist_matching)

        self.btn_chatbot = QPushButton("Chatbot")  # Add Chatbot button
        self.btn_chatbot.clicked.connect(self.open_chatbot)  # Connect button to method
        layout.addWidget(self.btn_chatbot)
        
        self.btn_peer_support = QPushButton("Peer Support and Community")  # Add Peer Support button
        self.btn_peer_support.clicked.connect(self.open_peer_support)  # Connect button to method
        layout.addWidget(self.btn_peer_support)
        
        self.btn_feedback = QPushButton("Feedback")  # Add Feedback button
        self.btn_feedback.clicked.connect(self.open_feedback)  # Connect button to method
        layout.addWidget(self.btn_feedback)
        
        self.setLayout(layout)

    def open_meditation(self):
        self.meditation_app = MeditationApp()
        self.meditation_app.show()

    def open_journal(self):
        self.journal_app = JournalApp()
        self.journal_app.show()

    def open_mood_tracker(self):  # Define method to open Mood Tracker window
        self.mood_tracker = MoodTracker()
        self.mood_tracker.show()

    def open_therapist_matching(self):
        self.therapist_matching = TherapistMatching()  # Create instance of TherapistMatching
        self.therapist_matching.show()  # Show the TherapistMatching window

    def open_chatbot(self):
        self.chatbot = Chatbot()  # Create instance of Chatbot
        self.chatbot.show()  # Show the Chatbot window
  
    def open_peer_support(self):
        self.peer_support = PeerSupport()  # Create instance of PeerSupport
        self.peer_support.show()  # Show the PeerSupport window
        
    def open_feedback(self):
        self.feedback_form = FeedbackForm()  # Create instance of FeedbackForm
        self.feedback_form.show()  # Show the FeedbackForm window
            
def main():
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
