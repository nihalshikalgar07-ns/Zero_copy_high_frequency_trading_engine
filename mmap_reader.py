import mmap
import os
import struct



ORDER_FORMAT = "Qc dI".replace(" ", "")
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


class MMapReader:

    def __init__(self, filename):

        self.fd = os.open(
            filename,
            os.O_RDWR
        )

        self.mm = mmap.mmap(
            self.fd,
            0,
            access=mmap.ACCESS_WRITE
        )

        self.offset = 0


    def read_order(self):

        if self.offset + ORDER_SIZE > self.mm.size():

            return None


        order_id, side, price, quantity = struct.unpack_from(
            ORDER_FORMAT,
            self.mm,
            self.offset
        )


        self.offset += ORDER_SIZE


        side = side.decode("ascii")


        return {

            "order_id": order_id,

            "side": side,

            "price": price,

            "quantity": quantity
        }


    def close(self):

        self.mm.close()

        os.close(self.fd)