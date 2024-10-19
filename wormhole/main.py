import os, sys
import time
import requests
import json

url_pattern = "https://api.wormholescan.io/api/v1/operations?page={page}&pageSize={pageSize}&sortOrder={sortOrder}"

page = 100
pageSize = 100
sortOrder = "ASC"

url = url_pattern.format(page=page, pageSize=pageSize, sortOrder=sortOrder)
datadir = "./output/"
filenames = os.listdir(datadir)
scrawled_page = max(
    [int(name.split("_")[1].split(".")[0]) for name in filenames], default=page
)
page = scrawled_page + 1

header = {"Connection": "close"}

sleepdur = 60
banned = False
index = 0
banned_time = 0
unbanned_time = 0
while True:
    url = url_pattern.format(page=page, pageSize=pageSize, sortOrder=sortOrder)
    try:
        before_req = time.perf_counter()
        r = requests.get(url, headers=header, timeout=120)
        after_req = time.perf_counter()
        print(f"req cost: {after_req-before_req}")
        if banned:
            unbanned_time = time.time()
            sleepdur = (unbanned_time - banned_time) // 2
            banned = False
        filepath = f"{datadir}/data_{page}.json"
        json.dump(r.json(), open(filepath, "w"))
        print(f"finished: {page}, {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
        page += 1
    except Exception as e:
        if banned:
            sleepdur *= 2
        else:
            banned_time = time.time()
        banned = True
        print(f"banned! sleep: {sleepdur}")
        time.sleep(sleepdur)
