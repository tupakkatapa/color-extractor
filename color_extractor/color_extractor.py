#!/usr/bin/env python3
# Simple command-line tool for extracting colors from image 
# by tupakkatapa

# General modules
from signal import signal, SIGINT
import argparse, logging, os, sys
from codetiming import Timer

# Colored text
import pyTextColor

# Color conversion
import colorsys

# Color extraction
import numpy as np
import scipy, scipy.cluster
from PIL import Image # Pillow

# Functions
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def parse_arguments():
    description = ( 'Command-line tool for extracting dominant colors from an image.\n'
                    '--------------------------------------------------------------------------\n'
                    'https://github.com/tupakkatapa/color-extractor\n')

    parser = argparse.ArgumentParser(description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
                        "argument",
                        help    = "Required. The path to the image file.",
                        type    = str,
                        nargs   = '?',
                        metavar = "FILE")

    parser.add_argument(
                        "-f",
                        "--force",
                        help    = "Overwrite output file if it already exists.",
                        action  = "store_true",
                        dest    = "force")
    parser.add_argument(
                        "-o",
                        "--output",
                        help    = "The output of the result will be saved to this file.",
                        type    = str,
                        nargs   = '?',
                        dest    = "output_path")
    parser.add_argument(
                        "--format",
                        help    = "Output color format. Default = 'hex'",
                        type    = str,
                        default = 'hex',
                        choices = ['hex','rgb','hsv'],
                        dest    = "output_format")
    parser.add_argument(
                        "--include-hashtag", 
                        help    = "Include '#' before hex color in output. Default = False", 
                        action  = "store_true")
    parser.add_argument(
                        "-c",
                        "--clusters",
                        help    = "The number of color clusters to pick colors from. Default = 20",
                        type    = int,
                        default = 20,
                        nargs   = '?',
                        dest    = "num_clusters")
    parser.add_argument(
                        "-n",
                        "--number",
                        help    = "The number of colors to output. Default = 5",
                        type    = int,
                        default = 5,
                        nargs   = '?',
                        dest    = "num_colors")
    parser.add_argument(
                        "-s",
                        "--sort",
                        help    = "The criteria to sort the colors by. Default = 'frequency'",
                        type    = str,
                        default = 'frequency',
                        choices = ['frequency','saturation', 'brightness'],
                        dest    = "sort_by")
    parser.add_argument(
                        "-m",
                        "--mod",
                        help    = "The modify the colors properties before sorting.",
                        type    = str,
                        choices = ['max-val','max-sat'],
                        nargs   = '+',
                        dest    = "mod")
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help    = "Increase output verbosity.",
                        action  = "store_true")
    args = parser.parse_args()

    # Print help if no given arguments
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return args


def hsv2rgb(hsv):
    """
    Convert HSV color to RGB color.
    :param hsv: tuple of HSV color values (h, s, v)
    :return: tuple of RGB color values (r, g, b)
    """
    h, s, v = hsv[0]/360.0, hsv[1]/255.0, hsv[2]/255.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    rgb = tuple(int(x * 255) for x in (r, g, b))

    return rgb


def rgb2hsv(rgb):
    """
    Convert RGB color to HSV color.
    :param rgb: tuple of RGB color values (r, g, b)
    :return: tuple of HSV color values (h, s, v)
    """
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hsv = (h * 360, s * 255, v * 255)

    return hsv 


def rgb2hex(rgb):
    """
    Convert RGB color to hex color.
    :param rgb: tuple of RGB color values (r, g, b)
    :return: hex color string
    """
    r, g, b = (int(x) for x in rgb)
    hex_str = '{:02x}{:02x}{:02x}'.format(r, g, b)
    
    return hex_str 


def find_most_frequent_colors(img_path, num_clusters, verbose=False):
    """
    Find the most frequent colors in an image using k-means clustering.
    :param img_path: path to image file
    :param num_clusters: number of clusters to use in k-means
    :param verbose: whether to print verbose output
    :return: list of HSV color values, sorted by frequency in descending order
    """
    if verbose: 
        print('[+] Reading image...')

    im = Image.open(img_path)
    im = im.resize((150, 150)) # Resize image to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    if verbose: 
        print(f'[+] Finding clusters...')

    # K-means clustering algorithm
    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters) 

    # Assign code and count occurances
    vecs, dist = scipy.cluster.vq.vq(ar, codes)     
    counts, bins = np.histogram(vecs, len(codes))   

    # Convert RGB codes to HSV codes
    codes_hsv = [rgb2hsv(code) for code in codes]

    # Sort clusters by frequency
    indexed = sorted(enumerate(counts), key=lambda i: i[1], reverse=True) 
    hsv_list_descending_common = []

    for index, count in indexed:
        hsv_list_descending_common.append(tuple(codes_hsv[index]))

    return hsv_list_descending_common


