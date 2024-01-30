from audio import audio_procces
import pyuac
from pydub import *
import os

def main():
    obj = audio_procces(file_dir='C:/Users/whatuser/PycharmProjects/mockexampapergeneration/IGCSE-mock-exam-papers/thing.wav')
    obj.prepare_slices()
    slices = obj.analyze_for_parts()
    audio_slices = obj.finalize_sections(slices)
    c=0
    for slice in audio_slices:
        c+=1
        print('got here')
        input(':::')
        slice.export(f'proccessed_sections/{c}.wav')


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        main()