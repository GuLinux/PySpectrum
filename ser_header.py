import struct
class SERHeader(object):
    FORMAT = '=14siiiiiii40s40s40sqq'
    SIZE=178
    def __init__(self, data):
        self.unpacked = struct.unpack(SERHeader.FORMAT, data)
        self.color_id = self.unpacked[2]
        self.width = self.unpacked[4]
        self.height = self.unpacked[5]
        self.depth = self.unpacked[6]
        self.frames = self.unpacked[7]
        self.observer = self.unpacked[8].decode().strip()
        self.instrument = self.unpacked[9].decode().strip()
        self.telescope = self.unpacked[10].decode().strip()
    def __str__(self):
        return 'frames: {}; size: {}x{}, depth: {}, planes: {}, frame bytes: {}, observer: {}, instrument: {}, telescope: {}'.format(
            self.frames, self.width, self.height, self.depth, self.planes(), self.frame_bytes(), self.observer, self.instrument, self.telescope
            )
    
    def planes(self):
        return 1 if self.color_id < 20 else 3
    
    def frame_bytes(self):
        return self.width * self.height * self.planes() * (1 if self.depth == 8 else 2)
    
    def pack(self):
        return struct.pack(SERHeader.FORMAT, self.unpacked[0], self.unpacked[1], self.color_id, self.unpacked[3], self.width, self.height, self.depth, self.frames, 
                           self.observer.encode(), self.instrument.encode(), self.telescope.encode(), self.unpacked[11], self.unpacked[12])
    