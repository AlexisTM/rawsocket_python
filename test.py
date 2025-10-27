#!/usr/bin/env python
import argparse
import time
import sys
from rawsocketpy import RawRequestHandler, RawAsyncServerCallback


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
    parser = argparse.ArgumentParser(
        description="Run a RawAsyncServerCallback on a given network interface."
    )
    default_iface = "wlp2s0" if sys.platform == "linux" else "Ethernet"

    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        default=default_iface,
        help=f"Network interface to bind to (default: {default_iface})",
    )

    parser.add_argument(
        "-p",
        "--protocol",
        type=lambda x: int(x, 0),  # allows hex like 0xEEFA or decimal
        default=0xEEFA,
        help="EtherType / protocol number (default: 0xEEFA)",
    )
    args = parser.parse_args()
    rs = RawAsyncServerCallback(
        args.interface,
        args.protocol,
        LongTaskTest,
        callback,
    )
    rs.spin()


if __name__ == "__main__":
    main()
