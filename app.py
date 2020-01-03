from flask import Flask ,jsonify, render_template
from consumer import consumer
from scraper import QuotesSpider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from mongoclient import mongoconnection
import json
import ujson


app = Flask(__name__)

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'


@app.route("/consume")
def consume():
    """
    call consumer.py
    """
    cons = consumer()
    return jsonify({"message":cons})
    
@app.route("/start_scrape")
def run_scraper():
    '''
    run the scraper to scrape the data
    '''
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        d = runner.crawl(QuotesSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run() # the script will block here until the crawling is finished
        return jsonify({"message":"scraper runned sucessfully"})
    except Exception as e:
        print(e)
        return jsonify({"message":"exception in run scrapper!"})    

@app.route("/data")
def data_table():
    conn = mongoconnection()
    cursor = conn.find({})
    l_scrape =[]
    for i in cursor:
        i.pop("_id")
        l_scrape.append(i)
    print(l_scrape)
    return jsonify({"data":l_scrape})   

if __name__ =="__main__":
    app.run(debug=True) 