Used to download music files from SoundCloud.com even if the download button is not available.

### 6/8/2014
  - now using songdetails lib to write ID3 tag information about artist name, track name, genre, and year released.

___

### Dependencies

[songdetails by Ciantic](https://github.com/Ciantic/songdetails)

### How to use

Just run the python script like:

```shell
$ soundcloud-downloader.py USER CLIENT_ID
```
* `USER`: the username like `bassenectar` (http://soundcloud.com/bassnectar)
* `CLIENT_ID`: the soundcloud Client ID (this script uses the soundcloud api)

### Get the client ID

Register your app on [http://soundcloud.com/you/apps/new](http://soundcloud.com/you/apps/new) and takes the `Client ID`.

### Integrate into the console

Edit your `.bashrc` file and paste the following code :

```shell
function soundcloud() {
    user=$1
    type=$2
    /path/to/soundcloud-downloader.py ${user} ${type} CLIENT_ID
}
```
And to download the all tracks at one time from Bassnectar user:
```shell
$ soundcloud bassnectar
# same action with the `type` argument
$ soundcloud bassnectar tracks 
```
And my favorites:
```shell
$ soundcloud oziks favorites
```
___

HAVE FUN :-)
