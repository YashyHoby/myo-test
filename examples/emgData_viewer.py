import asyncio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Queue, Event
from myo import Myo, MyoClient
from myo.types import FVData, EMGMode, IMUMode, ClassifierMode

class RealTimeFVClient(MyoClient):
    def __init__(self, queue, fps, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.fps = fps
        self.interval = 1.0 / fps

    async def on_fv_data(self, fvd: FVData):
        if not self.queue.full():  # キューが満杯でない場合のみ追加
            self.queue.put(fvd.fv)
        await asyncio.sleep(self.interval)  # データ取得の間隔をFPSに合わせる

    async def disconnect(self):
        if self._client and self._client.is_connected:
            await self._client.stop_notify()
            await self._client.disconnect()
            print("Myo device disconnected successfully.")

async def bluetooth_main(queue, stop_event, fps):
    client = None
    try:
        print("Searching for Myo device...")
        myo_device = await Myo.with_uuid()
        if myo_device is None:
            print("Myo device not found")
            return
        
        client = RealTimeFVClient(queue, fps)
        client.m = myo_device
        
        await client.connect()
        print("Myo device connected successfully.")

        await client.setup(
            classifier_mode=ClassifierMode.DISABLED,
            emg_mode=EMGMode.SEND_FILT,
            imu_mode=IMUMode.NONE,
        )
        print("Myo device setup complete.")

        await client.start()
        print("Myo device started.")

        while not stop_event.is_set():
            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Attempting to reconnect...")
        await asyncio.sleep(5)

    finally:
        if client:
            await client.disconnect()

def bluetooth_task(queue, stop_event, fps):
    asyncio.run(bluetooth_main(queue, stop_event, fps))

def plot_task(queue, stop_event, fps):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 50)
    ax.set_ylim(-2000, 2000)

    fv_lines = [ax.plot([], [], lw=2, label=f"FV{i+1}")[0] for i in range(8)]
    ax.legend(loc="upper left")
    x_data = []
    fv_data = [[] for _ in range(8)]
    current_frame = 0

    interval_ms = 1000 // fps  # 描画の更新間隔をFPSに合わせる

    def update(frame):
        nonlocal current_frame
        if not queue.empty():
            data = queue.get()
            current_frame += 1
            x_data.append(current_frame)
            for i in range(8):
                fv_data[i].append(data[i])
                # 最新の50データのみ表示
                fv_data[i] = fv_data[i][-50:]
            ax.set_xlim(max(0, current_frame-50), current_frame + 10)
            for i in range(8):
                fv_lines[i].set_data(x_data[-50:], fv_data[i])
        return fv_lines

    ani = animation.FuncAnimation(fig, update, blit=True, interval=interval_ms, repeat=False, cache_frame_data=False)

    def close_event(event):
        stop_event.set()
        plt.close(fig)

    fig.canvas.mpl_connect('close_event', close_event)
    plt.show()

if __name__ == "__main__":
    q = Queue(maxsize=1)  # 最新データだけを保持するキューサイズに制限
    stop_event = Event()
    
    fps = 30  # 取得したいFPSを指定
    bluetooth_process = Process(target=bluetooth_task, args=(q, stop_event, fps))
    bluetooth_process.start()

    plot_task(q, stop_event, fps)
    
    bluetooth_process.join()
