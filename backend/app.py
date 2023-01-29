from flask import Flask
from flask_cors import CORS
import json
import pandas as pd
from flask import request
import os
import time
import pickle
import pathlib
import torch
import torchvision.transforms as T
from tiatoolbox.models.architecture import get_pretrained_model, fetch_pretrained_weights
from tiatoolbox.models import IOPatchPredictorConfig
from umap import UMAP
from PIL import Image
import numpy as np
from sklearn.cluster import DBSCAN
import faiss
import numpy as np
import pandas as pd

def concat(path):
	return path[29:]+".jpg"

def findType(path):
	if "01_TUMOR" in path:
		return "Tumor" 
	if "02_STROMA" in path:
		return "Stroma"
	if "03_COMPLEX" in path:
		return "Complex"
	if "04_LYMPHO" in path:
		return "Lympho"
	if "05_DEBRIS" in path:
		return "Debris"
	if "06_MUCOSA" in path:
		return "Mucosa"
	if "07_ADIPOSE" in path:
		return "Adipose"
	if "08_EMPTY" in path:
		return "None"

app = Flask(__name__)
CORS(app)

@app.route('/') # ‘https://www.google.com/‘
def home():
	obj = pd.read_pickle('data.pkl')
	data = pd.DataFrame.from_dict(obj)
	return json.dumps(data.to_dict(orient='records'))

@app.route('/upload', methods=['POST'])
def upload_file():
	file = request.files['file']
	filename = "input_file.tif"
	file.save(filename)
	print(file)
	return json.dumps({"status": "success"})

@app.route('/model')
def model():
	# unpickle the data dict
	with open('data3d.pkl', 'rb') as p:
		data = pickle.load(p)

	# define the model and input transforms
	trans = T.ToTensor()
	model, config = get_pretrained_model(pretrained_model='resnet101-kather100k')
	encoder = torch.nn.Sequential(*(list(model.children())[:-1])) # strip the classification layer
	del model
	
	# load the projector
	projector = data['UMAP']

	# load the image
	img = trans(Image.open('input_file.tif')).unsqueeze(0)
	
	# get the feature vector
	with torch.no_grad():
		rep = encoder(img).detach().cpu().numpy()
	
	# get the 2d point
	emb = projector.transform(np.expand_dims(rep.squeeze(), 0))
	x, y, z = float(emb[0][0]), float(emb[0][1]), float(emb[0][2])

	#Faiss algorithm
	obj = pd.read_pickle('data3d.pkl')
	obj.pop('UMAP', None)
	obj.pop('cluster', None)
	obj.pop('DBSCAN', None)
	obj.pop('representation', None)
	obj.pop('label', None)

	data = pd.DataFrame.from_dict(obj)
	data_w_out_path = data.drop(columns=['path'])

	# Create an array of 3D vectors
	vectors = data_w_out_path.to_numpy()

	# Create an index for the vectors
	index = faiss.IndexFlatL2(vectors.shape[1])

	# Add the vectors to the index
	index.add(vectors)

	# Search for the nearest neighbors of a query vector
	query = np.asarray([[x, y, z]]).astype('float32')
	distances, neighbors = index.search(query, k=10)

	results = pd.DataFrame({'distances': distances[0], 'neighbors': neighbors[0]})
	data['index'] = data.index
	data = data[data["index"].isin(neighbors[0])]
	merged = pd.merge(results, data, left_on="neighbors", right_index=True)
	merged['path'] = merged.apply(lambda row : concat(row['path']), axis = 1)
	merged['type'] = merged.apply(lambda row : findType(row['path']), axis = 1)
	print(merged.path.tolist())

	# # The first column of `neighbors` is the index of the nearest neighbor
	# print("The nearest neighbors are:", neighbors[0])

	return json.dumps({"paths": merged.path.tolist(), "type": list(set(merged.type.tolist())), "typesall": merged.type.tolist()})

app.run(port=5001)