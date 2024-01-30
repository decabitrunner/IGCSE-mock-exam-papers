import json
import os
from pydub import AudioSegment
import whisper_timestamped as whisperT

class audio_procces:
    def __init__(self, file_dir):
        self.audio = AudioSegment.from_file(file_dir)
        self.times = open('timesindexed.json', 'r')
        self.times_indexed = json.load(self.times)

    def prepare_slices(self):
        try:
            os.mkdir('temp/slices')
        except FileExistsError:
            print('test version: file is not yet deleted')

        c = 0
        for deltat in self.times_indexed:
            c+=1
            audio_slice = self.audio[deltat[0]:deltat[1]]
            audio_slice.export(f'temp/slices/{c}.wav', format='wav')


    def analyze_for_parts(self):
        search_queries = ["Fragen 1 bis 8", "Fragen 9 bis 14", "Fragen 15 bis 19", "Fragen 20 bis 28",
                          "Fragen 29 bis 34", "Fragen 35 bis 37"]
        part_slices = []

        for root, dirs, files in os.walk('temp/slices'):
            c = 0


            for filename in files:
                model = whisperT.load_model('base')
                taudio = whisperT.load_audio(os.path.join('temp/slices', filename))
                timestamped_transcription = whisperT.transcribe(model, taudio, beam_size=5, best_of=5)
                start = 0
                end = 0
                for segment in timestamped_transcription["segments"]:
                    phrase = segment["text"]
                    if search_queries[c] in phrase:
                        start = (segment["start"]*1000)+ self.times_indexed[c][0]
                        part_slices.append([start])
                        break
                    if c == 1 or c == 4:
                        print(phrase)
                        input('l: ')
                c+=1
                if c == 2 or c == 4:
                    with open(f'transc{c}.json', 'w') as f:
                        json.dump(timestamped_transcription, f, indent=5)
                        print(f' {c} dumped file')
                        print(len(timestamped_transcription["segments"]))
        next_end = 0
        for i in range(len(part_slices)-1, -1, -1):

            if i == len(part_slices)-1:
                part_slices[i].append(1000*self.audio.duration_seconds)
            else:
                part_slices[i].append(next_end)
            next_end = part_slices[i][0]
        self.times.close()
        print(part_slices)
        input('wait: ')
        return part_slices

    def finalize_sections(self, part_slices):
        sections = []
        for section in part_slices:
            start = section[0]
            end = section[1]
            segment = self.audio[start:end]
            sections.append(segment)

        return sections