


import csv
import json
import statistics
import sys


def csv_read(_filename):
    reader = csv.reader(open(_filename, "r"))
    for row in reader:
        for col in row:
            print(col)

def csv_print_2d_list(data):
    writer = csv.writer(sys.stdout)   # writes directly to the console
    writer.writerows(data)

def csv_read_gold_adv(_filename):
    matches_dict = {}
    reader = csv.reader(open(_filename, "r"))
    idx = 0
    for row in reader:
        if idx > 0:
            ###
            match_id = row[2]
            gold_adv = row[1]
            if match_id not in matches_dict:
                matches_dict[match_id] = []
            matches_dict[match_id].append(float(gold_adv))
            ###
        idx += 1
    matches_list = [{
        "match_id": k,
        "gold_advs": v,
    } for k, v in matches_dict.items()]
    return matches_list


####

def matches_to_table(_matches, _length=60):
    headers = ["minute"]
    headers = headers + [e for e in range(0, _length+1)]
    # print(headers)
    body = []
    for match in _matches:
        k = match["match_id"]
        v = match["gold_advs"]
        gold_advs = [(v[e:e+1] or [None])[0] for e in range(0, _length+1)]
        row = [k] + gold_advs
        body.append(row)
    # print(body)
    table = []
    table = [headers] + body
    # print(table)
    return table

def transpose_matrix(m):
    res = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
    return res

def get_latest_gold_adv(_match):
    tmp = [
        (i, e)
    for i, e in enumerate(_match["gold_advs"]) if e is not None]
    return tmp[-1]

def get_gold_adv_gradient(_match):
    diff = _match["gold_adv_latest"][1] - _match["gold_adv_min"][1]
    dist = _match["gold_adv_latest"][0] - _match["gold_adv_min"][0]
    res = (diff / dist) if dist > 0 else 0
    return res

def moving_average(values, window):
    """
    Parameters
      values : list or iterable of numbers
      window : int  (must be >= 1)
    Returns:
      list of float
        Length = len(values) - window + 1  (the “valid” part)
    """
    # Compute the sum of the first window
    window_sum = sum(values[:window])
    averages = [window_sum / window]
    # Slide the window forward one element at a time
    for i in range(window, len(values)):
        # subtract the element that falls out, add the new element
        window_sum += values[i] - values[i - window]
        averages.append(window_sum / window)
    return averages

def process_matches(_matches):
    matches = [{
        "match_id": e["match_id"],
        "gold_advs": e["gold_advs"],
        "gold_adv_avg": statistics.mean(e["gold_advs"]),
        "gold_adv_min": sorted([(i,e) for i, e in enumerate(e["gold_advs"])], key=lambda x: x[1])[0],
        "gold_adv_max": sorted([(i,e) for i, e in enumerate(e["gold_advs"])], key=lambda x: x[1], reverse=True)[0],
        "gold_adv_latest": get_latest_gold_adv(e),
    } for e in _matches]
    matches = [{
        "match_id": e["match_id"],
        "gold_advs": e["gold_advs"],
        "gold_adv_avg": e["gold_adv_avg"],
        "gold_adv_min": e["gold_adv_min"],
        "gold_adv_max": e["gold_adv_max"],
        "gold_adv_latest": e["gold_adv_latest"],
        "gold_adv_gradient": get_gold_adv_gradient(e),
    } for e in matches]
    return matches

# matches = csv_read_gold_adv("radiant_gold_adv.csv")
matches = csv_read_gold_adv("_a.csv")
matches = matches[:2]
print(json.dumps(matches, indent=2))
matches = process_matches(matches)
# print(json.dumps(matches, indent=2))

matches = [e for e in matches if e["gold_adv_latest"][0] >= 30]
matches = sorted(matches, key=lambda x: x["gold_adv_gradient"], reverse=True)
# matches = sorted(matches, key=lambda x: x["gold_adv_latest"][1], reverse=True)
# matches = sorted(matches, key=lambda x: x["gold_adv_min"][1])
# matches = matches[:100]
# print(json.dumps(matches, indent=2))

# table = matches_to_table(_matches=matches, _length=96)
# csv_print_2d_list(table)




# import duckdb
# import pandas as pd

# # 1️⃣ Open a connection (in‑memory by default)
# con = duckdb.connect()

# # 2️⃣ Run a query directly on a CSV file
# df = con.execute("""
#     SELECT
#         city,
#         AVG(salary) AS avg_salary,
#         COUNT(*)   AS cnt
#     FROM read_csv_auto('employees.csv')
#     WHERE department = 'Engineering'
#     GROUP BY city
#     ORDER BY avg_salary DESC
#     LIMIT 10
# """).df()          # .df() converts the result to a pandas DataFrame

# print(df)

