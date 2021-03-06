#!/usr/bin/python2.7
import getpass
import sys
import urllib2
import feedparser
import os
import argparse

user_name = getpass.getuser()


def out(to_out):
    sys.stdout.write(to_out + "\n")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", help="Resets configuration file")
args = parser.parse_args()
if args.option:
    out("Are you sure you want to remove your config? (Y/n)")
    response = raw_input()
    if response.lower() in ['y', 'n']:
        if response.lower() == 'y':
            out("Removing config....")
            new_woed = raw_input("What is your WOIED?\n")
            f_c = raw_input("f/c\n")
            dir_ = "/home/" + user_name + "/.config/weather/config"
            out("Removing old config...")
            try:
                os.remove(dir_)
            except OSError:
                out("Error")
                exit(1)
            out("Writing new config...")
            config = open(dir_, "w")
            config.write(new_woed + "\n")
            config.write(f_c + "\n")
            config.write(user_name + "\n")
            out("Completed!")
            exit()
        else:
            out("Aborting...")
            exit()
a = "/home/" + user_name + "/.config/weather/config"
config_file = open(a, "r")
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
In {1} """.format(user_name.title(), other)


# my fun with it....
b = feed['entries'][0]['summary_detail']
b = b['value']
while '<' in b or '>' in b:
    b = b.replace(b[b.find('<'):b.find('>')+1],"")
c = b.split('\n')
print c[1], c[2]
print "\n"
print c[3]
print c[4]
print c[5]
print c[6]
print c[7]
print c[8]






