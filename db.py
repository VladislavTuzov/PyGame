import os
import os.path
import shelve


def save(points):
    with shelve.open("data/data", flag="c") as data:
        table = data.get("points")
        if table is not None:
            if int(min(table, key=int)) < points.value:
                table.append(str(points))
            data["points"] = sorted(table, key=int, reverse=True)[:10]
        else:
            data["points"] = [str(points)]


def extract():
    with shelve.open("data/data") as data:
        table = data.get("points")
    return table


if not os.path.exists("data"):
    os.mkdir("data")
