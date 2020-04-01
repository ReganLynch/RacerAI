
def get_left_most_point(unsorted_points):
    lm = (2000, 0)
    for pt in unsorted_points:
        if pt[0] < lm[0]:
            lm = pt
    return lm

def get_right_most_point(unsorted_points):
    rm = (0, 0)
    for pt in unsorted_points:
        if pt[0] > rm[0]:
            rm = pt
    return rm

def get_points_above_and_below_midsection(lm_point, rm_point, unsorted_points):
    points_above = []
    points_below = []
    print('LEFT MOST', lm)
    print('RIGHT MOST', rm)
    for curr_point in unsorted_points:
        v1 = (rm_point[0]-lm_point[0], rm_point[1]-lm_point[1])
        v2 = (rm_point[0]-curr_point[0], rm_point[1]-curr_point[1])
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            print('above?', curr_point)
            print 'on one side'
        elif xp < 0:
            print 'on the other'
        else:
            print 'on the same line!'
    return points_above, points_below

def get_min_shape_path(unsorted_points):
    #get lm
    #get rm
    #get all points above line (lm -> rm) (non-inclusive)
    #get all points below (lm -> rm) (non-inclusive)
    #sort all above by x (small to large)
    #sort all below by x (large to small)
    #return lm, all above (sorted), rm, all below (sorted)
    all_pts = unsorted_points.copy()
    lm = get_left_most_point(all_pts)
    rm = get_right_most_point(all_pts)
    all_pts.remove(lm)
    all_pts.remove(rm)
    pts_above, pts_below = get_points_above_and_below_midsection(lm, rm, all_pts)


    return 1
