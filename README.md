Used to download music files from SoundCloud.com even if the download button is not available.

Based on the working directory you run the script from, mp3 tracks in the directory will be checked to prevent
tracks from being downloaded twice.

Uses ID3 tagging to set:

    - Artist name
    - Title
    - Genre
    - Year

### 6/8/2014
  - now using songdetails lib to write ID3 tag information about artist name, track name, genre, and year released.

### 1/24/2016
  - Complete rewrite of script to work with soundcloud API changes.
  - Expanded functionality to allow for more types of downloades and pagination.

___

### Dependencies

[songdetails by Ciantic](https://github.com/Ciantic/songdetails)

### How to use

Just run the python script like:

```shell
$ soundcloud-downloader.py [type] [user] [[option],...] USER CLIENT_ID
```
* `TYPE` : The type of resources to download:
    - `favorites` - The favorited (liked) tracks.
    - `tracks` - The uploaded tracks (created by the user).
    - `playlist` - A playlist (or set).
    - `track` - A single track.
* `USER` : the username (permalink) like `brockberrigan` (http://soundcloud.com/brockberrigan)
* `OPTION(s)` : Options dependant on the specified type:
    - `favorites` options :
        - `limit` : The maximum number of favorites to fetch and download, if not provided all favorites will be
          fetched.
    - `tracks` options :
        - `limit` : The maximum number of tracks to fetch and download, if not provided all tracks will be
          fetched.
    - `playlist` options :
        - `playlist name` - The name (permalink) of the playlist owned by the `user` to download.
    - `track` options :
        - `track name` - The name (permalink) of the track created by the `user` to download.
* `CLIENT_ID` : the soundcloud Client ID (this script uses the soundcloud api)

### Get the client ID

Register your app on [http://soundcloud.com/you/apps/new](http://soundcloud.com/you/apps/new) and grab your app `Client ID`.

### Integrate into the console

Edit your `.bashrc` file and paste the following code :

```shell
function soundcloud() {
    /path/to/soundcloud-downloader.py "$@" CLIENT_ID
}
```

### Example usage


Getting favorites:
```shell
$ soundcloud favorites wekilledtheradio
# Limit to 30 most recent favorites
$ soundcloud favorites wekilledtheradio 30
```

Getting tracks:
```shell
$ soundcloud tracks brockberrigan 
# Limit to 10 most recent tracks 
$ soundcloud tracks brockberrigan 10
```

Getting a playlist (set):
```shell
$ soundcloud playlist wekilledtheradio shuffle-and-repeat-45min-plus-mix-tapes 
```

Getting a single track:
```shell
$ soundcloud track chillchap people
```


HAVE FUN :-)
