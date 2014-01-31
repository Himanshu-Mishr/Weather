import sys
import os
import time
import shutil


def out(to_out, stat=None):
    """
    This is a function for output to the terminal, it is to dictate the format in which info should
    be printed
    """
    green = "\033[92m"
    red = '\033[91m'
    reg = '\033[0m'
    if stat is None:
        sys.stderr.write(to_out + "\n")
    elif stat == "good":
        sys.stderr.write(green + "[+]" + reg + to_out + "\n")
    elif stat == "bad":
        sys.stderr.write(red + "[-]" + reg + to_out + "\n")
    else:
        raise ValueError("Invalid type")


def clean_up():
    out("Attempting to remove any other files associated")
    try:
        os.remove(".config/weather/config")
        out("Config file removed", "good")
    except IOError:
        out("Config file didn't exist...")

out("Note: This is an installer, please run this as root. If you are not, please exit now and rerun (5 seconds)")
#time.sleep(5)
out("Searching for installation...")  # Tell the user we are searching for the install
if not os.path.exists("/usr/local/bin/weather.py"):  # Check if it is installed
    out("None found", "good")  # Nothing installed
else:
    out("Installation found, would you like to remove?", "bad")  # Something is installed, prompt for removal
    answer = raw_input("(Y/n):\n")
    if not answer.isalpha():
        out("Please, only use characters, exiting", "bad")
        exit(1)
    if answer.lower().strip() in ["y", "n"]:
        if answer.lower() == "y":
            try:
                os.remove("/usr/local/bin/weather.py")
                out("Successfully removed", "good")
                clean_up()
            except OSError:
                exit()
        else:
            out("Exiting..", "good")
            exit()
if not os.getuid() == 0:
    out("This is an installer, it MUST be run as root", "bad")
    sys.exit(1)
out("Beginning install", "good")
shutil.copy2('weather.py', '/usr/local/bin')
os.chmod("/usr/local/bin/weather.py", 0755)
out("Ok, so firstly, I need to know, what is your WOEID? Don't worry, it's easy to find, google it\n.")
WOEID = raw_input("Ok, please enter your WOEID:\n")
out("Great, now do you want Fahrenheit, or Celsius? (f/c)\n")
f_c = raw_input()
out("Great, now, if you come across errors in the future, try resetting your config file (weather.py r)", "good")
out("Writing config file (can be found in .config/weather/config)", "good")
try:
    os.makedirs("/home/.config/weather")
except OSError:
    pass
config_file = open("/home/.config/weather/config", "w")
config_file.write(WOEID + "\n")
config_file.write(f_c + "\n")
config_file.close()
out("Finished writing config", "good")
out("This weather is provided by Yahoo! Weather")