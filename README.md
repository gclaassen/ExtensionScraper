# Extension Scraper

_V1.0.0_ *(updates incoming)*

## Scraper Scripts

- Written in Python

- These scrapers will allow the user to search in set source directories (all folders and subfolders in the source directory) for files with a set extension (and/or EXIF info).

- The files matching the extension will either be moved or copied to a destination directory

- The files will be renamed in the date and time of the ext

### pyPhotographScraper.py:

- Check exif data if a jpg otherwise ignore if stated in argument

- The images will be stored in a directory structure starting with make and then model:
  - /make/
    - /model/
      - 2012_02_03_14_00.jpg
      - 2012_02_03_14_01.jpg
      - 2012_02_03_14_02.jpg

## Argument List

| Command | Description                                      | Example        |
| ------- | ------------------------------------------------ | -------------- |
| -t      | File extension to be moved/copied                | -t _.ext1_ _.extn_      |
| -s      | Source Directory                                 | -s _src/dir/_  |
| -d      | Destination Path                                 | -d _dest/dir/_ |
| -c      | Copy the file to the destination **OR**          | -c             |
| -m      | Move the file from the source to the destination | -m             |
| -z      | Check all the ext types not only EXIF            | -z             |

Run **\_\_runScraper.bat**
or call command in terminal:

```
python ./pyscraper.py "-t" ".jpg" "-s" "c:/" "-d" "f:/scrapedFiles/" "-c" "-z"
```

## Required Modules

- exif (pyPhotographScraper.py)
- os
- getopt
- sys
- shutil
- time
- datetime

## Python

- Python 3.7.3

*vir ma. lief ma baie*
