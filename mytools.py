import numpy as np
import skimage
from skimage.filters import threshold_multiotsu, threshold_otsu, median, gaussian, threshold_li
import skimage.morphology as morphology
from skimage.morphology import disk, square, diamond, closing, opening, black_tophat, white_tophat, dilation, erosion
from skimage.segmentation import chan_vese , morphological_chan_vese, checkerboard_level_set, circle_level_set, clear_border
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from skimage.exposure import *
from skimage import util
from skimage.util import invert

from sklearn.preprocessing import minmax_scale

def process_color(batch):
    color_list = []
    LND_processor = get_indexes()
    for img in batch:
        if np.std(img) > 0:
            LND_processor.image = img
            color = LND_processor.color()
        else:
            a, b, d = img.shape
            color = np.zeros((a, b,3))

        color_list.append(color)
    return color_list
    
def process_water(batch):
    water_list = []
    LND_processor = get_indexes()
    for img in batch:
        if np.std(img) > 0:
            LND_processor.image = img
            mndwi = LND_processor.mndwi()
        else:
            a, b, d = img.shape
            mndwi = np.zeros((a, b))

        water_list.append(mndwi)
    return water_list


def process_veg(batch):
    veg_list = []
    LND_processor = get_indexes()
    for img in batch:
        if np.std(img) > 0:
            LND_processor.image = img
            ndvi = LND_processor.ndvi()
        else:
            a, b, d = img.shape
            ndvi = nbi = np.zeros((a, b))

        veg_list.append(ndvi)
    return veg_list


def process_urban(batch):
    urban_list = []
    LND_processor = get_indexes()
    for img in batch:
        if np.std(img) > 0:
            LND_processor.image = img
            nbi = LND_processor.nbi()
        else:
            a, b, d = img.shape
            nbi = np.zeros((a, b))

        urban_list.append(nbi)
    return urban_list

def process_swes(array, threshold):
  swe_processor = get_swes(threshold)
  length = len(array)
  swes_arr = np.empty_like(array)

  for n, img in zip (range(length), array) :
    end = '.' if n % 30 or n == 0 else '\n'
    print(n, end = end)
    swe_processor.mndwi = img
    mask = swe_processor.opticalMask()
    swes_arr[n] = mask

  print(f'\n{swes_arr.shape}')
  return swes_arr

def mean_index(batch, threshold):
  index_means = np.array([], dtype = np.float32)
  for img in batch:
    mask = (img >= threshold)
    index = np.zeros_like(img)
    index[mask] = img[mask]
    index_means = np.append(index_means, np.mean(index))

  return index_means


def yearly_means(water_means, num_years):
  splits = np.array_split(water_means, num_years)
  yearly_means = np.array([], dtype= float)

  for split in splits:
    mean = np.mean(split)
    yearly_means = np.append(yearly_means, mean)
  
  return yearly_means


def yearly_medians(water_means, num_years):
  splits = np.array_split(water_means, num_years)
  yearly_medians = np.array([], dtype= float)

  for split in splits:
    median = np.median(split)
    yearly_medians = np.append(yearly_medians, median)
  
  return yearly_medians




#########################################################

class slicer():
  def __init__(self, y_start, y_end, x_start, x_end):
    self.y_start = y_start
    self.y_end = y_end
    self.x_start = x_start
    self.x_end = x_end
    self.bounds = np.s_[y_start:y_end, x_start: x_end]
  
  def focus (self, batch):
    n = len(batch)
    h = self.y_end - self.y_start
    w = self.x_end - self.x_start
    water_arr = np.empty((n, h, w))

    for n, img in enumerate(batch):
      water_arr[n] = img[self.bounds]
  
    return water_arr


#########################################################

class get_indexes():

    image = np.zeros((10,10,6))


    def __init__(self, blue_indx = 0, green_indx = 1, red_indx = 2, nir_indx = 3, swir_indx = 4):
        
        self.blue_indx = blue_indx
        self.green_indx = green_indx
        self.red_indx = red_indx
        self.nir_indx = nir_indx
        self.swir_indx = swir_indx

    def color(self):
        img = self.image[...,[self.red_indx, self.green_indx, self.blue_indx]]
        return (img - np.min(img)) / (np.max(img) - np.min(img))

    def mndwi(self):
        self.green = self.image[..., self.green_indx]
        self.swir = self.image [..., self.swir_indx]
        mndwi = (self.green - self.swir) / (self.green + self.swir)
        return mndwi

    def ndwi(self):
        self.green = self.image[..., self.green_indx]
        self.nir = self.image [..., self.nir_indx]
        ndwi = (self.green - self.nir) / (self.green + self.nir)
        return ndwi

    def ndvi(self):
        self.nir = self.image [..., self.nir_indx]
        self.red = self.image[..., self.red_indx]
        ndvi = (self.nir - self.red) / (self.nir + self.red)
        return ndvi


    def ndbi(self):
        self.swir = self.image [..., self.swir_indx]
        self.nir = self.image [..., self.nir_indx]
        ndbi = (self.swir - self.nir) / (self.swir + self.nir)
        return ndbi

    def nbi(self):
        self.red = self.image[..., self.red_indx]
        self.swir = self.image [..., self.swir_indx]
        self.nir = self.image [..., self.nir_indx]
        nbi = (self.red * self.swir) / (self.nir)
        return nbi