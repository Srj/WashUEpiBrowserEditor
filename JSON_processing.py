#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
import copy
import sys


def main():
    """
    Main function to process the JSON file and convert it into a DataFrame.
    """
    # get filname from command line argument
    if len(sys.argv) ==3 :
        filetype = sys.argv[1]
        filename = sys.argv[2]

    else:
        sys.exit("Usage: python JSON_processing.py <filetype> <filename>")


    if filetype == 'json':
        with open(filename, mode="r", encoding="utf-8") as fp:
            obj = json.load(fp)
        browser = WashUEpiBrowser(obj)
        browser.get_dataframe().to_excel(f"{filename.split('.')[0]}.xlsx", index = False)
        print("Excel File generated")

    elif filetype == 'xlsx':
        df = pd.read_excel(filename, index_col = None).fillna('None')
        t = browser_df_to_json(df)
        with open(f"{filename.split('.')[0]}.json", "w") as fp:
            json.dump(t,fp)
        
        print("Datahub JSON file generated")

    else:
        sys.exit("Invalid filetype. Please use 'json' or 'xlsx'.")







class WashUEpiBrowserTrack:
    """
    A class to represent and manage the configuration of a WashU Epigenome Browser track.

    This version includes robust error handling with try-except blocks in all getter methods
    to gracefully handle cases where keys may be missing from the underlying dictionary.
    """

    def __init__(self, data):
        """
        Initializes the WashUEpiBrowserTrack object with data from a dictionary.

        Args:
            data (dict): A dictionary containing the track configuration.
        """
        self.data = copy.deepcopy(data)

    # ------------------ Getter Methods with Error Handling ------------------

    def get_name(self):
        """Returns the name of the track, or 'None' if the key is missing."""
        try:
            return self.data['name']
        except KeyError:
            return 'None'

    def get_type(self):
        """Returns the type of the track, or 'None' if the key is missing."""
        try:
            return self.data['type']
        except KeyError:
            return 'None'

    def get_label(self):
        """Returns the label of the track, or 'None' if the key is missing."""
        try:
            return self.data['label']
        except KeyError:
            return 'None'

    def get_options_label(self):
        """Returns the options label, or 'None' if the key is missing."""
        try:
            return self.data['options']['label']
        except (KeyError, TypeError):
            return 'None'

    def get_options_color(self):
        """Returns the options color, or 'None' if the key is missing."""
        try:
            return self.data['options']['color']
        except (KeyError, TypeError):
            return 'None'

    def get_options_bgColor(self):
        """Returns the options background color, or 'None' if the key is missing."""
        try:
            return self.data['options']['backgroundColor']
        except (KeyError, TypeError):
            return 'None'

    def get_options_height(self):
        """Returns the options height, or 'None' if the key is missing."""
        try:
            return self.data['options']['height']
        except (KeyError, TypeError):
            return 'None'

    def get_options_yScale(self):
        """Returns the options Y scale, or 'None' if the key is missing."""
        try:
            return self.data['options']['yScale']
        except (KeyError, TypeError):
            return 'None'

    def get_options_yMax(self):
        """Returns the options Y max value, or 'None' if the key is missing."""
        try:
            return self.data['options']['yMax']
        except (KeyError, TypeError):
            return 'None'

    def get_options_group(self):
        """Returns the options group, or 'None' if the key is missing."""
        try:
            return self.data['options']['group']
        except (KeyError, TypeError):
            return 'None'

    def get_url(self):
        """Returns the URL of the track, or 'None' if the key is missing."""
        try:
            return self.data['url']
        except KeyError:
            return 'None'

    def get_metadata(self):
        """Returns the metadata dictionary, or 'None' if the key is missing."""
        try:
            return self.data['metadata']
        except KeyError:
            return 'None'


