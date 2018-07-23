'''
example usage
--------------------------------------------

import os
from ewtoolbox import File, Folder, Archive

if __name__ == '__main__':
	fdr = '/Users/eric/testfolder'
	src = os.path.join(fdr, 'src')
	dst = os.path.join(fdr, 'dst')
	file = os.path.join(src, 'wwd-dc3.txt')

	#print os.getcwd()
	print os.path.isdir(fdr)
	print os.path.isfile(file)
	arc = Archive(dst, 'testzip.zip')
	#f = File(file)
	folder = Folder(src)
	#folder.select_file_by_partial_str('file')
	folder.select_file_by_partial_str('a')
	arc.add(folder)
	arc.write()
'''
