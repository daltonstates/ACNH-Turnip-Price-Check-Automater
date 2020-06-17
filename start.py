import praw
import time
import string
from win10toast import ToastNotifier
import webbrowser
from playsound import playsound

toaster = ToastNotifier()

reddit = praw.Reddit(client_id="1t0X1QMmWv8JMQ",
                     client_secret="Vgjq9re806hAC6YqMmCAThY1YOE", user_agent="states95")

# print(reddit.read_only)  # Output: True


NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

lastURL = ""

NUMBER_ARRAY = [
    ["0", "zero"],
    ["1", "one", "uni", "une"],
    ["2", "two"],
    ["3", "three", "thirty", "tree"],
    ["4", "four", "fourty"],
    ["5", "five", 'fifty', "fiive"],
    ["6", "six", "sixty"],
    ["7", "seven", "seventy"],
    ["8", "eight", "eighty"],
    ["9", "nine", "ninety"]
]


def readValue(post):
    stripPost = post.replace("-", "")

    return parseValue(stripPost)


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
    foundConsecutiveNumber = False
    output = ""
    for char in post:
        if char in NUMBERS and len(output) < 3:
            consectuiveNumbers += 1
            output += char
    print("Final Value: " +
          output+"\n")
    return output


def openURL():
    webbrowser.open(lastURL, new=2)


while True:
    for submission in reddit.subreddit("acturnips").new(limit=1):
        print(submission.title)
        print(submission.url)
        if lastURL != submission.url:
            lastURL = submission.url
            playsound('Master Sword.mp3')
            toaster.show_toast("New Turnip Price", submission.title + "\n" + readValue(
                submission.title), icon_path="leaf_icon.ico", callback_on_click=openURL)
                
    time.sleep(10)
