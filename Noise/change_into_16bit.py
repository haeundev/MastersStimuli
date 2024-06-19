import wave
import os
import numpy as np


def convert_to_16bit(file_path):
    # Open the original WAV file
    with wave.open(file_path, 'rb') as wav_file:
        # Get audio parameters
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)

    # Read audio data
    audio_data = np.frombuffer(frames, dtype=np.int16 if params.sampwidth == 2 else np.int8)

    # Check if it is already 16-bit audio
    if params.sampwidth == 2:
        print(f"{file_path} is already 16-bit.")
        return

    # Convert audio data to 16-bit
    if params.sampwidth == 1:  # 8-bit to 16-bit
        audio_data = audio_data.astype(np.int16) * 256
    else:
        raise ValueError("Unsupported sample width")

    # Write the converted data back to a WAV file
    with wave.open(file_path, 'wb') as wav_file:
        # Use original parameters but change sample width to 16 bits
        wav_file.setparams((params.nchannels, 2, params.framerate, params.nframes, params.comptype, params.compname))
        wav_file.writeframes(audio_data.tobytes())
    print(f"Converted and replaced {file_path}")


# Directory containing WAV files
directory = os.getcwd()

# Process each WAV file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        file_path = os.path.join(directory, filename)
        convert_to_16bit(file_path)
