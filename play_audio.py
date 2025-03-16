import pygame
import os


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Wait until the audio finishes playing


def order_received():
    play_audio('order_received.mp3')

def pending_order():
    play_audio('pending_order.mp3')

def download_audios():
    audio_path = os.path.join(os.getcwd(), 'order_received.mp3')
    if os.path.exists(audio_path):
        pass
    else:
        # download the audio.
        pass

    
    audio_path = os.path.join(os.getcwd(), 'pending_order.mp3')
    if os.path.exists(audio_path):
        pass
    else:
        # Download the audio.
        pass

