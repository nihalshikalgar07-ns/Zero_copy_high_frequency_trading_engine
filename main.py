import mmap
import os
import struct

from mmap_reader import (
    MMapReader,
    ORDER_FORMAT
)

from engine import TradeEngine


# CREATE TEST MMAP FILE

filename = "orders.mmap"


orders = [

    # order_id, side, price, quantity

    (1, b"S", 100.0, 10),

    (2, b"B", 101.0, 5),

    (3, b"B", 99.0, 8),

    (4, b"S", 98.0, 3)
]



# WRITE ORDERS TO MMAP FILE

order_size = struct.calcsize(ORDER_FORMAT)

file_size = order_size * len(orders)


with open(filename, "wb") as f:

    f.truncate(file_size)


with open(filename, "r+b") as f:

    mm = mmap.mmap(
        f.fileno(),
        file_size
    )


    offset = 0


    for order_id, side, price, quantity in orders:

        struct.pack_into(

            ORDER_FORMAT,

            mm,

            offset,

            order_id,

            side,

            price,

            quantity
        )


        offset += order_size


    mm.flush()

    mm.close()


# CREATE ENGINE

reader = MMapReader(filename)

engine = TradeEngine()


# READ + PROCESS ORDERS

while True:

    order = reader.read_order()


    if order is None:

        break


    # Process order through engine

    result = engine.process_order(order)


    print("\n--------------------------------")

    print(
        "Order ID:",
        result["order_id"]
    )


    print(
        "Entry:",
        result["engine_entry_ns"],
        "ns"
    )


    print(
        "Exit:",
        result["engine_exit_ns"],
        "ns"
    )


    print(
        "Latency:",
        result["engine_latency_ns"],
        "ns"
    )


    # Trades

    if result["trades"]:

        for trade in result["trades"]:

            print(
                "TRADE:",
                trade
            )

    else:

        print("No match")


# CLOSE MMAP

reader.close()