# 専用ドングルなしでMyo開発をしたい！
専用ドングルなしで、Myoを用いた開発を行うための環境構築や、基本的な計測アプリケーションについて、メモを残します。

## 開発環境
 <table>
    <tr>
      <td>os</td>
      <td>windows11</td>
    </tr>
    <tr>
      <td>言語</td>
      <td>Python 3.12.5</td>
    </tr>
    <tr>
      <td>仮想環境</td>
      <td>Python venv</td>
    </tr>
 </table>

## BLEでMyoを接続する（専用ドングルなし）
iomzさんが公開している[dl-myo](https://github.com/iomz/dl-myo)を利用します。

githubをクローンし、`dl-myo`下にある`Myo`ディレクトリを利用したいプロジェクトのPythonに、モジュールとして配置します。
（例：venvを利用している場合、`.venv/lib`下に`Myo`ディレクトリを配置すればよい）

あとは、bleakモジュールをインストールすれば準備完了です。
```
pip install bleak
```

## dl-myoサンプルコード
iomzさんが公開しているプロジェクトのサンプルコードを動かしてみましょう。

クローンしたプロジェクト内で開発している場合、`dl-myo`下で次のコマンドで実行できます。
```
py .\examples\sample_client.py
```
Myoが接続され、コンソール上に数値の羅列が表示されれば成功です。（このコードでは、データのファイル出力等はされません。）

## myo_projectsコード解説
### emgData_recorder.py
Myoから指定した秒数間データを取得し、`./emg_data`にjson形式で保存します。`--seconds`で秒数を指定できます。
```
py .\myo_progects\emgData_recorder.py --seconds 20
```
### fv_emgData_display.py
`emgData_recorder.py`で取得したデータのうち、fvデータ（フィルタリング済みの筋電値）をグラフ表示します。
```
py .\myo_progects\fv_emgData_display.py
```
### myo_viewer.py
Myoの筋電値をリアルタイムでグラフに描画します。
`--plot_type`で描画タイプを指定できます（`line`:棒グラフ、`radar`:レーダーチャート）
`--fps`で描画速度を指定できます。（デフォルトは30fps）
```
py .\myo_progects\myo_viewer.py --plot_type radar --fps 30
```



