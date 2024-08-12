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

## サンプルコード
iomzさんが公開しているプロジェクトのサンプルコードを動かしてみましょう。

クローンしたプロジェクト内で開発している場合、`dl-myo`下で次のコマンドで実行できます。
```
py .\examples\sample_client.py
```
Myoが接続され、コンソール上に数値の羅列が表示されれば成功です。（このコードでは、データのファイル出力等はされません。）