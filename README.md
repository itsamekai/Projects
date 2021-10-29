# Youtube-Comment-Scraper

Scrapes comments from youtube given a URL and exports it as a csv file, and allow translation of comments if needed. Requires [ChromeDriver.](https://chromedriver.chromium.org/)

------
### Usage

```
>etract_comments.py -h

usage: extract_comments.py [-h] [-s source] [-d destination] url
scrape comments from youtube, with the option to translate the data to another language.

positional arguments:
  url             Youtube URL

optional arguments:
  -h, --help      show this help message and exit
  -s source       source language if applicable, auto detected if not stated
  -d destination  translated language

>extract_comments.py -d en https://www.youtube.com/watch?v=gk4Zyu5-W7Y&ab_channel=Epicurious
```
-------
### Extracted File Location
The extracted data will be in a csv file at the file directory of the code, for example:
```
D:/Youtube-Comment-Scraper/comments.csv
```
------
### Languages Available
If the source language is not provided, google translate will try to automatically detect the source language. By default, it is using Google translate.

The languages available can be seen in the documentation [here.](https://pypi.org/project/translate-api/)

