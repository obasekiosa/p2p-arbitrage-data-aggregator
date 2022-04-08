import datetime
import time
import os
import random


FIAT = [
              'AED', 'AMD', 'ARS', 'AUD', 'BDT', 'BGN', 'BHD', 'BND', 'BOB', 'BRL', 'CAD', 'CHF', 'CLP',
              'CNY', 'COP', 'CRC', 'CZK', 'DOP', 'DZD', 'EGP', 'EUR', 'GBP', 'GEL', 'GHS', 'GTQ', 'HKD',
              'HNL', 'HUF', 'IDR', 'ILS', 'INR', 'JOD', 'JPY', 'KES', 'KHR', 'KWD', 'KZT', 'LAK', 'LBP',
              'LKR', 'MAD', 'MDL', 'MMK', 'MNT', 'MXN', 'NGN', 'NIO', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN',
              'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RUB', 'RWF', 'SAR', 'SDG', 'SEK', 'THB', 'TND',
              'TRY', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'XAF', 'XOF', 'ZAR'
]

CRYPTO = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'NGN', 'DAI']

SIDE = ['buy', 'sell']

# FIAT = [
#     'GBP', 'NGN', 'USD'
# ]

# CRYPTO = ['USDT', 'BTC','ETH']

# SIDE = ['buy', 'sell']

# PROXIES = []


def run_single(fiat, side, crypto):
    spider_name = "p2p_buy_ngn"
    extension = 'json'
    file_name = None
    if file_name is None:
        x = datetime.datetime.now()
        time_stamp = f"{x.year}_{x.month}_{x.day}_{x.hour}_{x.minute}_{x.second}"
        file_name = f"{fiat}_{side}_{crypto}_{time_stamp}"
    

    command_no_out = f"scrapy crawl {spider_name} -a fiat={fiat} -a side={side} -a crypto={crypto}"
    print("Running command")
    print(command_no_out)
    print()
    stream = os.popen(command_no_out)
    dump = stream.read()

def run_group(fiats, sides, cryptos):
    for crypto in cryptos:
        for fiat in fiats:
            for side in sides:
                run_single(fiat, side, crypto)
                time.sleep(random.randint(8, 13))

def run_parallel(fiats, sides, cryptos):
    from concurrent.futures import ThreadPoolExecutor
    import threading

    f_inputs = []
    s_inputs = []
    c_inputs = []

    for crypto in cryptos:
        for fiat in fiats:
            for side in sides:
                f_inputs.append(fiat)
                s_inputs.append(side)
                c_inputs.append(crypto)

    with ThreadPoolExecutor(max_workers=6) as executor:
        return executor.map(run_single, f_inputs, s_inputs, c_inputs, timeout=60)

def main(parallel = False):
    if not parallel:
        run_group(FIAT, SIDE, CRYPTO)
    else:
        run_parallel(FIAT, SIDE, CRYPTO)

if __name__ == "__main__":
    while True:
        main(True)
        time.sleep(30*60)
                
