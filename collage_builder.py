

def get_smallest_height(imgs):
    smallest_height = -1
    for img in imgs:
        if smallest_height == -1 or img['height'] < smallest_height:
            smallest_height = img['height']
    return smallest_height


def get_smallest_width(imgs):
    smallest_width = -1
    for img in imgs:
        if smallest_width == -1 or img['width'] < smallest_width:
            smallest_width = img['width']
    return smallest_width


def build_collage(imgs):

    # the final result this is building
    bounds = []

    # add the first one
    item = imgs[0].copy()
    item['x'] = 0
    item['y'] = 0
    bounds.append(item)

    i = 1
    while len(bounds) < len(imgs):
        item = imgs[i].copy()
        
        # take height of most recently added, see if anything can fit to the right

        # take width of most recently added, see if anything can fit to the bottom

        # if still nothing, add along top or along left, whichever is shorter

        # after adding clean up and resize

        i += 1

    return bounds

if __name__ == '__main__':
    
    imgs = [
        {'width': 50, 'height': 60, 'id': 1},
        {'width': 100, 'height': 60, 'id': 2},
        {'width': 50, 'height': 50, 'id': 3},
        {'width': 20, 'height': 60, 'id': 4},
        {'width': 30, 'height': 40, 'id': 5}
    ]
    
    final_bounds = build_collage(imgs)

    print('-------- Final results ---------')
    for bound in final_bounds:
        print(bound)
