import json

class Box:
    '''
    Class to create objects of detected boxes.
    '''

    def __init__(self,(cx,cy),corners,colour,orientation):
        self.centroid = (cx,cy)
        self.corners = corners
        self.colour = colour
        self.orientation = orientation

    def getDetails(self):
        detail = {}
        detail['centroid'] = self.centroid
        detail['colour'] = self.colour
        detail_json = json.dumps(detail)
        return detail_json



def main():
    b = Box((1,2),[(0,1),(0,3),(2,1),(2,3)],'red')
    print(b.getDetails())

if __name__ == '__main__':
    main()
