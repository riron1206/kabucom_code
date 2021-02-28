"""
kabuステーションに銘柄登録する
Usage:
    python kabusapi_register.py -s 6869 -e 1
    python kabusapi_register.py -s 6869 4519 3681 3402 3064 6758 6723 7203 6981 2503 -e 1  # 2件以上一気に登録
"""
import urllib.request
import json
import pprint
import argparse
import yaml
import pandas as pd

from get_token import get_pass, get_token, load_api_token


def kabusapi_register(token, symbol, exchange=1):
    """銘柄登録
    exchange=1は東証1
    """
    obj = {"Symbols": [{"Symbol": symbol, "Exchange": exchange}]}
    json_data = json.dumps(obj).encode("utf8")

    url = "http://localhost:18080/kabusapi/register"  # 本番url
    req = urllib.request.Request(url, json_data, method="PUT")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-KEY", token)

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

    return content


if __name__ == "__main__":
    token = load_api_token()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--symbol", type=str, nargs="*", help="stock code. default=5401=日本製鉄"
    )
    parser.add_argument(
        "-e", "--exchange", type=str, default="1", help="市場コード. default=1=東証1"
    )
    args = vars(parser.parse_args())  # 辞書型でほしいとき

    for s in args["symbol"]:
        content = kabusapi_register(token, s, args["exchange"])
        print(f"INFO: {content}")
