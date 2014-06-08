#!/usr/bin/python2
import urllib2, sys, re
import urllib
import glob
import songdetails

from xml.dom.minidom import parseString

if len(sys.argv) <= 1:
	exit("You need to enter a user to download from")

def get_tag(element, name):
	# retrieve a name tag on the element structure
	tagXml = element.getElementsByTagName(name)[0].toxml();

	return tagXml.replace('<' + name + '>', '').replace('</' + name + '>', '')

def get_title(track):
	# retrieve the title of the song
	title = "%s.mp3" % get_tag(track, 'title')

	return title.replace('/', '-')

def get_artist(user):
        return get_tag(user,'username')

def get_genre(track):
        return get_tag(track,'genre')

def get_year(track):
        year = track.getElementsByTagName('release-year')[0]
        if year.getAttribute('type')=='integer':
            return year.firstChild.nodeValue
        return ''

def get_url(track):
	# regular expression for the string we will search for in waveform-url tag
	regexp = 'https://w1.sndcdn.com/(.*?)_m.png'

	# find the song ID, if any
	match = re.search(regexp, get_tag(track, 'waveform-url'))

	if match:
		# create a new stream hyperlink with the song ID
		url = "http://media.soundcloud.com/stream/%s" % match.group(1)
	else:
		print "No song ID found for the %s user. Exiting." % sys.argv[1]
		sys.exit()

	return url

def get_already_downloaded():
        return glob.glob('*.mp3')


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
	soundcloud_api = "https://api.soundcloud.com/users/%s/%s?client_id=%s&limit=3" % (user, type, client_id)

	try:
		# open api URL for reading
		xml = urllib2.urlopen(soundcloud_api)
	except ValueError:
		# the user supplied URL is invalid or could not be retrieved
		exit("Error: The user '%s' can not be retrieved" % user)

	# store the contents (source) of our song's URL
	xmlsource = xml.read()
	xml.close()

	# parse xml datasource
	data = parseString(xmlsource)
	tracks = data.getElementsByTagName('track')

	print "Ready to download the %s %s of the %s user... " % (len(tracks), type, user)

        # download songs for each track for the user
	for track in tracks:

		title = get_title(track)
		artist = get_artist(track.getElementsByTagName('user')[0])
		url   = get_url(track)
		genre = get_genre(track)
		year = get_year(track)

		#print title
		#print artist
		#print url
		#print genre
		#print year
		#print '\n'

                #if the song already exsists in the directory do nothing
	        if unicode(title) in alreadyDownloadedTracks:
                    print 'Song Already Downloaded : '+unicode(title)+'\n'
                    continue

		print "Downloading File '%s'" % title
                try:
                    urllib.urlretrieve(url, title)
                    # set the ID3 tagging information for the track
                    song = songdetails.scan(title)
                    if song is not None:
                        song.artist = unicode(artist) 
                        title = title.replace('.mp3','')
                        song.title = unicode(title) 
                        song.genre = unicode(genre)
                        song.year = year
                        song.save()

                except IOError as e:
                    failedTracks.append(title)
                    print 'Connection to SoundCloud Failed, unable to download:\n '+title+'\n continuing to next song'


	print "Download Complete"
        if len(failedTracks)>0:
            print 'Failed Tracks:\n'
            for t in failedTracks:
                print t+'\n'

if __name__ == '__main__':
	main()
