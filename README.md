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

## Options

```console
$ color-extractor --help
usage: color-extractor [-h] [-f] [-o [OUTPUT_PATH]] [--format {hex,rgb,hsv}] [--include-hashtag] 
                       [-c [NUM_CLUSTERS]] [-n [NUM_COLORS]] [-s {saturation,value,brightness,chroma}] 
                       [-m {max-val,max-sat} [{max-val,max-sat} ...]] [-v]
                       [FILE]

Command-line tool for extracting dominant colors from an image.
--------------------------------------------------------------------------
https://github.com/tupakkatapa/color-extractor

positional arguments:
  FILE                  Required. The path to the image file.

options:
  -h, --help            show this help message and exit
  -f, --force           Overwrite output file if it already exists.
  -o [OUTPUT_PATH], --output [OUTPUT_PATH]
                        The output of the result will be saved to this file.
  --format {hex,rgb,hsv}
                        Output color format. Default = 'hex'
  --include-hashtag     Include '#' before hex color in output. Default = False
  -c [NUM_CLUSTERS], --clusters [NUM_CLUSTERS]
                        The number of color clusters to pick colors from. Default = 20
  -n [NUM_COLORS], --number [NUM_COLORS]
                        The number of colors to output. Default = 5
  -s {saturation,value,brightness,chroma}, --sort {saturation,value,brightness,chroma}
                        The criteria to sort the colors by. Default = 'frequency' 
                        (NOTE: the order of the arguments matters when used with --number)
  -m {max-val,max-sat} [{max-val,max-sat} ...], --mod {max-val,max-sat} [{max-val,max-sat} ...]
                        Modify the colors properties before sorting.
  -v, --verbose         Increase output verbosity.
```

## Examples

1. Find (20) color clusters from an image, sort them by frequency, pick the top 5 and print them to the console:

```console
$ color-extractor image.jpg
```

2. Find (20) color clusters from an image, pick the top 10, sort them by saturation and write the output to a file:

```console
$ color-extractor image.jpg -n 10 -s saturation -o output.txt
```

3. Find 30 color clusters from an image, sort them by saturation, pick the top one, maximize value and saturation and write the output to a file in the cache directory:

```console
$ color-extractor ~/pictures/wallpapers/image.jpg -c 30 -n 1 -s saturation -m max-val max-sat -o ~/.cache/color
```

## Links

https://stackoverflow.com/a/3244061