# Gather our code in a main() function
def main():
    # Parse command line arguments
    args = parse_arguments()

    # Setup logging
    #loglevel = logging.DEBUG if args.debug else logging.INFO if args.verbose else logging.WARNING
    #logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    # Run until exits or SIGINT is received.
    if args.verbose: print('Running. Press CTRL-C to exit.')
    while True:
        
        pytext = pyTextColor.pyTextColor()

        if args.verbose:
            # Start timer
            t = Timer()
            t.start()
            
            # Create banner
            script_name = os.path.splitext(os.path.basename(__file__))[0]
            banner_text = f"------ {script_name} ------>"
            
            # Format and print
            banner = pytext.format_text(text=banner_text, color="blue")
            print(banner)

        # Arguments
        output_format = args.output_format
        include_hashtag = args.include_hashtag
        img_path = args.argument
        output_path = args.output_path
        num_clusters = args.num_clusters
        sort_by = args.sort_by
        num_colors = args.num_colors
        mod = args.mod

        # Check if input file exists and is a valid image file
        if not os.path.isfile(img_path):
            print(pytext.format_text(text="[-] Invalid image path.", color="red"))
            exit(0)
        try:
            img = Image.open(img_path)
        except Exception as e:
            print(pytext.format_text(text="[-] Invalid image file.", color="red"))
            exit(0)

        if num_colors > num_clusters:
            print('[!] Number of clusters adjusted to match number of desired colors.')
            num_clusters = num_colors

        # Print arguments (if verbose flag is True)
        if args.verbose:
            print(f"Image path: {img_path}")
            print(f"Output path: {output_path}")
            print(f"Output format: {output_format}")
            if output_format == 'hex':
                print(f"Include hashtag: {include_hashtag}")
            print(f"Number of clusters: {num_clusters}")
            print(f"Sort by: {sort_by}")
            print(f"Number of colors: {num_colors}")
            print(f"Mod: {mod}")

            # Divider
            div = len(banner_text)*"-"+">"
            print(pytext.format_text(text=div, color="blue"))


        try:
            # Get most frequent colors
            palette = find_most_frequent_colors(img_path, num_clusters, verbose=args.verbose)
        except Exception as e:
            print(e)
            print(pytext.format_text(text="[-] Invalid image file.", color="red"))
            exit(0)

        # Sorting
        if sort_by == 'saturation':
            palette = sorted(palette, key = lambda x: x[1])
        elif sort_by == 'brightness':
            palette = sorted(palette, key = lambda x: x[2])

        # Loop through the palette, starting at the last color
        output_colors = []
        for i, hsv_color in enumerate(palette[-num_colors:], start=1):

            if mod:
                if 'max-sat' in mod: hsv_color[1] = 255
                if 'max-val' in mod: hsv_color[2] = 255
            
            rgb_color = hsv2rgb(hsv_color)
            hex_color = rgb2hex(rgb_color)

            if output_format == 'rgb':
                color = tuple(map(round, rgb_color))
            elif output_format == 'hex':
                if output_format == "hex" and args.include_hashtag:
                    color = '#' + hex_color
                else:
                    color = hex_color
            elif output_format == 'hsv':
                color = tuple(map(round, hsv_color))
            else:
                print("[-] Invalid output format")

            output_colors.append(color)

            # Format the text and background color of the print statement
            text_color = "#ffffff" if hsv_color[2] < 128 else "#000000"
            pytext_palette = pytext.format_text(text=color, color=text_color, bgcolor='#'+hex_color)

            print(f'[{num_colors-i+1}] {pytext_palette}')

        # Output
        if output_path and os.path.exists(os.path.dirname(output_path)):

            if os.path.isfile(output_path) and not args.force:
                user_input = input(f"[!] Output file {output_path} already exists. Do you want to overwrite? (y/n): ")
                if user_input != 'y':
                    print(f"[+] Exiting without overwriting {output_path}")
                    exit(0)
            
            with open(output_path, 'w') as f:
                
                # Save as ascending list, most common on top
                for item in output_colors[::-1]:
                    f.write(f'{item}\n')

            if args.verbose: print(f'[+] Saved to {output_path}')

        else:
            print(pytext.format_text(text="[-] Invalid path.", color="red"))
            exit(0)
        
        if args.verbose: t.stop()
        exit(0)

# Call the main() function to begin the program.
if __name__ == "__main__":
    main()