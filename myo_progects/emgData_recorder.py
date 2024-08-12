# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
import json
import datetime
import os

from myo import AggregatedData, MyoClient
from myo.types import (
    ClassifierEvent,
    ClassifierMode,
    EMGData,
    EMGMode,
    FVData,
    IMUData,
    IMUMode,
    MotionEvent,
    VibrationType,
)
from myo.constants import RGB_GREEN


class SampleClient(MyoClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_prefix = f"myo_data_{timestamp}"
        
        # ディレクトリの作成
        self.save_directory = "./emg_data"
        os.makedirs(self.save_directory, exist_ok=True)

    async def on_classifier_event(self, ce: ClassifierEvent):
        logging.info(ce.json())
        with open(f'{self.save_directory}/{self.file_prefix}_classifier_event.json', 'a') as f:
            json.dump(ce.to_dict(), f)
            f.write('\n')

    async def on_aggregated_data(self, ad: AggregatedData):
        logging.info(ad)
        with open(f'{self.save_directory}/{self.file_prefix}_aggregated_data.json', 'a') as f:
            json.dump(ad.to_dict(), f)
            f.write('\n')

    async def on_emg_data(self, emg: EMGData):
        # logging.info(emg)
        with open(f'{self.save_directory}/{self.file_prefix}_emg_data.json', 'a') as f:
            json.dump(emg.to_dict(), f)
            f.write('\n')

    async def on_fv_data(self, fvd: FVData):
        # logging.info(fvd.json())
        with open(f'{self.save_directory}/{self.file_prefix}_fv_data.json', 'a') as f:
            json.dump(fvd.to_dict(), f)
            f.write('\n')

    async def on_imu_data(self, imu: IMUData):
        # logging.info(imu.json())
        with open(f'{self.save_directory}/{self.file_prefix}_imu_data.json', 'a') as f:
            json.dump(imu.to_dict(), f)
            f.write('\n')

    async def on_motion_event(self, me: MotionEvent):
        logging.info(me.json())
        with open(f'{self.save_directory}/{self.file_prefix}_motion_event.json', 'a') as f:
            json.dump(me.to_dict(), f)
            f.write('\n')


async def main(args: argparse.Namespace):
    logging.info("scanning for a Myo device...")

    sc = await SampleClient.with_device(mac=args.mac, aggregate_all=True)

    # get the available services on the myo device
    info = await sc.get_services()
    logging.info(info)

    # setup the MyoClient
    await sc.setup(
        classifier_mode=ClassifierMode.ENABLED,
        emg_mode=EMGMode.SEND_FILT,  # for aggregate_all
        imu_mode=IMUMode.SEND_ALL,  # for aggregate_all
    )

    # start the indicate/notify
    await sc.start()

    # receive notifications for the specified time
    await asyncio.sleep(args.seconds)

    # stop the indicate/notify
    await sc.stop()

    logging.info("bye bye!")
    await sc.vibrate(VibrationType.LONG)
    await sc.led(RGB_GREEN)
    await sc.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="sets the log level to debug",
    )
    parser.add_argument(
        "--mac",
        default="",
        help="the mac address to connect to",
        metavar="<mac-address>",
    )
    parser.add_argument(
        "--seconds",
        default=10,
        help="seconds to read data",
        metavar="<seconds>",
        type=int,
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main(args))
