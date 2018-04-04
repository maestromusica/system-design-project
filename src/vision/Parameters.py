import numpy as np
#dims are stored sorted lowest to highest
Boxes = {'red':{'l':3.80,'w':1.90,'h':3.50,'weight':10},'blue':{'l':2.40,'w':1.95,'h':3.5,'weight':10},'green':{'l':3.00,'w':2.30,'h':3.5,'weight':10},'yellow':{'l':4.00,'w':1.30,'h':3.5,'weight':10},'pink':{'l':1.70,'w':1.70,'h':3.5,'weight':10},'orange':{'l':4.20,'w':2.10,'h':3.5,'weight':10}}
#Boxes = {'red':{'l':5,'w':4,'h':3.5,'weight':10},'blue':{'l':2,'w':1,'h':3.5,'weight':10},'green':{'l':3,'w':2,'h':3.5,'weight':10},'yellow':{'l':4,'w':1,'h':3.5,'weight':10},'purple':{'l':7,'w':5,'h':3#.5,'weight':10}}
offset = 0.3

test_boxes = [{'colour':'red','centroid':(1,1),'rotation':91.5,'width':4.1,'length':5.2}, {'colour':'red','centroid':(2,2),'rotation':91.5,'width':4.1,'length':5.2}, {'colour':'red','centroid':(3,3),'rotation':91.5,'width':5.7,'length':5.2}, {'colour':'red','centroid':(4,4),'rotation':91.5,'width':4.3,'length':5.6}, {'colour':'blue','centroid':(5,5),'rotation':5.6,'width':2.6,'length':4.3}, {'colour':'blue','centroid':(6,6),'rotation':5.6,'width':3.8,'length':3.2}, {'colour':'blue','centroid':(7,7),'rotation':5.6,'width':2.6,'length':3.9}, {'colour':'blue','centroid':(8,8),'rotation':5.6,'width':3.1,'length':2.8}, {'colour':'green','centroid':(9,9),'rotation':12.6,'width':2.7,'length':5.7}, {'colour':'green','centroid':(10,10),'rotation':12.6,'width':1.8,'length':4.3}, {'colour':'green','centroid':(11,11),'rotation':12.6,'width':6.4,'length':4.5}, {'colour':'yellow','centroid':(12,12),'rotation':12.6,'width':2.7,'length':5.7}, {'colour':'yellow','centroid':(13,13),'rotation':12.6,'width':2.8,'length':5.1}, {'colour':'yellow','centroid':(14,14),'rotation':12.6,'width':2.2,'length':4.5}, {'colour':'yellow','centroid':(15,15),'rotation':12.6,'width':5.8,'length':3.2}, {'colour':'yellow','centroid':(16,16),'rotation':12.6,'width':5.6,'length':5.2}, {'colour':'yellow','centroid':(17,17),'rotation':12.6,'width':4.7,'length':3.1}, {'colour':'purple','centroid':(18,18),'rotation':0,'width':2.5,'length':2.5}, {'colour':'purple','centroid':(19,19),'rotation':0,'width':2.5,'length':3.1}, {'colour':'purple','centroid':(20,20),'rotation':0,'width':1.4,'length':2.8}, {'colour':'purple','centroid':(21,21),'rotation':0,'width':1.9,'length':2.9}, {'colour':'purple','centroid':(22,22),'rotation':0,'width':2.1,'length':3.4}, {'colour':'purple','centroid':(23,23),'rotation':0,'width':2.1,'length':1.9}]

test_box_set = [{'colour':'red','centroid':(1,1),'rotation':91.5,'width':4.1,'length':5.2}, {'colour':'blue','centroid':(5,5),'rotation':5.6,'width':2.6,'length':4.3}, {'colour':'green','centroid':(9,9),'rotation':12.6,'width':2.7,'length':5.7}, {'colour':'yellow','centroid':(13,13),'rotation':12.6,'width':2.8,'length':5.1}, {'colour':'purple','centroid':(18,18),'rotation':0,'width':2.5,'length':2.5}]
