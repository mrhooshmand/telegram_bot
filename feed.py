import feedparser
import jdatetime
from datetime import datetime
import re




def getFeed(count=1):
    feeds = []
    NewsFeed = feedparser.parse('https://www.zoomit.ir/feed/')
    NewsFeed = NewsFeed['entries'][:count]
    for entry in NewsFeed:
        if entry.title and entry.link:
            description = entry.description if hasattr(entry, 'description') else ''
            text_only = re.sub(r'<[^>]*>', '', entry.summary)
            digest = text_only
            pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
            jd = jdatetime.datetime.fromgregorian(datetime=pub_date).strftime("%Y/%m/%d %H:%M")
            pattern = r'src="([^"]+)"'
            img_src = re.findall(pattern, entry.summary)[0]
            feeds.append({
                'title': entry.title,
                'link': entry.link,
                'description': description,
                'digest': digest,
                'published': jd,
                'img': img_src,
            })
    return feeds


getFeed()
