from unittest import TestCase
from rectpack.geometry import Rectangle
import rectpack.skyline as skyline
import rectpack.guillotine as guillotine
import rectpack.maxrects as maxrects
import rectpack.packer as packer


class TestRectangleSort(TestCase):

    def test_sort_none(self):
        """Test list is returned a is"""
        a = [(3, 3), (3, 1), (3, 2), (1, 2), (2, 1)]
        ordered = packer.SORT_NONE(a)
        self.assertEqual(a, ordered)
            
        # Test empty list
        self.assertEqual(packer.SORT_NONE([]), [])

    def test_sort_area(self):
        """Test rectangles are sorted by descending area"""
        a = [(5, 5), (7, 7), (3, 4), (100, 1)]
        ordered = packer.SORT_AREA(a)
        self.assertEqual(ordered, [(100, 1), (7, 7), (5, 5), (3, 4)])
        
        # Test empty list
        self.assertEqual(packer.SORT_AREA([]), [])

    def test_sort_peri(self):
        """Test rectangles are sorted by perimeter"""
        a = [(5, 5), (7, 7), (3, 4), (40, 1)]
        ordered = packer.SORT_PERI(a)
        self.assertEqual(ordered, [(40, 1), (7, 7), (5, 5), (3, 4)])

        # Test empty list
        self.assertEqual(packer.SORT_PERI([]), [])

    def test_sort_diff(self):
        """Test rectangles are sorted by the difference in side lengths"""
        a = [(7, 1), (1, 9), (2, 11), (5, 1)]
        ordered = packer.SORT_DIFF(a)
        self.assertEqual(ordered, [(2, 11), (1, 9), (7, 1), (5, 1)])

        # Test empty list
        self.assertEqual(packer.SORT_DIFF([]), [])

    def test_sort_sside(self):
        """Test rectangles are sorted by short side descending"""
        a = [(2, 9), (7, 3), (4, 5), (11, 3)]
        ordered = packer.SORT_SSIDE(a)
        self.assertEqual(ordered, [(4, 5), (11, 3), (7, 3), (2, 9)])

        # Test empty list
        self.assertEqual(packer.SORT_SSIDE([]), [])

    def test_sort_lside(self):
        """Test rectangles are sorted by long side descending"""
        a = [(19, 5), (32, 5), (6, 19), (9, 11)]
        ordered = packer.SORT_LSIDE(a)
        self.assertEqual(ordered, [(32, 5), (6, 19), (19, 5), (9, 11)])

        # Test empty list
        self.assertEqual(packer.SORT_LSIDE([]), [])

    def test_sort_ratio(self):
        """Test rectangles are sorted by width/height descending"""
        a = [(12, 5), (15, 4), (4, 1), (1, 2)]
        ordered = packer.SORT_RATIO(a)
        self.assertEqual(ordered, [(4, 1), (15, 4), (12, 5), (1, 2)])

        # Test empty list
        self.assertEqual(packer.SORT_RATIO([]), [])



