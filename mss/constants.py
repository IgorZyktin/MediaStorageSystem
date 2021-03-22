# -*- coding: utf-8 -*-

"""Constant values.
"""

__version__ = '2021.03.21'

UNKNOWN = 'UNKNOWN'

# image sizes
RES_TINY = 'TINY'
RES_SMALL = 'SMALL'
RES_MEAN = 'MEAN'
RES_BIG = 'BIG'
RES_HUGE = 'HUGE'
IMAGE_SIZES = {RES_TINY, RES_SMALL, RES_MEAN, RES_BIG, RES_HUGE}

# threshold for sizes
THRESHOLD_TINY = 0.1
THRESHOLD_SMALL = 1.0
THRESHOLD_MEAN = 5.0
THRESHOLD_BIG = 10.0

# duration types
DUR_MOMENT = 'MOMENT'
DUR_SHORT = 'SHORT'
DUR_MEDIUM = 'MEDIUM'
DUR_LONG = 'LONG'
DURATION_TYPES = {DUR_MOMENT, DUR_SHORT, DUR_MEDIUM, DUR_LONG}

# threshold for durations
THRESHOLD_MOMENT = 5
THRESHOLD_SHORT = 300
THRESHOLD_MEDIUM = 2400

# media types
TYPE_IMAGE = 'IMAGE'
TYPE_GIF = 'GIF'
TYPE_VIDEO = 'VIDEO'
TYPE_AUDIO = 'AUDIO'
MEDIA_TYPES = {TYPE_IMAGE, TYPE_GIF, TYPE_VIDEO, TYPE_AUDIO}

# search flags
FLAG_DESC = 'DESC'
FLAG_DEMAND = 'DEMAND'
FLAGS = {FLAG_DESC, FLAG_DEMAND}

KEYWORDS = IMAGE_SIZES | DURATION_TYPES | MEDIA_TYPES | FLAGS

KW_AND = 'AND'
KW_OR = 'OR'
KW_NOT = 'NOT'
KW_INCLUDE = 'INCLUDE'
KW_EXCLUDE = 'EXCLUDE'
OPERATORS = {KW_AND, KW_OR, KW_NOT, KW_INCLUDE, KW_EXCLUDE}

START_MESSAGE = r"""
███╗   ███╗███████╗██████╗ ██╗ █████╗                          
████╗ ████║██╔════╝██╔══██╗██║██╔══██╗                         
██╔████╔██║█████╗  ██║  ██║██║███████║                         
██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║                         
██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║                         
╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝                         
                                                               
███████╗████████╗ ██████╗ ██████╗  █████╗  ██████╗ ███████╗    
██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝    
███████╗   ██║   ██║   ██║██████╔╝███████║██║  ███╗█████╗      
╚════██║   ██║   ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══╝      
███████║   ██║   ╚██████╔╝██║  ██║██║  ██║╚██████╔╝███████╗    
╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    
                                                               
███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗          
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║          
███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║          
╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║          
███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║          
╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝          
                                                                                   
##############################################################
                                     
"""

TERMINAL_WIDTH = 79
ALL_THEMES = 'all_themes'
NEVER_FIND_THIS = '?????????????'
THUMBNAIL_SIZE = (384, 384)
PREVIEW_SIZE = (1024, 1024)
