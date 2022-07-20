# DyingRivers-ESA
## INTRODUCTION
The **Space Hubs Network** and the **European Space Agency (ESA)** organized an open challenge; "AI4EARTH" to utilize earth observation data in analyzing the human impact on earth. This project herein, uses data from mulitple satellite missions to examine the state of one of the oldest rivers on the planet; the Euphrates.

Walkthroughs:<br>1. Sentinel Hub data acquisition<br>
   <a href="https://colab.research.google.com/drive/1YxAxz_6iASgiZ2D-VxeIWBKZclORNwkX?authuser=1" target="_blank">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a><br>
2. Remote sensing indicies analysis<br>
   <a href="https://colab.research.google.com/drive/1aFctzWSIeyyxmMxOvfsDx7vQgxM8NtJv?authuser=1" target="_blank">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a><br>
3. Output statistics<br>
   <a href="https://colab.research.google.com/drive/1IFs-qtVHmP5ZnkreJRF1D5ZGYdXuI-Jx?authuser=1" target="_blank">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a><br>


## PROBLEM STATMENT
The [Euphrates river](http://waterinventory.org/surface_water/euphrates-river-basin) is one of the most ancient rivers on earth. Recently, various [reports](https://www.france24.com/en/live-news/20210830-desert-drying-euphrates-threatens-disaster-in-syria) show a significant decline in downstream waterflow, accompanied by a general deterioration in the basin. Referring to the streamgage records isn't a viable option due to long gaps in the gaging data. 

A viable solution is to resort to earth observation (EO) data to deduce a metric; analogous to river streamgage in its role of describing the state of the river's body and its basin across time. To this end, a set of remote sensing (RS) indicies could be calculated for a given river section. The closest RS index that would hold information about a water body is the Normalized Difference Water Index (mNDWI) [(Xu, 2006)](https://doi.org/10.1080/01431160600589179).

### ROI: Hindiya Barrage - IRAQ
The selected region of interest (ROI) was the **“Hindiya Barrage”** (Latitude 32° 43′ 01″ N, Longitude 44° 16′ 01″ E) along the Euphrates river in Iraq. for which the following indices were calculated:
1. The Normalized Difference Water Index (mNDWI).<br>
2. The Normalized Difference Vegetation Index (NDVI). <br>
3. The Normalized Built-up Index (NBI).<br>

<p align= 'center'>
    <img src="./plots/HindiyaBarrage_Landsat-4_SWIR.png" alt="HindiyaBarrage" width="500"><br>
    <i>Hindiya Barrage region-Landsat-4-TM: SWIR Band</i>
</p>



## DATA ACQUISITION: SENTINEL API
The data was composed of multi-spectral satellite imagery. The data was acquired through **[Sentinel Hub](https://www.sentinel-hub.com/) cloud API**. The imagery was obtained from 3 different satellite missions **(landsat 4-5, Landsat 8, sentinel 2)** to cover the time span from 1983 to 2021, acquiring 1 image per month. This amounts to 37 years at 1 month temporal resolution.

1. LANDSAT 4/5 TM: 1984 - Dec. 21, 2012 <BR>
Collection 2 Level 1 Data
2. LANDSAT 8: Feb 2013 - 31 dec 2015<BR>
Collection Landsat 8 L1
3. SENTINEL 2: Jan 2016 - 31 Sept 2021<BR>
Collection: sentinel-2-l1c

<p align= 'center'>
    <img src="./plots/Landsat_4_5.png" alt="HindiyaBarrage" width="750"><br>
    <i>Hindiya barrage: Landsat 4 & 5 missions</i><br>
</p>

<p align= 'center'>
    <img src="./plots/Sent_RGB.png" alt="HindiyaBarrage" width="350">
    <img src="./plots/water-extent.png" alt="HindiyaBarrage" width="360"><br>
    <i><b>Left:</b> Sentinel-2 RGB composite</i>
    <i><b>Right:</b> River Surface Water Extent (SWE)</i><br>
</p>

## REMOTE SENSING INDICIES
All imagery ran through a simple preprocessing pipline to extract the ROI square boundary and to mean center the image.<br>
*image_centered = image - min(image) / ((max(image) - min(image))*

Using the mean-centered image above the following remote sensing indicies were calculated:<br>

1. The Normalized Difference Water Index (mNDWI)<br>
   *mNDWI = (Green - SWIR) / (Green + SWIR)*
2. The Normalized Difference Vegetation Index (NDVI) <br>
*NDVI = (NIR - Red) / (NIR + Red)*

3. The Normalized Built-up Index (NBI)<br>
*NBI = (Red * SWIR) / NIR* <br>

*where NIR is near infra-red and SWIR is Short wave infra-red of the electromagnetic spectrum*.

<p align= 'center'>
    <img src="./plots/mNDWI.png" alt="mNDWI" width="800"><br>
    <i>Normalized Difference Water Index (mNDWI)</i><br>
    <i>1 month temporal resolution</i><br>
</p>

## RESULTS
The analysis was summarized into an infograph that showed the trend of the mNDWI over 37 years with at a 1 month resolution.

<p align= 'center'>
    <img src="./plots/water_037.png" alt="HindiyaBarrage" width="750"><br>
    <i>Normalized Difference Water Index (mNDWI)</i><br>
    <i>1 month temporal resolution</i><br>
</p>.

### **OUTPUT INFOGRAPH:** Play the video below.

[![Watch the video](./plots/play.png)](https://drive.google.com/file/d/11LjTLeMFhUQi4eDKy_k9dOVca1ueQh_d/view?usp=sharing)