class TestPackerOnline(TestCase):
    
    def test_bin_iter(self):
        # check iter only loops over closed and open bins (in that order)
        p = packer.PackerOnlineBNF(rotation=False)
        p.add_bin(50, 55)
        p.add_bin(30, 30)
        p.add_bin(5, 5)
        p.add_bin(40, 40)

        # No bins to iterate over
        bins = list(iter(p))
        self.assertEqual(len(bins), 0)

        # One open bin to iterate
        p.add_rect(50, 50)
        bins = list(iter(p))
        self.assertEqual(len(bins), 1)

        # One closed and one open bin
        p.add_rect(29, 29)
        bins = list(iter(p))
        self.assertEqual(len(bins), 2)
        self.assertEqual(bins[0].width, 50) # Test closed bins are first

        # Two closed bins, one skipped bin, and an open bin
        p.add_rect(40, 40)
        bins = list(iter(p))
        self.assertEqual(len(bins), 3)

    def test_getitem(self):
        # check exception raised when bin doesn't exist
        p = packer.PackerOnlineBNF(rotation=False)
        p.add_bin(50, 55)
        p.add_bin(30, 30)
        p.add_bin(40, 40)
        with self.assertRaises(IndexError):
            p[0]

        # check with one open bin
        p.add_rect(50, 50)
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 50)
        self.assertEqual(p[0].height, 55)
        self.assertEqual(p[0], p[-1])
        with self.assertRaises(IndexError):
            p[1]
        with self.assertRaises(IndexError):
            p[-2]

        # one closed bin, one skiped, and one open bin
        p.add_rect(39, 39)
        self.assertEqual(p[0].width, 50)
        self.assertEqual(p[0].height, 55)
        self.assertEqual(p[1].width, 40)
        self.assertEqual(p[1].height, 40)
        self.assertEqual(p[-1], p[1])
        with self.assertRaises(IndexError):
            p[-4]
        with self.assertRaises(IndexError):
            p[2]

    def test_bin_order(self):
        # check bins are packed in the order they were added
        p = packer.PackerOnlineBNF(rotation=False)
        p.add_bin(45, 45)
        p.add_bin(30, 30)
        p.add_bin(40, 40)

        p.add_rect(20, 20)
        self.assertEqual(p[0].width, 45)
        self.assertEqual(p[0].height, 45)

        p.add_rect(29, 29)
        self.assertEqual(p[1].width, 30)
        self.assertEqual(p[1].height, 30)

        # check bins are added at the end of the queue, and used last
        p.add_bin(39, 39)
        p.add_rect(39, 39)
        self.assertEqual(p[2].width, 40)
        self.assertEqual(p[2].height, 40)

    def test_len(self):
        # check returns length of open+closed bins.
        p = packer.PackerOnlineBNF()
        p.add_bin(50, 50)
        p.add_bin(40, 40)
        p.add_bin(60, 60)
        self.assertEqual(len(p), 0)

        p.add_rect(40, 40)
        self.assertEqual(len(p), 1)

        p.add_rect(41, 41)
        self.assertEqual(len(p), 2)

        p.add_rect(30, 30)
        self.assertEqual(len(p), 3)

    def test_bin_count(self):
        # test adding several bins in one go using count
        p = packer.PackerOnlineBFF(rotation=False)

        p.add_bin(100, 100, count=3)
        p.add_rect(90, 90)
        p.add_rect(95, 95)
        p.add_rect(96, 96)
        p.add_rect(97, 97) # This one can't be packed
        
        self.assertEqual(len(p), 3)

        # test adding infinite bins
        p = packer.PackerOnlineBFF(rotation=False)
        p.add_bin(100, 100, count=float("inf"))

        p.add_rect(90, 90)
        p.add_rect(95, 95)
        p.add_rect(96, 96)
        p.add_rect(97, 97)
        p.add_rect(200, 200)

        self.assertEqual(len(p), 4)

        # check it is possible to pack into bins added after the infinite bin
        p = packer.PackerOnlineBFF(rotation=False)
        p.add_bin(5, 5, count=float("inf"))
        p.add_bin(100, 100, count=float("inf"))
        p.add_bin(202, 202, count=1)
        p.add_bin(200, 200, count=float("inf"))
        
        p.add_rect(30, 30)
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 100)
        self.assertEqual(p[0].width, 100)

        p.add_rect(4, 4) # Bin aready opened used before new one
        self.assertEqual(len(p), 1)

        p.add_rect(80, 80)
        self.assertEqual(len(p), 2)
        self.assertEqual(p[1].width, 100)
        self.assertEqual(p[1].height, 100)

        p.add_rect(180, 180)
        self.assertEqual(len(p), 3)
        self.assertEqual(p[2].width, 202)
        self.assertEqual(p[2].height, 202)

        p.add_rect(180, 180)
        self.assertEqual(len(p), 4)
        self.assertEqual(p[3].width, 200)
        self.assertEqual(p[3].height, 200)
      
        # Check rectangles were packed
        self.assertEqual(len(p.rect_list()), 5)
        
    def test_add_bin_extra_kwargs(self): 
        # Check add_bin kwargs don't shadow packer options
        p = packer.PackerOnlineBFF(rotation=False)
        p.add_bin(10, 100, count=3, rot=True, args='yes')
        p.add_rect(90, 9)
        self.assertEqual(len(p), 0)
        
        # Check with more than one bin
        p = packer.PackerOnlineBFF(rotation=True)
        p.add_bin(10, 100, rot=True, args='yes', count=3)
        p.add_rect(90, 9)
        p.add_rect(90, 9)
        p.add_rect(90, 9)
        self.assertEqual(len(p), 3)
        self.assertEqual(len(p[0]), 1)
        self.assertEqual(len(p[1]), 1) 
        self.assertEqual(len(p[2]), 1)

        # Custom Packing algorithm...
        class CustomAlgo(maxrects.MaxRectsBssf):
            def __init__(self, width, height, rot=True, *args, **kwargs):
                self.extra_kwargs = kwargs
                super().__init__(width=width, height=height, rot=rot,
                                    *args, **kwargs)

        p = packer.PackerOnlineBFF(pack_algo=CustomAlgo)
        p.add_bin(100, 100, name='yes', count=2)
        p.add_rect(90, 80)
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p[0]), 1)
        self.assertTrue('name' in p[0].extra_kwargs)
        self.assertFalse('count' in p[0].extra_kwargs)
        

