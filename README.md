# heightmapper

This program creates custom heightmaps.

## Usage

The main function `make_heightmap()` takes 4 arguments:
- `ul_corner`: coordinates of upper-left corner of the heightmap rectangle
- `lr_corner`: coordinates of lower-right corner
- `scale`: heightmap scale in meters per pixel
- `path` (optional): the path where the resulting heightmap will be saved. If omitted, the heightmap will only be displayed
It will display and optionally save a heightmap with the specified parameters.

The scale is limited by the source data to about 100 meters per pixel

## Sample heightmap
I included two coordinate sets of Mt. Fuji and the Dreisam area for reference. Below is a Mt. Fuji heightmap at a scale of 200 meters per pixel.

![富士山](/sample.png)


This is a (arguably worse) replacement for the website terrain.party which no longer works :'(