import colorsys
import os
import sys
import time
import argparse
import subprocess

def clear_terminal():
    """Simple universal CLS system."""
    os.system('clear' if os.name == 'posix' else 'cls')

def rgb_to_ansi(r, g, b):
    """Converts RGB values to an ANSI color code."""
    return f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"

def rainbow_screen(delay, increment, char, saturation, brightness, reverse):
    clear_terminal()
    rows, columns = os.popen('stty size', 'r').read().split()
    rows, columns = int(rows), int(columns)
    
    # Display all parameters at the top
    print(f"Delay: {delay:.2f}s | Increment: {increment:.2f} | Char: {char} | Sat: {saturation:.1f} | Bright: {brightness:.1f}")
    print("-" * columns)

    hue = 1.0 if reverse else 0.0  # Starting hue based on direction

    for row in range(rows - 2):
        for col in range(columns):
            r, g, b = colorsys.hsv_to_rgb(hue % 1.0, saturation, brightness)
            sys.stdout.write(rgb_to_ansi(r, g, b) + str(char))
            hue = hue - increment if reverse else hue + increment
        sys.stdout.write("\033[0m\n")
        time.sleep(delay)

def rainbow_pipe(delay, increment, saturation, brightness, reverse):
    """Colorize piped input."""
    hue = 1.0 if reverse else 0.0
    
    for line in sys.stdin:
        for char in line:
            r, g, b = colorsys.hsv_to_rgb(hue % 1.0, saturation, brightness)
            sys.stdout.write(rgb_to_ansi(r, g, b) + char)
            hue = hue - increment if reverse else hue + increment
        sys.stdout.write("\033[0m")  # Reset
        sys.stdout.flush()
        time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rainbow screen with customizable parameters")
    parser.add_argument(
        "--delay", "-d", type=float, default=0.05,
        help="Delay between rows in seconds (default: 0.05)"
    )
    parser.add_argument(
        "--increment", "-i", type=float, default=0.1,
        help="Hue increment for each block (default: 0.1)"
    )
    parser.add_argument(
        "--char", "-c", type=str, default="█",
        help="Character to display (default: █)"
    )
    parser.add_argument(
        "--saturation", "-s", type=float, default=1.0,
        help="Color saturation, 0.0 to 1.0 (default: 1.0)"
    )
    parser.add_argument(
        "--brightness", "-b", type=float, default=1.0,
        help="Color brightness, 0.0 to 1.0 (default: 1.0)"
    )
    parser.add_argument(
        "--reverse", "-r", action="store_true",
        help="Reverse the rainbow direction"
    )
    parser.add_argument(
        "--pipe", "-p", action="store_true",
        help="Process piped input instead of generating rainbow screen"
    )
    args = parser.parse_args()

    try:
        if args.pipe:
            rainbow_pipe(
                args.delay,
                args.increment,
                args.saturation,
                args.brightness,
                args.reverse
            )
        else:
            rainbow_screen(
                args.delay,
                args.increment,
                args.char,
                args.saturation,
                args.brightness,
                args.reverse
            )
    except KeyboardInterrupt:
        print("\033[0m")  # Reset terminal colors on exit