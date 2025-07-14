import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

def parse_star_cnt(star_str):
  star_str.strip()
  if star_str[-1]=="k":
    return int(float(star_str[:-1])*1000)
  return int(star_str)

def get_repo_info(h_tag,star_tag):
  a_tags=h_tag.find_all('a')
  username=a_tags[0].text.strip()
  repositname=a_tags[1].text.strip()
  repourl='https://github.com'+a_tags[1]['href']
  stars=parse_star_cnt(star_tag.text.strip().replace(",",""))
  return username,repositname,repourl,stars

def get_topic_doc(topic_url):
  topicpage=requests.get(topic_url)
  if topicpage.status_code!=200:
    raise Exception(print("Failed to Load Code: {} on page {}".format(topicpage.status_code,topic_url)))
  topichtml=BeautifulSoup(topicpage.text,"html.parser")
  return topichtml

def get_topic_repo(topichtml):
  h_tags=topichtml.find_all('h3',{"class":"f3 color-fg-muted text-normal lh-condensed"})
  star_tags=topichtml.find_all('span',class_="Counter js-social-count")
  topic_user_repo_dict={
  'username':[],'repositname':[],'repourl':[],'stars':[]}
  for i in range(len(h_tags)):
    repo_info=get_repo_info(h_tags[i],star_tags[i])
    topic_user_repo_dict['username'].append(repo_info[0])
    topic_user_repo_dict['repositname'].append(repo_info[1])
    topic_user_repo_dict['repourl'].append(repo_info[2])
    topic_user_repo_dict['stars'].append(repo_info[3])
  d2f=pd.DataFrame(topic_user_repo_dict)
  return d2f

def scrape_topic_one(topic_url,topic_name):
  df_page=get_topic_repo(get_topic_doc(topic_url))
  fname=topic_name+".csv"
  if os.path.exists(fname):
    print("Already exists Skipping creation of File: {}".format(fname))
  else:
    df_page.to_csv(fname,index=False)

def get_topics(parsedhtml):
  titletags=parsedhtml.find_all('p',{"class":"f3 lh-condensed text-center Link--primary mb-0 mt-1"})
  titles=[]
  for title in titletags:
    titles.append(title.text.strip())
  return titles

def get_descs(parsedhtml):
  desctags=parsedhtml.find_all('p',{"class":"f5 color-fg-muted text-center mb-0 mt-1"})
  descs=[]
  for desc in desctags:
    descs.append(desc.text.strip())
  return descs

def get_urllist(parsedhtml):
  links=parsedhtml.find_all('a',class_="no-underline d-flex flex-column flex-justify-center")
  urllist=[]
  for link in links:
    url="https://github.com"+link['href']
    urllist.append(url)
  return urllist

def scrape_topics():
  topicurl="https://github.com/topics"
  response=requests.get(topicurl)
  if response.status_code!=200:
    raise Exception ("Failed to load page {} due to {}".format(topicurl,response.status_code))
  pagecontent=response.text
  parsedhtml = BeautifulSoup(pagecontent, "html.parser")
  dfdict={'Topic':get_topics(parsedhtml),'Url':get_urllist(parsedhtml),'Description':get_descs(parsedhtml)}
  df=pd.DataFrame(dfdict)
  return df

def scrape_topics_repos():
  topic_df=scrape_topics()
  for index,row in topic_df.iterrows():
    print("scraping process number: {} topic name: {} url: {} ".format(index,row['Topic'],row['Url']))
    scrape_topic_one(row['Url'],row['Topic'])
    print("sucess process number {}".format(index))

if __name__ == '__main__':
    scrape_topics_repos()
