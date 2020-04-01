
#class to define a line, lines should keep track
#of the next line that they connect to
class point(object):

    def __init__(self, x, y, prev_point=None):
        self.prev_point = prev_point
        self.x = x
        self.y = y


#used for creating shapes from the lines of a course
#this is then used to draw road paths, and objects correctly
def create_shapes_from_lines(lines):
    lines_copy = lines.copy()
    shapes = []
    while len(lines_copy) > 0:
        curr_unsorted_pts = []
        start_line = lines_copy.pop(0)
        curr_unsorted_pts.append(point(start_line[1][0], start_line[1][1]))
        i = 0
        #go through all lines that havent been processed yet
        while i < len(lines_copy):
            curr_line = lines_copy[i]
            found_line = False
            #check if the current line connects to any of the lines in the current SHAPE
            for curr_pt in curr_unsorted_pts:
                if curr_pt.x == curr_line[0][0] and curr_pt.y == curr_line[0][1]:
                    found_line = True
                    curr_unsorted_pts.append(point(curr_line[1][0], curr_line[1][1], curr_pt))
                    lines_copy.remove(curr_line)
                    break
                if curr_pt.x == curr_line[1][0] and curr_pt.y == curr_line[1][1]:
                    found_line = True
                    curr_unsorted_pts.append(point(curr_line[0][0], curr_line[0][1], curr_pt))
                    lines_copy.remove(curr_line)
                    break
            if found_line:
                i = 0
            else:
                i += 1
        #sort points by who they are connected to
        sorted_pts = []
        pt = curr_unsorted_pts[-1]
        while pt != None:
            sorted_pts.append((pt.x, pt.y))
            pt = pt.prev_point
        #append the current shape to all shapes
        shapes.append(sorted_pts)
    return shapes

#sortes the shapes based on their areas
#0th index will have the largest area
def sort_shapes_by_area(shapes):
    areas = []
    for shape in shapes:
        numerator = 0
        i = 1
        for i in range(0, len(shape) - 1):
            curr_pt = shape[i]
            next_pt = shape[i+1]
            numerator += (curr_pt[0]*next_pt[1] - curr_pt[1]*next_pt[0])
        numerator += (shape[-1][0]*shape[0][1] - shape[0][1]*shape[-1][0])
        area = numerator / 2
        areas.append(abs(area))
    return areas
