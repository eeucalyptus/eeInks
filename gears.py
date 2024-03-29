import inkex
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
        inkex.Effect.__init__(self)
        
        # Parse parameters from GUI
        self.arg_parser.add_argument(
            '-n', '--n', action = 'store',
            type = int, dest = 'n', default = 32,
            help = 'Number of teeth')
        self.arg_parser.add_argument(
            '-w', '--width', action = 'store',
            type = float, dest = 'width', default = 4,
            help = 'Width per tooth')
        self.arg_parser.add_argument(
            '-d', '--halfdepth', action = 'store',
            type = float, dest = 'halfdepth', default = 1,
            help = 'Half-depth')
        self.arg_parser.add_argument(
            '-s', '--slope', action = 'store',
            type = float, dest = 'slope', default = 1,
            help = 'Width of slope')

    def effect(self):
        # Get gear parameters from options
        n = self.options.n
        tooth_width = self.options.width
        halfdepth = self.options.halfdepth
        slope = self.options.slope

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Create a new layer.
        layer = svg.add(inkex.elements.Group.new('g', is_layer=True))
        layer.set(inkex.addNS('label', 'inkscape'), 'gear layer')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        
        my_shape = inkex.elements.PathElement()
        points = generate_teeth(tooth_width = tooth_width, slope_width = slope, halfdepth = halfdepth, n_teeth = n)
        
        svg_pts = " ".join([(lambda x,y: "{:0.3f},{:1.3f}".format(x, y))(x, y) for x,y in points])
        
        my_shape.path = "M " + svg_pts + " Z"

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

        layer.append(my_shape)  
        
# Execute effect
effect = GearGeneratorEffect()
effect.run()
