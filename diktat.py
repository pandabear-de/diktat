import logging
import csv
import random
from datetime import datetime
import configparser

# uncomment appropiatly default
loglevel = 'DEBUG'
# loglevel = 'INFO'
# loglevel = 'WARNING'
# loglevel = 'ERROR'
# loglevel = 'CRITICAL'

# Create and config logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
if loglevel == 'DEBUG':
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        filemode='w')
elif loglevel == 'INFO':
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.INFO,
                        format=LOG_FORMAT,
                        filemode='w')
elif loglevel == 'WARNING':
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.WARNING,
                        format=LOG_FORMAT,
                        filemode='w')
elif loglevel == 'ERROR':
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.ERROR,
                        format=LOG_FORMAT,
                        filemode='w')
elif loglevel == 'CRITICAL':
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.CRITICAL,
                        format=LOG_FORMAT,
                        filemode='w')
else:
    logging.basicConfig(filename="/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        filemode='w')

logger = logging.getLogger()

if loglevel not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
    logger.error(
        '!!! LogLevel in ini file not correct! - needs to be in (DEBUG, INFO, WARNING, ERROR, CRITICAL) - Set default DEBUG')

# logger.debug("Test Msg Debug")
# logger.info("Test Msg Info")
# logger.warning("Test Msg Warning")
# logger.error("Test Msg Error")
# logger.critical("Test Msg Critical")

# Read ini parameters
config = configparser.ConfigParser()
config.read('diktat.ini')

try:
    file_path = config['Paths']['file_path']
    file_wordlist_name = config['Paths']['file_wordlist_name']
    file_wordlistOUT_name = config['Paths']['file_wordlistOUT_name']
    DefaultWordList = str(config['Personalization']['DefaultWordList'])
    PracticeListSize = int(config['Personalization']['PracticeListSize'])
    logger.debug("### Read ini parameters ###")
    logger.debug("file_path: " + file_path)
    logger.debug("file_wordlist_name: " + file_wordlist_name)
    logger.debug("file_wordlistOUT_name: " + file_wordlistOUT_name)
    logger.debug("DefaultWordList: " + DefaultWordList)
    logger.debug("PracticeListSize: " + str(PracticeListSize))

except KeyError as e:
    logger.error("Path could not be set from ini: " + str(e))
    file_path = ''
    file_wordlist_name = ''
    file_wordlistOUT_name = ''
    DefaultWordList = ''
    PracticeListSize = 0
except Exception as e:
    logger.error("read from ini: " + str(e))
    raise


class Word:
    def __init__(self, user, insert_date, word, last_test_date, number_tests, consecutive_correct):
        """definition of WORD class"""
        self.user = user
        if insert_date == "":
            self.insert_date = datetime.now().date()
        else:
            self.insert_date = datetime.strptime(insert_date, '%Y%m%d')  # yyyymmdd
        self.word = word
        if last_test_date == "":
            self.last_test_date = datetime.now().date()
        else:
            self.last_test_date = datetime.strptime(last_test_date, '%Y%m%d')  # yyyymmdd
        self.number_tests = number_tests
        self.consecutive_correct = consecutive_correct

    def test_word(self, test_result):
        """Function to set the word-tested counter up by one and also sets the consecutive correct counter based on the test result. If the result is false, then the consequative counter is set back to 0"""
        logger.debug("### test_word ###")
        self.last_test_date = datetime.now().date()
        self.number_tests = self.number_tests + 1
        if test_result:
            self.consecutive_correct = self.consecutive_correct + 1
        elif not test_result:
            self.consecutive_correct = 0


def read_wordlist():
    """read_wordlist reads __read_wordlist__ into memory"""
    logger.debug("###Entered into read_wordlist ###")
    logger.debug("Open File: " + file_path + file_wordlist_name)

    data = []
    try:
        file = open(file_path + file_wordlist_name, newline='')
        reader = csv.reader(file)
    except FileNotFoundError:
        logger.error("Wordlist - File not found")
        return data
    except NameError:
        logger.error("Wordlist - NameError ")
        return data
    except Exception as e:
        logger.error("read wordlist other error: " + str(e))
        raise

    header = next(reader)  # The first line is the header

    for row in reader:
        user = row[0]
        insert_date = row[1]  # YYYYMMDD
        word = row[2]
        last_test_date = row[3]  # YYYYMMDD
        number_tests = int(row[4])
        consecutive_correct = int(row[5])
        data.append(Word(user, insert_date, word, last_test_date, number_tests, consecutive_correct))

        # debug print data
        #        for i in range(len(data) - 1):
        #            logger.debug(data[i])
    file.close()
    return data


def write_wordlist(wordlist):
    """Saves CSV to drive"""
    logger.debug("### write_wordlist ###")
    try:
        with open(file_path + file_wordlistOUT_name, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(("User", "Insert_Date", "Word", "Last_Test_Date", "Number_Tests", "Consecutive_Correct"))
            for i in range(0, len(wordlist)):
                writer.writerow((wordlist[i].user, wordlist[i].insert_date.strftime('%Y%m%d'), wordlist[i].word,
                                 wordlist[i].last_test_date.strftime('%Y%m%d'), str(wordlist[i].number_tests),
                                 str(wordlist[i].consecutive_correct)))

        csv_file.close()
    except FileNotFoundError:
        logger.error("Wordlist could not be written - File not found")
        return "false"
    except Exception as e:
        logger.error("write wordlist other error: " + str(e))
        raise


def add_word(wordlist, user, word):
    """helper to add a new word to the wordlist"""
    logger.debug("### add_word ###")
    logger.debug("added User: " + user + " Word: " + word)
    wordlist.append(Word(user, "", word, "", 0, 0))
    return wordlist


def get_practice_wordlist_current(user, numberwords_current, wordlist):
    """Creates a word list of current words"""
    try:
        practice_wordlist_current = random.sample(wordlist, numberwords_current)
    except ValueError:
        logger.error("practice_wordlist_current - no wordlist available")
        practice_wordlist_current = []
    except Exception as e:
        logger.error("write wordlist other error: " + str(e))
        raise

    return practice_wordlist_current


def get_practice_wordlist_previous(user, numberwords_previous, wordlist):
    """Creates a word list for non-current words"""
    pass


def select_practice_words(user, numberwords_current, numberwords_previous, wordlist):
    """Based on inputs (listname and number of words the practice lists should have) the function creates a list of random word-list"""
    logger.debug("### Entered select_practice_words ###")
    practice_wordlist = []
    practice_wordlist = get_practice_wordlist_current(user, numberwords_current,
                                                      wordlist)  # get_practice_wordlist_previous(user,numberwords_previous,wordlist)
    for i in range(0, len(practice_wordlist)):
        logger.debug(str(i) + ": " + practice_wordlist[i].word)
    return practice_wordlist


def settings():
    """Used to personalize settings of application. Settings are saved to ini file"""
    logger.info("### Entered Settings ###")

    try:
        # add the settings to the structure of the file, and lets write it out...
        config.set('Personalization', 'DefaultWordList', DefaultWordList)
        config.set('Personalization', 'PracticeListSize', str(PracticeListSize))
        logger.debug("DefaultWordList: " + DefaultWordList)
        logger.debug("PracticeListSize: " + str(PracticeListSize))

        logger.info("### Save Settings ###")
        # Writing our configuration file to 'example.ini'
        with open('diktat.ini', 'w') as configfile:
            config.write(configfile)
    except configparser.NoSectionError:
        logger.error("Settings could not be saved")
        return "false"
    except Exception as e:
        logger.error("Save settings: " + str(e))
        raise


def print_menu():
    """Prints simple Menu to screen"""
    logger.info("### PrintMenu ###")
    print('1 Einstellungen')
    print('2 Wörter üben')
    print('3 Wörter hinzufügen')
    print('4 Wörter anzeigen')
    print('9 Ende')


def main():
    # wordlist = []
    wordlist = read_wordlist()  # read current word list
    # print(wordlist[0].word)  # print word
    # wordlist[0].test_word(bool(1)) # this is how to record a test of a word. 0->mistake, 1-> correct

    # wordlist = add_word(wordlist,"Kind1","Tür")  # this is how to add a new word
    # practice_wordlist = select_practice_words(DefaultWordList, PracticeListSize, 0, wordlist)  # compile random practice wordlist
    # for i in range(0, len(practice_wordlist)):  # print current practice wordlist
    #    print(practice_wordlist[i].word)

    # print ("write_status: " + str(write_status))

    menu = 0
    print_menu()
    while menu == 0:
        menu = input('Auswahl?')
        if menu == '1':
            logger.info("### Settings selected ###")
            settings()
            menu = 0
        elif menu == '2':
            logger.info("### Practice words ###")
            practice_wordlist = select_practice_words(DefaultWordList, PracticeListSize, 1,
                                                      wordlist)  # compile random practice wordlist
            menu = 0
        elif menu == '3':
            logger.info("### Add words ###")
            menu = 0
        elif menu == '4':
            logger.info("### List words ###")
            menu = 0
        elif menu == '9':
            logger.info("### Exit menu ###")
            break
        else:
            logger.info("### Incorrect menu selection ###")
            menu = 0

    write_status = write_wordlist(wordlist)  # update/write wordlist to file


if __name__ == "__main__":
    main()
