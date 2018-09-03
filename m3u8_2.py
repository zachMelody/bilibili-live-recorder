from urlparse import urlparse
import requests
import urllib
import os
import sys

def get_url_list(host, body):
	lines = body.split('\n')
	ts_url_list = []
	for line in lines:
		if not line.startswith('#') and line != '':
			if line.startswith('http'):
				ts_url_list.append(line)
			else:
				ts_url_list.append('%s/%s' % (host, line))
	return ts_url_list

def get_host(url):
	urlgroup = urlparse(url)
	return urlgroup.scheme + '://' + urlgroup.hostname

def get_m3u8_body(url):
	print( 'read m3u8 file:', url)
	session = requests.Session()
	adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=10)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	r = session.get(url, timeout=10)
	return r.content

def download_ts_file(ts_url_list, download_dir):
	i = 0
	for ts_url in reversed(ts_url_list):
		i += 1
		file_name = ts_url[ts_url.rfind('/'):]
		curr_path = '%s%s' % (download_dir, file_name)
		print('\n[process]: %s/%s' % (i, len(ts_url_list)))
		print('[download]:', ts_url)
		print ('[target]:', curr_path)
		if os.path.isfile(curr_path):
			print('[warn]: file already exist')
			continue
		urllib.urlretrieve(ts_url, curr_path)

def main(url, download_dir):
	host = get_host(url)
	body = get_m3u8_body(url)
	ts_url_list = get_url_list(host, body)
	print('total file count:', len(ts_url_list))
	download_ts_file(ts_url_list, download_dir)

