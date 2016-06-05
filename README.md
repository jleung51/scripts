# MP3 Formatter

Python 3 script to rename MP3 files to the format `Artist - Title.mp3`.

## Usage

1. Find the music album to rename at [HikarinoAkari](http://hikarinoakariost.info/)
  * Don't judge me; if you judge me for this you can't modify this. It's in the [LICENCE](https://github.com/jleung51/mini_programs/blob/master/mp3-formatter/LICENCE), I swear, this is legit
2. Place the MP3 files into the directory `mp3-formatter/mp3/`, making sure that they are ordered by track number
3. `cd` to `mp3-formatter/`
4. Run:

```
./mp3_formatter.sh URL_TO_TRACKLIST ARTIST_NAME
```

## Setup

### Python 3 Installation

Run:

```
sudo apt-get install python3
```

### External Modules

#### [ID3](http://id3-py.sourceforge.net/)  
To install, navigate to the `id3-py-1.2 directory` and run:

```
python3 setup.py install
```

#### [Requests](http://docs.python-requests.org/en/master/)

To install, run:

```
sudo apt-get install python3-pip
pip3 install requests
```