class TestPackerOnlineBNF(TestCase):
 
    def test_bin_selection(self):
        # Check as soon as a rectangle fails to be packed into an open bin
        # the bin is closed, and it's packed into the next bin where it fits.
        p = packer.PackerOnlineBNF()
        p.add_bin(30, 30)
        p.add_bin(10, 10)
        p.add_bin(40, 40)

        # this rectangle fits into first bin
        p.add_rect(5, 5) 
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 30)

        # This rectangle doesn't fit into the open bin (first), so the bin
        # is closed and rectangle packed into next one where it fits.
        p.add_rect(29, 29)
        self.assertEqual(len(p), 2)
        self.assertEqual(p[1].width, 40)

        # Try to add a rectangle that would have fit into the first bin
        # but it is packed
        p.add_rect(10, 10)
        self.assertEqual(len(p), 2)
        last_rect = p.rect_list()[-1]
        pbin, x, y, w, h, rid = last_rect
        self.assertEqual(pbin, 1)


    def test_infinite_bin(self):
        # Test infinite bins are only tested once when a rectangle
        # doesn't fit
        p = packer.PackerOnlineBNF()
        p.add_bin(50, 50, count=50)
        p.add_bin(100, 100, count=float("inf"))

        p.add_rect(90, 90)
        self.assertEqual(len(p), 1)
        p.add_rect(95, 95)
        self.assertEqual(len(p), 2)

        # check other bins
        p.add_rect(40, 40)
        self.assertEqual(len(p), 3)
        self.assertEqual(p[2].width, 50)
        
        p.add_rect(45, 45)
        self.assertEqual(len(p), 4)
        self.assertEqual(p[3].width, 50)

    def test_rotation(self):
        p = packer.PackerOnlineBNF(rotation=False)
        p.add_bin(30, 10)
        p.add_bin(50, 10)
        p.add_rect(10, 30)

        # rectangle didnt't fit in any of the bins when rotations was disabled
        self.assertEqual(len(p.rect_list()), 0)

        # Check no bin was opened
        self.assertEqual(len(p), 0)

        # With rotation the rectangle is successfully packer
        p = packer.PackerOnlineBNF(rotation=True)
        p.add_bin(30, 10)
        p.add_bin(50, 10)
        p.add_rect(10, 30)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 30, 10, None))
        self.assertEqual(len(p), 1)



class TestPackerOnlineBFF(TestCase):
    
    def test_bin_selection(self):
        # check rectangle is packed into the first open bin where it fits,
        # if it can't be packed into any use the first available bin
        p = packer.PackerOnlineBFF(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)

        p.add_bin(20, 20, count=2)
        p.add_bin(100, 100)

        # Packed into second bin
        p.add_rect(90, 90)
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 100)

        # rectangles are packed into open bins whenever possible
        p.add_rect(10, 10)
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p.rect_list()), 2)

        p.add_rect(5, 5)
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p.rect_list()), 3)

        # rectangle doesn't fit, open new bin
        p.add_rect(15, 15)
        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 4)
    
        # if there are more than one possible bin select first one
        p.add_rect(5, 5)
        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 5)
        self.assertTrue((0, 10, 90, 5, 5, None) in p.rect_list())

    def test_count(self):
        # check only the first bin is evaluated when there are more than one
        p = packer.PackerOnlineBFF(rotation=False)
        p.add_bin(30, 30, count=10)
        p.add_bin(40, 40, count=float("inf"))
        p.add_bin(100, 100, count = 2)

        # packed into second bin, first bin left unopened
        p.add_rect(40, 40)
        self.assertEqual(len(p), 1) # check was packed
        self.assertEqual(p[0].width, 40)

        # first and second bins skipped
        p.add_rect(45, 45)
        self.assertEqual(len(p), 2)
        self.assertEqual(p[1].width, 100)

        # packed into open bins before openning a new one
        p.add_rect(45, 45)
        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 3)

        # Exhaust bin count
        p.add_rect(70, 70)
        self.assertEqual(len(p), 3)
        self.assertEqual(p[2].width, 100)
        self.assertEqual(len(p.rect_list()), 4)

        p.add_rect(80, 80) # No bins where to pack this rectangle
        self.assertEqual(len(p), 3)
        self.assertEqual(len(p.rect_list()), 4)
     
        # Fill open 100x100 bin
        p.add_rect(45, 45)
        p.add_rect(45, 45)
        self.assertEqual(len(p), 3)
        self.assertEqual(len(p.rect_list()), 6)
        
        # try to exhaust infinite bin
        for r in range(200):
            p.add_rect(39, 39)
        self.assertEqual(len(p), 203)


class TestPackerOnlineBBF(TestCase):

    def test_bin_selection(self):
        # Check rectangles are packed into the bin with the best fittness
        # score. In this case the one wasting less area.
        p = packer.PackerOnlineBBF(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)
      
        p.add_bin(10, 10)
        p.add_bin(15, 15)
        p.add_bin(55, 55)
        p.add_bin(50, 50)
        
        # First rectangle is packed into the first bin where it fits
        p.add_rect(50, 30)
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 55)

        # Another bin is opened when it doesn't fit into first one
        p.add_rect(50, 30)
        self.assertEqual(len(p), 2)
        self.assertEqual(p[1].width, 50)

        # rectangle is placed into the bin with the best fitness, not
        # the first one where it fits.
        p.add_rect(20, 20)
        self.assertEqual(len(p), 2)
        self.assertTrue((1, 0, 30, 20, 20, None) in p.rect_list())

    def test_count(self):
        # test bins with more than one element are only check the first one
        # to decide if a rectangle can be packed
        p = packer.PackerOnlineBBF(rotation=False, pack_algo=guillotine.GuillotineBlsfMaxas)

        p.add_bin(30, 30, count=2)
        p.add_bin(90, 90, count=float("inf"))
        p.add_bin(150, 30)

        # Try infinite bin
        for r in range(100):
            p.add_rect(60, 60)
        self.assertEqual(len(p), 100)

        # pack into bin following infinite bin
        p.add_rect(130, 30)
        self.assertEqual(len(p), 101)
        self.assertEqual(p[100].width, 150)

        # check best fit is selected, not first bin
        p.add_rect(20, 20)
        self.assertEqual(len(p), 101)
        for bin, x, y, width, height, rid in p.rect_list():
            if width==20:
                self.assertEqual(bin, 100)


