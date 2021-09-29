import csv
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import requests
import re
import argparse
import translators as ts


# this script does not get replies of comments as i think it is redundant / will only contribute towards the main comment's purpose
# eg when doing analysis, if the main comment is about: "oh i like this person" -> the replies will mainly be about contributing postivity towards the main comment

# run it thru cmd by: py extract_comments.py <url>

# script requires the use of chromedriver.exe

parser = argparse.ArgumentParser(description='scrape comments from youtube, with the option to translate the data to another language.')
parser.add_argument('URL', metavar="url", type=str, help='Youtube URL')
parser.add_argument('-s', metavar="source", type=str, help='source language if applicable, auto detected if not stated')
parser.add_argument('-d', metavar="destination", type=str, help='translated language')

args = parser.parse_args()
# url[1] is the link
# returns status code 200 if valid, url can be accessed
# also checks with regex if the link is valid
validate = requests.get(args.URL, allow_redirects=False)
if validate.status_code == 200 and re.match('^(http(s?):\/\/)?(www\.)?youtu(be)?\.([a-z])+\/(watch(.*?)(\?|\&)v=)?(.*?)(&(.)*)?$', args.URL):
    
    with Chrome(executable_path=r'C:\Users\resay\Downloads\chromedriver.exe') as driver:
        wait = WebDriverWait(driver,15)
        driver.get(args.URL)
        time.sleep(5)
        try:
            unavailable_check = driver.find_element_by_xpath('//*[@id="reason"]')
            if unavailable_check:
                print("Given URL is not a valid Youtube URL or the video does not exist.")
                driver.close()
        except:
            print("URL validated. Please wait.")
            print("Scraping comments from: " + args.URL)
            # gets xpaths: 
            # title of the video
            title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
            # comments's xpath
            comments = driver.find_element_by_xpath('//*[@id="comments"]')
        

            # the scroll part is the most confusing thing about extracting data from youtube, don't really understand this yet. kinda copied this off the internet 
            # scroll down
            last_height = driver.execute_script("return document.documentElement.scrollHeight")
            count = 0
            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(1.5)
        
            # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # scrolls 1 last time just in case
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            #username and comment's xpath
            username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
            comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
            date_elems = driver.find_elements_by_xpath('//*[@id="header-author"]/yt-formatted-string/a')
            upvote_elems = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')


            # utf-8 encoding writes to new column but utf-16 doesn't?
            # utf-8 does not support emoji so it will look weird on excel. cannot use utf-16 dew to formatting issues.
            file = open('comments.csv', "w", newline='', encoding="utf-8")
            writer = csv.writer(file)   
            # writes the title of video, url of video, and the date when this data is pulled.
            writer.writerow([title, args.URL, date.today()])
            # empty row to break
            writer.writerow(["Username", "Comment", "Date", "Likes"])
            # loops thru the elements and gets the text, write it into excel.

            # translate-api too slow - but its the only one that works well
            # https://pypi.org/project/translate-api/
            # googletrans is buggy

            
            if args.d and args.s:
                for username, comment, commented_date, upvote in zip(username_elems, comment_elems, date_elems, upvote_elems):
                    writer.writerow([username.text, ts.google(comment.text, from_language = args.s, to_language = args.d), commented_date.text, upvote.text])
            
            elif args.d and not args.s:
                for username, comment, commented_date, upvote in zip(username_elems, comment_elems, date_elems, upvote_elems):  
                    writer.writerow([username.text, ts.google(comment.text, to_language = args.d), commented_date.text, upvote.text])
            
            else:
                for username, comment, commented_date, upvote in zip(username_elems, comment_elems, date_elems, upvote_elems):
                    writer.writerow([username.text, comment.text, commented_date.text, upvote.text])

            print("video URL: " + args.URL)
            print("Video Title: " + title)
            if args.s and args.d:
                print("translated from " + args.s + " to " + args.d)
            elif args.d and not args.s:
                print("translated to " + args.d)

            driver.close()

else:
    print("Given URL is not a valid Youtube URL or the video does not exist.")


