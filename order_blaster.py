import asyncio
import time
import random
import struct

from engine import TradeEngine


# CONFIG


TARGET_RATE = 100_000
BATCH_SIZE = 1_000
RUN_SECONDS = 10

SYMBOLS = (
    b"AAPL",
    b"MSFT",
    b"GOOG",
    b"TSLA"
)


# ORDER FORMAT

ORDER_STRUCT = struct.Struct(
    "<QQIB4s"
)


# CREATE ORDER

def create_order(order_id):

    price = random.randint(
        10000,
        50000
    )

    quantity = random.randint(
        1,
        1000
    )

    side = random.randint(
        0,
        1
    )

    symbol = random.choice(
        SYMBOLS
    )

    return ORDER_STRUCT.pack(
        order_id,
        price,
        quantity,
        side,
        symbol
    )


# DECODE ORDER

def decode_order(data):

    (
        order_id,
        price,
        quantity,
        side,
        symbol
    ) = ORDER_STRUCT.unpack(data)

    return {
        "order_id": order_id,
        "side": "B" if side == 0 else "S",
        "price": price / 100,
        "quantity": quantity,
        "symbol": symbol.decode("ascii")
    }


# IPC BUS

class MockIPCBus:

    def __init__(self):

        self.queue = asyncio.Queue(
            maxsize=100_000
        )

    async def publish(self, data):

        await self.queue.put(data)


# PRODUCER

async def order_producer(bus):

    order_id = 1

    interval = (
        BATCH_SIZE /
        TARGET_RATE
    )

    next_time = time.perf_counter()

    end_time = (
        next_time +
        RUN_SECONDS
    )

    sent = 0

    while next_time < end_time:

        for _ in range(BATCH_SIZE):

            order = create_order(
                order_id
            )

            await bus.publish(
                order
            )

            order_id += 1
            sent += 1

        next_time += interval

        sleep_time = (
            next_time -
            time.perf_counter()
        )

        if sleep_time > 0:

            await asyncio.sleep(
                sleep_time
            )

    return sent


# HFT ENGINE CONSUMER

async def hft_consumer(bus):

    # YOUR HFT ENGINE
    engine = TradeEngine()

    received = 0
    total_trades = 0

    while True:

        # Receive order from IPC bus
        data = await bus.queue.get()

        try:

            # Binary → Python order
            order = decode_order(
                data
            )

            
            # CONNECTED TO YOUR HFT ENGINE

            result = engine.process_order(
                order
            )

            received += 1

            total_trades += len(
                result["trades"]
            )

            # DISPLAY PROGRESS

            if received % 10_000 == 0:

                print(
                    f"Processed: "
                    f"{received:,} | "
                    f"Trades: "
                    f"{total_trades:,} | "
                    f"Last latency: "
                    f"{result['engine_latency_ns']} ns"
                )

        finally:

            bus.queue.task_done()


# MAIN

async def main():

    bus = MockIPCBus()

    # Start HFT consumer
    consumer_task = asyncio.create_task(
        hft_consumer(bus)
    )

    print()
    print("=" * 60)
    print("HFT LOAD TEST STARTED")
    print("=" * 60)
    print(
        f"Target rate : {TARGET_RATE:,} orders/sec"
    )
    print(
        f"Duration    : {RUN_SECONDS} seconds"
    )
    print("=" * 60)

    start = time.perf_counter()

    # Start blasting orders
    sent = await order_producer(
        bus
    )

    # Wait until consumer processes
    # all orders
    await bus.queue.join()

    elapsed = (
        time.perf_counter() -
        start
    )

    actual_rate = (
        sent / elapsed
    )

    print()
    print("=" * 60)
    print("HFT LOAD TEST COMPLETE")
    print("=" * 60)

    print(
        f"Orders sent : {sent:,}"
    )

    print(
        f"Time        : {elapsed:.3f} sec"
    )

    print(
        f"Throughput  : "
        f"{actual_rate:,.0f} orders/sec"
    )

    print("=" * 60)

    # Stop consumer
    consumer_task.cancel()

    try:
        await consumer_task
    except asyncio.CancelledError:
        pass


# START

if __name__ == "__main__":

    asyncio.run(
        main()
    )