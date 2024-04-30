# from binance.client import Client
# from binance.enums import SIDE_BUY, SIDE_SELL
# import itertools
# import numpy as np
# import pandas as pd
# import time

# # Step 1: Initialize Binance Client
# api_key = '916865ef218422590a47257c6154815d81410869c407e6232b3aeef91c342e66'
# api_secret = '19dc4027f63d345e5d8a9686304bd523f4755da017c36d1399a568a27c78923b'
# client = Client(api_key, api_secret)

# # Step 2: Data Collection (Real-time)
# def get_currency_pairs():
#     currency_pairs = {}
#     symbols = client.get_all_tickers()
#     for symbol in symbols:
#         symbol_name = symbol['symbol']
#         if 'USDT' in symbol_name:  # Filter symbols ending with USDT
#             currency_pairs[symbol_name] = float(symbol['price'])
#     return currency_pairs

# # Step 3: Grouping Currencies
# def group_currencies(currency_pairs):
#     grouped_currencies = [list(group) for group in itertools.zip_longest(*[iter(currency_pairs)]*3)]
#     return grouped_currencies

# # Step 4: Calculating Potential Profits
# def calculate_profit(group, currency_pairs):
#     # Ensure group is a string
#     if not isinstance(group, str):
#         print("Error: Input is not a string.")
#         return None
    
#     # Split the string into currency pairs
#     c1, c2, c3 = group.split('/')
    
#     # Check if all currency pairs are present in the dictionary and have valid prices
#     if c1 not in currency_pairs or currency_pairs[c1] is None or currency_pairs[c1] == 0 \
#         or c2 not in currency_pairs or currency_pairs[c2] is None or currency_pairs[c2] == 0 \
#         or c3 not in currency_pairs or currency_pairs[c3] is None or currency_pairs[c3] == 0:
#         print(f"One or more currency pairs missing or have invalid prices in currency_pairs dictionary.")
#         return None
    
#     # Calculate profit
#     profit = (1 / currency_pairs[c1]) * (1 / currency_pairs[c2]) * currency_pairs[c3] - 1
#     return profit

# # Step 5: Executing Trades
# def execute_trades(client, grouped_currencies, currency_pairs):
#     max_profit = -float('inf')
#     best_group = None
#     profits = {}  # Dictionary to store profits for each group
    
#     for group in grouped_currencies:
#         if None in group:
#             print("Skipping group with None value:", group)
#             continue
        
#         c1, c2, c3 = group
        
#         # Join the currency pairs with '/' separator to ensure a string input
#         group_str = '/'.join(group)
        
#         # Calculate the expected profit for the triangular arbitrage
#         profit = calculate_profit(group_str, currency_pairs)
        
#         # If profit is None, skip this group
#         if profit is None:
#             continue
        
#         # Determine the investment for this trade in USDT
#         investment_usdt = min(currency_pairs[c1], currency_pairs[c2] / currency_pairs[c1], currency_pairs[c3] / currency_pairs[c2])
        
#         # If investment is 0, skip this group
#         if investment_usdt == 0:
#             continue
        
#         # Calculate the profit in USDT
#         profit_usdt = investment_usdt * profit
#         print(group,'INVESTMENT (USDT): ',investment_usdt,' / ','PROFIT (USDT): ',profit_usdt)
        
#         # Check if this group has the maximum profit so far
#         if profit_usdt > max_profit:
#             max_profit = profit_usdt
#             best_group = group
        
#         # Store the profit for this group
#         profits[group_str] = profit_usdt
    
#     # If no profitable group found, print a message and return
#     if best_group is None:
#         print("No profitable trade found with the current currency pairs.")
#         return
    
#     c1, c2, c3 = best_group
    
#     # Define the order quantity in USDT
#     quantity_usdt = 5  # Fixed quantity in USDT
    
#     # Calculate the corresponding quantities for each currency
#     quantity_c1 = quantity_usdt / currency_pairs[c1]
#     quantity_c2 = quantity_c1 * currency_pairs[c1] / currency_pairs[c2]
#     quantity_c3 = quantity_c2 * currency_pairs[c2] / currency_pairs[c3]
    
#     # Place buy orders
#     order1 = client.create_order(
#         symbol=c1 + c2,
#         side=SIDE_BUY,
#         type='MARKET',
#         quoteOrderQty=quantity_usdt
#     )
    
#     # Wait for the order to be filled
#     # You may need to implement logic to check order status
    
#     # Place sell orders
#     order2 = client.create_order(
#         symbol=c2 + c3,
#         side=SIDE_SELL,
#         type='MARKET',
#         quantity=quantity_c2
#     )
    
#     order3 = client.create_order(
#         symbol=c3 + c1,
#         side=SIDE_SELL,
#         type='MARKET',
#         quantity=quantity_c3
#     )
    
#     # Wait for the orders to be filled
    
#     # Log trade execution details
#     print("Triangular arbitrage trade executed:")
#     print("Buy:", order1)
#     print("Sell:", order2)
#     print("Sell:", order3)
    
#     # Print all groups with their profits in USDT
#     print("Groups with profits (USDT):")
#     for group, profit_usdt in profits.items():
#         print("Group:", group, "Profit (USDT):", profit_usdt)

