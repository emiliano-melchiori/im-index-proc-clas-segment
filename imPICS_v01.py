import sys, os, struct
import osgeo.gdal as gdal, gdalnumeric
import matplotlib.pyplot as pyplot
import numpy
from scipy import ndimage
import re

class GDALCalcINDEXES (object):

	def __init__(self, ptf1,ptf2):
		self.pathf1 = ptf1 # declaracion de variable global
		self.pathf2 = ptf2
		print 'prog iniciado' , self.pathf1, self.pathf2

	def im_dilate(self, data, it):
		ldata = data
		strct = ndimage.generate_binary_structure(2,1)
		datadil = ndimage.binary_closing(ldata, structure=strct,iterations=it)
		return datadil
		
	def im_show(self, raster):
		data = None
		data = raster
		pyplot.hot()
		pyplot.imshow(data < 40) # figura 1
		pyplot.title('ndvi')
		#pyplot.colorbar()
		fig1 = pyplot.figure()
		ax1 = fig1.add_subplot(111)
		ax1.set_ylabel('lat')
		ax1.set_xlabel('long')
		ax1.set_title('imagen test')
		dataflt = self.im_dilate(data < 40, 3)
		ax1.imshow(dataflt)
		#pyplot.subplot(2,2,1)
		#pyplot.imshow((data > 0.5) * data)
		#pyplot.subplot(2,2,4)
		#hist,bins = numpy.histogram(data,bins=255)
		#width = 0.2*(bins[1]-bins[0])
		#center = (bins[:-1]+bins[1:])/2
		#ax2 = fig2.add_subplot(111)
		#ax2.set_title('histograma de la imagen')
		#x2.set_xlabel('valores digitales')
		#ax2.set_ylabel('cuentas')
		#ax2.bar(center, hist, align = 'center', width = width)
		#pyplot.bar(center, hist, align = 'center', width = width)
		pyplot.show()

	def im_props (self, raster):
		geo = raster.GetGeoTransform()
		project = raster.GetProjection()
		cols = raster.RasterXSize
		rows = raster.RasterYSize
		print raster
		print cols, rows
		print geo
		print project
		
	def calc_ndvi(self, ir_band, r_band):
		irb = ir_band.astype(numpy.float)
		rb = r_band.astype(numpy.float)
		ndvi = numpy.zeros_like(irb).astype(numpy.float)
		ndvi = ((irb - rb) / (irb + rb))
		return ndvi
		
	def calc_nbr(self, ir_band, r_band, b_band):
		irb = ir_band.ReadAsArray().astype(numpy.float)
		rb = r_band.ReadAsArray().astype(numpy.float)
		bb = b_band.ReadAsArray().astype(numpy.float)
		nbr = numpy.zeros_like(irb).astype(numpy.float)
		# ... calcular nbr aqui
		return nbr
	
	def scan_dir(self, path_):
		os.chdir(path_)
		tif_files = []
		for files in os.listdir("."):
			if files.endswith(".tif"):
				tif_files.append(files)
		return tif_files

	def loadfile(self, pathtofile):
		files = self.scan_dir(pathtofile)
		files.sort()
		print files
		bfp = 1
		imcount = 0
		for sfile in files:
			pathtofile_ = pathtofile +'/'+ sfile
			if os.path.exists(pathtofile_):
				if re.search("BAND6",pathtofile_):
					print 'descartada: ', pathtofile_
					continue # vuelve al for
					
				print pathtofile_
				if bfp: # primer banda de la imagen se lee para obtener los valores ncols, nrows
					a = gdal.Open(pathtofile_).ReadAsArray().astype(int)
					bfp = 0;
					print a.shape, a.dtype, type(a), a.nbytes
					cols = a.shape[1]
					rows = a.shape[0]
					nparray = numpy.zeros((6,rows,cols),int) # bandas 1..5,7 sin banda 6
					print nparray.shape, nparray.dtype, type(nparray), nparray.nbytes
				
				if numpy.any(a):
					nparray[imcount,:,:] = a # usa el archivo cargado previamente
					a = None
				else:		
					nparray[imcount,:,:] = gdal.Open(pathtofile_).ReadAsArray().astype(int)
					print 'cargada:', pathtofile_
					
				#if nparray[imcount,:,:].any(): # chequear la correcta apertura del archivo. valores != 0
				if numpy.any(nparray[imcount,:,:]):
					imcount +=1
					#print "imagen cargada correctamente - banda:",imcount					
				else:
					print "Error cargando datos o imagen vacia -  chequear fuentes"
					# if operative: send mail
				print "---crap---"
			else: #if os.path.exists(pathtofile_):
				print 'The file does not exist.'
		return nparray
    
    # The function from which the script runs.
	def run(self):
		dirpath = self.pathf1
		file1 = self.loadfile(dirpath)
		ndvi_f1 = self.calc_ndvi(file1[3],file1[1])
		self.im_show(file1[3])
		#outFilePath = fpb1

# Start the script by calling the run function.
if __name__ == '__main__':
	ptf1 = "/root/Descargas/landsat/fecha1"
	ptf2 = "_sin_especificar_"
	obj = GDALCalcINDEXES(ptf1,ptf2)
	obj.run()



