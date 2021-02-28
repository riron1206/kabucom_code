# kabu.com API用コード

## 事前準備

- auカブコム証券の口座作る
  - https://kabu.com/

- kabuステーション（通常プラン） に申し込んでアプリもダウンロードする
  - https://kabu.com/kabustation/
  - kabuステーション（本体）は利用料は 990円（税込）/月 だが、信用口座開設済みの場合無料 なので信用口座開設するといい（信用口座開設は即日で通った）



## 実行手順

#### 0.kabuステーションのアプリ起動しておく
**※アプリ起動しておかないとapi使えない**

#### 1.token取得
**※../../auth.yaml おいておく必要あり！！！！**

```
python get_token.py
-> カレントディレクトリに token.yaml が出力される
```

#### 2.銘柄情報取得
```
python kabusapi_symbol.py -s 5401 -o output_tmp
-> 銘柄情報として output_tmp/kabusapi_symbol_5401.csv が出力される
```

#### 3.kabuステーションに銘柄登録
※銘柄コードと市場コードは2.銘柄情報取得のcsvからわかる
※登録した銘柄はkabuステーションの右上の<>から確認できる
```
python kabusapi_register.py -s 5401 -e 1
```

#### 4.注文発注（現物）買/売
```
python kabusapi_sendorder_cash.py -i input_tmp/input_kabusapi_sendorder_cash.csv
-> input_tmp/input_kabusapi_sendorder_cash1.csv の注文が実行される
```

#### 5.kabuステーションの登録銘柄のリアルタイムの情報を取得する
※9-15時の間じゃないと使えない
※kabuステーションに銘柄登録しておかないと使えない
```
python kabusapi_websocket.py
```

#### 5-1.リアルタイムでkabuステーションの登録銘柄の注文を入れる
※注文csv必要
※kabuステーションに銘柄登録しておかないと使えない
```
python kabusapi_websocket.py -i input_tmp/input_kabusapi_sendorder_cash.csv
```


