"""
２．注文発注（現物）買/売
Usage:
    python kabusapi_sendorder_cash.py -i input_tmp/input_kabusapi_sendorder_cash.csv
    -> input_tmp/input_kabusapi_sendorder_cash1.csv の注文が実行される
"""
import os
import urllib.request
import json
import pprint
import argparse
import yaml
import datetime
import pandas as pd

from get_token import get_pass, get_token, load_api_token

order_columns = [
    "Symbol",
    "Exchange",
    "SecurityType",
    "FrontOrderType",
    "Side",
    "CashMargin",
    "DelivType",
    "FundType",
    "AccountType",
    "Qty",
    "Price",
    "ExpireDay",
]


def kabusapi_sendorder_cash(token, obj):
    json_data = json.dumps(obj).encode("utf-8")

    url = "http://localhost:18080/kabusapi/sendorder"  # 本番url
    req = urllib.request.Request(url, json_data, method="POST")
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


def test_kabusapi_sendorder_cash(token, pass_dict):
    """kabusapi_sendorder_cash テスト
    {'Code': 21, 'Message': '可能額が不足しております。ご注文内容をご確認ください'} になるはず
    """
    # today = datetime.date.today()  # 現在の日（今日）
    # today = str(today).replace("-", "")
    # tomorrow = int(today) + 1

    # テストデータ
    # https://kabucom.github.io/kabusapi/reference/index.html#operation/sendorderPost
    obj = {
        "Password": pass_dict["ORDERPASS"],  # 注文パスワード
        "Symbol": "9433",  # 銘柄コード
        "Exchange": 1,  # 市場コード
        "SecurityType": 1,  # 商品種別. 1=株式のみ
        "FrontOrderType": 20,  # 執行条件. 1=東証, 3=名証, 5=福証, 6=札証
        "Side": "2",  # 売買区分. 1=売、2=買
        "CashMargin": 1,  # 信用区分. 1=現物, 2=新規, 3=返済
        "DelivType": 2,  # 受渡区分. 0=指定なし, 1=自動振替, 2=お預り金
        "FundType": "AA",  # 資産区分（預り区分）. (半角スペース2つ)=現物売の場合, 02=保護, AA=信用代用, 11=信用取引
        "AccountType": 2,  # 口座種別. 2=一般, 4=特定, 12=法人
        "Qty": 100,  # 注文数量. 信用一括返済の場合、返済したい合計数量を入力
        "Price": 2762.5,  # 注文価格. FrontOrderTypeで成行を指定した場合、0を指定
        "ExpireDay": 0,  # 注文有効期限. yyyyMMdd形式. 「0」を指定すると、kabuステーション上の発注画面の「本日」に対応する日付として扱う
        # "ExpireDay": tomorrow,
    }
    # テストデータ出力
    df = pd.DataFrame.from_dict(obj, orient="index").T
    print(df)
    os.makedirs(output_tmp, exist_ok=True)
    out_csv = f"output_tmp/tmp.csv"
    df.to_csv(out_csv, index=False, encoding="SHIFT-JIS")

    kabusapi_sendorder_cash(token, obj)


if __name__ == "__main__":
    token = load_api_token()
    pass_dict = get_pass()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_csv",
        type=str,
        default="input_tmp/input_kabusapi_sendorder_cash.csv",
    )
    parser.add_argument(
        "-d", "--debug", action="store_const", const=True, default=False
    )
    args = vars(parser.parse_args())  # 辞書型でほしいとき

    if args["debug"]:
        test_kabusapi_sendorder_cash(token, pass_dict)
    else:
        df = pd.read_csv(args["input_csv"])
        objs = df[order_columns].to_dict("index")
        for k, obj in objs.items():
            # print(obj)
            obj["Password"] = pass_dict["ORDERPASS"]  # 注文パスワード
            print("-" * 100)
            print("kabusapi_sendorder_cash:", "Symbol:", obj["Symbol"])
            kabusapi_sendorder_cash(token, obj)
