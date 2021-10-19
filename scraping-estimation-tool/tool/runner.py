import requests

data = {
  'project': 'estimation_tool_scrapy',
  'spider': 'speed_score',
  'arg1': 'srichaitanyaschool.net'
}

response = requests.post('http://localhost:6800/schedule.json', data=data)
