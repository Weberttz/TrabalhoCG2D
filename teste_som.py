import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Sons/suspense_sobrenatural.wav")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()

input("Pressione Enter para encerrar...")
pygame.quit()