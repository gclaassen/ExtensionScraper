# Extension Scraper
*In Development*

Scraper Scripts written in Python

These scrapers will allow the user to search in set source directories (all folders and subfolders in the source directory) for files with a set extension (and EXIF info).

The files matching the extension will either be moved or copied to a destination directory

## Argument List
| Command | Description | Example |
| ------- | ----------- | ------- |
| -t      | File extension to be moved/copied | -t *.ext* |
| -s      | Source Directory | -s *src/dir/* |
| -d      | Destination Path | -d *dest/dir/* |
| -c      | Copy the file to the destination **OR** | -c |
| -m      | Move the file from the source to the destination | -m |

Run **__runScraper.bat**
or call command in terminal:
```
python ./pyscraper.py "-t" ".jpg" "-s" "c:/" "-d" "f:/scrapedFiles/" "-c" 
```

## Required Modules
- exif (photograph)
- os
- getopt
- sys
- shutil
- time

## Python
- Python 3.7.3
