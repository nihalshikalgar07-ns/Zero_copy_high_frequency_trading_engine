class MatchingEngine:

    def __init__(self):

        # Order books
        self.buy_orders = []
        self.sell_orders = []


    
    def match_order(self, order):

        trades = []


       
        if order["side"] == "BUY":

            while (
                order["quantity"] > 0
                and self.sell_orders
            ):

                sell_order = self.sell_orders[0]


                # BUY price must be >= SELL price
                if order["price"] < sell_order["price"]:
                    break


                # Determine executable quantity
                trade_quantity = min(
                    order["quantity"],
                    sell_order["quantity"]
                )


                # Trade price
                trade_price = sell_order["price"]


                # Create trade
                trade = {
                    "buy_order_id": order["order_id"],
                    "sell_order_id": sell_order["order_id"],
                    "price": trade_price,
                    "quantity": trade_quantity
                }

                trades.append(trade)


                # Reduce quantities

                order["quantity"] -= trade_quantity

                sell_order["quantity"] -= trade_quantity


                # Remove fully filled SELL order

                if sell_order["quantity"] == 0:

                    self.sell_orders.pop(0)


        

        elif order["side"] == "SELL":

            while (
                order["quantity"] > 0
                and self.buy_orders
            ):

                buy_order = self.buy_orders[0]


                # SELL price must be <= BUY price
                if order["price"] > buy_order["price"]:
                    break


                # Determine executable quantity
                trade_quantity = min(
                    order["quantity"],
                    buy_order["quantity"]
                )


                # Trade price
                trade_price = buy_order["price"]


                # Create trade
                trade = {
                    "buy_order_id": buy_order["order_id"],
                    "sell_order_id": order["order_id"],
                    "price": trade_price,
                    "quantity": trade_quantity
                }

                trades.append(trade)


                # Reduce quantities

                order["quantity"] -= trade_quantity

                buy_order["quantity"] -= trade_quantity


                # Remove fully filled BUY order

                if buy_order["quantity"] == 0:

                    self.buy_orders.pop(0)



        if order["quantity"] > 0:

            if order["side"] == "BUY":

                self.buy_orders.append(order)

            elif order["side"] == "SELL":

                self.sell_orders.append(order)


        return trades