import os
import random
import pygame
import csv
from datetime import datetime


def play_audio_files(directory):
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Audio Player")
    font = pygame.font.Font(None, 74)
    middle_font = pygame.font.Font(None, 45)
    small_font = pygame.font.Font(None, 35)
    clock = pygame.time.Clock()

    # Load listen icon
    listen_icon = pygame.image.load('icon.png')
    listen_icon = pygame.transform.scale(listen_icon, (100, 100))

    # Get a list of audio files in the directory
    audio_files = [f for f in os.listdir(directory) if f.endswith('.wav') or f.endswith('.mp3')]

    # Randomize the audio files
    random.shuffle(audio_files)

    bg_color = (26, 92, 74)
    text_color = (255, 255, 255)
    button_color = (50, 150, 200)
    highlight_color = (244, 174, 66)
    progress_bar_bg_color = (100, 100, 100)  # Color for the outer box of the progress bar

    # Create CSV file to log results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"result_{timestamp}.csv"
    csv_filepath = os.path.join(csv_filename)

    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Audio File', 'User Choice', 'Is Correct'])

    def start_playing():
        for index, audio_file in enumerate(audio_files):
            # Load and play the audio file
            pygame.mixer.music.load(os.path.join(directory, audio_file))
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                # Display listen icon
                screen.fill(bg_color)
                screen.blit(listen_icon, (350, 150))

                # Display progress bar background
                pygame.draw.rect(screen, progress_bar_bg_color, (150, 500, 500, 30))

                # Display progress bar
                progress = (index + 1) / len(audio_files)
                pygame.draw.rect(screen, text_color, (150, 500, 500 * progress, 30))

                # Display current file index
                file_index_text = small_font.render(f'File {index + 1} of {len(audio_files)}', True, text_color)
                screen.blit(file_index_text, (10, 10))

                pygame.display.flip()
                clock.tick(30)

            # Display choice buttons
            user_choice = get_user_choice(audio_file)  # Get user's choice
            is_correct = user_choice in audio_file  # Check if the user's choice is correct

            # Log the result to CSV
            with open(csv_filepath, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([audio_file, user_choice, is_correct])
                print(f"Logged result to {csv_filepath}")

        # Quit pygame after all files have been played
        pygame.quit()

    def get_user_choice(audio_file):
        word_pair = get_word_pair(audio_file)
        choice = None

        while choice is None:
            screen.fill(bg_color)

            # Draw the buttons
            button1_rect = pygame.Rect(150, 400, 200, 100)
            button2_rect = pygame.Rect(450, 400, 200, 100)
            pygame.draw.rect(screen, button_color, button1_rect)
            pygame.draw.rect(screen, button_color, button2_rect)

            button1_text = middle_font.render(word_pair[0], True, text_color)
            button2_text = middle_font.render(word_pair[1], True, text_color)
            #screen.blit(button1_text, button1_rect.move(20, 30))
            #screen.blit(button2_text, button2_rect.move(20, 30))

            text1_rect = button1_text.get_rect(center=button1_rect.center)
            screen.blit(button1_text, text1_rect)
            text2_rect = button2_text.get_rect(center=button2_rect.center)
            screen.blit(button2_text, text2_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        choice = word_pair[0]
                    elif button2_rect.collidepoint(event.pos):
                        choice = word_pair[1]

        return choice

    def get_word_pair(audio_file):
        word_pairs = {
            'rich': 'reach', 'itch': 'each', 'sin': 'scene', 'list': 'least',
            'chip': 'cheap', 'filled': 'field', 'grin': 'green', 'bet': 'bat',
            'pet': 'pat', 'met': 'mat', 'set': 'sat', 'ten': 'tan',
            'men': 'man', 'Ken': 'can', 'cut': 'cot', 'but': 'bot',
            'hut': 'hot', 'nut': 'not', 'sub': 'sob', 'fund': 'fond',
            'pup': 'pop', 'look': 'Luke', 'pull': 'pool', 'full': 'fool',
            'should': 'shooed', 'bull': 'Boole', 'could': 'cooed', 'would': 'wooed'
        }
        # Extract word from filename
        word = audio_file.split('_')[-1].split('.')[0]

        if word in word_pairs:
            return word, word_pairs[word]
        else:
            for key, value in word_pairs.items():
                if value == word:
                    return value, key

        return word, "Unknown"

    # Main loop to wait for the start button press
    running = True
    while running:
        screen.fill(bg_color)

        # Draw the start button
        start_button_rect = pygame.Rect(300, 250, 200, 100)
        pygame.draw.rect(screen, highlight_color, start_button_rect)
        start_text = font.render('Start', True, bg_color)
        text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_playing()
                    running = False

        clock.tick(30)

    pygame.quit()

def select_mode():
    selected_mode = mode_var.get()
    if selected_mode == 'Environment':
        play_audio_files('Environment')
    elif selected_mode == 'SingleTalker':
        play_audio_files('SingleTalker')
    elif selected_mode == 'PinkNoise':
        play_audio_files('PinkNoise')

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Mode")
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 35)
    clock = pygame.time.Clock()

    bg_color = (26, 92, 74)
    text_color = (255, 255, 255)
    mode_select_button_color = (50, 150, 200)
    highlight_color = (244, 174, 66)

    global mode_var
    mode_var = 'Environment'

    running = True
    while running:
        screen.fill(bg_color)

        # Draw the buttons for mode selection
        env_button_rect = pygame.Rect(150, 150, 200, 100)
        single_button_rect = pygame.Rect(450, 150, 200, 100)
        pink_button_rect = pygame.Rect(300, 300, 200, 100)

        pygame.draw.rect(screen, highlight_color, env_button_rect)
        pygame.draw.rect(screen, highlight_color, single_button_rect)
        pygame.draw.rect(screen, highlight_color, pink_button_rect)

        env_text = small_font.render('Environment', True, bg_color)
        single_text = small_font.render('Single Talker', True, bg_color)
        pink_text = small_font.render('Pink Noise', True, bg_color)

        env_text_rect = env_text.get_rect(center=env_button_rect.center)
        screen.blit(env_text, env_text_rect)

        single_text_rect = single_text.get_rect(center=single_button_rect.center)
        screen.blit(single_text, single_text_rect)

        pink_text_rect = pink_text.get_rect(center=pink_button_rect.center)
        screen.blit(pink_text, pink_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if env_button_rect.collidepoint(event.pos):
                    mode_var = 'Environment'
                    running = False
                elif single_button_rect.collidepoint(event.pos):
                    mode_var = 'SingleTalker'
                    running = False
                elif pink_button_rect.collidepoint(event.pos):
                    mode_var = 'PinkNoise'
                    running = False

        clock.tick(30)

    pygame.quit()

    if mode_var == 'Environment':
        play_audio_files('Environment')
    elif mode_var == 'SingleTalker':
        play_audio_files('SingleTalker')
    elif mode_var == 'PinkNoise':
        play_audio_files('PinkNoise')


if __name__ == "__main__":
    main()