class WashUEpiBrowser:
    def __init__(self, data_json):
        """
        Initializes the WashUEpiBrowserTrack object with data from a dictionary.

        Args:
            data (dict): A dictionary containing the track configuration.
        """
        self.data_json = copy.deepcopy(data_json)
        self.df = pd.DataFrame()


    def _process_track(self, track):

        data_dict = {
            'name': [track.get_name()],
            'type': [track.get_type()],
            'label': [track.get_label()],
            'options_label': [track.get_options_label()],
            'options_color': [track.get_options_color()],
            'options_bgColor': [track.get_options_bgColor()],
            'options_height': [track.get_options_height()],
            'options_yScale': [track.get_options_yScale()],
            'options_yMax': [track.get_options_yMax()],
            'options_group': [track.get_options_group()],
            'url': [track.get_url()],
        }
        metadata = track.get_metadata()
        metadata_dict = {}
        for i,j in metadata.items():
            if isinstance(j,str):
                metadata_dict["metadata." + i + ".Name"] = j
                metadata_dict["metadata." + i + ".Color"] = 'None'
            elif isinstance(j,dict):
                try:
                    metadata_dict["metadata." + i + ".Name"] = j['name']
                    metadata_dict["metadata." + i + ".Color"] = j['color']
                except (KeyError, TypeError):
                    metadata_dict["metadata." + i + ".Name"] = 'Error'
                    metadata_dict["metadata." + i + ".Color"] = 'Error'
            else:
                raise 'Metadata Format Not Recognized'


        return {**data_dict, **metadata_dict}


    def get_dataframe(self):

        self.df = pd.DataFrame()
        for x in self.data_json:
            self.df = pd.concat([self.df, pd.DataFrame(self._process_track(WashUEpiBrowserTrack(x)))], ignore_index = True)

        return self.df.fillna('None')                         



def create_track(track_dict):
    json_obj = {}
    json_obj['name'] = track_dict['name']
    json_obj['type'] = track_dict['type']
    json_obj['label'] = track_dict['label']
    json_obj['url'] =  track_dict['url']

    json_obj['options'] = {} 

    if track_dict["options_label"] != 'None':
        json_obj['options']['label'] = track_dict["options_label"]

    if track_dict["options_color"] != 'None':
        json_obj['options']['color'] = track_dict["options_color"]
    if track_dict["options_bgColor"] != 'None': 
        json_obj['options']['bgColor'] = track_dict["options_bgColor"]
    if  track_dict["options_height"] != 'None':
        json_obj['options']['height'] = track_dict["options_height"]
    if track_dict["options_yScale"] != 'None':
        json_obj['options']['yScale'] = track_dict["options_yScale"]
    if track_dict["options_yMax"] != 'None':
        json_obj['options']['yMax'] = track_dict["options_yMax"]
    if track_dict["options_group"] != 'None':
        json_obj['options']['group'] = track_dict["options_group"]


    #process metadata
    json_obj["metadata"] = {}
    for k, v in track_dict.items():
        if k.startswith('metadata.'):
            if v != "None":

                _ , k , attr_ = k.split('.')
                if k not in json_obj["metadata"].keys():
                    json_obj["metadata"][str.lower(k)] = {}

                json_obj["metadata"][str.lower(k)][str.lower(attr_)] = v


    for k, v in json_obj["metadata"].items():
        if len(v) == 1:
            json_obj["metadata"][k] = json_obj["metadata"][k]['name']


    extras = {'isSelected': False,
                 'fileObj': '',
                 'files': [],
                 'tracks': [],
                 'querygenome': '',
                 'isText': False,
                 'textConfig': {},
                 'apiConfig': {},
                 'queryEndpoint': {},
                 'datahub': 'Custom hub',
                 'selectedTabIndex': 0,
                 'trackAdded': False,
                 'urlError': ''}
    return {**json_obj, **extras}




def browser_df_to_json(df):
    json_obj = []
    for _, row in df.iterrows():
        json_obj.append(create_track(row.to_dict()))
    return json_obj



if __name__ == "__main__":
    main()








