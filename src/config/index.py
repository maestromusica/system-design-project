import os
import json

topicsPath = os.path.join(os.path.dirname(__file__), "./topics.json")
topics = json.load(open(topicsPath))
configPath = os.path.join(os.path.dirname(__file__), "./config.json")
config = json.load(open(configPath))
