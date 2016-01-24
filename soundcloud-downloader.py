#!/usr/bin/python2
import urllib2, sys, re, os
import urllib
import glob
import songdetails
import json

class SC:

    clientId                = ''

    requestLimit            = 50

    requestOffset           = 0

    apiRequestUrl           = "https://api.soundcloud.com"

    apiRequestExtras        = "?client_id={0}&limit={1}&offset={2}"

    apiDownloadEndPoint     = "https://api.soundcloud.com/i1/tracks/{0}/streams?client_id={1}"

    alreadyDownloadedTracks = []

    failedTracks            = []

    skippedTrackCount       = 0

    requestTypes            = ['track', 'tracks', 'favorites', 'playlist']



    def __init__(self,clientId):

        if not clientId:
            exit("You failed to supply your SoundCloud Client ID")

        self.clientId = clientId



    def run(self):

        self.getAlreadyDownloadedTracks()

        argCount = len(sys.argv)

        if argCount < 2:
            exit("You must specify a requestType: {0}".format(self.requestTypes));

        requestType = sys.argv[1]

        if requestType not in self.requestTypes:
            exit("Request type {0} not supported!".format(requestType))

        if argCount < 3:
            exit("You must specify a user to download from!");

        user = sys.argv[2]


        if requestType == 'playlist':

            if argCount < 4:
                exit("You must specify a playlist name");

            playlistName = sys.argv[3]

            playlist = self.resolvePlaylist(user,playlistName)

            if not playlist['id']:
                exit("Unable to find playlist '{0}' by user '{1}'".format(playlistName,user))

            self.downloadTracks(playlist['tracks'])

        elif requestType == 'favorites' or requestType == 'tracks':

            q = "/users/{0}/{1}".format(user,requestType)

            limit = 'all'

            if argCount == 5:
                limit = int(sys.argv[3])

            tracks = self.pageData(q,limit)

            self.downloadTracks(tracks)

        elif requestType == 'track':

            if argCount < 4:
                exit("You must specify a track to download!");

            track = sys.argv[3]

            track = self.resolveTrack(user,track)

            if not track['id']:
                exit("Could not find track '{0}' by user '{1}'".format(track,user))

            q = "/tracks/{0}".format(track['id'])

            track = self.apiRequest(self.buildApiEndPoint(q))

            self.downloadTrack(track)

        
        # Reset the skipped track count
        self.skippedTrackCount = 0



    def pageData(self,q,limit):

        allData     = []

        if limit != 'all':
            self.requestLimit = limit

        while True:

            data = self.apiRequest(self.buildApiEndPoint(q))

            if len(data):
                allData.extend(data)
                self.requestOffset += self.requestLimit
            else:
                break

            if limit != 'all' and self.requestOffset >= limit:
                break;

        
        self.requestOffset = 0
        self.requestLimit = 50

        return allData



    def resolveTrack(self,user,trackName):
        return self.resolve("{0}/{1}".format(user,trackName))



    def resolvePlaylist(self,user,playlistName):
        return self.resolve("{0}/sets/{1}".format(user,playlistName))



    def resolve(self,q):
        return self.apiRequest(self.apiRequestUrl + "/resolve?url=http://soundcloud.com/{0}&client_id={1}".format(q,self.clientId))



    def buildApiEndPoint(self,q):
        return self.apiRequestUrl + q + self.apiRequestExtras.format(self.clientId,self.requestLimit,self.requestOffset)



    def apiRequest(self,url):

	try:

            data = urllib2.urlopen(url).read()

            return json.loads(data)

	except ValueError:
            exit("Error: The user '%s' can not be retrieved" % user)



    def getAlreadyDownloadedTracks(self):

        self.alreadyDownloadedTracks = glob.glob('*')



    def getDownloadUrl(self,track):
    
    	if not track['id']:

            print "No song ID found for the %s user. Exiting." % sys.argv[1]
            sys.exit()

        url = self.apiDownloadEndPoint.format(track['id'],self.clientId) 

        try:

            data = json.loads(urllib2.urlopen(url).read())

            if data['http_mp3_128_url']:
                return data['http_mp3_128_url']

        except IOError:
            print "IOError getting download url for track {0}".format(track['permalink'])
	except ValueError:
            print "ValueError getting download url for track {0}".format(track['permalink'])
	except KeyError:
            print "ValueError getting download url for track {0}".format(track['permalink'])


        return False



    def downloadTrack(self,track):


        title       = track['title'].replace('.mp3','')
        filename    = title + '.mp3'
        artist      = track['user']['username']
        genre       = track['genre']
        year        = track['release_year']

        try:

            #if the song already exsists in the directory do nothing
            if filename in self.alreadyDownloadedTracks:
                print 'Song Already Downloaded : '+filename+'\n'
                self.skippedTrackCount += 1
                return

            url = self.getDownloadUrl(track)

            if not url:
                self.failedTracks.append(title)
                print "Unable to get download url for track '{0}', continueing to next track".format(title)
                return

            print "Downloading track '{0}'".format(title)

            try:

                urllib.urlretrieve(url, title)

                # set the ID3 tagging information for the track
                song = songdetails.scan(title)
                if song is not None:
                    song.artist = artist
                    song.title = title
                    song.genre = genre
                    song.year = year
                    song.save()

                os.rename( title, filename )

            except IOError as e:
                self.failedTracks.append(title)
                print 'Connection to SoundCloud Failed, unable to download:\n '+title+'\n continuing to next song'

        except UnicodeEncodeError as e:
            print 'Could not handle printing the unicode for the track\n'



    def downloadTracks(self,tracks):

	for track in tracks:
	    self.downloadTrack(track)

	failCount    = len(self.failedTracks)
	successCount = len(tracks) - failCount - self.skippedTrackCount

        print "\n\n******************** RUN STATS ***********************\n"
        print " {0} - Successfully downloaded".format(successCount)
        print " {0} - Skipped (already downloaded)".format(self.skippedTrackCount)
        print " {0} - Tracks failed to download : \n".format(failCount)

        for track in self.failedTracks:
            print "     " + track

        print "\n******************************************************\n\n\n"


if __name__ == '__main__':

    clientId = sys.argv[-1]

    soundcloud = SC(clientId)
    soundcloud.run()

