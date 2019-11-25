from PIL import Image
from sys import argv

if argv[1] == 'i2p':
    a = Image.open(argv[2])
    a.save(argv[2][:argv[2].find('.')]+'.ppm')
elif argv[1] == 'p2a':
    a = Image.open(argv[2])
    a.save(argv[2][:argv[2].find('.')]+'.jpg')  
