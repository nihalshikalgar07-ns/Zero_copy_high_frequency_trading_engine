

import time

from Matching_Engine import MatchingEngine


class TradeEngine:

    def __init__(self):

        self.matcher = MatchingEngine()


    # PROCESS ORDER

    def process_order(self, order):

        # ENGINE ENTRY

        engine_entry_ns = time.perf_counter_ns()


        # MATCHING ENGINE

        trades = self.matcher.match_order(order)


        # ENGINE EXIT

        engine_exit_ns = time.perf_counter_ns()


        # ENGINE LATENCY

        engine_latency_ns = (
            engine_exit_ns
            - engine_entry_ns
        )


        # RETURN RESULT

        return {

            "order_id":
                order["order_id"],
                
            "side":order["side"],
            
            "price":order["price"],
            
            "quantity":order["quantity"],

            "trades":
                trades,

            "engine_entry_ns":
                engine_entry_ns,

            "engine_exit_ns":
                engine_exit_ns,

            "engine_latency_ns":
                engine_latency_ns
        }