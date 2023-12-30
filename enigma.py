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

class Socket():
    def __init__(self, x, y, s):
        self.x = x
        self.y = y
        self.s = s

    def render(self):
        pygame.draw.circle(screen, "purple", (self.x, self.y), 20)
        pygame.draw.circle(screen, "grey", (self.x, self.y), 15)
        size = font.size(self.s)
        surface = font.render(self.s, True, "black")
        screen.blit(surface, (self.x - (size[0]/2), self.y - (size[1]/2) - 40))


class PlugHead():
    def __init__(self, x, y, w, s):
        self.rect = pygame.Rect(x - w/2, y - w/2, w, w)
        self.picked = False
        self.s = s

    def update(self, pos):
        self.rect.x = pos[0] - self.ofset[0]
        self.rect.y = pos[1] - self.ofset[1]

    def pick(self, pos):
        self.ofset = [pos[0] - self.rect.x, pos[1] - self.rect.y]
        self.picked = True
        global picked #TODO Better return than global
        picked = True

    def setPlug(self):
        global picked
        for s in sockets:
            for p in plugs:
                if s in (p.head[0].s, p.head[1].s):
                    break
            else:
                if self.rect.colliderect((sockets[s].x - 20, sockets[s].y - 20, 40, 40)): #Remove magic numbers
                    self.rect.x = sockets[s].x - 20
                    self.rect.y = sockets[s].y - 20 #TODO remove magic number
                    #print(rotor[0].r[alpha2index(self.s)], "to", rotor[0].r[alpha2index(s)])
                    rotor[0].r[alpha2index(s)] = rotor[0].r[alpha2index(self.s)] #this is so inelegant. must have made a seperate class for the plugboard, it is so different form rotors. It behaves differently. Will do it in the next version of the code lets keep going for now.
                    rotor[0].r[alpha2index(rotor[0].r[alpha2index(self.s)])] = s
                    rotor[0].r[alpha2index(self.s)] = self.s
                    self.s = s
                    picked = False #TODO better return than global
                    self.picked = False
                    print(rotor[0].r)
                    break
        else:
            self.rect.x = sockets[self.s].x - 20
            self.rect.y = sockets[self.s].y - 20 #TODO remove magic number
            self.picked = False
            picked = False


class Plug():
    def __init__(self, x1, y1, x2, y2, s):
        self.head = [PlugHead(x1, y1, 40, s[0]), PlugHead(x2, y2, 40, s[1])]
        self.color = "purple"

    def update(self, pos):
        for h in self.head:
            if h.picked:
                h.update(pos)

    def pick(self, pos):
        for h in self.head:
            if h.rect.collidepoint(pos):
                h.pick(pos)

    def setPlug(self):
        for h in self.head:
            if h.picked == True:
                h.setPlug()

    def render(self):
        pygame.draw.rect(screen, self.color, self.head[0].rect,  border_radius = 15)
        pygame.draw.rect(screen, self.color, self.head[1].rect, border_radius = 15)
        pygame.draw.line(screen, self.color, self.head[0].rect.center, self.head[1].rect.center, width = 5)


def alpha2index(a):
    return ord(a) - ord('A') #TODO this doesn't feel safe. what if the aplhas are not contiguous

def index2alpha(n):
    return chr(ord('A') + n) #TODO this doesn't feel safe. what if the aplhas are not contiguous

def render():
    if state == LIGHTBOARD:
        for key in keys.values():
            key.render()

        sizeFont = fontRotor.size(" 00 ")
        space = 10
        x = (width/2) + ((sizeFont[0]/2)+space)
        y = 25
        for r in rotor[1:-1]:
            r.render(x, y)
            x -= sizeFont[0]+space

    if state == PLUGBOARD:
        for plug in sockets.values():
            plug.render()
        for plug in plugs:
            plug.render()

