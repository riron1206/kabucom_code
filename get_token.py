"""
kabuコムAPIのトークン取得
Usage:
    python .\get_token.py
    -> token.yaml が出力される
"""

import json
import requests
import yaml


def get_pass(yaml_path="../../auth.yaml"):
    """kabuコムAPIのパスワードロード"""
    with open(yaml_path) as f:
        pass_dict = yaml.safe_load(f)
    return pass_dict


def get_token(API_URL, API_PASSWORD):
    """
    kabuコムAPIのトークン取得
    kabuステーションのアプリ起動していないと失敗する
    """
    URL = API_URL + "/token"
    headers = {"content-type": "application/json"}
    payload = {"APIPassword": API_PASSWORD}

    try:
        response = requests.post(
            URL, data=json.dumps(payload).encode("utf8"), headers=headers
        )
    except Exception as e:
        print(e)

    return json.loads(response.text).get("Token")


def load_api_token(yaml_path="token.yaml"):
    """yamlに書いたkabuコムAPIのtokenロード"""
    with open(yaml_path) as f:
        pass_dict = yaml.safe_load(f)
    return pass_dict["token"]


if __name__ == "__main__":
    pass_dict = get_pass()

    # 検証
    API_URL = pass_dict["KENSYO"]["API_URL"]
    API_PASSWORD = pass_dict["KENSYO"]["API_PASSWORD"]

    # 本番
    API_URL = pass_dict["HONBAN"]["API_URL"]
    API_PASSWORD = pass_dict["HONBAN"]["API_PASSWORD"]

    token = get_token(API_URL, API_PASSWORD)
    print("token:", token)
    with open("token.yaml", "w") as file:
        yaml.dump({"token": token}, file)
