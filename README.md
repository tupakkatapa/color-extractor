# Color Extractor

A command-line tool for extracting dominant colors from an image.

I use this program to extract the most saturated color from my randomly changing desktop wallpaper to sync my LED lights with.

## Installation

```console
$ git clone https://github.com/tupakkatapa/color-extractor.git

$ cd color-extractor

$ pip3 install -e .
```

## Usage

```console
$ color-extractor [path to image file] [options]
```

**Important note**: The order of the options [--number], [--sort], and [--mod] provided matters. Multiple instances of these options can be used and the actions will be performed in the order they were provided. If the number of wanted colors (--number) is not specified but other actions are (--sort or --mod), the limiting to the desired number of colors will always be performed last.

## Options

```console
$ color-extractor --help
usage: color_extractor.py [-h] [-f] [-o [OUTPUT_PATH]] [--format {hex,rgb,hsv}] [--include-hashtag] 
                          [-c [NUM_CLUSTERS]] [-n NUM_COLORS] [-s {saturation,value,brightness,chroma}]
                          [-r] [-m {max-val,max-sat}] [-v] [FILE]

Command-line tool for extracting dominant colors from an image.
--------------------------------------------------------------------------
https://github.com/tupakkatapa/color-extractor
--------------------------------------------------------------------------
The order of the options [--number], [--sort], and [--mod] provided mattersand these options can have many instances.

positional arguments:
  FILE                  Required. The path to the image file.

options:
  -h, --help            show this help message and exit
  -f, --force           Overwrite output file if it already exists. Default = False
  -o [OUTPUT_PATH], --output [OUTPUT_PATH]
                        The output of the result will be saved to this file.
  --format {hex,rgb,hsv}
                        Output color format. Default = 'hex'
  --include-hashtag     Include '#' before hex color in output. Default = False
  -c [NUM_CLUSTERS], --clusters [NUM_CLUSTERS]
                        The number of color clusters to pick colors from. Default = 20
  -n NUM_COLORS, --number NUM_COLORS
                        The number of colors to output. Default = 5
  -s {saturation,value,brightness,chroma}, --sort {saturation,value,brightness,chroma}
                        The criteria to sort the colors by. Default = 'frequency'
  -r, --reverse         Reverse the sort order. Default = False
  -m {max-val,max-sat}, --mod {max-val,max-sat}
                        Modify the color properties. 'max-val' maximizes the value/brightness of the color(s) 
                        and 'max-sat' maximizes the saturations of the color(s). Default = None
  -v, --verbose         Increase output verbosity.
```

## Examples

1. Find (20) color clusters from an image, sort them by frequency, pick the top 5 and print them to the console:

```console
$ color-extractor image.jpg
```

2. Find (20) color clusters from an image, pick the top 10, sort them by saturation and write the output to a file:

```console
$ color-extractor image.jpg -n 10 -s brightness -o output.txt
```

3. Find 30 color clusters from an image, sort them by saturation, pick the top one, maximize value and saturation and write the output to a file in the cache directory:

```console
$ color-extractor ~/pictures/wallpapers/image.jpg -c 30 -s saturation -n 1 -m max-val max-sat -o ~/.cache/color
```

## Links

https://stackoverflow.com/a/3244061


