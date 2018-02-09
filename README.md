# pexif

Script to check exif data of given images.
Uses `DateTimeOriginal` tag to add date time to the image file name and can group photos by day, month or year taken.
It does not process subfolders and works only with jpeg files.
Useful to organise/clean up big folders with hundreds of photos, especially if files have wrong or broken created/modified date properties

## Usage:

* to see basic info about given folder:
```javascript
python3 pexif.py ./dir
```

* to see specific image exif tags:
```javascript
python3 pexif.py ./dir --tags Model Artist Orientation WhiteBalance Copyright
```

* to see all available image exif tags:
```javascript
python3 pexif.py ./dir --all
```

* to add date prefix to image file names:
```javascript
python3 pexif.py ./dir --rename
```

* to group image into folders (Y - by year, M - my month, D - by day):
```javascript
python3 pexif.py ./dir --group Y
```

Available tags:
```javascript
    "GPSInfo",
    "ResolutionUnit",
    "ExifOffset",
    "Make",
    "Model",
    "Artist",
    "Orientation",
    "DateTime",
    "YCbCrPositioning",
    "Copyright",
    "XResolution",
    "YResolution",
    "ExifVersion",
    "ComponentsConfiguration",
    "ShutterSpeedValue",
    "DateTimeOriginal",
    "DateTimeDigitized",
    "ApertureValue",
    "ExposureBiasValue",
    "MeteringMode",
    "UserComment",
    "Flash",
    "FocalLength",
    "ColorSpace",
    "ExifImageWidth",
    "ExifInteroperabilityOffset",
    "FocalPlaneXResolution",
    "FocalPlaneYResolution",
    "SubsecTime",
    "SubsecTimeOriginal",
    "SubsecTimeDigitized",
    "ExifImageHeight",
    "FocalPlaneResolutionUnit",
    "ExposureTime",
    "FNumber",
    "ExposureProgram",
    "CustomRendered",
    "ISOSpeedRatings",
    "ExposureMode",
    "FlashPixVersion",
    "WhiteBalance",
    "MakerNote",
    "SceneCaptureType"
```
