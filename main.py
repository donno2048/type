from json import loads
from pygame import init, QUIT, KEYDOWN, K_BACKSPACE
from pygame.display import update, set_mode
from pygame.time import Clock
from pygame.font import Font
from pygame.event import get
from time import time
from urllib.request import urlopen
from string import printable
MAX_LENGTH = 100
def get_text():
    text = loads(urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary').read())['extract']
    for letter in text:
        if letter not in printable:
            return get_text()
    return text
def get_texts():
    texts = [""]
    words = get_text().split()
    for word in words:
        if len(texts[-1]) + len(word) + 1 > MAX_LENGTH:
            texts += [word]
        else:
            texts[-1] += word + " "
    return texts
def main():
    init()
    font = Font('consola.ttf', 20)
    screen = set_mode((11 * MAX_LENGTH, 60))
    texts = get_texts()
    if texts:
        text = texts.pop(0).strip()
    else:
        texts = get_texts()
        text = texts.pop(0).strip()
    typed = ''
    start_time = 0
    while True:
        screen.fill((255, 255, 255))
        for index, letter in enumerate(text):
            color = (0, 0, 0)
            if index < len(typed):
                if letter == typed[index]:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
            screen.blit(font.render(letter, True, color), (index * 11, 0))
        screen.blit(font.render(typed, True, (0, 0, 0)), (0, 30))
        update()
        for e in get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:
                    typed = typed[:-1] if typed else typed
                try:
                    if e.unicode in printable:
                        if not start_time: start_time = time()
                        typed += e.unicode
                except:
                    pass
                if text == typed:
                    print(60 * len(text.split()) / (time() - start_time), "WPM")
                    start_time = 0
                    if texts:
                        text = texts.pop(0).strip()
                    else:
                        texts = get_texts()
                        text = texts.pop(0).strip()
                    typed = ''
        Clock().tick(60)
if __name__ == '__main__':
    main()