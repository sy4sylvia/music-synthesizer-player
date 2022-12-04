# music_visualizer.py
from visualizer_components import *


def get_cur_x(circle_x, radius, ang):
    return circle_x + radius * np.cos(np.radians(ang - 90))


def get_cur_y(circle_y, radius, ang):
    return circle_y + radius * np.sin(np.radians(ang - 90))


def generate_visualizer(filename):
    analyzer = MusicAnalyzer()
    analyzer.load(filename)

    pygame.init()

    info = pygame.display.Info()

    # set the width and the height of the pygame window to be 90% of the screen size
    window_w = int(info.current_w * 0.9)
    window_h = int(info.current_h * 0.9)

    window = pygame.display.set_mode([window_w, window_h])
    # set the title of the pygame window
    pygame.display.set_caption('Music Visualizer')

    # construct the center of the circle, circle_x and circle_y are the x and y coordinates of the center of the circle\
    # times 0.5 to set the center of the circle to be the center of the pygame window as well
    circle_x = int(window_w * 0.5)
    circle_y = int(window_h * 0.5)

    # initialize the current ticks and last ticks timestamp, later updated while the pygame window is running
    cur_ticks = pygame.time.get_ticks()
    last_ticks = cur_ticks
    total_time = 0

    # set the background color to be pure black
    background_color = (40, 40, 40)
    # circle_color is the color for the circle that is the root of the rotated bars (black)
    circle_color = (40, 40, 40)
    # poly_color is the color for the bars (white)
    poly_color = (255, 255, 255)
    # set the radius of the circle
    radius = 100

    # create custom complex frequency patterns for the bars
    freq_patterns = []
    left, right, cnt = 50, 150, 24
    for idx in range(0, 6):
        freq_patterns.append({
            "start": left,
            "end": right,
            "count": cnt
        })
        left = right
        right = right * 2

    # used to store the simple bars that are not rotated
    basic_bars = []
    # cnt the number of bars to calculate how many degrees each bar should take place on the circular surface
    bar_cnt = 0

    # construction of bars according to the frequencies
    for freq_type in freq_patterns:
        # group bars according to the range of frequencies
        cur_freq_type_bars = []
        step = int((freq_type["end"] - freq_type["start"]) / freq_type["count"])
        remainder = (freq_type["end"] - freq_type["start"]) % freq_type["count"]
        # start of the interval
        cur_start = freq_type["start"]

        for i in range(freq_type["count"]):
            # count the number of bars
            bar_cnt += 1

            cur_stop = cur_start + step + 1
            if remainder != 0:
                cur_stop += 1
                arr = np.arange(start=cur_start, stop=cur_stop)
                # use remainder as cnt here to proceed to the next bar
                remainder -= 1
                cur_start += step + 3
            else:
                arr = np.arange(start=cur_start, stop=cur_stop)
                cur_start += step + 2

            cur_freq_type_bars.append(arr)

        basic_bars.append(cur_freq_type_bars)

    angle_per_bar = 360 / bar_cnt
    angle = 0

    bars = []
    for bar_group in basic_bars:
        rotated_bars = []
        cur_color = (255, 0, 255)
        for cur_basic in bar_group:
            cur_x = get_cur_x(circle_x, radius, angle)
            cur_y = get_cur_y(circle_x, radius, angle)

            # limit the max_height of the rotated bar in case it cannot be displayed completely on the pygame window
            cur_rotated_bar = RotatedBar(cur_x, cur_y, cur_basic, cur_color, angle=angle, width=8, max_height=330)

            rotated_bars.append(cur_rotated_bar)

            angle += angle_per_bar

        bars.append(rotated_bars)

    # initialize the pygame.mixer
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)

    running = True
    while running:
        cur_ticks = pygame.time.get_ticks()
        delta_time = (cur_ticks - last_ticks) * 0.001
        last_ticks = cur_ticks
        total_time += delta_time

        # initialize, fill the background color for the pygame window
        window.fill(background_color)

        # the pygame window would not automatically close even when the music is stopped, this is for a better view for
        # the last image left on the window
        # added so the pygame window could be closed, otherwise run into an infinity loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # poly_points is used to draw the polygon, should be collected from all the rectangles of the bar
        poly_points = []

        for bar_group in bars:
            for bar in bar_group:
                cur_time = pygame.mixer.music.get_pos() * 0.001
                bar.update_all(delta_time, cur_time, analyzer)

                # update the shape(freq and amplitude) of the rectangle
                bar.x = get_cur_x(circle_x, radius, bar.angle)
                bar.y = get_cur_y(circle_y, radius, bar.angle)
                bar.update_rect()

                for point in bar.rect.points:
                    poly_points.append(point)

        pygame.draw.polygon(window, poly_color, poly_points)
        pygame.draw.circle(window, circle_color, (circle_x, circle_y), int(radius))

        # update the full display window to the screen
        pygame.display.flip()

    pygame.quit()
