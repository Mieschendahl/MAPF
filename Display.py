import sys, time

class Display:
    x = 0
    y = 0

    def rgb_to_ansi(r, g, b, background=False):
        return "\x1b[%d;5;%dm" % (48 if background else 38, 16 + 36 * round(r) + 6 * round(g) + round(b))

    def grey_to_ansi(v, background=False):
        return "\x1b[%d;5;%dm" % (48 if background else 38, 232 + v)

    def flipansi(ansi):
        return ansi[ : 2] + ("3" if ansi[3] == "4" else "4") + ansi[3 : ]

    def translate(x, y):
        return "\x1b[%d;%dH" % (y + 1, x + 1)

    def screen(show):
        if show:
            return Display.buffer1
        return Display.buffer2

    def cursor(show):
        if show:
            return Display.cursor1
        return Display.cursor2
        
    def outbounds():
        return Display.y < 0 or Display.x < 0 or Display.y >= len(Display.data) or Display.x >= len(Display.data[Display.y])

    def get():
        return Display.x, Display.y

    def outputdisplay():
        output = ""
        lastcolor = ""
        i = 0

        for line in Display.data:
            output += Display.translate(Display.xoffset, Display.yoffset + i)
            for char in line:
                char, color = char[-1], char[ : -1]

                if lastcolor != color:
                    output += Display.normal + (color if color else "")
                    lastcolor = color

                output += char
            i += 1
        return output + Display.normal

    def setdisplay(width, height, xoffset=0, yoffset=0):
        Display.width, Display.height, Display.xoffset, Display.yoffset = width, height, xoffset, yoffset
        Display.data = [[" "] * Display.width for _ in range(Display.height)]

    def fill(value=" "):
        for row in Display.data:
            for j, char in enumerate(row):
                row[j] = value

    def clear():
        Display.fill()
        Display.set(0, 0)

    def set(x, y): 
        Display.y = min(len(Display.data) - 1, max(0, y))
        Display.x = min(len(Display.data[Display.y]) - 1, max(0, x))

    def move(length):
        while length > 0:
            length -= 1
            x, y = Display.x, Display.y
            if x + 1 < len(Display.data[Display.y]):
                x += 1
            elif y + 1 < len(Display.data):
                x = 0
                y += 1
            else:
                return False
            Display.x, Display.y = x, y

        while length < 0:
            length += 1
            x, y = Display.x, Display.y
            if x - 1 >= 0:
                x -= 1
            elif y - 1 >= 0:
                x = len(Display.data[Display.y - 1]) - 1
                y -= 1
            else:
                return False
            Display.x, Display.y = x, y
        return True

    def setchar(char, color=""):
        Display.data[Display.y][Display.x] = color + char

    def setstring(string, color=""):
        for char in string:
            if char == "\n":
                Display.setchar(" ", color)
                Display.x, Display.y = 0, Display.y + 1
                if Display.outbounds():
                    break
            else:
                Display.setchar(char, color)
                if not Display.move(1):
                    break

    def startloading(width):
        Display.loading = True

        wheel = ["Loading |", "Loading /", "Loading -", "Loading \\"]
        # wheel = ["Loading .|", "Loading ../", "Loading ...-", "Loading ..\\"]
        i = 0
        while Display.loading:
            l = max(0, width - len(wheel[i]))
            sys.stdout.write("\x1b[%dD" % width + wheel[i] + " " * l + "\x1b[%dD" % (l - 1))
            sys.stdout.flush()

            i = (1 + i) % len(wheel)
            time.sleep(0.1)

        sys.stdout.write("\x1b[2K\x1b[%dD" % width)
        sys.stdout.flush()

    def stoploading(thread):
        if Display.loading:
            Display.loading = False
            thread.join()

Display.cursor1 = "\x1b[?25h"
Display.cursor2 = "\x1b[?25l"

Display.buffer1 = "\x1b[?1049h"
Display.buffer2 = "\x1b[?1049l"

Display.normal = "\x1b[0m"
Display.crosscolor = Display.grey_to_ansi(7, True)

Display.color = {"grey" : Display.rgb_to_ansi(3, 3, 3), "white" : Display.rgb_to_ansi(5, 5, 5),
                 "red" : Display.rgb_to_ansi(4, 1, 1), "blue" : Display.rgb_to_ansi(2, 3, 5),
                 "green" : Display.rgb_to_ansi(1, 4, 1), "yellow" : Display.rgb_to_ansi(4, 4, 1), 
                 "pink" : Display.rgb_to_ansi(4, 1, 4), "cyan" : Display.rgb_to_ansi(1, 4, 4),
                 "purple" : Display.rgb_to_ansi(3, 1, 5), "clear" : "",
                 "black" : Display.rgb_to_ansi(0, 0, 0),
                 "greyback" : Display.flipansi(Display.rgb_to_ansi(3, 3, 3)),
                 "blueback" : Display.flipansi(Display.rgb_to_ansi(1, 1, 3))}
