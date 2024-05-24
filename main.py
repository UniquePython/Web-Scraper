from requests import get
from bs4 import BeautifulSoup
import os
import webbrowser

file_path = 'top_stories.html'
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Existing file '{file_path}' deleted.")

response = get('https://news.ycombinator.com/news')
response2 = get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(response.text, 'html.parser')
soup2 = BeautifulSoup(response2.text, 'html.parser')

links = soup.select('.titleline > a') 
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline > a') 
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score')
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if points > 99:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)
 
hn_stories = create_custom_hn(mega_links, mega_subtext)

html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hacker News Top Stories</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #7AB2B2;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #EEF7FF;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .container h1 {
            text-align: center; 
        }
        .story {
            margin-bottom: 20px;
            background-color: #f5eee2;
            border-color: black;
            border-radius: 15px;
            padding: 20px;
            color: white;
        }
        .story a {
            text-decoration: underline;
            color: #333;
        }
        .story a:hover {
            text-decoration: underline;
        }
        .votes {
            color: #888;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hacker News Top Stories</h1>
'''

for story in hn_stories:
    html_content += f'''
        <div class="story">
            <a href="{story['link']}" target="_blank">{story['title']}</a>
            <div class="votes">{story['votes']} points</div>
        </div>
    '''

html_content += '''
    </div>
</body>
</html>
'''

with open('top_stories.html', 'w') as file:
    file.write(html_content)

print("Webpage created as 'top_stories.html'")

webbrowser.open(f'file://{os.path.realpath(file_path)}')