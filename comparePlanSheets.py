# import module
from pdf2image import convert_from_path, pdfinfo_from_path
import PySimpleGUI as sg
from PIL import Image, ImageChops
import tempfile

first_pdf_file = sg.popup_get_file('1st PDF', default_path='')
try:
    first_fp = int(sg.popup_get_text('Page number of first plan'))
except:
    first_fp = 1
first_lp = first_fp + 1

second_pdf_file = sg.popup_get_file('2nd PDF', default_path='')
try:
    second_fp = int(sg.popup_get_text('Page number on second plan'))
except:
    second_fp = 1
second_lp = second_fp + 1

pp = "C://Users//rhodes//Downloads//Release-21.03.0//poppler-21.03.0//Library//bin"


first_image = convert_from_path(first_pdf_file, dpi=180, first_page=first_fp, last_page=first_lp, poppler_path=pp)
first_image[0].save('{}.png'.format('1stSheet'), 'PNG')
second_image = convert_from_path(second_pdf_file, dpi=180, first_page=second_fp, last_page=second_lp, poppler_path=pp)
second_image[0].save('{}.png'.format('2ndSheet'), 'PNG')

from PIL import Image, ImageChops, ImageDraw
point_table = ([0] + ([255] * 255))

def new_gray(size, color):
    img = Image.new('L',size)
    dr = ImageDraw.Draw(img)
    dr.rectangle((0,0) + size, color)
    return img

def black_or_b(b, a, opacity=0.50):
    diff = ImageChops.difference(a, b)
    diff = diff.convert('L')
    # Hack: there is no threshold in PILL,
    # so we add the difference with itself to do
    # a poor man's thresholding of the mask: 
    #(the values for equal pixels-  0 - don't add up)
    thresholded_diff = diff
    for repeat in range(3):
        thresholded_diff  = ImageChops.add(thresholded_diff, thresholded_diff)
    h,w = size = diff.size
    mask = new_gray(size, int(255 * (opacity)))
    shade = new_gray(size, 0)
    new = a.copy()
    new.paste(shade, mask=mask)
    # To have the original image show partially
    # on the final result, simply put "diff" instead of thresholded_diff bellow
    new.paste(b, mask=thresholded_diff)
    return new

a = Image.open("1stSheet.png")
b = Image.open("2ndSheet.png")
c = black_or_b(a, b)
c.show()