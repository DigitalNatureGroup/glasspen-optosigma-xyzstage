# pyOptSigma_TCPInterface

## tcp通信形式
- port: 2430
- '{stage番号},{動かす量}'の形式で文字表現したstringを数値1バイトに変換してで送る
  - ex in Matlab) 2番目のステージを-100動かすならwrite(t,unicode2native('2,-100'))

## setup
- clone this repo
- pip install pyserial (or pip3)

## 実行
- python tcp_server COM3とか
- [クライアント側を実行]