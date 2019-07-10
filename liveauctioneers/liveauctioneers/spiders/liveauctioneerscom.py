# -*- coding: utf-8 -*-
#不是规范C！O！D！E！R！
#有些注释是旧的网站（classic）的代码
#之后重构了或是补全注释了再更新吧

import scrapy
from scrapy import Spider, Request,Selector
from urllib.parse import urlencode
import datetime
import time
import json
import re
from lxml import etree
import requests
from liveauctioneers.items  import *
import pymysql
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC


class LiveauctioneerscomSpider(scrapy.Spider):
    name = 'liveauctioneerscom'
    allowed_domains = ['classic.liveauctioneers.com','www.liveauctioneers.com','item-api-prod.liveauctioneers.com','p1.liveauctioneers.com']
    start_urls = ['http://classic.liveauctioneers.com']
    # first_page='http://classic.liveauctioneers.com/c/{category}/1/?rows={rows}&sort={sort}&pagenum={page}'
    first_page='https://www.liveauctioneers.com/c/{category}/?page={page}&pageSize={rows}&sort={sort}'
    item_info_base='https://www.liveauctioneers.com/item/{item_id}'
    bidding_info_base='https://item-api-prod.liveauctioneers.com/spa/small/item/{item_id}/bidding?c=20170802'

    today=datetime.date.today()
    today_str=today.strftime('%Y-%m-%d')

    logging.basicConfig(filename='scarpy_{}.log'.format(today_str))

    facets_list=['','categories','creators','materialsTechniques','origins','stylePeriods']
    price_pattern=re.compile('(\D)(\d*)')
    item_id_pattern=re.compile('/item/(.*?)_.*')
    itemFacets_pattern=re.compile('itemFacets.*?"categories":\[(.*?)\],"creators":\[(.*?)\],"materialsTechniques":\[(.*?)\],"origins":\[(.*?)\],"stylePeriods":\[(.*?)\]')
    auctionType_pattern=re.compile('catalog":{"byId":{.*?:{"buyersPremium".*?"isCatalogOnly":(.*?),"isTimed":(.*?),')

    def datename_datetimeObjectTrans(self,input_date_str):
        judgedate=re.search('(\d) days Left',input_date_str,re.I)
        judgehour=re.search('(\d) hours Left',input_date_str,re.I)
        if judgedate:
            datetime_output=self.today+datetime.timedelta(days=int(judgedate.group(1)))
        elif judgehour:
            datetime_output=datetime.datetime.now()+datetime.timedelta(hours=int(judgehour.group(1)))
        else:
            datetime_output=datetime.datetime.strptime(('2019'+input_date_str),'%Y%b %d')
        return datetime_output

    def parse_itempage(self, response):
        """
        解析商品缩略主界面,找到今天所有拍卖的物品
        """
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='开始爬取第'+str(response.meta.get('page'))+'页'))
        today_item_number=0
        
        # target_day=datetime.datetime.now()+datetime.timedelta(days=self.settings.get('DURATION'))-datetime.timedelta(hours=15)
        # year=str(self.today.timetuple().tm_year)
        # month=datetime.datetime.strftime(target_day,'%b')
        # day=str(target_day.timetuple().tm_mday)
        # starting_date=month+' '+day
        # starting_date_int=int(year+datetime.datetime.strftime(target_day,'%m%d'))

        # #判断这一页是不是没有
        # last_item_date_str=year+response.xpath('string(//div[@class="mt25"][last()]//div[contains(@class,"item_box")][last()]//div[@class="datetimestamp"][2])').extract()[0]
        # last_item_date_int=int(datetime.datetime.strptime(last_item_date_str,'%Y%b %d').strftime('%Y%m%d'))
        # if starting_date_int<=last_item_date_int:
            # logging.info('----------------------------------------{info}----------------------------------------'.format(info='这一页有需要新爬取内容'))
            
            # dividors=response.xpath('//div[@class="mt25"]')
            # rows=len(dividors)
            # for i in range(1,rows+1):
            #     div_item=response.xpath('//div[@class="mt25"]['+str(i)+']//div[contains(@class,"item_box")]')
            #     columns=len(div_item)
            #     for j in range(1,columns+1):
            #         path='string(//div[@class="mt25"]['+str(i)+']//div[contains(@class,"item_box")]['+str(j)+']//div[@class="datetimestamp"][2])'

        starting_date=int((self.today+datetime.timedelta(days=self.settings.get('DURATION'))).strftime('%Y%m%d'))
        dividors=response.xpath('//div[@class="card___1ZynM cards___2C_7Z"]')
        if dividors:
            for i in range(1,len(dividors)+1):
                date_str=response.xpath('string(//div[@class="card___1ZynM cards___2C_7Z"][{num}]//span[@class="card-date___285QP"])'.format(num=i)).extract()[0]
                if date_str:
                    date=int(self.datename_datetimeObjectTrans(date_str).strftime('%Y%m%d'))
                    if starting_date==date and date:
                        if today_item_number<self.settings.get('MAX_ITEM'):
                            
                            today_item_number+=1
                            logging.info('----------------------------------------{info}----------------------------------------'.format(info='今天爬取的第'+str(today_item_number)+'个item'))
                            #获取商品id
                            href=response.xpath('string(//div[@class="card___1ZynM cards___2C_7Z"][{num}]//a[@class="link___ link-primary___ item-title___24bKg"]/@href)'.format(num=i)).extract()[0]
                            item_id=int(re.search(self.item_id_pattern,href).group(1))
                            
                            #爬取商品具体信息
                            logging.info('----------------------------------------{info}----------------------------------------'.format(info='爬取'+str(item_id)+'的具体信息'))
                            yield Request(self.item_info_base.format(item_id=item_id),headers=self.settings.get('HEADERS'),cookies=self.settings.get('COOKIES'),callback=self.parse_iteminfo,meta={'item_id':item_id,'cookiejar':1},dont_filter=True)
                            
                            #爬取商品交易信息
                            logging.info('----------------------------------------{info}----------------------------------------'.format(info='爬取'+str(item_id)+'今天的bidding信息'))
                            yield Request(self.bidding_info_base.format(item_id=item_id),callback=self.parse_itembiddinginfo,meta={'item_id':item_id})
                        else:
                            logging.info('----------------------------------------{info}----------------------------------------'.format(info='今天item已经爬取完，剩下跳过'))
                    else:
                        logging.info('----------------------------------------{info}----------------------------------------'.format(info='这是界面上不是今天要爬取的'))
                else:
                    logging.info('----------------------------------------{info}----------------------------------------'.format(info='这个物品没有交易时间'))

        # if (today_item_number<self.settings.get('MAX_ITEM') ) and (response.meta.get('page')<self.settings.get('MAX_PAGE') and (starting_date_int==last_item_date_int)):     
        if (today_item_number<self.settings.get('MAX_ITEM') ) and (response.meta.get('page')<response.meta.get('max_page') ):     
            #数量不够继续爬取
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='还没有达到指定数量，继续下一页'))
            page=response.meta.get('page')+1
            yield Request(self.first_page.format(category=response.meta.get('category'),sort=self.settings.get('SORT'),rows=self.settings.get('ROWS'),page=page),
            callback=self.parse_itempage,
            headers=self.settings.get('HEADERS'),
            meta={'category':response.meta.get('category'),'sort':'dateasc','rows':self.settings.get('ROWS'),'page':page,'max_page':response.meta.get('max_page')})
        elif today_item_number==self.settings.get('MAX_ITEM'):
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='今天数量已经达标'))
        else:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='超出页数索引'))
            # if starting_date_int<last_item_date_int:
            #     logging.info('----------------------------------------{info}----------------------------------------'.format(info='网页上所有今天的都被爬取了'))
            # else:
            #     logging.info('----------------------------------------{info}----------------------------------------'.format(info='今天数量已经达标'))

        # else:
        #     logging.info('----------------------------------------{info}----------------------------------------'.format(info='这一页没有可以爬取的'))
        #     page=response.meta.get('page')+1
        #     yield Request(self.first_page.format(category=self.category,sort=self.settings.get('SORT'),rows=self.settings.get('ROWS'),page=page),
        #     callback=self.parse_itempage,
        #     meta={'category':self.category,'sort':'dateasc','rows':self.settings.get('ROWS'),'page':page})
 
    def parse_iteminfo(self,response):
        """
        解析商品基本信息
        """
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='执行爬取'+str(response.meta.get('item_id'))+'的具体信息'))
        try:
            item_info=Liveauctioneers_ItemInfo()

            item_info['item_id']=response.meta.get('item_id')
            item_info['name']=response.xpath('string(//h1[@class="title___EAYj9"]/span)').extract()[0]

            floor_price=response.xpath('string(//span[@class="price___pIaPZ"]/span)').extract()[0].replace(',','')
            item_info['currency']=re.match(self.price_pattern,floor_price).group(1)
            item_info['floor_price']=re.match(self.price_pattern,floor_price).group(2)
            item_info['estimate_price_low']=re.match(self.price_pattern,response.xpath('string(//div[@class="estimateRow___376L-"]/span/span[1])').extract()[0].replace(',','')).group(2)
            item_info['estimate_price_high']=re.match(self.price_pattern,response.xpath('string(//div[@class="estimateRow___376L-"]/span/span[2])').extract()[0].replace(',','')).group(2)

            closing_datetime=response.xpath('string(//span[@class="strong___38gT9"])').extract()[0]
            datetimestamp=datetime.datetime.strptime(closing_datetime,'%a, %b %d, %Y %I:%M %p %Z')
            datetimestamp=datetimestamp+datetime.timedelta(hours=8)
            item_info['closing_date']=datetime.datetime.strftime(datetimestamp,'%Y-%m-%d')
            item_info['closing_time']=datetime.datetime.strftime(datetimestamp,'%H:%M:%S')

            premium=response.xpath('//ul[@class="buyers-premium___12Vqg"]//li')
            premium_info=''
            for i in range(1,len(premium)+1):
                premium_info+=response.xpath('string(//ul[@class="buyers-premium___12Vqg"]//li['+str(i)+'])').extract()[0]
                premium_info+=';'
            item_info['buyers_premium']=premium_info
            item_info['record_date']=self.today_str
            item_info['save_action_date']=(self.today+datetime.timedelta(days=random.choice([3,7]))).strftime('%Y-%m-%d')

            #生成实验组和对照组
            item_info['experiment_type']=random.randint(0,1)

            auctioneer_href=response.xpath('string(//div[@class="name___1vn-M"]/a/@href)').extract()[0]
            auctioneer_id=re.search('auctioneer/(\d*?)/',auctioneer_href).group(1)
            item_info['lot_number']=response.xpath('string(//span[@class="title item-link___2xkny"]/span)').extract()[0].replace('Lot ','')
            item_info['auctioneer_id']=auctioneer_id
            item_info['description']=response.xpath('string(//div[@class="description___TbjN2"]/div)').extract()[0]
            item_info['first_image_url']=response.xpath('string(//img[@class="image___2Qbmt"]/@src)').extract()[0].split('?')[0]
            
            #需要正则匹配的信息
            response_text=response.text
            itemFacets=re.search(self.itemFacets_pattern,response_text)
            for i in range(1,6):
                facet_string=itemFacets.group(i).replace('\"','')
                facet_name=self.facets_list[i]
                item_info[facet_name+'1_1']=item_info[facet_name+'1_2']=item_info[facet_name+'2_1']=item_info[facet_name+'2_2']=''
                if facet_string:
                    l1_categories=re.findall('l1CategoryName:(.*?),',facet_string)
                    l1_len=min(2,len(l1_categories))
                    for j in range(0,l1_len):
                        item_info[facet_name+'1_'+str(j+1)]=l1_categories[j]
                    l2_categories=re.findall('l2CategoryName:(.*?),',facet_string)
                    l2_len=min(2,len(l2_categories))
                    for j in range(0,l2_len):
                        item_info[facet_name+'2_'+str(j+1)]=l2_categories[j]

            auction_type_result=re.search(self.auctionType_pattern,response_text)
            if auction_type_result.group(1)=='true':
                item_info['auction_type']='BrowseOnly'
            elif auction_type_result.group(2)=='true':
                item_info['auction_type']='Timed'
            else:
                item_info['auction_type']='Live'
            yield item_info
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='基本信息获取有误'))

        #拍卖商信息
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='获取对应拍卖商基本信息'))
        try:
            auctioneer_info=Liveauctioneers_AuctioneersInfo()
            auctioneer_info['auctioneer_id']=auctioneer_id
            auctioneer_info['name']=response.xpath('string(//div[@class="name___1vn-M"]/a)').extract()[0]
            auctioneer_info['location']=response.xpath('string(//div[@class="address___2hK24 address___11j7p"]/div)').extract()[0]
            if response.xpath('//span[@class="top-badge___2QYfO"]'):
                auctioneer_info['whether_top']='ture'
            else:
                auctioneer_info['whether_top']='false'
            yield auctioneer_info
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='拍卖商基本信息获取有误'))

        #拍卖商粉丝信息
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='获取拍卖商粉丝信息'))
        try:
            post_data={"sellerIds":[int(auctioneer_id)]}
            r=requests.post('https://item-api-prod.liveauctioneers.com/follower-count/?c=20170802',json=post_data)
            r_json=json.loads(r.text)

            auctioneer_followers=Liveauctioneers_AuctioneersFollowers()
            auctioneer_followers['auctioneer_id']=auctioneer_id
            auctioneer_followers['followers']=r_json.get('data')[0].get(auctioneer_id)
            auctioneer_followers['record_date']=self.today_str
            auctioneer_followers['record_time']=datetime.datetime.now().strftime('%H:%M:%S')
            yield auctioneer_followers
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='拍卖商粉丝信息有误'))

    def parse_itembiddinginfo(self,response):
        """
        解析商品当日交易信息
        """
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='获取item：'+str(response.meta.get("item_id"))+'的bidding信息'))
        try:
            item_bidding_info=Liveauctionners_item_bidding_overview()
            #获取watching人数
            post_data={"ids":[response.meta.get('item_id')]}
            r=requests.post('https://item-api-prod.liveauctioneers.com/saved-items/count?c=20170802',json=post_data)
            r_json=json.loads(r.text)
            item_bidding_info['bidders_watching']=r_json.get('data').get('savedItemCounts')[0].get('savedCount')

            item_bidding_info['current_day_date']=self.today_str
            item_bidding_info['current_day_time']=datetime.datetime.now().strftime('%H:%M:%S')

            #获取其他字段
            result=json.loads(response.text)
            field_map={'item_id':'itemId','bids_now':'bidCount','whether_sold':'isSold','sold_price':'salePrice'}
            for field, attr in field_map.items():
                item_bidding_info[field]=result.get('data')[0].get(attr)
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='商品bidding信息获取有误'))

        yield item_bidding_info
        
        #如果已经成交则单独记录成交信息
        if result.get('data')[0].get('isSold')==True:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='商品已经成交,记录每次拍卖详情'))
            yield Request(self.item_info_base.format(item_id=response.meta.get('item_id')),callback=self.parse_auctioninfo,headers=self.settings.get('HEADERS'),meta={'item_id':response.meta.get('item_id')})

    def parse_auctioninfo(self,response):
        """
        爬取具体交易信息
        """
        logging.info('----------------------------------------{info}----------------------------------------'.format(info='记录已经成交商品：'+str(response.meta.get("item_id"))+'信息'))
        try:
            pattern=re.compile('"amount":(.*?),"bidderId":(.*?),"currency":"(.*?)","source":"(.*?)"')
            results=re.findall(pattern,response.text)
            number_of_results=len(results)
            item_id=response.meta.get("item_id")
            for result in results:
                item_auction_info=Liveauctioneers_ItemAuctionInfo()
                item_auction_info["item_id"]=item_id
                item_auction_info["bidding_number"]=number_of_results
                item_auction_info["bidding_type"]=result[3]
                item_auction_info["bidding_price"]=result[0]
                item_auction_info["bidding_currency"]=result[2]
                item_auction_info["bidder_id"]=result[1]
                number_of_results-=1
                yield item_auction_info
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='成交信息获取失败'))

    def parse_saveAndFollowToday(self,response):
        """
        save操作与跟踪bidding信息
        """
        #对今天开始操作
        try:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='连接数据库'))
            db=pymysql.connect(host=self.settings.get('MYSQL_HOST'),database=self.settings.get('MYSQL_DATABASE'),user=self.settings.get('MYSQL_USER'),password=self.settings.get('MYSQL_PASSWORD'),port=self.settings.get('MYSQL_PORT'))
            cursor=db.cursor()
            sql_need_to_be_saved='SELECT item_id FROM items_info WHERE save_action_date=date_format("{date}","%Y-%m-%d")  AND experiment_type=1;'.format(date=self.today_str)
            cursor.execute(sql_need_to_be_saved)
            item_need_to_be_save=[]
            items=cursor.fetchall()
            if items:
                for item in items:
                    logging.info('----------------------------------------{info}----------------------------------------'.format(info='待保存：'+str(item[0])))
                    item_need_to_be_save.append(int(item[0]))
            else:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='没有要保存的item'))

            logging.info('----------------------------------------{info}----------------------------------------'.format(info='生成浏览器'))

            chrome_options = webdriver.chrome.options.Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option('prefs',prefs)
            browser=webdriver.Chrome(options=chrome_options)
            # browser=webdriver.Chrome()


            for i in range(self.settings.get('NUMBER_OF_ACCOUNTS')):
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='开始登陆账号'+str(i)))

                browser.get('https://www.liveauctioneers.com')
                wait=WebDriverWait(browser,120)
                enter=wait.until(EC.presence_of_element_located((By.XPATH,'//a[@class="link___ link-primary-weak___ link-default___3gIWR"]')))
                enter.click()
                name=wait.until(EC.presence_of_element_located((By.XPATH,'//input[@class="form-control form-control"]')))
                name.send_keys('Liveauctioneers_spider{number}@outlook.com'.format(number=i+1))
                password=browser.find_element_by_xpath('//input[@class="form-control recordingExclude form-control"]')
                password.send_keys('nospiderpassword{number}'.format(number=i+1))
                login_button=browser.find_element_by_xpath('//button[@class="button___ button-primary-red___ button-primary___ submit___1XYKo"]')
                login_button.click()
                cookies=browser.get_cookies()
                browser.delete_all_cookies()

                logging.info('----------------------------------------{info}----------------------------------------'.format(info='设置cookies'))
                for cookie in cookies:
                    browser.add_cookie(cookie)

                browser.get('https://www.liveauctioneers.com')

                for j in range(len(item_need_to_be_save)):
                    logging.info('----------------------------------------{info}----------------------------------------'.format(info='账号'+str(i)+'的保存item操作'))
                    item_id=item_need_to_be_save[j]
                    if  random.randint(0,1):    
                        logging.info('----------------------------------------{info}----------------------------------------'.format(info='决定保存：'+str(item_id)))
                        
                        #执行操作
                        try:
                            browser.get(self.item_info_base.format(item_id=item_need_to_be_save[j]))
                            flag_saveItem=flag_itemSaved=True
                            savecode=0
                            
                            try:
                                save_item=browser.find_element_by_xpath('//button[@class="button___ button-secondary-blue___ button-secondary___ button___A-PDg"]')
                            except:
                                flag_saveItem=False
                            try:
                                item_saved=browser.find_element_by_xpath('//button[@class="button___ button-secondary-blue___ button-secondary___ button___A-PDg undefined"]')
                            except:
                                flag_itemSaved=False
                            
                            try:
                                watching_before_text=browser.find_element_by_xpath('//div[@class="message-wrapper___3kM-l"]/span').text
                                watching_before=int(re.search('(\d) bidders watching this item',watching_before_text,re.I).group(1))
                            except: 
                                watching_before=0

                            if flag_saveItem:
                                AC(browser).move_to_element(save_item).move_by_offset(5,5).click().perform()
                                time.sleep(5)
                                savecode=1

                                loop_flag=True
                                try:
                                    watching_after_text=browser.find_element_by_xpath('//div[@class="message-wrapper___3kM-l"]/span').text
                                    watching_after=int(re.search('(\d) bidders watching this item',watching_after_text,re.I).group(1))
                                except: 
                                    watching_after=0
                                    savecode=5

                                if watching_before+1>=watching_after:
                                    pass
                                else:
                                    sleep(5)
                                    savecode=4

                            elif flag_itemSaved:
                                logging.info('----------------------------------------{info}----------------------------------------'.format(info='商品之前已经被保存了：'+str(item_id)))
                                savecode=2
                            else:
                                logging.info('----------------------------------------{info}----------------------------------------'.format(info='保存出了点问题1：'+str(item_id)))
                        except:
                            logging.info('----------------------------------------{info}----------------------------------------'.format(info='保存出了点问题3：'+str(item_id)))

                        #保存记录
                        logging.info('----------------------------------------{info}----------------------------------------'.format(info='save_item记录进入数据库'))
                        accounts_saved_info=Liveauctioneers_AccountsSavedInfo()
                        accounts_saved_info['account_id']=i
                        accounts_saved_info['item_id']=item_id
                        accounts_saved_info['record_date']=self.today_str
                        accounts_saved_info['record_time']=datetime.datetime.now().strftime('%H:%M:%S')
                        accounts_saved_info['save_code']=savecode
                        yield accounts_saved_info
                        logging.info('----------------------------------------{info}----------------------------------------'.format(info='保存操作完成：'+str(item_id)))
                    else:
                        logging.info('----------------------------------------{info}----------------------------------------'.format(info='不决定保存该item'))

                browser.delete_all_cookies()
            browser.close()
                    
            # 生成持续跟踪物品信息爬取
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='抓取历史item每日bidding信息'))
            sql_follow_today='SELECT item_id FROM items_info WHERE closing_date-1>=date_format("{date}","%Y-%m-%d")+1 AND record_date<date_format("{date}","%Y-%m-%d");'.format(date=self.today_str)
            cursor.execute(sql_follow_today)
            items_follow_today=cursor.fetchall()
            if items_follow_today:
                for item in items_follow_today:
                    yield Request(self.bidding_info_base.format(item_id=item[0]),callback=self.parse_itembiddinginfo,meta={'item_id':item[0]})
            else:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='没有需要抓取历史item每日bidding信息'))

            db.close()
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info=self.today_str+':出错：数据库，已经被保存或其他'))
            
    def parse_dichoFindPage(self,response):

        logging.info('----------------------------------------{info}----------------------------------------'.format(info='开始寻找最优初始界面'))
        #寻找最大页码
        a=1
        b=int(response.xpath('string(//ul[@class="paginator___35V-U paginator___3_KwX"]//li[last()-1]/a)').extract()[0])
        max_page=b
        flag=True

        #死循环直到找到合适页码
        while flag:
            mid_page=int((a+b)/2)
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='中值为'+str(mid_page)))

            page_info=requests.get(self.first_page.format(category=response.meta.get('category'),sort=self.settings.get('SORT'),rows=self.settings.get('ROWS'),page=mid_page),headers=self.settings.get('HEADERS'))
            compare_result=self.parse_comparePage(page_info)

            if compare_result==1:
                a=mid_page
            elif compare_result==2:
                b=mid_page
            elif compare_result==3:
                b=b+2
            elif compare_result==0:
                flag=False

            if b-a<=1:
                flag=False
            
        #找到最优化后以此页为基础爬取
        if not flag:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='找到最优化界面开始爬取界面'+str(mid_page)))
            yield Request(self.first_page.format(category=response.meta.get('category'),sort=self.settings.get('SORT'),rows=self.settings.get('ROWS'),page=mid_page),
                callback=self.parse_itempage,
                headers=self.settings.get('HEADERS'),
                meta={'category':response.meta.get('category'),'sort':'dateasc','rows':self.settings.get('ROWS'),'page':mid_page,'max_page':max_page})
            
    def parse_comparePage(self,response):
        #判定范围是前一天或者两天
        equal_condition_low=int((self.today+datetime.timedelta(days=self.settings.get('DURATION'))-datetime.timedelta(days=self.settings.get('LOWER_BOUND'))).strftime('%Y%m%d'))
        equal_condition_high=int((self.today+datetime.timedelta(days=self.settings.get('DURATION'))-datetime.timedelta(days=self.settings.get('UPPER_BOUND'))).strftime('%Y%m%d'))

        selector=Selector(text=response.text)
        last_item_date_str=selector.xpath('string(//div[@class="card___1ZynM cards___2C_7Z"][last()]//span[@class="card-date___285QP"])').extract_first()

        if last_item_date_str:
            last_item_date=self.datename_datetimeObjectTrans(last_item_date_str)
            last_item_date=int(last_item_date.strftime('%Y%m%d'))
            if last_item_date<equal_condition_low:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='中间值小了'))
                return 1
            elif last_item_date>equal_condition_high:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='中间值大了'))
                return 2
            else:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='满足要求'))
                return 0
        else:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='奇怪的商品'))
            return 3

    def start_requests(self):
        """
        请求开始
        """
        logging.info('----------------------------------------{info}----------------------------------------'.format(info=self.today_str+':爬虫开始运行'))

        try:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='开始保存操作与抓过去item拍卖次数'))
            yield Request(url='https://www.liveauctioneers.com',callback=self.parse_saveAndFollowToday,priority=1,headers=self.settings.get('HEADERS'))
        except:
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='保存或者抓取中有错'))

        # 获取当日新数据
        for i in range(0,len(self.settings.get('CATEGORIES'))):
            category=self.settings.get('CATEGORIES')[i]
            logging.info('----------------------------------------{info}----------------------------------------'.format(info='开始获取今日新{}item'.format(category)))
            try:
                yield Request(self.first_page.format(category=category,sort=self.settings.get('SORT'),rows=self.settings.get('ROWS'),page=1),
                callback=self.parse_dichoFindPage,
                headers=self.settings.get('HEADERS'),
                meta={'category':category,'sort':'dateasc','rows':self.settings.get('ROWS'),'page':1})
            except:
                logging.info('----------------------------------------{info}----------------------------------------'.format(info='今日新{}item获取过程有误'.format(category)))

        