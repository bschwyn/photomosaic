import os
from PIL import Image
import pickle
import time

class OriginalPhoto():

    def __init__(self, file):
        im = Image.open(file)
        self.width, self.height = im.size



class Photomosaic():

    def __init__(self, targetpicturefile, source_directory):
        self.pic_file = targetpicturefile
        self.mosaic_source_directory = source_directory

    def construct_mosaic(self, rows, cols, scale):
        im = Image.open(self.pic_file)
        gridbox_size = self.get_grid_size(rows, cols, im, scale)
        rgb_matrix = self.construct_average_color_grid( rows, cols, im)
        nearest_photos = self.get_photo_grid(gridbox_size, rows, cols, rgb_matrix, self.mosaic_source_directory)
        final_photos = self.stitch_photos(gridbox_size, nearest_photos)
        return final_photos

    def get_grid_size(self, rows, cols, image, scale):
        target_width, target_height = image.size
        grid_width = int(round(target_width*scale/cols))
        grid_height = int(round(target_height*scale/rows))
        return (grid_width, grid_height)

    def construct_average_color_grid(self,rows, cols, image): #tested
        #divide picture in rows and columns. Return a matrix of the same size, with the average rgb color of each
        #section of the grid
        w, h = image.size
        w = w//cols
        h = h//rows
        rgb_matrix = [[[0,0,0] for x in range(cols)] for y in range(rows)]
        for i in range(rows):
            for j in range(cols):
                x,y = j*w, i*h
                r,g,b = self.get_average_color(x,y, w, h, image)
                rgb_matrix[i][j] = [r,g,b]
        return rgb_matrix

    def get_colorfiles(self, source_pictures):
        if os.path.isfile('./averagecolors_to_pictures7.pickle'):
            with open('./averagecolors_to_pictures7.pickle', 'rb') as handle:
                color_files_list = pickle.loads(handle.read())
        else:
            color_files_list = self.construct_color_files_list(source_pictures)
        return color_files_list

    def get_photo_grid(self, gridbox_size, rows, cols, rgb_matrix, source_pictures):
        """given a matrix of colors, creates a matrix of photos where each photo has the nearest color average to the grid location.
        Also resizes photos"""

        w, h = gridbox_size
        nearest_photos = [[None for x in range(cols)] for y in range(rows)]
        color_files = self.get_colorfiles(source_pictures)
        print(len(color_files))

        for i in range(rows):
            for j in range(cols):
                r, g, b = rgb_matrix[i][j]
                photo = self.find_nearest_photo_L2norm(r, g, b, color_files)
                resized_nearest_photo = photo.resize((w,h))
                nearest_photos[i][j] = resized_nearest_photo
        return nearest_photos

    def construct_color_files_list(self, source_pictures):
        avg_colors_of_pictures = {}
        for root, subFolders, files in os.walk(source_pictures):
            for file in files:
                # if file is a picture
                # calculate rgb average
                # save rgb average and filename
                try:
                    with Image.open(root +"/" + file) as im:
                        w, h = im.size
                        r2, g2, b2 = self.get_average_color(0, 0, w, h, im)
                    avg_colors_of_pictures[(r2, g2, b2)] = root + "/" + file
                except IOError:
                    print('error', file)
        self.save_colors(avg_colors_of_pictures)
        return avg_colors_of_pictures

    def save_colors(self, avg_colors_of_pictures):
        with open('./averagecolors_to_pictures7.pickle', 'wb') as f:
            pickle.dump(avg_colors_of_pictures, f, protocol=pickle.HIGHEST_PROTOCOL)




    def find_nearest_photo_L2norm(self,r,g,b, colorlist):
        """calculates a distance between an rgb value and every rgb value in a list, then returns the file associated with
        the minimum distance rgb value"""
        mindist = 255**2 + 255**2 + 255**2
        minfile = None
        for (r2,g2,b2), file in colorlist.items():
            dist = (r2-r)**2 + (g2-g)**2 + (b2-b)**2
            if dist < mindist:
                mindist = dist
                minfile = file
        im = Image.open(minfile)

        print(minfile)
        return im


    def stitch_photos(self, gridbox_size, nearest_photos): #tested
        """ takes a matrix of smaller photos and pastes them into a new photo with their edges lined up, like a patchwork quilt"""
        #souce width and source height are the size of the photos

        width, height = gridbox_size

        rows = len(nearest_photos)
        cols = len(nearest_photos[0])
        im = Image.new("RGB", size=(width*cols, height*rows))
        for i in range(rows):
            for j in range(cols):
                source_photo = nearest_photos[i][j]
                #x,y are the upper left orner
                x,y = width*j, height*i
                im.paste(source_photo, box = (x,y))
                im.close()
        return im

    def get_average_color(self, x,y, w,h, image): #tested
        """returns a 3-tuple containing the RGB value of the average color of the given rectangle
        bounded by [x, x+w], and [y, y+h] """

        r,g,b = 0,0,0
        count = 0
        if image.mode != 'RGB':
            image = image.convert('RGB')
        for s in range(x, x + w):
            for t in range(y, y+h):
                pixl_r, pixl_g, pixl_b = image.getpixel((s,t))
                #else:
                r += pixl_r
                g += pixl_g
                b += pixl_b
                count +=1
        return (r//count, g//count, b//count)

def test_average_color_grid():
    rows = 2
    cols = 1

    im = Image.new('RGB',(2,4))
    im.putpixel(xy = (0,0), value = (0,0,0))
    im.putpixel(xy = (1,0), value = (100,0,0))
    im.putpixel(xy = (0,1), value = (0,200,20))
    im.putpixel(xy = (1,1), value = (100,200,20))
    im.putpixel(xy = (0,2), value = (20,0,200))
    im.putpixel(xy = (1,2), value = (20,100,0))
    im.putpixel(xy = (0,3), value = (0,100,0))
    im.putpixel(xy = (1,3), value = (0,0,200))

    expected = [[[50,100,10]],[[10,50,100]]]

    photomosaic = Photomosaic("/home/ben/Documents/AirBrush_20180306185448.jpg",'/home/ben/Documents/mosaic_test/')
    gridbox = photomosaic.get_grid_size(rows, cols, im, 1)
    actual = photomosaic.construct_average_color_grid(rows, cols,im)
    assert actual == expected

def test_stitch_photos():
    im1 = Image.new('RGB',(1,1))
    im1.putpixel(xy = (0,0), value=(0,0,0))
    im2 = Image.new('RGB', (1,1))
    im2.putpixel(xy = (0,0), value = (255, 0,0))
    im3 = Image.new('RGB', (1,1))
    im3.putpixel(xy = (0,0), value=(0,255,0))
    im4 = Image.new('RGB', (1,1))
    im4.putpixel(xy = (0,0), value=(0,0,255))

    nearest_photos = [[im1, im2], [im3, im4]]


    photomosaic = Photomosaic("/home/ben/Documents/AirBrush_20180306185448.jpg",'/home/ben/Documents/mosaic_test/')
    stitched_image = photomosaic.stitch_photos((1,1),nearest_photos)

    assert stitched_image.size ==(2,2)
    assert stitched_image.getpixel((0,0)) == (0,0,0)
    assert stitched_image.getpixel((1,0)) == (255,0,0)
    assert stitched_image.getpixel((0,1)) == (0,255,0)
    assert stitched_image.getpixel((1,1)) == (0,0,255)

def test_get_average_color():
    im = Image.new('RGB',(2,2))
    im.putpixel(xy = (0,0), value = (0,0,0))
    im.putpixel(xy = (1,0), value = (100,0,0))
    im.putpixel(xy = (0,1), value = (0,200,20))
    im.putpixel(xy = (1,1), value = (100,200,20))


    photomosaic = Photomosaic("/home/ben/Documents/AirBrush_20180306185448.jpg",'/home/ben/Documents/mosaic_test/')
    actual = photomosaic.get_average_color(0,0,2,2, im)
    expected = (50, 100, 10)
    assert actual == expected

def test_pickle():
    d = {5:3, "hello": "goodbye", 5:"twelve", "siz":333}
    with open('./pickletest', 'wb') as f:
        pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open('./pickletest','rb') as f:
        c = pickle.loads(f.read())
    assert d == c

def test_construct_color_files_list():

    source_pictures = '/home/ben/Pictures/'
    d = {}
    count = 0
    c2 = 0
    for root, dirs, files in os.walk(source_pictures):
        print('..........')
        for file in files:
            print(root + file)
            count +=1

            if os.path.isfile(root+ '/' + file):
                c2 +=1
            else:
                print('wrong', root + file)
        print('c2', c2)

    print(count)


#test_construct_color_files_list()
test_pickle()
test_get_average_color()
test_average_color_grid()
test_stitch_photos()
print('testspass')
#having even more test cases would have helped --- I didn't write ones for some of the other functions that seemed harder to pass

#usual /home/ben/Documents/AirBrush_20180306185448.jpg
def main():
    print('start')
    photomosaic = Photomosaic("/home/ben/Pictures/backup pics/1c17411e3b4343dbcc7206e41585ae6d-d5xkb9b.jpg",'/home/ben/Pictures/')
    x = photomosaic.construct_mosaic(90, 80, 5)
    x.save('/home/ben/Documents/aphotomosaic12.jpg')
    print('end')

if __name__ == "__main__":
    main()