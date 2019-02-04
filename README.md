# Map
This module serves as a Basemap-like wrapper for Cartopy.

## Installation
```
git clone https://github.com/tb1516/Map
cd Map
python setup.py install
```

## Dependencies
This module requires Python 3.6 or newer, MetPy 0.10 or newer, Cartopy and Matplotlib to work.

## Usage
The purpose of this module is to provide usability similar to that of Basemap for plotting with Cartopy. For example, creating a PlateCarree projection can be done as follows, by creating an instance of a Map object:

```python
from Map import Map
m = Map(projection='PlateCarree',central_longitude=0.0,res='h')
```

The 'res' argument provides a default resolution for plotting geographic and political boundaries, using Cartopy's available resolutions:
Low: 'l' or '110m'
Moderate: 'm' or '50m'
High: 'h' or '10m'

The next step is to create a figure and axes instance. The projection is stored as an attribute of the Map object, so it can be retrieved via "m.proj":

```python
plt.figure(figsize=(14,9))
ax = plt.axes(projection=m.proj)
```

Geography can then be drawn similarly to Basemap's functionality. Note that if you want to use a different resolution for any of these than that specified for the default, it can be added as an argument to each of these functions (e.g., "m.drawcoastlines(res='m')).

```python
m.drawcoastlines(linewidth=1.0)
m.drawcountries(linewidth=1.0)
m.drawstates(linewidth=0.5,color='gray')
```

Counties are also available, but since Cartopy doesn't have a county shapefile, this function makes use of MetPy's county shapefiles.

```python
m.drawcounties(linewidth=0.1,alpha=0.5)
```

Filling land, lakes and oceans is also available:

```python
m.fillcontinents(zorder=0)
m.filloceans(zorder=0,res='l')
m.filllakes(zorder=0)
```

There are also additional functions for contour, contourf, colorbar, barbs and quiver that have similar functionality to
that of Basemap as well. For instance, if there is a dataset in lat/lon coordinates, the following functions will assume a
default PlateCarree() projection (unless a different data projection is passed as an argument), and the colorbar will be
resized to the same height or width of the main axis.

```python
cs = m.contourf(lon,lat,data)
m.colorbar(cs)
```
