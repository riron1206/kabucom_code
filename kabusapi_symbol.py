"""
12．銘柄情報取得
Usage:
    python kabusapi_symbol.py -s 5401
    -> 銘柄情報として kabusapi_symbol_5401.csv が出力される
"""
import os
import urllib.request
import json
import pprint
import argparse
import yaml
import pandas as pd

from get_token import get_pass, get_token, load_api_token


def kabusapi_symbol(token, symbol):
    url = f"http://localhost:18080/kabusapi/symbol/{symbol}@1"  # 本番url
    req = urllib.request.Request(url, method="GET")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-KEY", token)
    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            # pprint.pprint(content)
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
        "-s", "--symbol", type=str, default="5401", help="stock code. default=5401=日本製鉄"
    )
    parser.add_argument("-o", "--output_dir", type=str, default="output_tmp")
    args = vars(parser.parse_args())  # 辞書型でほしいとき

    content = kabusapi_symbol(token, args["symbol"])

    df = pd.DataFrame.from_dict(content, orient="index").T
    print(df)
    os.makedirs(args["output_dir"], exist_ok=True)
    out_csv = f'{args["output_dir"]}/kabusapi_symbol_{str(args["symbol"])}.csv'
    df.to_csv(out_csv, index=False, encoding="SHIFT-JIS")
    print(f"INFO: output {out_csv}")
