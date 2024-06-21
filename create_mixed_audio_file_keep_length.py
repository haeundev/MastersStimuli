import array
import os
import numpy as np
import wave
import matplotlib.pyplot as plt


def calculate_adjusted_rms(clean_rms, snr):
    snr_ratio = float(snr) / 20
    noise_rms = clean_rms / (10 ** snr_ratio)
    return noise_rms


def calculate_amplitude(wav_file):
    buffer = wav_file.readframes(wav_file.getnframes())
    amplitude = np.frombuffer(buffer, dtype="int16").astype(np.float64)
    return amplitude


def calculate_rms(amplitude):
    return np.sqrt(np.mean(np.square(amplitude), axis=-1))


def save_waveform(output_path, params, amplitude):
    with wave.Wave_write(output_path) as output_file:
        output_file.setparams(params)
        output_file.writeframes(array.array('h', amplitude.astype(np.int16)).tobytes())


def plot_waveforms(time_axis, clean_amp, adjusted_noise_amp, mixed_amp, output_path):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    axs[0].plot(time_axis, clean_amp, label='Clean Signal')
    axs[0].set_title('Clean Signal')
    axs[0].set_ylabel('Amplitude')
    axs[0].legend()

    axs[1].plot(time_axis, adjusted_noise_amp, label='Noise Signal', color='orange')
    axs[1].set_title('Noise Signal')
    axs[1].set_ylabel('Amplitude')
    axs[1].legend()

    axs[2].plot(time_axis, mixed_amp, label='Mixed Signal', color='green')
    axs[2].set_title('Mixed Signal')
    axs[2].set_xlabel('Time (seconds)')
    axs[2].set_ylabel('Amplitude')
    axs[2].legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

    print(f"Saved waveform plot as {output_path}")


def process_audio(clean_file, noise_file, snr_list, noise_mode='SingleTalker'):
    clean_wav = wave.open(clean_file, "r")
    noise_wav = wave.open(noise_file, "r")

    clean_amp = calculate_amplitude(clean_wav)
    noise_amp = calculate_amplitude(noise_wav)

    clean_rms = calculate_rms(clean_amp)

    noise_len = len(noise_amp)
    clean_len = len(clean_amp)
    start = (noise_len - clean_len) // 2
    end = start + clean_len
    divided_noise_amp = noise_amp[start:end]
    noise_rms = calculate_rms(divided_noise_amp)

    for snr in snr_list:
        adjusted_noise_rms = calculate_adjusted_rms(clean_rms, snr)
        adjustment_factor = adjusted_noise_rms / noise_rms
        adjusted_noise_amp = noise_amp * adjustment_factor

        mixed_amp = clean_amp + adjusted_noise_amp[start:end]

        max_int16 = np.iinfo(np.int16).max
        min_int16 = np.iinfo(np.int16).min
        if mixed_amp.max() > max_int16 or mixed_amp.min() < min_int16:
            reduction_rate = min(max_int16 / mixed_amp.max(), min_int16 / mixed_amp.min())
            mixed_amp *= reduction_rate
            clean_amp *= reduction_rate
            adjusted_noise_amp *= reduction_rate

        new_noise_amp = adjusted_noise_amp.copy()
        new_noise_amp[start:end] = mixed_amp

        save_path = f"{noise_mode}_SNR_{snr}_dB_{os.path.basename(clean_file)}"
        save_waveform(save_path, noise_wav.getparams(), new_noise_amp)

        # time_axis = np.linspace(0, len(clean_amp) / clean_wav.getframerate(), num=len(clean_amp))
        # fig_filename = f"{noise_mode}_SNR_{snr}_dB_{os.path.basename(clean_file)}.png"
        # plot_waveforms(time_axis, clean_amp, adjusted_noise_amp[start:end], mixed_amp, fig_filename)


if __name__ == '__main__':
    # clean_file = 'Words/Target/F3/bat.wav'
    # noise_file = 'Sentences/F3/A shape with no corners is called a circle.wav'
    # snr_list = [-4, 0, 4]
    # process_audio(clean_file, noise_file, snr_list)

    snr_list = [-2, -5]
    dir_clean = 'Words/Target/F3'  # get all wav files in the following directory
    # dir_noise = 'Noise/Concat_p4_Nz.wav'
    dir_noise = 'Sentences/F3'
    # noise_file = 'Noise/Concat_p4_Nz.wav'
    for file in os.listdir(dir_clean):
        if file.endswith(".wav"):
            clean_file = os.path.join(dir_clean, file)
            # get random noise file
            noise_file = os.path.join(dir_noise, np.random.choice(os.listdir(dir_noise)))
            process_audio(clean_file, noise_file, snr_list)