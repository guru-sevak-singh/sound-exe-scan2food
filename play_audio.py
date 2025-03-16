import pygame
import os
import wget

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
        download_url = "https://guru-sevak-singh.github.io/sound-exe-scan2food/order_received.mp3"
        # download the audio.
        wget.download(download_url, os.path.join(os.getcwd(), 'order_received.mp3'))

    
    audio_path = os.path.join(os.getcwd(), 'pending_order.mp3')
    if os.path.exists(audio_path):
        pass
    else:
        # Download the audio.
        download_url = "https://guru-sevak-singh.github.io/sound-exe-scan2food/pending_order.mp3"
        wget.download(download_url, os.path.join(os.getcwd(), 'pending_order.mp3'))


download_audios()