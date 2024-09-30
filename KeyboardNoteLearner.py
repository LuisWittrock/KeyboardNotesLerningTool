import random
import numpy as np
import aubio
import pyaudio

p = pyaudio.PyAudio()
BUFFER_SIZE = 1024
CHANNELS = 1
RATE = 44100

pDetection = aubio.pitch("default", BUFFER_SIZE, BUFFER_SIZE // 2, RATE)
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

notes = ["A","A#","B","B#","C#","D","D#","E","F","G","G#"]

def freq_to_note(freq):
    if freq == 0:
        return None
    note_number = 12*np.log2(freq/440)+49
    note_number = round(note_number)
    return notes[note_number%12]

def detect_pitch(data):
    samples = np.frombuffer(data, dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    return freq_to_note(pitch)

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=BUFFER_SIZE)

print("Play a note to start...")

target_note = random.choice(notes)
print(f"Play this note: {target_note}")

while True:
    try:
        data = stream.read(BUFFER_SIZE)
        detected_note = detect_pitch(data)
        
        if detected_note == target_note:
            print(f"Correct! You played {detected_note}")
            target_note = random.choice(notes)
            print(f"Now play this note: {target_note}")
        elif detected_note:
            print(f"Detected: {detected_note}. Try again!")
        
    except KeyboardInterrupt:
        print("\nStopping...")
        break

stream.stop_stream()
stream.close()
p.terminate()
    
    
