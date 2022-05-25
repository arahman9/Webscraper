import os
import requests
from bs4 import BeautifulSoup

# scrapes through fifaindex.
def futScraper():
    with open("players.txt", "w+", errors="replace") as playerList:
        i = 1
        while i < 5:
            futSite = requests.get("https://www.fifaindex.com/players/" + str(i) + "/").text
            soup = BeautifulSoup(futSite, 'html5lib')
            # grabs all the players in the table and their attributes in the form of td
            for player in soup.tbody.find_all('tr'):
                playerList.write("\n")
                # grabs the attributes in one go, doesnt differentiate between them, so I can't pick out exactly what
                # attributes I want.
                for td in player.find_all('td'):
                    try:
                        pData = td.text
                        playerList.write(pData + ',')
                    except UnicodeEncodeError:
                        pass
                try:
                    playerList.write(player.find("img", class_="team small")['title'])
                except TypeError:
                    pass
                except AttributeError:
                    pass
            i += 1
            print('Completed page ' + str(i) + ' of 4')

    # removes empty lines by checking if the 2nd index is a number and by checking the length of a line
    with open("players.txt", "r") as completedList:
        lines = completedList.readlines()
        with open("fplayers.txt", "w+") as formatList:
            for line in lines:
                if len(line) > 2:
                    try:
                        x = int(line[2])
                        print(line)
                        formatList.write(line)
                    except ValueError:
                        pass
                else:
                    pass
    os.remove('players.txt')

    # removes any extraneous commas by taking each line from a fplayers.txt and converting it into a list
    # and then popping out the first two and last 3 indices.
    with open("fplayers.txt", "r") as completedList:
        with open("formattedPlayers.csv", "w+") as newPlayerList:
            lines = completedList.readlines()
            for line in lines:
                nLine = []
                newLine = ''
                for letter in line:
                    nLine.append(letter)
                nLine.pop(0)
                nLine.pop(0)
                nLine.insert(2, ',')
                i = len(nLine) - 1
                while i >= 0:
                    if nLine[i] == ',':
                        print(i)
                        nLine.pop(i)
                        break
                    i -= 1
                newLine = ''.join(nLine)
                LL = newLine.split(',')
                print(LL)
                LL.pop(5)
                newLine = ','.join(LL)
                newPlayerList.write(newLine)
                print(newLine)
                sections = newPlayerList.readlines()
    os.remove('fplayers.txt')
