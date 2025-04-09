import os
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as ipw
import traceback
import functools
import fnmatch

from glob import glob

from skimage.io import imread
from skimage.color import rgb2gray

from ipyfilechooser import FileChooser

from astropy.io import fits

from scipy.ndimage import median_filter

FILE_PATTERNS = ['*.png', '*.jpg', '*.npy', '*.fits']


class ImageInspectorMVC(ipw.VBox):
    """inspect images as obtained from ICON files.
    
    this class is based on code written by Giovanni Pizzi
    
    NOTE: NOT USED YET! FOR NOW WE JUST USE THE NOTEBOOK.
    """
    def __init__(self, **kwargs):
        """Initialize the image inspector."""
        super().__init__(**kwargs)
        self.rendered = False
            
    def render(self):
        """Render the image inspector."""
        
        # widget to choose navigate between folders
        folder_selector = FileChooser(
            os.path.realpath('.'),
            show_only_dirs=True,
            select_desc="Select folder",
            change_desc="Change folder",
        )
        
        folder_selector.layout = ipw.Layout(width='600px')  # Expand width of the folder selection
        folder_selector._select.layout = ipw.Layout(width="200px")

        # widget to choose the file
        file_selection_widget = ipw.Select(
            options=[],
            description="Files in folder:",
            style={'description_width': 'initial'},
            layout={'width': '400px'}
        )
        refresh_button = ipw.Button(
            description="Refresh file list", 
            style={'description_width': 'initial'})
        
        # normalization and filter checkboxes
        normalize_to_max_checkbox = ipw.Checkbox(value=False, description='Normalize to max')
        apply_median_filter_checkbox = ipw.Checkbox(value=False, description='Apply median 3x3 filter')
        logy_checkbox = ipw.Checkbox(value=False, description='Log y scale', layout=widgets.Layout(width=f'{3*72}px'))

        # sliders for contrast and range
        vmin_vmax_slider = ipw.FloatRangeSlider(value=[0, 1], min=0, max=1., step=0.001, description='Contrast:', layout=widgets.Layout(width=f'{7*72}px'))
        x_range_slider = ipw.IntRangeSlider(value=[0, 1], min=0, max=1, step=1, description='X Range:', layout=widgets.Layout(width=f'{8.5*72}px'))
        y_range_slider = ipw.IntRangeSlider(value=[0, 1], min=0, max=1, step=1, description='Y Range:', orientation='vertical', layout=widgets.Layout(height=f'{7*72}px'))
        
        # widget to show errors
        error_widget = ipw.HTML()
        
        self.rendered = True