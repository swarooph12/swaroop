import scrapy

class RedditSpider(scrapy.Spider):
	#spider name
	name = 'amazon'
	#list of allowed domains
	allowed_domains = ['www.amazon.in/s?k=Tents+-+Shelter+Lightspeed&ref=nb_sb_noss']
	#staring url for scraping
	start_urls = ['https://www.amazon.in/s?k=Tents+-+Shelter+Lightspeed&ref=nb_sb_noss']
	#location of csv file
	custom_settings = {
		'FEED_URI' : 'tmp/amazon.csv'
	}

	def parse(self, response):
		#Extracting the content using css selectors(earlier logic)
		titles = response.css('._eYtD2XCVieq6emjKBH3m::text').extract()
		votes = response.css('._1rZYMD_4xY3gRcSS3p8ODO::text').extract()
		times = response.css('._3jOxDPIQ0KaOWpzvSQo-1s::text').extract()
		comments = response.css('.FHCV02u6Cp2zYL0fhQPsO::text').extract()
		#Give the extracted content row wise.
		for item in zip(titles,votes,times,comments):
			#create a dictionary of title, vote, publish date and comments
			scraped_info = {
				'title' : item[0],
				'vote' : item[1],
				'created_at' : item[2],
				'comments' : item[3],
			}
			#yield or give the scraped info to scrapy
			yield scraped_info