class TestPacker(TestCase):

    def test_init(self):
        # Test rotation is enabled by default
        p = packer.PackerBNF(rotation=True)
        p.add_bin(100, 10)
        p.add_rect(10, 89)
        p.pack()
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 89, 10, None))

        # Test default packing algo
        p = packer.PackerBFF()
        p.add_bin(10, 10)
        p.add_rect(1, 1)
        p.pack()
        for b in p:
            self.assertIsInstance(b, maxrects.MaxRectsBssf)
        
        # Test default sorting algo is unsorted
        p = packer.PackerBFF(pack_algo=guillotine.GuillotineBssfSas, rotation=False)
        p.add_bin(100, 100, count=20)
       
        p.add_rect(70, 70)
        p.add_rect(90, 55)
        p.add_rect(90, 90)
        p.add_rect(55, 90)
        p.add_rect(60, 60)
        p.pack()

        self.assertTrue((0, 0, 0, 70, 70, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 90, 55, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((3, 0, 0, 55, 90, None) in p.rect_list())
        self.assertTrue((4, 0, 0, 60, 60, None) in p.rect_list())

        # Test custom packing algo is stored and used
        p = packer.PackerBFF(pack_algo=guillotine.GuillotineBafSas)
        p.add_bin(10, 10)
        p.add_rect(1, 1)
        p.pack()
        for b in p:
            self.assertIsInstance(b, guillotine.GuillotineBafSas)

        # check custom sorting algo is used
        p = packer.PackerBFF(sort_algo=packer.SORT_AREA, 
                pack_algo=skyline.SkylineBl, rotation=False)
        p.add_bin(100, 100, count=300)
        p.add_rect(60, 70)
        p.add_rect(90, 80)
        p.add_rect(60, 55)
        p.add_rect(70, 90)
        p.pack()
        self.assertTrue((0, 0, 0, 90, 80, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 90, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 60, 70, None) in p.rect_list())
        self.assertTrue((3, 0, 0, 60, 55, None) in p.rect_list())

        # check rectangle rotation can be disabled
        p = packer.PackerBFF(sort_algo=packer.SORT_AREA, 
                pack_algo=skyline.SkylineBl, rotation=False)
        p.add_bin(90, 20)
        p.add_rect(20, 90)
        p.pack()

        self.assertEqual(len(p.rect_list()), 0)

        p = packer.PackerBFF(sort_algo=packer.SORT_AREA, 
                pack_algo=skyline.SkylineBl, rotation=True)
        p.add_bin(90, 20)
        p.add_rect(20, 90)
        p.pack()

        self.assertEqual(len(p.rect_list()), 1)

    def test_iter(self):
        # check __iter__ only loops over open and closed bins
        p = packer.PackerBNF()
        p.add_bin(50, 50, count=2)
        p.add_bin(100, 100, count=float("inf"))

        p.add_rect(40, 40)
        p.add_rect(91, 91)
        p.add_rect(41, 41)
        p.add_rect(10, 10) # can't be packed first bin because it's closed
        p.pack()
        bins = list(iter(p))
        self.assertEqual(len(bins), 4)

        # test the same with BFF mode (where bins aren't closed)
        p = packer.PackerBFF()
        p.add_bin(50, 50, count=2)
        p.add_bin(100, 100, count=float("inf"))

        p.add_rect(40, 40)
        p.add_rect(91, 91)
        p.add_rect(41, 41)
        p.add_rect(10, 10) # packed into first bin
        p.pack()
        bins = list(iter(p))
        self.assertEqual(len(bins), 3)

    def test_pack(self):

        # check packing without bins doens't rise errors
        p = packer.PackerBFF()
        p.add_rect(10, 10)
        p.pack()

        self.assertEqual(p.rect_list(), [])
        self.assertEqual(p.bin_list(), [])
        self.assertEqual(list(iter(p)), [])

        # no errors when there are no rectangles to pack
        p = packer.PackerBFF()
        p.add_bin(10, 10)
        p.pack()
        self.assertEqual(p.rect_list(), [])
        self.assertEqual(p.bin_list(), [])

        # Test rectangles are packed into first available bin
        p = packer.PackerBFF(rotation=False, sort_algo=packer.SORT_NONE)
        p.add_bin(20, 10)
        p.add_bin(50, 50)
        p.add_rect(10, 20)
        p.add_rect(41, 41) # Not enough space for this rectangle
        p.pack()

        self.assertEqual(len(p.bin_list()), 1)
        self.assertEqual(p[0].width, 50)
        self.assertEqual(p[0].height, 50)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 10, 20, None))

        # Test rectangles too big
        p = packer.PackerBFF()
        p.add_bin(30, 30)
        p.add_rect(40, 50)
        p.pack()
        self.assertEqual(len(p.bin_list()), 0) 
        self.assertEqual(len(p.rect_list()), 0)

        # check nothing is packed before calling pack
        p = packer.PackerBFF()
        p.add_bin(10, 10)
        p.add_rect(3, 3)

        self.assertEqual(len(p.bin_list()), 0)
        self.assertEqual(len(p.rect_list()), 0)
   
        # Test repacking after adding more rectangles and bins
        p = packer.PackerBFF(sort_algo=packer.SORT_NONE)
        p.add_bin(100, 100)
        p.add_rect(3, 3)
        p.pack()

        self.assertEqual(len(p.bin_list()), 1)
        self.assertEqual(len(p.rect_list()), 1)

        p.add_rect(10, 10)
        p.add_rect(120, 100)
        p.add_bin(200, 200)
        p.pack()
        
        self.assertEqual(len(p.bin_list()), 2)
        self.assertEqual(len(p.rect_list()), 3)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 3, 3, None))
        self.assertEqual(p.rect_list()[1], (0, 3, 0, 10, 10, None))
        self.assertEqual(p.rect_list()[2], (1, 0, 0, 120, 100, None))
        self.assertEqual(p.bin_list()[0], (100, 100))
        self.assertEqual(p.bin_list()[1], (200, 200))

    def test_repack(self):
        # Test it is possible to add more rentangles/bin and pack again
        p = packer.PackerBFF(rotation=False, sort_algo=packer.SORT_NONE)
        p.add_bin(50, 50)
        p.add_rect(20, 20)
        p.pack()

        self.assertEqual(len(p.rect_list()), 1)
        self.assertEqual(len(p.bin_list()), 1)
        self.assertTrue((0, 0, 0, 20, 20, None) in p.rect_list())
        
        # Add more rectangles and re-pack
        p.add_rect(10, 10)
        p.add_rect(70, 50)
        p.pack()
        self.assertEqual(len(p.rect_list()), 2)
        self.assertEqual(len(p.bin_list()), 1)
        self.assertTrue((0, 0, 0, 20, 20, None) in p.rect_list())
        self.assertTrue((0, 20, 0, 10, 10, None) in p.rect_list())

        # Add more bins and re-pack
        p.add_bin(70, 70)
        p.add_bin(100, 100)
        p.pack()
        self.assertEqual(len(p.rect_list()), 3)
        self.assertEqual(len(p.bin_list()), 2)
        self.assertTrue((0, 0, 0, 20, 20, None) in p.rect_list())
        self.assertTrue((0, 20, 0, 10, 10, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 50, None) in p.rect_list())

    def test_repack_rectangle_sort(self):
        # check rectangles are sorted before a repack
        p = packer.PackerBNF(rotation=False, sort_algo=packer.SORT_AREA)
        p.add_bin(100, 100)
        p.add_bin(90, 90)
        p.add_bin(80, 80)

        p.add_rect(70, 70)
        p.add_rect(80, 80)
        p.pack()

        self.assertTrue((0, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 70, None) in p.rect_list())

        # add bigger rectangle and repack
        p.add_rect(90, 90)
        p.pack()
        self.assertTrue((0, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 70, 70, None) in p.rect_list())


