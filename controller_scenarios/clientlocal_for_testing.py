#!/usr/bin/env python3

import time
import random
import subprocess
import datetime
import sys
import os
import requests
import subprocess
import asyncio
import concurrent.futures
import logging

MINUTE = 60

def main():
    sleeping_time = random.randint((float(sys.argv[1])-3), (float(sys.argv[1])+3))
    sleeping_time = random.randint(0, sleeping_time)
    first_start_time = time.time()

    while (time.time() - first_start_time) < 5*MINUTE:
#        subprocess.call(["iperf3", "-c", "10.0.0.50", "-p", "5202", "-u", "-R", "-t", "2", "-J"])
        logging.basicConfig(
                level=logging.INFO,
                format='%(threadName)10s %(name)18s: %(message)s',
                stream=sys.stderr,
            )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(post())
        # print(r.text)
        # subprocess.call(["curl", "-s", "-X", \
        # "POST", "-F", "file=@images/"+img+";type=image/jpeg", "http://193.190.127.181:8000/ca_tf/imageUpload/"+img])

        # time.sleep(random.randint(0,3))
        time.sleep(sleeping_time)
        sleeping_time = random.randint(0, sleeping_time)


async def post():
        log = logging.getLogger('run_blocking_tasks')
        log.info('starting')

        log.info('creating executor tasks')

        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            loop = asyncio.get_event_loop()
            response = []
            futures = [
                loop.run_in_executor(
                    executor,
                    post_skata,
                    i,
                )
                for i in range(5)
            ]
            log.info('waiting for executor tasks')
            completed, pending = await asyncio.wait(futures)
            results = [t.result() for t in completed]
            log.info('results: {!r}'.format(results))

            log.info('exiting')

            #for response in await asyncio.gather(*futures):
            #    pass


def post_skata(n):
    time.sleep(random.randint(0, n))
    log = logging.getLogger('blocks({})'.format(n))
    #log.info('running')

    n = str(random.randint(1, 3))
    img = "n" + n + ".jpg"
    post_url = "http://10.0.0.50:8000/ca_tf/imageUpload/" + img
    size = os.path.getsize("../images/" + img)
    pts = time.time()  # * 1000
    json = {"size": size, "start_time": pts}
    files = {"file": open("../images/" + img, "rb")}
    log.info('running')
    r = requests.post(post_url, files=files, data=json)

    log.info('done')

if __name__ == "__main__":
    main()
