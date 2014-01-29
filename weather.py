#!/usr/bin/python2.7
import getpass
import sys
import urllib2
import feedparser


def out(to_out):
    sys.stderr.write(to_out + "\n")
user_name = getpass.getuser()
config_file = open(".config/weather/config", "r")
config_file_info = config_file.readlines()
config_file.close()
WOEID = config_file_info[0].strip()
f_c = 0
if config_file_info[1].strip() == "f":
    f_c = "f"
elif config_file_info[1].strip() == "c":
    f_c = "c"
else:
    out("Ruh-roh, there seems to be an issue with your config file. Try running weather.py r")
    exit(1)
url = "http://weather.yahooapis.com/forecastrss?w={}".format(WOEID)
if f_c == "c":
    url += "&u=c"
request = urllib2.urlopen(url)
response = request.read()
if "Yahoo! Weather - Error" in response:
    out("Seems to be an issue with either your WOEID or Yahoo")
    exit()
feed = feedparser.parse(response)
other = feed['feed']['title']
current_cond = str(feed).split("Current Conditions:")[1]
current_cond = current_cond.split("\\n")
current_cond = " ".join(current_cond).split()[2:5]
current_cond = " ".join(current_cond).replace("<br", "")
other = other.split("-")[1]
print """
Hello {0}!\n
In {1} right now it is\n
{2}
""".format(user_name, other, current_cond)