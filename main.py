import PyPDF2 as pdf2
from pdf2image import convert_from_path
import requests
import whisper_timestamped as whisper
from pyuac import main_requires_admin
import time
from pydub import *
import json

urlpdf = 'https://dynamicpapers.com/wp-content/uploads/2015/09/0525_s23_qp_13.pdf'
urlaudio = 'https://dynamicpapers.com/wp-content/uploads/2015/09/0525_s23_sf_13.mp3'

qparmsp = {"downloadformat": "pdf"}
response = requests.get(urlpdf, params=qparmsp)
with open('C:/Users/peter/PycharmProjects/mockexampapergeneration/IGCSE-mock-exam-papers/thing.pdf', 'wb') as f:
    f.write(response.content)
qparmsa = {"downloadformat": "wav"}
response = requests.get(urlaudio, params=qparmsa)
with open('C:/Users/peter/PycharmProjects/mockexampapergeneration/IGCSE-mock-exam-papers/thing.wav', 'wb') as f:
    f.write(response.content)

pdfobj = open('thing.pdf', 'rb')
pdfreader = pdf2.PdfReader(pdfobj)
print(len(pdfreader.pages))

pageobj = pdfreader.pages[0]
print(pageobj.extract_text())

images = convert_from_path('thing.pdf', poppler_path='poppler-23.11.0/library/bin')
for i in range(len(images)):
    if i == 2:
        images[i].save('page1.png', 'PNG')

start = (16.3-10) *1000
end = (18.48+30) *1000

with open('timesindexed.json', 'w') as f:
    times = []
    j = open('ishouldhavesavedittoafile.json', 'r')
    parsable = json.load(j)
    search_queries = ["Fragen 1 bis 8", "Fragen 9 bis 14", "Fragen 15 bis 19", "Fragen 20 bis 28", "Fragen 29 bis 34", "Fragen 35 bis 37"]
    c = 0
    for segment in parsable["segments"]:
        text = segment["text"]
        print(text)
        print(c)
        start = 0
        end = 0
        if text == "Cambridge Assessment International Education June 2023":
            for word in segment["words"]:
                if word["text"] == "June":
                    end = (word["start"] + 30)*1000
                    times.append((start, end))
        if c< len(search_queries) and search_queries[c] in text:
            st = segment["start"]
            if st > 40:
                start = (st - 30) *1000
            else:
                start = (st - (st*0.5)) *1000
            end = (segment["end"] + 30) *1000
            times.append((start, end))
            c+=1
    json.dump(times, f)
    j.close()







'''
@main_requires_admin
def main():
    model = whisper.load_model('tiny', device='cpu')
    audio = whisper.load_audio('thing.wav')
    result = whisper.transcribe(model, audio, language='de')
    import json
    with open('dumpfile2.json', 'w') as f:
        json.dump( result, f, indent = 2, ensure_ascii = False)

main()
'''