class TestPackerBNF(TestCase):
    
    def test_bin_seelection(self):
        """Test bins are closed after one failed packing attempt"""
        p = packer.PackerBNF(pack_algo=guillotine.GuillotineBafSas, 
                sort_algo=packer.SORT_NONE, rotation=False)
        p.add_bin(50, 50, count=100)
        p.add_bin(100, 100)
        p.add_bin(300, 300, count=100)

        p.add_rect(40, 40)
        p.add_rect(90, 90)
        p.add_rect(5, 5)
        p.add_rect(20, 20)
        p.add_rect(10, 10)
        p.pack()
        
        self.assertTrue((0, 0, 0, 40, 40, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((1, 0, 90, 5, 5, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 20, 20, None) in p.rect_list())
        self.assertTrue((2, 0, 20, 10, 10, None) in p.rect_list())

        self.assertEqual(len(p), 3)
        self.assertEqual(p[0].width, 50)
        self.assertEqual(p[1].width, 100)
        self.assertEqual(p[2].width, 50)

    def test_repack(self):
        # Test can be packed a second time withou needing to add all 
        # bin/rectangles again
        p = packer.PackerBNF(pack_algo=guillotine.GuillotineBafSas,
                sort_algo=packer.SORT_NONE, rotation=False)
        p.add_bin(100, 100)
        p.add_rect(20, 20)
        p.pack()
        
        self.assertTrue((0, 0, 0, 20, 20, None) in p.rect_list())

        # Add rectangles and repack
        p.add_rect(80, 80)
        p.pack()
        self.assertTrue((0, 0, 0, 20, 20, None) in p.rect_list())
        self.assertTrue((0, 20, 0, 80, 80, None) in p.rect_list())

    def test_repack_rectangle_sort(self):
        # check rectangles are sorted before a repack
        p = packer.PackerBNF(rotation=False, sort_algo=packer.SORT_AREA)
        p.add_bin(100, 100)
        p.add_bin(90, 90)
        p.add_bin(80, 80)

        p.add_rect(70, 70)
        p.add_rect(80, 80)
        p.pack()

        self.assertTrue((0, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 70, None) in p.rect_list())

        # add bigger rectangle and repack
        p.add_rect(90, 90)
        p.pack()
        self.assertTrue((0, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 70, 70, None) in p.rect_list())


class TestPackerBFF(TestCase):
  
    def test_bin_selection(self):
        # check rectangle is packed into the first open bin where it fits,
        # if it can't be packed into any use the first available bin
        p = packer.PackerBFF(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)
        p.add_bin(20, 20, count=2)
        p.add_bin(100, 100)

        # Packed into second bin
        p.add_rect(90, 90)
        p.pack()
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 100)

        # rectangles are packed into open bins whenever possible
        p.add_rect(10, 10)
        p.pack()
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p.rect_list()), 2)

        p.add_rect(5, 5)
        p.pack()
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p.rect_list()), 3)

        # rectangle doesn't fit, open new bin
        p.add_rect(15, 15)
        p.pack()
        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 4)
    
        # if there are more than one possible bin select first one
        p.add_rect(5, 5)
        p.pack()
        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 5)
        self.assertTrue((0, 10, 90, 5, 5, None) in p.rect_list())



