#!/usr/bin/python3

import sys
import os
import argparse
import imghdr
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

IMAGE_TYPES = ["jpeg"]
DATE_TIME_ORIGINAL_TAG = "DateTimeOriginal"
PREFIX_FORMAT = "%Y-%m-%d_%H-%M"
AVAILABLE_TAGS = [
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
]

def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description="show exif values of jpegs from given directory, batch rename or group up by DateTimeOriginal")
    parser.add_argument("directory", help="Path to a pictures directory")
    parser.add_argument("--group", "-g",
                        dest="group_by",
                        action="store",
                        nargs="?",
                        const=1,
                        help="move items into directories by Y(years), M(months), D(days)",
                        choices=["Y","M","D"])
    parser.add_argument("--rename", "-r",
                        dest="is_rename",
                        action="store_true",
                        help="add YYYY-MM-DD_HH-MM-SS_ at the beginning of the item name")
    parser.add_argument("--tags",
                        dest="tags",
                        action="store",
                        default=[],
                        nargs = "*",
                        help="define a list of exif tags to be printed",
                        choices=AVAILABLE_TAGS)
    parser.add_argument("--all", "-a",
                        dest="is_all_tags",
                        action="store_true",
                        help="print all available tags")
    return parser

def get_exif_fields(image, fields):
    """Returns a dictionary with given tags from the exif data of a PIL Image file"""

    exif_decoded = {}
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded in fields or decoded == DATE_TIME_ORIGINAL_TAG:
                exif_decoded[decoded] = value
    return exif_decoded

def get_date_object_from_exif_field(date_time_exif):
    """Returns data object parsed from exif datetime field"""

    exif_date_format = "%Y:%m:%d %H:%M:%S"
    return datetime.strptime(date_time_exif, exif_date_format)

def get_item_name_prefix(date_object, prefix_format = PREFIX_FORMAT):
    """Returns a item prefix as formatted date string"""

    return date_object.strftime(prefix_format)

def rename_item(item, directory, item_name_prefix):
    """Adds a given prefix to the beginning of the picture name"""

    new_item_name = "%s_%s" % (item_name_prefix, item)
    item_path = os.path.join(directory, item)

    #check if already renamed
    if item[0:len(item_name_prefix)] == item_name_prefix:
        return False
    else:
        os.rename(item_path, os.path.join(directory, new_item_name))
    return new_item_name

def get_group_by_list(group_by, item_year, item_month, item_day):
    """Maps short group by flags, returns group-by attribute of a given file """
    return {
        "Y": item_year,
        "M": item_month,
        "D": item_day
    }.get(group_by, item_year)

def group_item(item, directory, group_by_attr):
    item_path = os.path.join(directory, item)
    group_dir = os.path.join(directory, group_by_attr)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)
    os.rename(item_path, os.path.join(group_dir, item))
    return True

def print_item_exif_list(item_title, exif_data, tags):
    """Prints exif tags of the picture"""

    print(item_title)
    for field in tags:
        if (field in exif_data):
            print("%s: %s" % (field, exif_data[field]))
    print("---------------------------")

def print_skipped(folder_counter, item_hidden_counter, item_skipped_counter):
    """Prints skipped counters"""

    print("")
    print("Skipped hidden files: %s" % item_hidden_counter)
    print("Skipped folders:      %s" % folder_counter)
    print("Skipped files:        %s" % item_skipped_counter)

def print_processed(item_counter, item_renamed_counter, item_grouped_counter):
    """Prints processed counters"""

    print("")
    print("Processed: %s" % item_counter)
    print("Renamed:   %s" % item_renamed_counter)
    print("Grouped:   %s" % item_grouped_counter)

def print_groups(years, months, days):
    """Prints groups"""

    if len(years) + len(months) + len(days) > 0:
        print("")
        print("Years:  %s" % years)
        print("Months: %s" % months)
        print("Days:   %s" % days)
        print("")

def process_folder(parsed_args):
    """Main cycle, iterates on files of the given folder"""
    
    #args
    directory = parsed_args.directory
    tags = parsed_args.tags
    is_rename = parsed_args.is_rename
    is_all_tags = parsed_args.is_all_tags
    group_by = parsed_args.group_by

    #counters
    item_counter = 0
    item_skipped_counter = 0
    folder_counter = 0
    item_hidden_counter = 0
    item_renamed_counter = 0
    item_grouped_counter = 0

    #groups
    years = []
    months = []
    days = []

    if not os.path.isdir(directory):
        print("Invalid directory: \"%s\"" % directory)
        return
    items = os.listdir(directory)
    items_amount = len(items)
    print("\nFound %s files in `%s`" % (items_amount, directory))
    if not items_amount:
        print("Nothing to process")
        return

    print("Valid pictures:\n")

    for item in items:
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            folder_counter += 1
            continue

        if item.startswith("."):
            item_hidden_counter += 1
            continue

        if not imghdr.what(item_path) in IMAGE_TYPES:
            item_skipped_counter += 1
            continue

        valid_image = Image.open(item_path)

        if (is_all_tags):
            tags = AVAILABLE_TAGS

        exif_data = get_exif_fields(valid_image, tags)
        item_title = "%s. \"%s\"" % (item_counter, item)
        if DATE_TIME_ORIGINAL_TAG not in exif_data:
            item_skipped_counter += 1
            continue

        item_counter += 1
        date_object = get_date_object_from_exif_field(exif_data[DATE_TIME_ORIGINAL_TAG])

        if (is_rename):
            item_name_prefix = get_item_name_prefix(date_object)
            new_item_name = rename_item(item, directory, item_name_prefix)
            if new_item_name:
                item = new_item_name
                item_renamed_counter += 1
                item_title += " => \"%s\"" % new_item_name

        print_item_exif_list(item_title, exif_data, tags)

        item_year = date_object.strftime("%Y")
        item_month = date_object.strftime("%Y-%m")
        item_day = date_object.strftime("%Y-%m-%d")

        if (item_year not in years):
            years.append(item_year)

        if (item_month not in months):
            months.append(item_month)

        if (item_day not in days):
            days.append(item_day)

        if (group_by):
            group_by_item = get_group_by_list(group_by, item_year, item_month, item_day)
            if group_item(item, directory, group_by_item):
                item_grouped_counter += 1

    #output
    print_skipped(folder_counter, item_hidden_counter, item_skipped_counter)
    print_processed(item_counter, item_renamed_counter, item_grouped_counter)
    print_groups(years, months, days)

if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    process_folder(parsed_args)
