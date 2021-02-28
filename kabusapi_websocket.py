"""
kabuステーションの登録銘柄のリアルタイムの株価情報を取得する
Usage:
    python kabusapi_websocket.py  # リアルタイム情報取得
    python kabusapi_websocket.py -i input_tmp/input_kabusapi_sendorder_cash.csv  # リアルタイムでkabuステーションの登録銘柄の注文を入れる

1件のデータは以下の項目持つ
# https://kabucom.github.io/kabusapi/reference/index.html#operation/boardGet
{
    "OverSellQty": 1179600.0,  # OVER気配数量
    "UnderBuyQty": 1299100.0,  # UNDER気配数量
    "TotalMarketValue": 14929633573520.0,  # 時価総額
    "Exchange": 1,  # 市場コード
    "ExchangeName": "東証１部",  # 市場名称
    "TradingVolume": 11654100.0,  # 売買高
    "TradingVolumeTime": "2020-10-12T12:45:39+09:00",  # 売買高時刻
    "VWAP": 7075.3639,  # 売買高加重平均価格（VWAP）
    "TradingValue": 82456998700.0,  # 売買代金
    "BidQty": 1000.0,  # 最良売気配数量
    "BidPrice": 7145.0,  # 最良売気配値段
    "BidTime": "2020-10-12T12:45:39+09:00",  # 最良売気配時刻
    "BidSign": "0101",  # 最良売気配フラグ 0101:一般気配
    "MarketOrderSellQty": 0.0,  # 売成行数量
    "Sell1": {
        "Time": "2020-10-12T12:45:39+09:00",
        "Sign": "0101",
        "Price": 7145.0,
        "Qty": 1000.0,
    },  # 売気配数量1本目
    "Sell2": {"Price": 7146.0, "Qty": 6700.0},  # 売気配数量2本目
    "Sell3": {"Price": 7147.0, "Qty": 3800.0},  # 売気配数量3本目
    "Sell4": {"Price": 7148.0, "Qty": 9500.0},  # 売気配数量4本目
    "Sell5": {"Price": 7149.0, "Qty": 19800.0},  # 売気配数量5本目
    "Sell6": {"Price": 7150.0, "Qty": 82900.0},  # 売気配数量6本目
    "Sell7": {"Price": 7151.0, "Qty": 4800.0},  # 売気配数量7本目
    "Sell8": {"Price": 7152.0, "Qty": 4700.0},  # 売気配数量8本目
    "Sell9": {"Price": 7153.0, "Qty": 2000.0},  # 売気配数量9本目
    "Sell10": {"Price": 7154.0, "Qty": 4600.0},  # 売気配数量10本目
    "AskQty": 3300.0,  # 最良買気配数量
    "AskPrice": 7144.0,  # 最良買気配値段
    "AskTime": "2020-10-12T12:45:39+09:00",  # 最良買気配時刻
    "AskSign": "0101",  # 最良買気配フラグ 0101:一般気配
    "MarketOrderBuyQty": 0.0,  # 買成行数量
    "Buy1": {
        "Time": "2020-10-12T12:45:39+09:00",
        "Sign": "0101",
        "Price": 7144.0,
        "Qty": 3300.0,
    },  # 買気配数量1本目
    "Buy2": {"Price": 7143.0, "Qty": 1600.0},  # 買気配数量2本目
    "Buy3": {"Price": 7142.0, "Qty": 7900.0},  # 買気配数量3本目
    "Buy4": {"Price": 7141.0, "Qty": 3700.0},  # 買気配数量4本目
    "Buy5": {"Price": 7140.0, "Qty": 3500.0},  # 買気配数量5本目
    "Buy6": {"Price": 7139.0, "Qty": 6200.0},  # 買気配数量6本目
    "Buy7": {"Price": 7138.0, "Qty": 3300.0},  # 買気配数量7本目
    "Buy8": {"Price": 7137.0, "Qty": 2900.0},  # 買気配数量8本目
    "Buy9": {"Price": 7136.0, "Qty": 2100.0},  # 買気配数量9本目
    "Buy10": {"Price": 7135.0, "Qty": 3200.0},  # 買気配数量10本目
    "Symbol": "9984",  # 銘柄コード
    "SymbolName": "ソフトバンクグループ",  # 銘柄名
    "CurrentPrice": 7144.0,  # 現値
    "CurrentPriceTime": "2020-10-12T12:45:39+09:00",  # 現値時刻
    "CurrentPriceChangeStatus": "0058",  # 現値前値比較  0056: 変わらず, 0057: UP, 0058: DOWN
    "CurrentPriceStatus": 1,  # 現値ステータス  1: 現値
    "CalcPrice": 7144.0,  # 計算用現値
    "PreviousClose": 6997.0,  # 前日終値
    "PreviousCloseTime": "2020-10-09T00:00:00+09:00",  # 前日終値日付
    "ChangePreviousClose": 147.0,  # 前日比
    "ChangePreviousClosePer": 2.1,  # 騰落率
    "OpeningPrice": 6989.0,  # 始値
    "OpeningPriceTime": "2020-10-12T09:00:00+09:00",  # 始値時刻
    "HighPrice": 7150.0,  # 高値
    "HighPriceTime": "2020-10-12T11:19:30+09:00",  # 高値時刻
    "LowPrice": 6970.0,  # 安値
    "LowPriceTime": "2020-10-12T09:05:55+09:00",  # 安値時刻
}
"""
import sys
import websocket
import _thread
import re
import ast
import argparse
import json
import datetime
import traceback
import pandas as pd

