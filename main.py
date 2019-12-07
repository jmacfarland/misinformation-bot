from utils import Utils
from dataset import Dataset

d = Dataset()
d.load_csv('data/cresci-rtbust-2019.csv', 5)
print(d)
