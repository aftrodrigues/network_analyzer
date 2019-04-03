import re
import subprocess as sub
import datetime

class info:
	def __init__(self, address, request, media_type=None, data=None, hora=None, status=None, resolution=None):
		self.address = address
		self.request = request
		self.media_type = media_type
		self.data = data

		hora = hora.split(':')
		self.hora = datetime.time(int(hora[0]), int(hora[1]), int(hora[2]) )
		self.status = status
		
		self.resolution=resolution
	def __str__(self):
		return "%s-> %s %s??%s" % (self.address, self.request, self.data, self.hora)

path = ''
file_name = 'access2.log'

log = False

def get_data_from_file():
	fr = open(path + file_name, 'r')
	txt = fr.readlines()

	for line in txt:
		ip_client = line[ :line.find(' ')]
		
		try:
			request = re.search('(?<=GET /).+(HTTP)', line).group(0)
			if '.mpd' in request:
				request_media = 'manifest'
				request = request.split('.')[0]
			elif 'video' in request:
				request_media = 'video'
				request = request.split('.')[0]
			elif 'audio' in request:
				request_media = 'audio'
				request = request.split('.')[0]
			else:
				request_media = None

			if request_media == 'video':
				resolution = re.search('(?<=x).+?(?=_)',request).group(0)
				print 'resolution: ' + resolution + 'p'
			
			data = re.search('[0-9]+/[a-zA-Z]*/[0-9]{4}',line).group(0)
			hora = re.search('(?<=[0-9]{2}/[a-zA-Z]{3}/[0-9]{4}:).*:[0-9]{2}',line).group(0)
			status = re.search('(?<=(HTTP/1.1" ))[0-9]*', line).group(0)

			if log:
				print 'IP: ' + ip_client
				print 'request: ' + request
				print 'request_type: ' + request_media
				print 'data: ' + data
				print 'hora: ' + hora
				print 'Status: ' + status
			
		except Exception as e:
			print 'ERROR: ' + str(e)
			print line
			break


def get_data(address, file):
	#txt = sub.check_output(['curl', address + '/' + file, '-s'])
	#txt = txt.split('\n')

	fr = open(path + file_name, 'r')
	txt = fr.readlines()
	print txt[0]
	dados = []
	for line in txt:
		if len(line) == 0:
			continue

		

		ip_client = line[ :line.find(' ')]
		
		try:
			request = re.search('(?<=GET /).+(HTTP)', line).group(0)
			if '.mpd' in request:
				request_media = 'manifest'
				request = request.split('.')[0]
			elif 'video' in request:
				request_media = 'video'
				request = request.split('.')[0]
			elif 'audio' in request:
				request_media = 'audio'
				request = request.split('.')[0]
			else:
				request_media = None

			resolution=None
			if request_media == 'video':
				resolution = re.search('(?<=x).+?(?=_)',request).group(0)
							
			data = re.search('[0-9]+/[a-zA-Z]*/[0-9]{4}',line).group(0)
			hora = re.search('(?<=[0-9]{2}/[a-zA-Z]{3}/[0-9]{4}:).*:[0-9]{2}',line).group(0)
			status = re.search('(?<=(HTTP/1.1" ))[0-9]*', line).group(0)

			dados.append( info(ip_client, request, media_type=request_media, data=data, hora=hora, status=status, resolution=resolution) )

			if log:
				print 'IP: ' + ip_client
				print 'request: ' + request
				print 'request_type: ' + request_media
				print 'data: ' + data
				print 'hora: ' + hora
				print 'Status: ' + status
			
		except Exception as e:
			print 'ERROR: ' + str(e)
			print line
			break
	return dados

if __name__ == '__main__':
	get_data('10.0.0.171', 'apache2.log')