def init():
    r1 = ['J', 'G', 'D', 'Q', 'O', 'X', 'U', 'S', 'C', 'A', 'M', 'I', 'F', 'R', 'V', 'T', 'P', 'N', 'E', 'W', 'K', 'B', 'L', 'Z', 'Y', 'H']
    r2 = ['N', 'T', 'Z', 'P', 'S', 'F', 'B', 'O', 'K', 'M', 'W', 'R', 'C', 'J', 'D', 'I', 'V', 'L', 'A', 'E', 'Y', 'U', 'X', 'H', 'G', 'Q']
    r3 = ['J', 'V', 'I', 'U', 'B', 'H', 'T', 'C', 'D', 'Y', 'A', 'K', 'E', 'Q', 'Z', 'P', 'O', 'S', 'G', 'X', 'N', 'R', 'M', 'W', 'F', 'L']
    ukw = ['Q', 'Y', 'H', 'O', 'G', 'N', 'E', 'C', 'V', 'P', 'U', 'Z', 'T', 'F', 'D', 'J', 'A', 'X', 'W', 'M', 'K', 'I', 'S', 'R', 'B', 'L']
    plugboard = ['A', 'B', 'K', 'D', 'R', 'U', 'G', 'T', 'I', 'J', 'C', 'L', 'O', 'N', 'M', 'P', 'Q', 'E', 'S', 'H', 'F', 'V', 'W', 'X', 'Y', 'Z']

    def createKeys(x, y, string):
        for s in string:
            keys[s] = KeyLight(x, y, s)
            sockets[s] = Socket(x, y, s)
            x += 100

    createKeys(100, 100, "QWERTYUIOP")
    createKeys(150, 200, "ASDFGHJKL")
    createKeys(250, 300, "ZXCVBNM")

    for n in range(26):
        for p in plugs:
            if chr(ord('A')+n) in (p.head[0].s, p.head[1].s):
                break
        else:
            if chr(ord('A')+n) != plugboard[n]:
                plugs.append(Plug(sockets[chr(ord('A')+n)].x,
                                            sockets[chr(ord('A')+n)].y,
                                            sockets[plugboard[n]].x,
                                            sockets[plugboard[n]].y,
                                            [chr(ord('A')+n), plugboard[n]]))

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

PLUGBOARD = 1
LIGHTBOARD = 2
state = LIGHTBOARD
pygame.init()
font = pygame.font.Font(None, 64)
fontRotor = pygame.font.Font(None, 32)
height = 400
width = 1100
keys = {}
keyPressed = None
keyOut = None
picked = False
rotor = []
plugs = []
sockets = {}
screen = pygame.display.set_mode([width, height])
init()

quit = False
while not quit:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if state == LIGHTBOARD:
                    state = PLUGBOARD
                elif state == PLUGBOARD:
                    state = LIGHTBOARD

            if state == LIGHTBOARD:
                if keyPressed is None and e.unicode.upper() in keys:
                    keyPressed = e.unicode
                    keyOut = rotor[0].output(keyPressed.upper())
                    rotor[1].inc() #Can I make this implicit in the class inself may be a class enigma that wraps, rotors and plugboard and lightboard
                    keys[keyOut].lit = True
                    print(keyOut, end="")

        if e.type == pygame.KEYUP:
            if state == LIGHTBOARD:
                if keyPressed is e.unicode:
                    keyPressed = None
                    keys[keyOut].lit = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            if state == PLUGBOARD:
                if picked:
                    for p in plugs:
                        p.setPlug()
                else:
                    pos = pygame.mouse.get_pos()
                    for p in plugs:
                        p.pick(pos)

            if state == LIGHTBOARD:
                for r in rotor[1:-1]:
                    r.set_rotor(pygame.mouse.get_pos())

        if state == PLUGBOARD:
            for p in plugs:
                p.update(pygame.mouse.get_pos())

    screen.fill((255, 255, 255))
    render()
    pygame.display.flip()

pygame.quit()

