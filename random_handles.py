import csv, sys
from random import randint

URL = "http://test.cottagelabs.com:8080/xmlui/handle/{handle}?show=full"

csv_file = sys.argv[1]
html_out = sys.argv[2]

reader = csv.reader(open(csv_file))

all_handles = []
first = True
for row in reader:
    if first:
        first = False
        continue
    all_handles.append(row[0])

to_check = int(len(all_handles) / 100)

check_handles = []
for i in range(to_check):
    key = randint(0, len(all_handles))
    check_handles.append(all_handles[key])
    del all_handles[key]

page = "<html><body>"
i = 1
for h in check_handles:
    link = URL.replace("{handle}", h)
    frag = str(i) + ": <a href='" + link + "' target='_blank'>" + link + "</a><br>"
    page += frag
    i += 1
page += "</body></html>"

with open(html_out, "wb") as f:
    f.write(page)

