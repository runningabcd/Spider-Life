import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# import pylab as pla

font_zh = FontProperties(fname='/Library/Fonts/Songti.ttc')

# pla.rcParams['font.sans-serif'] = ['Songti']

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

pds['turn_volume'] = (pds.goodsFactPrice//100 * pds.soldQuantity) // 10000

data_show = pds.groupby('optName').turn_volume.sum().plot.bar()

# data_show = pds.boxplot(column='turn_volume', by='optName')

data_show.set_title(f'拼多多各行业销量前一万名商品销售额({pds.turn_volume.sum()}万)', color='k', fontproperties=font_zh)

data_show.set_ylabel('成交额/万', fontproperties=font_zh)

data_show.set_xlabel('行业分类', fontproperties=font_zh)

for x in data_show.get_xticklabels():
    x.set_fontproperties(font_zh)

plt.show()