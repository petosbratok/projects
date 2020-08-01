#-*- coding: utf-8 -*-
from sys import argv
import random
from msvcrt import getch
import os.path

class Encrypt():
	def __init__(self):
		self.encryption_key = []
		self.decryption_key = []
		print("\n*** Ecnryption application started***\n")
		self.main()

	def main(self):
		"""  Main menu """
		while True:
			print("What do we need to do?\n1) Encrypt file\n2) Decrypt file\n3) Quit")
			answer = str(getch())
			if ("b'1'") in answer:
				self.encrypt()
			elif ("b'2'") in answer:
				self.decrypt()
			elif ("b'3'") in answer:
				self.quit()
			else:
				print("There's no option like this. Try again.")
				self.main()

	def filePath(self):
		""" Get file path """
		while not False:
				self.file_path = input("Enter your file's path or 'quit' to end session: ")
				if os.path.isfile(self.file_path):
					break
				else:
					print("Can't find the file. Type file name again.")

	def crypt(self):
		"""  Encryption(decryption) algorithm """
		if self.encryption_key == []:
			for _ in range(5):
				key = random.randint(-25, 25)
				self.encryption_key.append(key)
				self.decryption_key.append(key*-1)

		with open(self.file_path, 'r') as f:
			lines = [line.rstrip('\n') for line in f.readlines()]

		with open(self.file_path, 'w', encoding='utf8') as f:
			for line in lines:
				new_line = ''
				lineInBytes = bytes(line, 'utf-8')
				for i in range(len(lineInBytes)):
					letter = lineInBytes[i]
					currentKey = self.encryption_key[i % 5]
					id = letter + currentKey
					if id < 32:
						id = 127 - 32 + id
					if id > 126:
						id = id - 127 + 32
					new_line += chr(id)
				f.write(new_line + '\n')

	def encrypt(self):
		""" Encryption process """
		self.filePath()
		self.crypt()
		print('File has succesfully been ecnrypted.\n')
		print('*** ATTENTION! ***')
		print('Your decryption key is: ', end='')
		[print(key, end=' ') for key in self.decryption_key]
		print('')
		print('Write it down somewhere or you will lose your files!\n')
		self.encryption_key = []
		self.decryption_key = []

	def decrypt(self):
		""" Decryption process """
		self.filePath()
		self.encryption_key = input('Write the decrypion key without commas: ')
		self.encryption_key = [int(x) for x in self.encryption_key.split()]
		self.crypt()
		print('Succesful decryption\n')
		self.encryption_key = []
		self.decryption_key = []

	def quit(self):
		print('*** Shutting down ***')
		exit(0)

if __name__ == '__main__':
	Encrypt()
