
import eyed3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC


class MP3Song:
    def __init__(self, path) -> None:
        self.format = "mp3"
        self.path = path
        self.song = eyed3.load(path)
        self.tags = self.song.tag

    @property
    def title(self):
        return self.tags.title

    @title.setter
    def title(self, t):
        self.tags.title = t

    @property
    def artists(self):
        return self.tags.artist

    @artists.setter
    def artists(self, a):
        if isinstance(a, list):
            a = ", ".join(a)
        self.tags.artist = a

    @property
    def album_artist(self):
        return self.tags.album_artist

    @album_artist.setter
    def album_artist(self, aa):
        self.tags.album_artist = aa

    @property
    def album(self):
        return self.tags.album

    @album.setter
    def album(self, a):
        self.tags.album = a

    @property
    def track_num(self):
        return self.tags.track_num[0]

    @track_num.setter
    def track_num(self, tn):
        if tn is not None:
            tn = int(tn)
        self.tags.track_num = tn

    @property
    def lyrics(self):
        l = self.tags.lyrics
        if any(l):
            return l[0].text
        else:
            return ""

    @lyrics.setter
    def lyrics(self, l):
        if any(self.tags.lyrics):
            self.tags.lyrics[0].text = l
        else:
            self.tags.lyrics.set(l)

    def save(self):
        self.tags.save(encoding="utf8")


class M4ASong:
    def __init__(self, path) -> None:
        self.format = "m4a"
        self.path = path
        self.song = MP4(path)
        self.tags = self.song.tags

    def _get_tag(self, tag):
        t = self.tags.get(tag)
        if t:
            return t[0]
        else:
            return None

    @property
    def title(self):
        return self._get_tag("\xa9nam")

    @title.setter
    def title(self, t):
        self.tags["\xa9nam"] = [t]

    @property
    def artists(self):
        return self._get_tag("\xa9ART")

    @artists.setter
    def artists(self, a):
        if isinstance(a, list):
            a = ", ".join(a)
        self.tags["\xa9ART"] = [a]

    @property
    def album_artist(self):
        return self._get_tag("aART")

    @album_artist.setter
    def album_artist(self, aa):
        self.tags["aART"] = [aa]

    @property
    def album(self):
        return self._get_tag("\xa9alb")

    @album.setter
    def album(self, a):
        self.tags["\xa9alb"] = [a]

    @property
    def track_num(self):
        tn = self._get_tag("trkn")
        if tn:
            return tn[0]
        return tn

    @track_num.setter
    def track_num(self, tn):
        if tn is not None:
            self.tags["trkn"] = [(int(tn), 0)]
        else:
            self.tags.pop("trkn", None)

    @property
    def lyrics(self):
        l = self._get_tag("\xa9lyr")
        if l is None:
            return ""
        return l

    @lyrics.setter
    def lyrics(self, l):
        self.tags["\xa9lyr"] = [l]

    def save(self):
        self.song.save(self.path)


class FLACSong:
    def __init__(self, path) -> None:
        self.format = "flac"
        self.path = path
        self.song = FLAC(path)
        self.tags = self.song.tags

    def _get_tag(self, tag):
        t = self.tags.get(tag)
        if t:
            return t[0]
        else:
            return None

    @property
    def title(self):
        return self._get_tag("title")

    @title.setter
    def title(self, t):
        self.tags["title"] = [t]

    @property
    def artists(self):
        return self._get_tag("artist")

    @artists.setter
    def artists(self, a):
        if isinstance(a, list):
            a = ", ".join(a)
        self.tags["artist"] = [a]

    @property
    def album_artist(self):
        return self._get_tag("albumartist")

    @album_artist.setter
    def album_artist(self, aa):
        self.tags["albumartist"] = [aa]

    @property
    def album(self):
        return self._get_tag("album")

    @album.setter
    def album(self, a):
        self.tags["album"] = [a]

    @property
    def track_num(self):
        tn = self._get_tag("tracknumber")
        if tn:
            return tn.split('/')[0]
        return tn

    @track_num.setter
    def track_num(self, tn):
        if tn is not None:
            self.tags["tracknumber"] = [tn]
        elif "tracknumber" in self.tags:
            del self.tags["tracknumber"]

    @property
    def lyrics(self):
        l = self._get_tag("lyrics")
        if l is None:
            return ""
        return l

    @lyrics.setter
    def lyrics(self, l):
        self.tags["lyrics"] = [l]

    def save(self):
        self.song.save(self.path)


class Song:
    def __new__(cls, path):
        ext = path.suffix.lower()
        if ext == ".mp3":
            return MP3Song(path)
        elif ext == ".m4a":
            return M4ASong(path)
        elif ext == ".flac":
            return FLACSong(path)
        else:
            raise Exception(
                " X Not supported file format: " + path.name
            )
