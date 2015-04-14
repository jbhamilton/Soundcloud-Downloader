#!/usr/bin/python2
import urllib2, sys, re, os
import urllib
import glob
import songdetails
import json

if len(sys.argv) <= 1:
	exit("You need to enter a user to download from")

def get_url(track):
	# regular expression for the string we will search for in waveform-url tag
	regexp = 'https://w1.sndcdn.com/(.*?)_m.png'

	# find the song ID, if any
	match = re.search(regexp, track['waveform_url'])

	if match:
		# create a new stream hyperlink with the song ID
		url = "http://media.soundcloud.com/stream/%s" % match.group(1)
	else:
		print "No song ID found for the %s user. Exiting." % sys.argv[1]
		sys.exit()

	return url

def get_already_downloaded():
        return glob.glob('*')


def main():
        failedTracks = []
	print "Getting Information... "

        #get the titles of the tracks we already have downloaded in the directory
	alreadyDownloadedTracks = get_already_downloaded()

	# retrieve the user of the songs to download
	user = sys.argv[1]

	# retrieve type to download (tracks or favorites)
	type = sys.argv[2]

	if type != "tracks" and type != "favorites":
		type = "tracks"

	# retrieve the client_id from the final command-line argument
	client_id = sys.argv[-1]

	# retrieve the URL of the song to download from the final command-line argument
	soundcloud_api = "https://api.soundcloud.com/users/%s/%s?client_id=%s&limit=9999&offset=0" % (user, type, client_id)

	try:
		# open api URL for reading
		data = urllib2.urlopen(soundcloud_api).read()
		tracks = json.loads(data)
	except ValueError:
		# the user supplied URL is invalid or could not be retrieved
		exit("Error: The user '%s' can not be retrieved" % user)


	print "Ready to download the %s %s of the %s user... " % (len(tracks), type, user)

        # download songs for each track for the user
	for track in tracks:

	        title = track['title'].replace('.mp3','')
	        filename = title+'.mp3'
	        artist = track['user']['username']
	        url = get_url(track)
	        genre = track['genre']
	        year = track['release_year']

                try:
                    #if the song already exsists in the directory do nothing
	            if filename in alreadyDownloadedTracks:
                        print 'Song Already Downloaded : '+filename+'\n'
                        continue

		    print "Downloading File '%s'" % filename
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
                        failedTracks.append(title)
                        print 'Connection to SoundCloud Failed, unable to download:\n '+title+'\n continuing to next song'
                except UnicodeEncodeError as e:
                    print 'Could not handle printing the unicode for the track\n'


	print "Download Complete"
        if len(failedTracks)>0:
            print 'Failed Tracks:\n'
            for t in failedTracks:
                print t+'\n'

if __name__ == '__main__':
	main()