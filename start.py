import praw
import time
import string
from win10toast import ToastNotifier
import webbrowser
from playsound import playsound

toaster = ToastNotifier()

reddit = praw.Reddit(client_id="1t0X1QMmWv8JMQ",
                     client_secret="Vgjq9re806hAC6YqMmCAThY1YOE", user_agent="states95")

lastURL = ""

NUMBER_ARRAY = [
    ["0", "zero"],
    ["1", "one", "uni", "une", "uno"],
    ["2", "two", "dos"],
    ["3", "three", "thirty", "tree", "tres"],
    ["4", "four", "fourty", "quatro"],
    ["5", "five", 'fifty', "fiive", "cinco"],
    ["6", "six", "sixty", "seis"],
    ["7", "seven", "seventy", "siete"],
    ["8", "eight", "eighty", "ocho"],
    ["9", "nine", "ninety", "nueve"]
]


def readValue(post):
    return parseValue(post)


def parseValue(post):
    wordExist = False

    for index, t in enumerate(NUMBER_ARRAY):
        for i in t:
            if post.find(i) != -1:
                wordExist = True
                post = post.replace(i, str(index))
    if wordExist:
        print("Converted: " + post)

    return parseNumbers(post)


# Grab Numbers from Converted Post Title
def parseNumbers(post):
    consectuiveNumbers = 0
    output = ""
    for char in post:
        if char.isdigit() and len(output) < 3:
            consectuiveNumbers += 1
            output += char
    print("Final Value: " +
          output+"\n")
    return output

def openURL():
    webbrowser.open(lastURL, new=2)

print("*****Animal Crossing Turnip Exchange Price Checker*****")
min_price = input("Minimum Price (Default is 0): ")

while True:
    if min_price.isdigit() and len(min_price) <= 3 and len(min_price) >= 1 and int(min_price) >= 0:
        break
    elif min_price == "":
        min_price = 0
        break
    else:
        if len(min_price) > 3 and len(min_price) < 1:
            print("Invalid Input - Must be a Number between 0-999")
        else:
            print("Invalid Input - Only Enter Numbers")
        min_price = input("Minimum Price: ")

print("Setting Minimum Price to: " + str(min_price))

while True:
    print("Checking /r/acturnips Every 10 Seconds for New Posts")
    for submission in reddit.subreddit("acturnips").new(limit=1):
        print(submission.title)
        print(submission.url)
        value = readValue(submission.title)
        if lastURL != submission.url and int(min_price) <= int(value):
            lastURL = submission.url
            #playsound('Master Sword.mp3')
            toaster.show_toast("New Turnip Price", submission.title + "\n" + value, icon_path="leaf_icon.ico")

    time.sleep(10)
