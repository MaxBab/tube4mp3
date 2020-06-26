# tube4mp3

The script downloads provided Youtube clip and converts it to mp3 file.  
The script supports to download the clip within the specified time frame.

The clip may have an intro not related to a song or some post song filming.
In order to get the pure song on the mp3 file, the time frame could be provided.

## Install
The script depends on the youtube-dl and ffmpeg.  
Install the packages from the requirements.txt file into the virtualenv.
```
$ virtualenv tube4mp3 && source tube4mp3/bin/activate
$ pip install -r requirements.txt
```

## Usage
Two modes are supported to use.
* Direct download - Provide the parameters for the clip with the arguments directly.
```
./tube4mp3.py --url youtube_clip_url
./tube4mp3.py --url youtube_clip_url --start-time 0:0:10 --end-time 0:4:50
```
* Download from list - provide a list of clip urls with additional optional parameters.
```
./tube4mp3.py --url youtube_clip_url --clip-list list_file.txt
```
For the sample of the list, see clip_list.txt.sample file.

## Download arguments
The script supports the following arguments to be provided:
* url - The url of the clip
* start-time - The start time of the clip to download (optional)
* end-time - The end time of the clip to download (optional)
* clip-list - The file with the clip lists and optional arguments
* verbose - Show verbose information