class TestPackerBBF(TestCase):
    """BBF (Bin Best Fit): Pack rectangle in bin that gives best fitness"""

    def test_bin_selection(self):
        # Check rectangles are packed into the bin with the best fittness
        # score. In this case the one wasting less area.
        p = packer.PackerBBF(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)
        p.add_bin(10, 10)
        p.add_bin(15, 15)
        p.add_bin(55, 55)
        p.add_bin(50, 50)
        
        # First rectangle is packed into the first bin where it fits
        p.add_rect(50, 30)
        p.pack()
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0].width, 55)

        # Another bin is opened when it doesn't fit into first one
        p.add_rect(50, 30)
        p.pack()
        self.assertEqual(len(p), 2)
        self.assertEqual(p[1].width, 50)

        # rectangle is placed into the bin with the best fitness, not
        # the first one where it fits.
        p.add_rect(20, 20)
        p.pack()
        self.assertEqual(len(p), 2)
        self.assertTrue((1, 0, 30, 20, 20, None) in p.rect_list())

    def test_repack_rectangle_sort(self):
        # check rectangles are sorted before a repack
        p = packer.PackerBBF(rotation=False, sort_algo=packer.SORT_AREA)
        p.add_bin(100, 100)
        p.add_bin(90, 90)
        p.add_bin(80, 80)

        p.add_rect(70, 70)
        p.add_rect(80, 80)
        p.pack()

        self.assertTrue((0, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 70, None) in p.rect_list())

        # add bigger rectangle and repack
        p.add_rect(90, 90)
        p.pack()
        self.assertTrue((0, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 70, 70, None) in p.rect_list())