from get_token import get_pass, get_token, load_api_token
from kabusapi_sendorder_cash import kabusapi_sendorder_cash, order_columns

# pass_dict = get_pass()
# token = get_token(pass_dict["HONBAN"]["API_URL"], pass_dict["HONBAN"]["API_PASSWORD"])
# print("token:", token)
token = load_api_token()

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input_csv", type=str, default=None,
)
args = vars(parser.parse_args())  # 辞書型でほしいとき
order_df = pd.read_csv(args["input_csv"]) if args["input_csv"] is not None else None


def order_yoritsuki(message):
    """寄付きの条件で注文"""
    d = json.loads(message)  # jsonを辞書型に変換
    symbol_df = order_df[
        (order_df["Symbol"] == d["Symbol"])
        & (order_df["yoritsuki_low"] < d["OpeningPrice"])
        & (d["OpeningPrice"] < order_df["yoritsuki_high"])
    ]
    if symbol_df.shape[0] > 0:
        order_obj = symbol_df.iloc[0][order_columns].to_dict()
        kabusapi_sendorder_cash(token, order_obj)


def check_dxt(message):
    """wsで取ったリアルタイムの株価情報の1行分のデータを解体できるか確認"""
    try:
        d = json.loads(message)  # jsonを辞書型に変換
        day_str = re.sub("T.*", "", d["CurrentPriceTime"])
        day = datetime.datetime.strptime(day_str, "%Y-%m-%d")
        time_str = re.sub(".*T", "", d["CurrentPriceTime"])
        time_str = re.sub("\+.*", "", time_str)
        time = datetime.datetime.strptime(f"{day_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        return [d["Symbol"], day, time, d["CurrentPrice"]]
    except Exception:
        traceback.print_exc()
        return None


def on_message(ws, message):
    print("--- RECV MSG. --- ")
    ############################# 変更部分 #################################
    if order_df is None:
        print("message:", message)
        data = check_dxt(message)  # データチェック
        print("ws data:", data)
    else:
        order_yoritsuki(message)  # 寄付きの条件で注文
    ########################################################################


def on_error(ws, error):
    print("--- ERROR --- ")
    print(error)


def on_close(ws):
    print("--- DISCONNECTED --- ")


def on_open(ws):
    print("--- CONNECTED --- ")

    def run(*args):
        while True:
            line = sys.stdin.readline()
            if line != "":
                print("closing...")
                ws.close()

    _thread.start_new_thread(run, ())


url = "ws://localhost:18080/kabusapi/websocket"  # 本番url
# websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    url, on_message=on_message, on_error=on_error, on_close=on_close
)
ws.on_open = on_open
ws.run_forever()
