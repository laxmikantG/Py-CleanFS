import sys
import os
import hashlib
import shutil

FLAG_REMOVEALL = False

class CleanFS:

	def __init__(self, location):
			'''
			'''
			self.remove = FLAG_REMOVEALL
			self.path = location
			self.paths = list()
			self.duplicates = list()
			self.removings = list()
			self.empty_dirs = list()
			self.totalDups = 0
			self.dupssize = 0
			self.tempdirs = ["Thumbs.db"]
			self.removings_count = 0
			self.removings_size = 0
			self.empty_dirs_count = 0

	def processFS(self):
			'''
			'''
			for directory, dirnames, filenames in os.walk(self.path):
					if not self.is_hidden(directory):
						self.removeRecursivelyEmptyDirs(directory)
						self.processFiles(filenames, directory)
			self.printCountToconsole()

	def is_hidden(self, directory):
			folder = directory.split("/home/laxmikant/")[1:]
			if folder:
				folder = folder[0]
				return folder.startswith(".") or folder.startswith("__")
			else:return False

	def printCountToconsole(self):
			info ="\n"+"*"*50+" RESULT "+ "*"*50 +'''\n Total Duplicates : %s\n Total Duplicates Size: %s KB\n Total Temp Files : %s\n Total Temp file Size: %s KB\n Total Empty Dirs : %s 
								'''%(self.totalDups, self.dupssize,
										 self.removings_count, self.removings_size,
										 self.empty_dirs_count)
			print info


	def processFiles(self, filenames, directory):
			'''
			'''
			if directory.startswith("__") or directory.startswith("."): return False
			for file_name in filenames:
				exactfile = os.path.join(directory, file_name)
				if os.path.isfile(exactfile):
					self.remove_temp_files(file_name, exactfile)
					if(os.path.exists(exactfile)):
							sha = self.get_sha1(exactfile)
							size = self.get_file_size(exactfile)
							if sha and sha not in self.paths:
									self.paths.append(sha)					
							else:
									self.totalDups+=1
									self.dupssize+= size
									self.duplicates.append(exactfile)
									print "\n %s] Remove Duplicate :"%(self.totalDups), exactfile, str(size) +"KB", 
									if self.remove:os.remove(exactfile)

	def remove_temp_files(self, file_name, exactfile):
			'''
			'''
			fname, ext = os.path.splitext(file_name)
			if ext.endswith("so"):print fname
			filesize = self.get_file_size(exactfile)
			if(ext.endswith("~") or file_name in self.tempdirs or filesize == 0 ):
					self.removings_count+=1
					self.removings.append(exactfile)
					self.removings_size+=filesize
					print "\n %s] Removing Temp file: "%(self.removings_count), exactfile, str(filesize)+"KB"
					if self.remove:os.remove(exactfile)

	def get_sha1(self, filepath):
				sha1 = hashlib.sha1()
				try:
					f = open(filepath, 'rb')
					sha1.update(f.read(16 * 1024 * 1024))
					f.close()
					shaenc = sha1.hexdigest()
				except Exception, e:
					shaenc = None	
				return shaenc 

	def removeRecursivelyEmptyDirs(self, dirpath):
			if(self.is_empty_dir(dirpath)):
				self.empty_dirs.append(dirpath)
				self.empty_dirs_count +=1 
				print "\n %s] Removing:"%(self.empty_dirs_count,), dirpath
				if self.remove:shutil.rmtree(dirpath)

	def is_empty_dir(self, dir):
			isEmpty=True
			subDirs=[]
			if not self.is_hidden(dir):
				print "\n In DIR :- ", dir
				for entry in os.listdir(dir):
					try:
							if os.path.isfile(os.path.join(dir, entry))==True:
								isEmpty = False
							else:
								subEmpty = self.is_empty_dir(os.path.join(dir, entry))
								if subEmpty== True:
									subDirs.append(os.path.join(dir, entry))
								else:
									isEmpty=False
					except Exception, e:
							print " Error ", str(os.path.join(dir, entry))
							isEmpty=False
			return isEmpty			

	def get_file_size(self, fpath):

			''' '''
			return float(os.stat(fpath).st_size)/1024

def main():
		path = sys.argv[1]
		CFS = CleanFS(path)
		CFS.processFS()


if __name__ == "__main__":
	main()