class TestPackerGlobal(TestCase):
    """
    GLOBAL: For each bin pack the rectangle with the best fitness.
    """
    def test_limit_cases(self):
        #Test pack works without rectangles and/or bins"""
        p = packer.PackerGlobal()
        p.add_bin(20, 20, count=1)
        p.add_bin(100, 100, count=100)
        p.pack()
        self.assertEqual(len(p.rect_list()), 0)
        self.assertEqual(len(p.bin_list()), 0)

        # check no exception is raised when there are no rectangles to pack
        p = packer.PackerGlobal()
        p.add_rect(30, 30)
        p.add_rect(20, 20)
        p.pack()
        self.assertEqual(len(p.rect_list()), 0)
        self.assertEqual(len(p.bin_list()), 0)

        # neither bins nor rectangles
        p = packer.PackerGlobal()
        p.pack()
        self.assertEqual(len(p.rect_list()), 0)
        self.assertEqual(len(p.bin_list()), 0)

    def test_bin_selection(self):
        # Test rectangles with better fitness are placed first 
        p = packer.PackerGlobal(pack_algo=skyline.SkylineMwfl, 
                rotation=False)
        p.add_bin(100, 100)
        p.add_rect(40, 10)
        p.add_rect(100, 50)
        p.add_rect(90, 30)
        p.pack()

        self.assertEqual(len(p.rect_list()), 3)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 40, 10, None))
        self.assertEqual(p.rect_list()[1], (0, 0, 10, 90, 30, None))
        self.assertEqual(p.rect_list()[2], (0, 0, 40, 100, 50, None))
        
        # check can handle more than one bin
        p = packer.PackerGlobal(pack_algo=skyline.SkylineMwfl, 
                rotation=False)
        p.add_bin(50, 50, count=3)
        p.add_bin(100, 100)
        p.add_rect(40, 40)
        p.add_rect(80, 80)
        p.add_rect(10, 10)
        p.pack()
        
        self.assertEqual(len(p.rect_list()), 3)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 10, 10, None))
        self.assertEqual(p.rect_list()[1], (0, 10, 0, 40, 40, None))
        self.assertEqual(p.rect_list()[2], (1, 0, 0, 80, 80, None))

    def test_add_bin_w_count(self):
        # Test rectangles with more than one member
        p = packer.PackerGlobal(pack_algo=skyline.SkylineMwfl, 
                rotation=False)
        p.add_bin(50, 50, count=30)
        p.add_bin(100, 100)

        p.add_rect(40, 21)
        p.add_rect(100, 50)
        p.add_rect(90, 80)
        p.add_rect(50, 40)
        p.add_rect(50, 50)

        p.pack()

        self.assertEqual(len(p.rect_list()), 4)
        self.assertEqual(p[0].width, 50)
        self.assertEqual(p[1].width, 50)
        self.assertEqual(p[2].width, 50)
        self.assertEqual(p[3].width, 100)
        self.assertTrue((0, 0, 0, 40, 21, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 50, 40, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 50, 50, None) in p.rect_list()) 
        self.assertTrue((3, 0, 0, 100, 50, None) in p.rect_list())
      
    def test_fitness2(self):
        p = packer.PackerGlobal(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)

        p.add_bin(100, 100)
        p.add_rect(20, 10)
        p.add_rect(80, 10)
        p.add_rect(80, 80)
        p.pack()

        self.assertEqual(len(p.rect_list()), 3)
        self.assertEqual(p.rect_list()[0], (0, 0, 0, 80, 80, None))
        self.assertEqual(p.rect_list()[1], (0, 0, 80, 80, 10, None))
        self.assertEqual(p.rect_list()[2], (0, 0, 90, 20, 10, None))

    def test_repack(self):
        """Test can be packed a second time"""
        p = packer.PackerGlobal(pack_algo=guillotine.GuillotineBafSas, 
                rotation=False)
        p.add_bin(100, 100, count=float("inf"))
        p.add_rect(60, 60)
        p.add_rect(55, 55)
        p.pack()

        self.assertEqual(len(p), 2)
        self.assertEqual(len(p.rect_list()), 2)
        self.assertTrue((0, 0, 0, 60, 60, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 55, 55, None) in p.rect_list())

        # Add more rectangles and repack
        p.add_rect(80, 10)
        p.add_rect(80, 80)
        p.pack()
        
        self.assertEqual(len(p.rect_list()), 4)
        self.assertTrue((0, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((0, 0, 80, 80, 10, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 60, 60, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 55, 55, None) in p.rect_list())

    def test_repack_rectangle_sort(self):
        # check rectangles are sorted before a repack
        # GuillotineBaf -> selects bin where less area is wasted 
        p = packer.PackerGlobal(rotation=False, pack_algo=guillotine.GuillotineBafMaxas)
        p.add_bin(100, 100)
        p.add_bin(90, 90)
        p.add_bin(80, 80)

        p.add_rect(70, 70)
        p.add_rect(80, 80)
        p.pack()

        self.assertTrue((0, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 70, 70, None) in p.rect_list())

        # add bigger rectangle and repack
        p.add_rect(90, 90)
        p.pack()
        self.assertTrue((0, 0, 0, 90, 90, None) in p.rect_list())
        self.assertTrue((1, 0, 0, 80, 80, None) in p.rect_list())
        self.assertTrue((2, 0, 0, 70, 70, None) in p.rect_list())
      
    def test_add_bin_extra_kwargs(self): 
        # Check add_bin kwargs don't shadow packer options
        p = packer.PackerGlobal(rotation=False)
        p.add_bin(10, 100, count=3, rot=True, args='yes')
        p.add_rect(90, 9)
        p.pack()
        self.assertEqual(len(p), 0)
        
        # Check with more than one bin
        p = packer.PackerGlobal(rotation=False)
        p.add_bin(10, 100, rot=True, args='yes', count=3)
        p.add_rect(9, 90)
        p.add_rect(9, 90)
        p.add_rect(9, 90)
        p.pack()
        self.assertEqual(len(p), 3)
        self.assertEqual(len(p[0]), 1)
        self.assertEqual(len(p[1]), 1) 
        self.assertEqual(len(p[2]), 1)

        # Custom Packing algorithm...
        class CustomAlgo(maxrects.MaxRectsBssf):
            def __init__(self, width, height, rot=True, *args, **kwargs):
                self.extra_kwargs = kwargs
                super().__init__(width=width, height=height, rot=rot,
                                    *args, **kwargs)

        p = packer.PackerGlobal(pack_algo=CustomAlgo)
        p.add_bin(100, 100, name='yes', count=2)
        p.add_rect(90, 80)
        p.pack()
        self.assertEqual(len(p), 1)
        self.assertEqual(len(p[0]), 1)
        self.assertTrue('name' in p[0].extra_kwargs)
        self.assertFalse('count' in p[0].extra_kwargs)
        



class TestNewPacker(TestCase):

    def test_default_options(self):
        """Test newPacker default options"""
        # Test default options
        p = packer.newPacker()
        
        # Default mode Online BBF
        self.assertIsInstance(p, packer.PackerBBF)

        # Default rotations True
        self.assertEqual(p._rotation, True)

        # Default packing algorithm SkylineBlWm
        p.add_rect(100, 10)
        p.add_bin(10, 100)
        p.pack()
        self.assertIsInstance(p[0], maxrects.MaxRectsBssf)
        self.assertEqual(len(p[0]), 1)

        # Default sortin algorithm SORT_LSIDE
        self.assertEqual(p._sort_algo, packer.SORT_AREA)
        
    def test_rotation(self):
        """Test newPacker rotation argument"""
        p = packer.newPacker(rotation=False) 
        p.add_rect(100, 10)
        p.add_bin(10, 100)
        p.pack()
        self.assertEqual(len(p.rect_list()), 0)
        
        p = packer.newPacker(rotation=True) 
        p.add_rect(100, 10)
        p.add_bin(10, 100)
        p.pack()
        self.assertEqual(len(p.rect_list()), 1)

    def test_pack_algo(self):
        """Test NewPacker use correct PackingAlgorithm"""
        p = packer.newPacker(pack_algo=skyline.SkylineMwfl)
        p.add_rect(10, 10)
        p.add_bin(100, 100)
        p.pack()
        self.assertIsInstance(p[0], skyline.SkylineMwfl)

    def test_mode_offline(self):
        """Test newPacker returns correct Packer when in offline mode"""
        p = packer.newPacker(mode=packer.PackingMode.Offline, 
                bin_algo=packer.PackingBin.BNF)
        self.assertIsInstance(p, packer.PackerBNF)

        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.BFF)
        self.assertIsInstance(p, packer.PackerBFF)
        
        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.BBF)
        self.assertIsInstance(p, packer.PackerBBF)
        
        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.Global)
        self.assertIsInstance(p, packer.PackerGlobal)

    def test_mode_online(self):
        """Test newPacker return correct Packer when in online mode"""
        p = packer.newPacker(mode=packer.PackingMode.Online,
                bin_algo=packer.PackingBin.BNF)
        self.assertIsInstance(p, packer.PackerOnlineBNF)

        p = packer.newPacker(mode=packer.PackingMode.Online,
                bin_algo=packer.PackingBin.BFF)
        self.assertIsInstance(p, packer.PackerOnlineBFF)

        p = packer.newPacker(mode=packer.PackingMode.Online,
                bin_algo=packer.PackingBin.BBF)
        self.assertIsInstance(p, packer.PackerOnlineBBF)

        with self.assertRaises(AttributeError):
            p = packer.newPacker(mode=packer.PackingMode.Online,
                    bin_algo=packer.PackingBin.Global)

    def test_offline_sorting(self):
        """Test newPacker uses provided sort algorithm"""
        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.BFF, 
                sort_algo=packer.SORT_RATIO)
        self.assertEqual(p._sort_algo, packer.SORT_RATIO)
        
        # Test sort_algo is ignored when not applicable
        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.Global, 
                sort_algo=packer.SORT_RATIO)

        p = packer.newPacker(mode=packer.PackingMode.Online,
                bin_algo=packer.PackingBin.BFF, 
                sort_algo=packer.SORT_RATIO)

    def test_bin_id(self):
        """Test correct bin id is assigned to each bin"""

        # width, height, count, bid
        bins   = [(100, 50, 1, "first"), (50, 50, 1, "second"), (200, 200, 10, "many")]
        binIdx = {(b[0], b[1]): b[3] for b in bins} 
        rects = [(199, 199), (100, 40), (40, 40), (20, 20), (180, 179)]

        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.BFF)
        
        for b in bins:
            p.add_bin(b[0], b[1], count=b[2], bid=b[3])
        
        for r in rects:
            p.add_rect(r[0], r[1])

        p.pack()

        # verify bin ids correctly assigned
        for abin in p:
            self.assertEqual(binIdx[(abin.width, abin.height)], abin.bid)
 
    def test_bin_default_id(self):
        """Test default bin id is None"""
        bins   = [(100, 50, 1), (50, 50, 1), (200, 200, 10)]
        rects = [(199, 199), (100, 40), (40, 40), (20, 20), (180, 179)]

        p = packer.newPacker(mode=packer.PackingMode.Offline,
                bin_algo=packer.PackingBin.BFF)
        
        for b in bins:
            p.add_bin(b[0], b[1], count=b[2])
        
        for r in rects:
            p.add_rect(r[0], r[1])

        p.pack()

        # verify bin ids correctly assigned
        for abin in p:
            self.assertEqual(abin.bid, None)
 





































