import csv
import itertools
import sys

sigs = []

with open(sys.argv[1]) as f:
    r = csv.DictReader(f)
    rows = list(r)

result = []

for row in rows:
    signature = f"{row['First name'].strip()} {row['Last name'].strip()}, {row['Address'].strip()}, {row['City'].strip()} ({row['Email'].strip()})"
    result.append(
        (row["Target Name"], row["Letter Subject"], row["Letter Body"], signature)
    )

f = lambda k: (k[0], k[1], k[2])
result.sort()
result = itertools.groupby(result, key=f)

for (target, subject, body), stuff in result:
    sigs = [x[3] for x in stuff]
    sigs = list(sorted(list(set(sigs))))

    print(f"<h6>TO: {target}</h6>")
    print(f"<b><i>{subject}</i></b><br/><br/>")
    print()
    print(body.replace("\n", "<br>"))
    print("<br><br>")
    print("<b>Signed:</b><br>")
    print("<br>".join(sigs))
