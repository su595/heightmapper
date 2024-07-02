# heightmapper

This program creates custom heightmaps. It is not very practical, because it uses an unreliable API to get the elevation data. It is rather meant as a programming exercise.

## Usage

The main function `make_heightmap()` takes 4 arguments:
- `ul_corner`: coordinates of upper-left corner of the heightmap rectangle
- `lr_corner`: coordinates of lower-right corner
- `scale`: heightmap scale in meters per pixel
- `path` (optional): the path where the resulting heightmap will be saved. If omitted, the heightmap will only be displayed
It will display and optionally save a heightmap with the specified parameters.

The scale is limited by the source data to about 100 meters per pixel

## Examples
I pre-defined some coordinate sets for testing. Below is a Mt. Fuji heightmap at a scale of 200 meters per pixel.

![富士山](/sample1.png)

This is Fukuoka city at a scale of 300 meters per pixel.

![福岡市](/sample2.png)
