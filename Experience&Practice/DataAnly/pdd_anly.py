import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_zh = FontProperties(fname='/Library/Fonts/Songti.ttc')

file_path = '/Users/hacker/Desktop/goods_rank.json'

with open(file_path, 'rb') as f:
    data = f.readlines()

data = list(map(lambda x: x.rstrip(), data))

data_json_str = b"[" + b','.join(data) + b"]"

pds = pd.read_json(data_json_str)

plt.style.use('ggplot')

# pds.head().soldQuantity.hist()
# data_show = pds.boxplot(column='soldQuantity', by='optName')
#
# data_show.set_title('Pdd SoldQuantity Analysis', size=18, color='r')

data_show = pds.boxplot(column='goodsFactPrice', by='optName')

data_show.set_title('Pdd Sale Today Analysis', size=18, color='r')

for x in data_show.get_xticklabels():
    x.set_fontproperties(font_zh)

plt.show()