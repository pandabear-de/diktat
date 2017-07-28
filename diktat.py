import logging
import csv
import random
from datetime import datetime, timedelta, date

file_path = "/Users/jakob/documents/Python_Projects/diktat/"
file_wordlist_name = "wordlist.csv"
file_wordlistOUT_name = "wordlist.csv"

class Word:
    def __init__(self,user,insert_date,word,last_test_date,number_tests,consecutive_correct):
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

    #def add_word(self,user,word):
    #    logger.debug("### add_word ###")
    #    self.user = user
    #    self.insert_date = datetime.now().strftime('%Y%m%d-%H%M%S')  # yyyymmdd
    #    self.word = word
    #    #self.last_test_date = ""  # yyyymmdd
    #    self.number_tests = 0
    #    self.consecutive_correct = 0

    def test_word(self,test_result):
        logger.debug("### test_word ###")
        self.last_test_date = datetime.now().date()
        self.number_tests = self.number_tests + 1
        if test_result:
            self.consecutive_correct = self.consecutive_correct +1
        elif not test_result:
            self.consecutive_correct = 0

def read_wordlist():
    """read_wordlist reads __read_wordlist__ into memory"""
    logger.debug("###Entered into read_wordlist ###")
    #file_path = "/Users/jakob/documents/Python_Projects/"
    #file_wordlist_name = "wordlist.csv"
    logger.debug("Open File: " + file_path + file_wordlist_name)
    file = open(file_path + file_wordlist_name, newline='')
    reader = csv.reader(file)

    header = next(reader)  # The first line is the header
    data = []
    for row in reader:
        user = row[0]
        insert_date = row[1] #YYYYMMDD
        word = row[2]
        last_test_date = row[3] # YYYYMMDD
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
    with open(file_path + file_wordlistOUT_name, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(("User","Insert_Date","Word","Last_Test_Date","Number_Tests","Consecutive_Correct"))
        for i in range(0,len(wordlist)):
            writer.writerow((wordlist[i].user, wordlist[i].insert_date.strftime('%Y%m%d'), wordlist[i].word, wordlist[i].last_test_date.strftime('%Y%m%d'), str(wordlist[i].number_tests), str(wordlist[i].consecutive_correct)))

        csv_file.close()

def add_word(wordlist,user,word):
    logger.debug("### add_word ###")
    logger.debug("added User: " + user + " Word: " + word)
    wordlist.append(Word(user, "", word, "",  0, 0))
    return wordlist

# Create and config logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename= "/Users/jakob/documents/Python_Projects/diktat/diktat.log",
                    level= logging.DEBUG,
                    format= LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()

#Test the logger
#logger.debug("Test Msg Debug")
#logger.info("Test Msg Info")
#logger.warning("Test Msg Warning")
#logger.error("Test Msg Error")
#logger.critical("Test Msg Critical")

def get_practice_wordlist_current(user,numberwords_current, wordlist):
    practice_wordlist_current = random.sample(wordlist, numberwords_current)
    return practice_wordlist_current

def get_practice_wordlist_previous(user,numberwords_previous,wordlist):
    pass

def select_practice_words(user,numberwords_current, numberwords_previous, wordlist):
    logger.debug("### Entered select_practice_words ###")
    practice_wordlist = []
    practice_wordlist = get_practice_wordlist_current(user,numberwords_current, wordlist) #+ get_practice_wordlist_previous(user,numberwords_previous,wordlist)
    return practice_wordlist


def main():
    #wordlist = []
    wordlist = read_wordlist() #read current word list
    #print(wordlist[0].word) #print word
    #wordlist[0].test_word(bool(1)) #this is how to record a test of a word. 0->mistake, 1-> correct

    #wordlist = add_word(wordlist,"Kind1","Tür")  #this is how to add a new word
    practice_wordlist = select_practice_words("a",5,2,wordlist) #compile random practice wordlist
    for i in range(0,len(practice_wordlist)): #print current practice wordlist
        print(practice_wordlist[i].word)


    write_status = write_wordlist(wordlist) #update/write wordlist to file
    #print ("write_status: " + str(write_status))

if __name__ == "__main__":
    main()