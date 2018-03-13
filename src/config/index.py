import os
import json

topicsPath = os.path.join(os.path.dirname(__file__), "./topics.json")
topics = json.load(open(topicsPath))
configPath = os.path.join(os.path.dirname(__file__), "./config.json")
config = json.load(open(configPath))

boxes = [{'colour':'red','centroid':(1,1),'rotation':91.5,'width':4.1,'length':5.2}, \
{'colour':'red','centroid':(2,2),'rotation':91.5,'width':4.1,'length':5.2}, \
{'colour':'red','centroid':(3,3),'rotation':91.5,'width':5.7,'length':5.2}, \
{'colour':'red','centroid':(4,4),'rotation':91.5,'width':4.3,'length':5.6}, \
{'colour':'blue','centroid':(1,1),'rotation':5.6,'width':2.6,'length':4.3}, \
{'colour':'blue','centroid':(2,2),'rotation':5.6,'width':3.8,'length':3.2}, \
{'colour':'blue','centroid':(3,3),'rotation':5.6,'width':2.6,'length':3.9}, \
{'colour':'blue','centroid':(4,4),'rotation':5.6,'width':3.1,'length':2.8}, \
{'colour':'green','centroid':(1,1),'rotation':12.6,'width':2.7,'length':5.7}, \
{'colour':'green','centroid':(2,2),'rotation':12.6,'width':1.8,'length':4.3}, \
{'colour':'green','centroid':(3,3),'rotation':12.6,'width':6.4,'length':4.5}, \
{'colour':'yellow','centroid':(1,1),'rotation':12.6,'width':2.7,'length':5.7}, \
{'colour':'yellow','centroid':(2,2),'rotation':12.6,'width':2.8,'length':5.1}, \
{'colour':'yellow','centroid':(3,3),'rotation':12.6,'width':2.2,'length':4.5}, \
{'colour':'yellow','centroid':(4,4),'rotation':12.6,'width':5.8,'length':3.2}, \
{'colour':'yellow','centroid':(5,5),'rotation':12.6,'width':5.6,'length':5.2}, \
{'colour':'yellow','centroid':(6,6),'rotation':12.6,'width':4.7,'length':3.1}, \
{'colour':'purple','centroid':(1,1),'rotation':0,'width':2.5,'length':2.5}, \
{'colour':'purple','centroid':(2,2),'rotation':0,'width':2.5,'length':3.1}, \
{'colour':'purple','centroid':(3,3),'rotation':0,'width':1.4,'length':2.8}, \
{'colour':'purple','centroid':(4,4),'rotation':0,'width':1.9,'length':2.9}, \
{'colour':'purple','centroid':(5,5),'rotation':0,'width':2.1,'length':3.4}, \
{'colour':'purple','centroid':(6,6),'rotation':0,'width':2.1,'length':1.9}]
