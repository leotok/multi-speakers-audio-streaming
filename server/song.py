import json
import time
import threading

class AudioHandler(object):

    def __init__(self, chunk_size=1000):
        self.chunk_size = chunk_size
        self.songs = songs = [
            {
                "name": "jump_1", 
                "path": "songs/jump_1.u8"
            },
            {
                "name": "frozen_star", 
                "path": "songs/frozen_star.u8"
            },
            {
                "name": "high_star", 
                "path": "songs/high_star.u8"
            },
            {
                "name": "smash_star", 
                "path": "songs/smash_star.u8"
            },
        ]
        self.song_index = 0

    def get_chunks(self, song):
        with open(song["path"], "rb") as f:
            chunk = f.read(self.chunk_size)

            while chunk != b"":
                yield chunk
                chunk = f.read(self.chunk_size)

    @property
    def current_song(self):
        return self.songs[self.song_index]

    def next_song(self):
        print "index",  self.song_index
        if self.song_index == len(self.songs) - 1:
            self.song_index = 0
        else:
            self.song_index += 1

class StreammingThread(threading.Thread):

    def __init__(self, threadID, client, audio):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.audio = audio
        self.client = client
        self.should_stop = False

    def run(self):
        print "Starting thread "
        self.stream(self.client, self.audio)
        print "Stopped streamming thread"

    def stream(self, client, audio):
        while True:
            client.publish("song/info", json.dumps(self.audio.current_song))

            for chunk in audio.get_chunks(self.audio.current_song):
                client.publish("song/stream", chunk)
                time.sleep(0.12)

                if self.should_stop:
                    return 

            audio.next_song()

    def stop(self):
        self.should_stop = True

