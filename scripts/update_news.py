import json,re,urllib.request
from xml.etree import ElementTree as ET
OUT="news.json"
SOURCES=[("Domain Incite","https://domainincite.com/feed"),("The gTLD Club","https://www.gtld.club/feeds/posts/default?alt=rss"),("DNW","https://domainnamewire.com/feed/")]
KEY=("gtld","icann","new domain","top-level domain","tld")
def fetch(u):
 r=urllib.request.Request(u,headers={"User-Agent":"gtld.click weekly updater/1.0"}); return urllib.request.urlopen(r,timeout=20).read()
def parse(source,url):
 root=ET.fromstring(fetch(url)); out=[]
 for i in root.findall(".//item")[:30]:
  t=(i.findtext("title") or "").strip(); l=(i.findtext("link") or "").strip(); d=re.sub("<[^>]+>"," ",i.findtext("description") or "").strip(); date=(i.findtext("pubDate") or "")[:16]
  if t and l and any(k in (t+" "+d).lower() for k in KEY): out.append({"title":t,"summary":re.sub(r"\s+"," ",d)[:280],"source":source,"date":date,"url":l})
 return out
try: current=json.load(open(OUT,encoding="utf-8"))
except: current=[]
found=[]
for s,u in SOURCES:
 try: found+=parse(s,u)
 except Exception: pass
seen=set(); merged=[]
for x in sorted(found+current,key=lambda x:x.get("date",""),reverse=True):
 k=(x.get("title","").lower(),x.get("source","").lower())
 if k not in seen: seen.add(k); merged.append(x)
json.dump(merged[:12],open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
