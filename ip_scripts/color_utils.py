import numpy as np
from skimage import color

def convert_colorspace(img,colorspace_list):
	""" Converts RGB image to the formats in colorspace_list

	Paramters
	---------

	img : Input Image

	colorspace_list : string list of colorspaces to be converted to. This param can also be a string
	Possible strings are ['RGB', 'I', 'LAB', 'rgI', 'HSV', 'rgb', 'C', 'H']

	Returns
	--------

	out_arr : list of images in various colorspaces. Shape: (|colorspace_list|, )

	"""



	colorspace = np.atleast_1d(colorspace_list)

	out_arr = [[]]*len(colorspace)

	for i,colorspace in enumerate(colorspace_list):
		
		if colorspace == 'RGB':
			if img.max()>1: out_arr[i] = img/255.0
			else: out_arr[i] = img

		elif colorspace == 'I':
			out_arr[i] = color.rgb2gray(img)

		elif colorspace == 'LAB':
			out_arr[i] = color.rgb2lab(img)
			out_arr[i][:,:,0] = out_arr[i][:,:,0]/100.0
			out_arr[i][:,:,1] = (out_arr[i][:,:,1]+127)/255.0	
			out_arr[i][:,:,2] = (out_arr[i][:,:,1]+127)/255.0

		elif colorspace == 'rgI':
			out_arr[i] = np.zeros(img.shape)
			out_arr[i][:,:,0:2] = img[:,:,0:2]
			out_arr[i][:,:,2] = color.rgb2gray(img)

		elif colorspace == 'HSV':
			out_arr[i] = color.rgb2hsv(img)

		elif colorspace == 'rgb':
			out_arr[i] = rgb2rgb_norm(img)

		elif colorspace == 'C':
			out_arr[i] = rgb2C(img)

		elif colorspace == 'H:':
			out_arr[i] == color.rgb2hsv(img)[:,:,0]

		else:
			print('Not Implemented. Error')
			return None

	return out_arr

def rgb2C(img):
	""" Converts RGB to Opponent color space
	Paramters
	---------

	img : Input Image

	Returns
	--------

	out_arr : Opponent colorspace image

	Refer to https://engineering.purdue.edu/~bouman/ece637/notes/pdf/Opponent.pdf for more details
	"""
	
	out_arr = np.zeros(img.shape)
	out_arr[:,:,0] = color.rgb2lab(img)[:,:,0]
	out_arr[:,:,1] = img[:,:,1] - img[:,:,0]
	out_arr[:,:,2] = img[:,:,2] - (img[:,:,1] + img[:,:,0])
	return out_arr


