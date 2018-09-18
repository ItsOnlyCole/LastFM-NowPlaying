from xml.dom import minidom
from urllib.request import urlopen
import sys
import time
import threading

userName = input("Enter your LastFM username: ")

#Public API Key for Accessing Last FM
apiKey = ("460cda35be2fbf4f28e8ea7a38580730")

#Global Variables
currentTrackURL = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&nowplaying="true"&user=' + str(userName) + '&api_key=' + str(apiKey))
runCheck = True
waitTime = 0
noSongPlaying = ("Nothing Currently Playing     ")

#Defines the funcions for use in different threads.
def checkForNewSong():
    global runCheck
    global waitTime
    while runCheck == True:
        #Loads Current Song info from Last FM
        currentTrackXML = urlopen(currentTrackURL).read()
        currentTrack = minidom.parseString(currentTrackXML)
        songName = currentTrack.getElementsByTagName('name')
        songArtist = currentTrack.getElementsByTagName('artist')
        songInfo = songName[0].firstChild.nodeValue + " by " + songArtist[0].firstChild.nodeValue + "     "

        currentSongFile = open("currentSong.txt", "r")
        #Checks if currentSong is already in currentSong.txt If it isn't, clears the file.
        if currentSongFile.readline() != songInfo:
            currentSongFile.close()
            #Runs twice; Once for clearing and once for adding the curren song.
            currentSongFile = open("currentSong.txt", "w")
            currentSongFile.write(songInfo)
            currentSongFile.close()

        print(songInfo)
        #Adds wait before next check.
        time.sleep(waitTime)
        #End of While Loop

    #Sets the current song to "Nothing Currently Playing"
    currentSongFile = open("currentSong.txt", "w")
    currentSongFile.write(noSongPlaying)
    currentSongFile.close()
    #Closes the Application
    sys.exit()

def exitCheck():
    global runCheck
    while runCheck == True:
        exitInput = input("Type Exit to close: \n")
        if exitInput == "exit" or exitInput == "Exit" or exitInput == "EXIT":
            print("Closing Application...")
            runCheck = False


#Checks for currentSong.txt. If doesn't exist, creates file.
currentSongFile = open("currentSong.txt", "w")
#Used to keep currentSong.txt on "Nothing Currently Playing" until first song is pulled from LastFM
currentSongFile.write(noSongPlaying)
currentSongFile.close()
#Creates Threads for the two functions
newSongThread = threading.Thread(target=checkForNewSong)
exitThread = threading.Thread(target=exitCheck)
newSongThread.start()
exitThread.start()
