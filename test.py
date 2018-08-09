
from rawsocketpy import RawRequestHandler, RawAsyncServerCallback
import time

def callback(handler, server):
    print("Testing")
    handler.setup()
    handler.handle()
    handler.finish()

class LongTaskTest(RawRequestHandler):
    def handle(self):
        time.sleep(1)
        print(self.packet)

    def finish(self):
        print("End")

    def setup(self):
        print("Begin") 

def main():
    rs = RawAsyncServerCallback("wlp2s0", 0xEEFA, LongTaskTest, callback)
    rs.spin()

if __name__ == '__main__':
    main()
