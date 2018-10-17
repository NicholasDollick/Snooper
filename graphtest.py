from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import hcolor
import numpy as np

graph = Pyasciigraph(
    separator_length=4,
    multivalue=False,
    human_readable='si',
)

dataset = {'Sunday':0, 'Monday':0, 'Tuesday':0,
    'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0}

chart = []
keys = sorted(dataset.keys())
mean = np.mean(list(dataset.values()))
median = np.median(list(dataset.values()))

for key in keys:
    chart.append((key, dataset[key]))

thresholds = {
    int(mean): Gre, int(mean * 2): Yel, int(mean * 3): Red,
}

print("[*] Fetching data for /u/thisisatest\n")

data = hcolor(chart, thresholds)

for line in graph.graph('Weekly activity distribution (per day)', data):
    print(line)

test = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
print()