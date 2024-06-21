import array
import os
import numpy as np
import random
import wave
import matplotlib.pyplot as plt


def calculate_adjusted_rms(clean_rms, snr):
    """Calculate the RMS value for the noise based on the SNR."""
    snr_factor = float(snr) / 20
    noise_rms = clean_rms / (10 ** snr_factor)
    return noise_rms


def calculate_amplitude(wave_file):
    """Calculate the amplitude of the wave file."""
    buffer = wave_file.readframes(wave_file.getnframes())
    amplitude = np.frombuffer(buffer, dtype="int16").astype(np.float64)
    return amplitude


def calculate_rms(amplitude):
    """Calculate the RMS of the amplitude."""
    return np.sqrt(np.mean(np.square(amplitude), axis=-1))


def save_waveform(output_path, params, amplitude):
    """Save the waveform to a file."""
    with wave.Wave_write(output_path) as output_file:
        output_file.setparams(params)  # nchannels, sampwidth, framerate, nframes, comptype, compname
        output_file.writeframes(array.array('h', amplitude.astype(np.int16)).tobytes())


def plot_waveforms(clean_amp, noise_amp, mixed_amp, clean_wav, snr, noise_mode, clean_file):
    """Plot and save the waveforms as PNG images."""
    time_axis = np.linspace(0, len(clean_amp) / clean_wav.getframerate(), num=len(clean_amp))

    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    axs[0].plot(time_axis, clean_amp, label='Clean Signal')
    axs[0].set_title('Clean Signal')
    axs[0].set_ylabel('Amplitude')
    axs[0].legend()

    axs[1].plot(time_axis, noise_amp, label='Noise Signal', color='orange')
    axs[1].set_title('Noise Signal')
    axs[1].set_ylabel('Amplitude')
    axs[1].legend()

    axs[2].plot(time_axis, mixed_amp, label='Mixed Signal', color='green')
    axs[2].set_title('Mixed Signal')
    axs[2].set_xlabel('Time (seconds)')
    axs[2].set_ylabel('Amplitude')
    axs[2].legend()

    plt.tight_layout()

    fig_filename = f"{noise_mode}_SNR_{snr}_dB_{os.path.basename(clean_file)}.png"
    plt.savefig(fig_filename)
    plt.close(fig)

    print(f"Saved waveform plot as {fig_filename}")


def process_waveforms(clean_file, noise_file, noise_mode, snr_list):
    """Process waveforms by mixing clean and noise files at different SNRs."""
    clean_wav = wave.open(clean_file, "r")
    noise_wav = wave.open(noise_file, "r")

    clean_amp = calculate_amplitude(clean_wav)
    noise_amp = calculate_amplitude(noise_wav)

    clean_rms = calculate_rms(clean_amp)

    start = random.randint(0, len(noise_amp) - len(clean_amp))
    divided_noise_amp = noise_amp[start: start + len(clean_amp)]
    noise_rms = calculate_rms(divided_noise_amp)

    for snr in snr_list:
        adjusted_noise_rms = calculate_adjusted_rms(clean_rms, snr)
        adjusted_noise_amp = divided_noise_amp * (adjusted_noise_rms / noise_rms)
        mixed_amp = clean_amp + adjusted_noise_amp

        max_int16 = np.iinfo(np.int16).max
        min_int16 = np.iinfo(np.int16).min
        if mixed_amp.max() > max_int16 or mixed_amp.min() < min_int16:
            reduction_rate = min(max_int16 / mixed_amp.max(), min_int16 / mixed_amp.min())
            mixed_amp *= reduction_rate
            clean_amp *= reduction_rate

        save_path = f"{noise_mode}_SNR_{snr}_dB_{os.path.basename(clean_file)}"
        save_waveform(save_path, clean_wav.getparams(), mixed_amp)
        #plot_waveforms(clean_amp, adjusted_noise_amp, mixed_amp, clean_wav, snr, noise_mode, clean_file)


if __name__ == '__main__':
    CLEAN_DIR = 'Words/Target/F3'
    # NOISE_FILE = 'Noise/Concat_p4_Nz.wav'
    # NOISE_MODE = 'PinkNoise'

    NOISE_FILE = 'Noise/Concat_p4_Nz.wav'
    NOISE_MODE = 'PinkNoise'

    SNR_LIST = [-2, -5]

    for file in os.listdir(CLEAN_DIR):
        if file.endswith(".wav"):
            CLEAN_FILE = os.path.join(CLEAN_DIR, file)
            process_waveforms(CLEAN_FILE, NOISE_FILE, NOISE_MODE, SNR_LIST)
