import pygame

class Rotor():
    def __init__(self, r, left=None, right=None):
        self.r = r
        self.pos = 0
        self.left = left
        self.right = right

    def output(self, s):
        if self.left == None:
            return self.right.output_inv(self.r[ord(s)-ord('A')])
        else:
            return self.left.output(self.r[ord(s)-ord('A')])

    def output_inv(self, s):
        if self.right:
            return self.right.output_inv(chr(ord('A') + self.r.index(s)))
        else:
            return chr(ord('A') + self.r.index(s))

    def inc(self):
        x = self.r.pop()
        self.r.insert(0, x)
        if self.pos < 25:
            self.pos += 1
        else:
            if self.left:
                self.left.inc()
            self.pos = 0

    def render(self, x, y):
        surface = fontRotor.render(f" {self.pos:02d} ", True, "black", "grey")
        rect = screen.blit(surface, (x, y))
        pygame.draw.rect(screen, "black", rect, width=1)


class KeyLight():
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.lit = False

    def render(self):
        color = "yellow" if self.lit else "black"
        colorFont = "black" if self.lit else "white"
        pygame.draw.circle(screen, color, (self.x, self.y), 40)
        size = font.size(self.letter)
        surface = font.render(self.letter, True, colorFont)
        screen.blit(surface, (self.x - (size[0]/2), self.y - (size[1]/2)))


keys = {}
keyPressed = None
keyOut = None
rotor = []

def render():
    for key in keys.values():
        key.render()

    sizeFont = fontRotor.size(" 00 ")
    space = 10
    x = (width/2) + ((sizeFont[0]/2)+space)
    y = 25
    for r in rotor[1:-1]:
        r.render(x, y)
        x -= sizeFont[0]+space

def init():
    def createKeys(x, y, string):
        for s in string:
            keys[s] = KeyLight(x, y, s)
            x += 100

    createKeys(100, 100, "QWERTYUIOP")
    createKeys(150, 200, "ASDFGHJKL")
    createKeys(250, 300, "ZXCVBNM")

    r1 = ['J', 'G', 'D', 'Q', 'O', 'X', 'U', 'S', 'C', 'A', 'M', 'I', 'F', 'R', 'V', 'T', 'P', 'N', 'E', 'W', 'K', 'B', 'L', 'Z', 'Y', 'H']
    r2 = ['N', 'T', 'Z', 'P', 'S', 'F', 'B', 'O', 'K', 'M', 'W', 'R', 'C', 'J', 'D', 'I', 'V', 'L', 'A', 'E', 'Y', 'U', 'X', 'H', 'G', 'Q']
    r3 = ['J', 'V', 'I', 'U', 'B', 'H', 'T', 'C', 'D', 'Y', 'A', 'K', 'E', 'Q', 'Z', 'P', 'O', 'S', 'G', 'X', 'N', 'R', 'M', 'W', 'F', 'L']
    ukw = ['Q', 'Y', 'H', 'O', 'G', 'N', 'E', 'C', 'V', 'P', 'U', 'Z', 'T', 'F', 'D', 'J', 'A', 'X', 'W', 'M', 'K', 'I', 'S', 'R', 'B', 'L']
    plugboard = ['B', 'A', 'D', 'C', 'F', 'E', 'H', 'G', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def addRotor(r):
        if len(rotor) == 0:
            r.right = None
        else:
            r.right = rotor[-1]
            rotor[-1].left = r
        rotor.append(r)

    addRotor(Rotor(plugboard))
    addRotor(Rotor(r1))
    addRotor(Rotor(r2))
    addRotor(Rotor(r3))
    addRotor(Rotor(ukw))


pygame.init()
font = pygame.font.Font(None, 64)
fontRotor = pygame.font.Font(None, 32)
height = 400
width = 1100
screen = pygame.display.set_mode([width, height])
init()

quit = False
while not quit:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

        if e.type == pygame.KEYDOWN:
            if keyPressed is None and e.unicode.upper() in keys:
                keyPressed = e.unicode
                keyOut = rotor[0].output(keyPressed.upper())
                rotor[1].inc()
                keys[keyOut].lit = True
                print(keyOut, end="")

        if e.type == pygame.KEYUP:
            if keyPressed is e.unicode:
                keyPressed = None
                keys[keyOut].lit = False

    screen.fill((255, 255, 255))
    render()
    pygame.display.flip()

pygame.quit()