# # Main function
# if __name__ == "__main__":
#     # Step 2: Data Collection (Real-time)
#     currency_pairs = get_currency_pairs()

#     # Step 3: Grouping Currencies
#     grouped_currencies = group_currencies(currency_pairs)

#     # Step 5: Executing Trades
#     execute_trades(client, grouped_currencies, currency_pairs)
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL

# Step 1: Initialize Binance Client
api_key = '916865ef218422590a47257c6154815d81410869c407e6232b3aeef91c342e66'
api_secret = '19dc4027f63d345e5d8a9686304bd523f4755da017c36d1399a568a27c78923b'
client = Client(api_key, api_secret)

# Step 2: Data Collection (Real-time)
def get_currency_pairs():
    currency_pairs = {}
    symbols = client.get_all_tickers()
    for symbol in symbols:
        symbol_name = symbol['symbol']
        if 'USDT' in symbol_name:  # Filter symbols ending with USDT
            currency_pairs[symbol_name] = float(symbol['price'])
    return currency_pairs

# Step 3: Grouping Currencies
def group_currencies(currency_pairs):
    grouped_currencies = [list(group) for group in zip(*[iter(currency_pairs)]*3)]
    return grouped_currencies

# Step 4: Calculating Potential Profits
def calculate_profit(group, currency_pairs):
    # Ensure group is a string
    if not isinstance(group, str):
        print("Error: Input is not a string.")
        return None
    
    # Split the string into currency pairs
    c1, c2, c3 = group.split('/')
    
    # Check if all currency pairs are present in the dictionary and have valid prices
    if c1 not in currency_pairs or currency_pairs[c1] is None or currency_pairs[c1] == 0 \
        or c2 not in currency_pairs or currency_pairs[c2] is None or currency_pairs[c2] == 0 \
        or c3 not in currency_pairs or currency_pairs[c3] is None or currency_pairs[c3] == 0:
        print(f"One or more currency pairs missing or have invalid prices in currency_pairs dictionary.")
        return None
    
    # Calculate profit
    profit = (1 / currency_pairs[c1]) * (1 / currency_pairs[c2]) * currency_pairs[c3] - 1
    return profit

# Step 5: Executing Trades
def execute_trades(client, grouped_currencies, currency_pairs):
    max_profit = -float('inf')
    best_group = None
    
    for group in grouped_currencies:
        if None in group:
            print("Skipping group with None value:", group)
            continue
        
        c1, c2, c3 = group
        
        # Calculate profit (unchanged)
        profit = calculate_profit('/'.join(group), currency_pairs)
        if profit is None:
            continue
        
        # Determine investment for this trade in USDT
        investment_usdt = min(currency_pairs[c1], currency_pairs[c2] / currency_pairs[c1], currency_pairs[c3] / currency_pairs[c2])
        if investment_usdt == 0:
            continue
        
        # Calculate profit in USDT
        profit_usdt = investment_usdt * profit
        print(group, 'Investment (USDT):', investment_usdt, 'Profit (USDT):', profit_usdt)
        
        # Check if this group has the maximum profit so far
        if profit_usdt > max_profit:
            max_profit = profit_usdt
            best_group = group
    print(best_group,max_profit)
    # If no profitable group found, print a message and return
    if best_group is None:
        print("No profitable trade found with the current currency pairs.")
        return
    
    c1, c2, c3 = best_group
    
    # Execute trades
    quantity_usdt = 5  # Fixed quantity in USDT
    
    # Place buy orders
    order1 = client.create_order(
        symbol=c1 + 'USDT',
        side=SIDE_BUY,
        type='MARKET',
        quoteOrderQty=quantity_usdt
    )
    # Wait for order1 to be filled
    
    # Place buy order for Currency B using Currency A
    order2 = client.create_order(
        symbol=c2 + c1,
        side=SIDE_BUY,
        type='MARKET',
        quoteOrderQty=quantity_usdt
    )
    # Wait for order2 to be filled
    
    # Place buy order for Currency C using Currency B
    order3 = client.create_order(
        symbol=c3 + c2,
        side=SIDE_BUY,
        type='MARKET',
        quoteOrderQty=quantity_usdt
    )
    # Wait for order3 to be filled
    
    # Convert Currency C back to USDT
    order4 = client.create_order(
        symbol=c3 + 'USDT',
        side=SIDE_SELL,
        type='MARKET',
        quoteOrderQty=quantity_usdt
    )
    # Wait for order4 to be filled
    
    # Log trade execution details
    print("Triangular arbitrage trades executed:")
    print("Buy", c1, "with USDT:", order1)
    print("Buy", c2, "with", c1, ":", order2)
    print("Buy", c3, "with", c2, ":", order3)
    print("Convert", c3, "back to USDT:", order4)

# Main function
if __name__ == "__main__":
    # Step 2: Data Collection (Real-time)
    currency_pairs = get_currency_pairs()

    # Step 3: Grouping Currencies
    grouped_currencies = group_currencies(currency_pairs)

    # Step 5: Executing Trades
    execute_trades(client, grouped_currencies, currency_pairs)

