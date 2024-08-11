import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from tkinter import Tk, filedialog

# ファイル選択ダイアログを表示してファイルを選択
def select_file():
    root = Tk()
    root.withdraw()  # Tkinterのメインウィンドウを非表示にする
    file_path = filedialog.askopenfilename(
        initialdir="EMG_data",
        title="Select a JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
    )
    return file_path

# データの読み込み
def load_aggregated_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# ファイル選択
file_path = select_file()
if not file_path:
    print("No file selected.")
    exit()

# グラフの初期設定
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 100)  # X軸の範囲は必要に応じて変更
ax.set_ylim(-2000, 2000)  # Y軸の範囲はFVデータの値に合わせる

# リアルタイムで描画するための初期データ
x_data = []
fv_data = [[] for _ in range(8)]  # FVデータ

# FVデータのライン設定
fv_lines = [ax.plot([], [], lw=2, label=f"FV{i+1}")[0] for i in range(8)]  # FVデータのライン

ax.legend(loc="upper left")

# アニメーション関数
def update(frame):
    # フレームに対応するデータを追加
    x_data.append(frame)
    for i in range(8):
        fv_data[i].append(data[frame]['fvd']['fv'][i])

    # X軸が右にずれるように範囲を更新
    ax.set_xlim(max(0, frame-100), frame + 10)

    # データを更新
    for i in range(8):
        fv_lines[i].set_data(x_data, fv_data[i])

    return fv_lines

# データの読み込み
data = load_aggregated_data(file_path)

# アニメーションの設定
ani = animation.FuncAnimation(
    fig, update, frames=len(data), blit=True, interval=50, repeat=False)

plt.show()
