#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *
import simplestyle
import math

def generate_teeth(tooth_width = 4, slope_width = 1, halfdepth = 1, n_teeth = 32):
    # Derived gear constants
    land_width = (tooth_width - 2*slope_width) / 2
    circumfence = tooth_width*n_teeth
    middle_radius = circumfence/(2*math.pi)
    outer_radius = middle_radius+halfdepth
    inner_radius = middle_radius-halfdepth
    tooth_angle = (tooth_width / circumfence) * 2*math.pi 
    slope_angle = (slope_width/tooth_width) * tooth_angle
    land_angle = (tooth_angle - 2*slope_angle) / 2

    points = []

    for i in range(n_teeth):
        tooth_origin_angle = i*tooth_angle
        
        # inner land:
        angle = tooth_origin_angle + land_angle
        radius = inner_radius
        points.append((math.cos(angle)*radius, math.sin(angle)*radius))
        
        # rising slope
        angle = tooth_origin_angle + land_angle + slope_angle
        radius = outer_radius
        points.append((math.cos(angle)*radius, math.sin(angle)*radius))
        
        # outer land
        angle = tooth_origin_angle + 2*land_angle + slope_angle
        radius = outer_radius
        points.append((math.cos(angle)*radius, math.sin(angle)*radius))
        
        # falling slope
        angle = tooth_origin_angle + 2*land_angle + 2*slope_angle
        radius = inner_radius
        points.append((math.cos(angle)*radius, math.sin(angle)*radius))
    
    
    return points

class GearGeneratorEffect(inkex.Effect):
    """
    eeGearsGenerator 
    Creates new layer with a gear
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)
        
        # Define string option "--what" with "-w" shortcut and default value "World".
        self.OptionParser.add_option('-n', '--n', action = 'store',
          type = 'int', dest = 'n', default = 32,
          help = 'Number of teeth')
        self.OptionParser.add_option('-w', '--width', action = 'store',
          type = 'float', dest = 'width', default = 4,
          help = 'Width per tooth')
        self.OptionParser.add_option('-d', '--halfdepth', action = 'store',
          type = 'float', dest = 'halfdepth', default = 1,
          help = 'Half-depth')
        self.OptionParser.add_option('-s', '--slope', action = 'store',
          type = 'float', dest = 'slope', default = 1,
          help = 'Width of slope')

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts gear into SVG document.
        """
        # Get script's "--what" option value
        n = self.options.n
        tooth_width = self.options.width
        halfdepth = self.options.halfdepth
        slope = self.options.slope

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'gear layer')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        
        points = generate_teeth(tooth_width = tooth_width, slope_width = slope, halfdepth = halfdepth, n_teeth = n)
        
        svg_pts = " ".join([(lambda x,y: "{:0.3f},{:1.3f}".format(x, y))(x, y) for x,y in points])
        
        style = {   'stroke'        : 'none',
                'stroke-width'  : '1',
                'fill'          : '#000000'
            }

        attribs = {
                'style'     : simplestyle.formatStyle(style),
                'height'    : "10",
                'width'     : "20",
                'd'         : "M " + svg_pts + " Z",
            }
            
        path = inkex.etree.SubElement(layer, inkex.addNS('path','svg'), attribs )
        
# Create effect instance and apply it.
effect = GearGeneratorEffect()
effect.affect()