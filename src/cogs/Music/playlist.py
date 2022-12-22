
import copy
import random
from enum import Enum
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class Track:
    url: str
    title: str
    channelName: str
    duration: timedelta
    idTrack: int = None

    def __eq__(self, other):
        if isinstance(other, Track):
            return self.url == other.url
        elif isinstance(other, int):
            return self.idTrack == other

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        return f'Title: {self.title} Channel: {self.channelName} Duration: {self.duration}'


class Playlist:
    class RepeatType(Enum):
        NONE = 0
        ONE = 1
        ALL = 2

    def __init__(self, tracks: list[Track]=None):
        self.__repeat = self.RepeatType.NONE
        self.__indexTrack = 0
        if tracks is None:
            self.__tracks = []
        else:
            self.__tracks = tracks
            self.__updateTracksID()

    def __add__(self, other):
        s = set(copy.deepcopy(self.__tracks))
        o = set(copy.deepcopy(other.__tracks))
        return Playlist(list(s.union(o)))

    def __sub__(self, other):
        s = set(copy.deepcopy(self.__tracks))
        o = set(copy.deepcopy(other.__tracks))
        return Playlist(list(s.difference(o)))

    def __iter__(self):
        self.__indexTrack = -1
        return self

    def __next__(self):
        if self.isEmpty:
            raise StopIteration

        if (self.__repeat is not self.RepeatType.ONE) or self.__indexTrack == -1:
            self.__indexTrack += 1
        if self.__indexTrack >= len(self.__tracks):
            if self.__repeat is self.RepeatType.ALL:
                self.__indexTrack = 0
            else:
                raise StopIteration

        return self.__tracks[self.__indexTrack]

    def __repr__(self):
        return f'Playlist(tracks: {self.trackCount}, repeatType: {self.__repeat}, indexTrack: {self.__indexTrack})'

    def __str__(self):
        if self.isEmpty:
            return 'Playlist is empty'

        return f'Playlist:\n - '+'\n - '.join([str(track.idTrack)+' | '+str(track) for track in self.__tracks])

    def __updateTracksID(self) -> None:
        for i, track in enumerate(self.__tracks):
            track.idTrack = i+1

    def setRepeat(self, repeat) -> None:
        if isinstance(repeat, Playlist.RepeatType):
            self.__repeat = repeat

    def getRepeat(self):
        return self.__repeat

    def addTrack(self, track: Track) -> None:
        if isinstance(track, Track) and track not in self.__tracks:
            self.__tracks.append(track)
            self.__updateTracksID()

    def removeTrack(self, idTrack: int) -> None:
        if idTrack in self.__tracks:
            self.__tracks.remove(idTrack)

    def reset(self) -> None:
        self.__tracks.clear()

    def shuffle(self) -> None:
        random.shuffle(self.__tracks)

    @property
    def trackCount(self) -> int:
        return len(self.__tracks)

    @property
    def totalDuration(self) -> timedelta:
        return sum((track.duration for track in self.__tracks), start=timedelta(0))

    @property
    def isEmpty(self) -> bool:
        return len(self.__tracks) == 0

