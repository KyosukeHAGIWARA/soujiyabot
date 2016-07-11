# slack_bot
slackのbot with Python 

## もとにしたもの
[PythonでSlackbotを作るシリーズ](http://blog.bitmeister.jp/?p=3892)(http://blog.bitmeister.jp/?p=3892)

## いぞん
+ python (3.x)
+ slackbot (0.4.1)
+ slacker (0.9.21)

## cleanup.py
+ ユーザーリストから乱択してお掃除当番を決める
+ 当番になった人は今後の当選確率が1/2になる
+ 当たらなかった人は2倍になる
+ 週1回で1年間回すと10人の当番回数の分散はおよそ1くらいになる
  + (実験で確かめた)
+ パラメータradixをいじると確率が操作できる(当たらなかった時の確率がradix倍に増える)
  + radix = 1 のとき完全乱択になる
+ botに"clean-up duty"と話しかけると当番を決める
+ botに"clean-up reset"と話しかけると履歴を消す
+ botに"clean-up statistics"と話しかけると今までの当番統計を出す

## そのほか
+ cleanup.pyはもっと抽象度高く書けば掃除当番以外にも使えそうとおもった。

## らいせんす
  MIT
