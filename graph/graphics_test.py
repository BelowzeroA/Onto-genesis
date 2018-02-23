from graphics import *
import ctypes

user32 = ctypes.windll.user32


def main():

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    win = GraphWin('Draw a Triangle', screen_width / 2, screen_height / 2)
    # win = GraphWin('Draw a Triangle')
    # win.yUp() # right side up coordinates
    # win.setBackground('grey')
    message = Text(Point(win.getWidth() / 2, 30), 'Click on three points')
    message.setTextColor('red')
    message.setStyle('italic')
    message.setSize(20)
    message.draw(win)

    # Get and draw three vertices of triangle
    # p1 = win.getMouse()
    # p1.draw(win)
    # p2 = win.getMouse()
    # p2.draw(win)
    # p3 = win.getMouse()
    # p3.draw(win)
    # vertices = [p1, p2, p3]

    p1 = Point(40, 100)
    p2 = Point(100, 200)

    circle1 = Circle(center=p1, radius=5)
    circle1.setFill('black')
    circle1.draw(win)

    circle2 = Circle(center=p2, radius=5)
    circle2.draw(win)

    line = Line(p1, p2)
    line.config['width'] = 3
    line.draw(win)
    # # Use Polygon object to draw the triangle
    # triangle = Polygon(vertices)
    # triangle.setFill('gray')
    # triangle.setOutline('cyan')
    # triangle.setWidth(4)  # width of boundary line
    # triangle.draw(win)

    message.setText('Click anywhere to quit') # change text message
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()