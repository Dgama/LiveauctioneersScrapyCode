from lxml import etree
import urllib.request
import re
import datetime
import requests
import json
import time
from urllib.parse import quote
import pymysql
import random


# today=datetime.date.today()
# today_compare=today.strftime('%b %d')
# reponse=urllib.request.urlopen('http://classic.liveauctioneers.com/c/art/1/?sort=dateasc&rows=24')
# html=etree.parse(reponse,etree.HTMLParser())
# rel=html.xpath('string(//div[@class="mt25"][1]//div[contains(@class,"item_box")][1]/@rel)')
# print(rel)
# dividors=html.xpath('//div[@class="mt25"]')
# rows=len(dividors)
# for i in range(1,rows+1):
#     div_item=html.xpath('//div[@class="mt25"]['+str(i)+']//div[contains(@class,"item_box")]')
#     columns=len(div_item)
#     for j in range(1,columns+1):
#         path='string(//div[@class="mt25"]['+str(i)+']//div[contains(@class,"item_box")]['+str(j)+']//div[@class="datetimestamp"][2])'
#         date=html.xpath(path)
#         if today_compare==date:
#             print('match')
#         else:
#             print('not match')
# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# request=urllib.request.Request(url='https://www.liveauctioneers.com/item/72312039',headers=headers)
# response=urllib.request.urlopen(request)
# html=etree.parse(response,etree.HTMLParser())
# result=html.xpath('string(//div[@class="price___pIaPZ"]/span)')
# res2=html.xpath('//div[@class="price___pIaPZ"]/span')
# print('hhh'+result)
# print(res2)

#模拟登陆
# login_url='https://item-api-prod.liveauctioneers.com/auth/spalogin?c=20170802'
# session=requests.Session()
# headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# 'Referer':'http://www.liveauctioneers.com/'}
# post_data={
#     'password':'Redback1020',
#     'username':'1413476657@qq.com'
# }
# response=session.post(login_url,data=post_data,headers=headers)
# resp2=session.get('https://www.liveauctioneers.com/item/72312039_1867-kkk-ku-klux-klan-lynching-reward-robe-pin',headers=headers)
# if resp2.status_code==200:
#     html=etree.HTML(resp2.text)
#     print(html.xpath('//div[@class="table-cell___2ekBD"]'))

# print(time.strftime('%Y-%m-%d',time.localtime(1561891177)))

# data={"ids":[72936034]}
# headers2={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# 'Referer':'https://www.liveauctioneers.com/item/72936034_francis-bacon-british-expressionist-oil-on-paper',
# 'Content-Type':' application/json; charset=utf-8'}

# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# 'cookie': 'ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; aJS=no; JS=no; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; join-modal-last-seen=2019-06-30; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; ki_t=1561596784612%3B1561888361382%3B1561901238485%3B4%3B68; sailthru_content=e1cd400e88231be1228745002a8b5fc8c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b01660f86a4ad18c08e22e7f125847c743e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e648e8f3cbb938790a8bf18bf709670ce177cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae109; lastRskxRun=1561901240149; RT="z=1&dm=www.liveauctioneers.com&si=0x9cub3zrwjf&ss=jxiz3jnj&sl=4&tt=ns2&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=klwj&ul=2d3yn'}
# r=requests.get(url='https://www.liveauctioneers.com/item/72312039',headers=headers)
# print(r.text)
# # print(response.read())
# html=etree.parse(r,etree.HTMLParser())
# # print(html)
# result=html.xpath('string(//h1[@class="live_item_header___3p3ha"]//span)')
# print(result)

# cookie={
  # {name="ajs_group_id",value="null'},
  # {name="_ga",value="GA1.2.702269890.1561596772"},
  # {name=" _gid",value="GA1.2.1319034618.1561596772"},
  # {name="_gaexp",value="GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1"},
  # {name="__stripe_mid",value="1e116401-2ddb-4347-91c4-f867cf51d4ea"},
  # {name="cto_lwid",value="44b2c8a5-4ba4-4456-bdc5-bc388b9fca83"},
  # {name="ajs_anonymous_id",value="%22ef3a5847-2d25-431d-a51e-8778b609070c%22"},
  # {name="sailthru_visitor",value="99da3d35-168f-45dc-8e6a-9ca3197bf55b"},
  # {name="ki_r",value=""},
  # {name="rskxRunCookie",value="0"},
  # {name="rCookie",value="xfhduhawoibc2hgmdf7p9k"},
  # {name="bidder-has-logged-in",value="true"},
  # {name="pagination-page-size",value="120"},
  # {name="aJS",value="no"},
  # {name="JS",value="no"},
  # {name="optimizelyEndUserId",value="oeu1561685890151r0.4308360687264412"},
  # {name="__utmz",value="118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376"},
  # {name="__qca",value="P0-242406864-1561685890483"},
  # {name="location",value="%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D"},
  # {name="ip_country",value="CN"},
  # {name="SnapABugHistory",value="1#"},
  # {name="last_logged_in_user",value="Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110"},
  # {name="join-modal-last-seen",value="2019-06-30"},
  # {name="_session_id",value="c7fdff05-ae14-4228-9c13-b89553bb8114"},
  # {name="__utma",value="118153238.702269890.1561596772.1561816152.1561888265.7"},
  # {name="__utmc",value="118153238"},
  # {name="la_latest_lots",value="%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D"},
  # {name="ajs_user_id",value="2829818"},
  # {name="ki_t",value="1561596784612%3B1561888361382%3B1561901238485%3B4%3B68"},
  # {name="sailthru_content",value="e1cd400e88231be1228745002a8b5fc8c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b01660f86a4ad18c08e22e7f125847c743e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e648e8f3cbb938790a8bf18bf709670ce177cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae109"},
  # {name="lastRskxRun",value="1561901240149"},
  # {name="RT",value='z=1&dm=www.liveauctioneers.com&si=0x9cub3zrwjf&ss=jxiz3jnj&sl=4&tt=ns2&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=klwj&ul=2d3yn"'}
  # }




# script='''
# function main(splash)
#   splash:set_custom_headers({
#     ["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
#     })
#   splash:init_cookies({
#     {name="ajs_group_id",value="null"},
#     {name="_ga",value="GA1.2.702269890.1561596772"},
#     {name=" _gid",value="GA1.2.1319034618.1561596772"},
#     {name="_gaexp",value="GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1"},
#     {name="__stripe_mid",value="1e116401-2ddb-4347-91c4-f867cf51d4ea"},
#     {name="cto_lwid",value="44b2c8a5-4ba4-4456-bdc5-bc388b9fca83"},
#     {name="ajs_anonymous_id",value="%22ef3a5847-2d25-431d-a51e-8778b609070c%22"},
#     {name="sailthru_visitor",value="99da3d35-168f-45dc-8e6a-9ca3197bf55b"},
#     {name="ki_r",value=""},
#     {name="rskxRunCookie",value="0"},
#     {name="rCookie",value="xfhduhawoibc2hgmdf7p9k"},
#     {name="bidder-has-logged-in",value="true"},
#     {name="pagination-page-size",value="120"},
#     {name="aJS",value="no"},
#     {name="JS",value="no"},
#     {name="optimizelyEndUserId",value="oeu1561685890151r0.4308360687264412"},
#     {name="__utmz",value="118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376"},
#     {name="__qca",value="P0-242406864-1561685890483"},
#     {name="location",value="%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D"},
#     {name="ip_country",value="CN"},
#     {name="SnapABugHistory",value="1#"},
#     {name="last_logged_in_user",value="Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110"},
#     {name="join-modal-last-seen",value="2019-06-30"},
#     {name="_session_id",value="c7fdff05-ae14-4228-9c13-b89553bb8114"},
#     {name="__utma",value="118153238.702269890.1561596772.1561816152.1561888265.7"},
#     {name="__utmc",value="118153238"},
#     {name="la_latest_lots",value="%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D"},
#     {name="ajs_user_id",value="2829818"},
#     {name="ki_t",value="1561596784612%3B1561888361382%3B1561901238485%3B4%3B68"},
#     {name="sailthru_content",value="e1cd400e88231be1228745002a8b5fc8c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b01660f86a4ad18c08e22e7f125847c743e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e648e8f3cbb938790a8bf18bf709670ce177cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae109"},
#     {name="lastRskxRun",value="1561901240149"},
#     {name="RT",value='z=1&dm=www.liveauctioneers.com&si=0x9cub3zrwjf&ss=jxiz3jnj&sl=4&tt=ns2&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=klwj&ul=2d3yn"'}
#     })
#   assert(splash:go("https://www.liveauctioneers.com/item/72312039"))
#   return {
#     png=splash:png(),
#     html = splash:html()
#   }
# end
# '''

# url='http://localhost:8050/execute?lua_source='+quote(script)
# response=requests.get(url)
# print(response.text)

# import http.cookiejar

# cookie=http.cookiejar.CookieJar()
# handler=urllib.request.HTTPCookieProcessor(cookie)
# opener=urllib.request.build_opener(handler)
# response=opener.open("http://www.liveauctioneers.com")
# for item in cookie:
#   print(item.name+"="+item.value)

# cookies='ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; aJS=no; JS=no; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-01; ki_t=1561596784612%3B1561947391628%3B1561956599649%3B5%3B74; sailthru_content=c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae1091660f86a4ad18c08e22e7f125847c74348e8f3cbb938790a8bf18bf709670ce1d296e1e375f653cad6f982362e365811; lastRskxRun=1561956600876; RT="z=1&dm=www.liveauctioneers.com&si=lrdka89whi&ss=jxjrgcw5&sl=0&tt=0&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=72c&ul=96q5g&hd=96qvp"'
# jar=requests.cookies.RequestsCookieJar()
# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# for cookie in cookies.split(";"):
#   key,value=cookie.split("=",1)
#   jar.set(key,value)
# cookies2=dict([l.split("=",1) for l in cookies.split(";")])
# print(cookies2)
# r=requests.get("https://www.liveauctioneers.com/item/72312039_1867-kkk-ku-klux-klan-lynching-reward-robe-pin",cookies=jar,headers=headers)
# html=etree.HTML(r.text)
# a=html.xpath('//div[@class="table-cell___2ekBD"]')
# print(a)
# string=''
# for i in range(1,len(a)+1):
#   string+=html.xpath('string(//ul[@class="buyers-premium___12Vqg"]//li['+str(i)+'])')
#   string+=';'

# print(string)

# print(html.xpath('//ul[@class="buyers-premium___12Vqg"]/text()'))

# r=requests.get('https://www.liveauctioneers.com/item/72312039_1867-kkk-ku-klux-klan-lynching-reward-robe-pin',headers=headers)
# html=etree.HTML(r.text)
# print(r.status_code)


# login_url='https://item-api-prod.liveauctioneers.com/auth/spalogin?c=20170802'
# session=requests.Session()
# headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# 'Referer':'http://www.liveauctioneers.com/'}
# post_data={
#     'password':'Redback1020',
#     'username':'1413476657@qq.com'
# }

# cookies='ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-01; __stripe_sid=5acd003d-a062-411e-aca8-b5289ffd85c5; _gat=1; sailthru_pageviews=3; sailthru_content=c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b6048e8f3cbb938790a8bf18bf709670ce1d296e1e375f653cad6f982362e365811c97e884180c8b3e40c6678af6ccae1091660f86a4ad18c08e22e7f125847c743; ki_t=1561596784612%3B1561947391628%3B1561988107170%3B5%3B81; lastRskxRun=1561988108247; bidder-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYmlkZGVyIiwiaWF0IjoxNTYxOTg4MTM0LCJleHAiOjE1NjcxNzIxMzQsImlzcyI6Iml0ZW0tYXBpIiwic3ViIjoiMjgyOTgxOCJ9.5kYpLAJO0KAC3uLeiCbXnBpG3OrQnm5xVC1WgT6j5MY; 5Xq_name=Evans%20Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; 5Xq_nuid=2829818%3A%3A%3Ab8ca267f47fe88dc529f5e65e5e098fa; 5Xq_nverify=055adb9b7ff485302e035dca15a11f75%3A%3A%3A0db0f432361a660ec0b72c0c43d87fc1; RT="z=1&dm=www.liveauctioneers.com&si=2wlbm4i3cgx&ss=jxkdvqi3&sl=a&tt=xij&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=1ibbj&nu=d41d8cd98f00b204e9800998ecf8427e&cl=1iu1h&ul=1izqw"'
# # cookies='ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; aJS=no; JS=no; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-01; ki_t=1561596784612%3B1561947391628%3B1561956599649%3B5%3B74; sailthru_content=c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae1091660f86a4ad18c08e22e7f125847c74348e8f3cbb938790a8bf18bf709670ce1d296e1e375f653cad6f982362e365811; lastRskxRun=1561956600876; RT="z=1&dm=www.liveauctioneers.com&si=lrdka89whi&ss=jxjrgcw5&sl=0&tt=0&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=72c&ul=96q5g&hd=96qvp"'
# jar=requests.cookies.RequestsCookieJar()
# # jar=session.cookies.RequestsCookieJar()
# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# for cookie in cookies.split(";"):
#   key,value=cookie.split("=",1)
#   jar.set(key,value)

# # response=session.post(login_url,data=post_data,headers=headers)
# # print(response.text)
# # session.cookies.update(jar)

# headers2={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# "cookies":'ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-01; __stripe_sid=5acd003d-a062-411e-aca8-b5289ffd85c5; _gat=1; sailthru_pageviews=3; sailthru_content=c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b6048e8f3cbb938790a8bf18bf709670ce1d296e1e375f653cad6f982362e365811c97e884180c8b3e40c6678af6ccae1091660f86a4ad18c08e22e7f125847c743; ki_t=1561596784612%3B1561947391628%3B1561988107170%3B5%3B81; lastRskxRun=1561988108247; bidder-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYmlkZGVyIiwiaWF0IjoxNTYxOTg4MTM0LCJleHAiOjE1NjcxNzIxMzQsImlzcyI6Iml0ZW0tYXBpIiwic3ViIjoiMjgyOTgxOCJ9.5kYpLAJO0KAC3uLeiCbXnBpG3OrQnm5xVC1WgT6j5MY; 5Xq_name=Evans%20Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; 5Xq_nuid=2829818%3A%3A%3Ab8ca267f47fe88dc529f5e65e5e098fa; 5Xq_nverify=055adb9b7ff485302e035dca15a11f75%3A%3A%3A0db0f432361a660ec0b72c0c43d87fc1; RT="z=1&dm=www.liveauctioneers.com&si=2wlbm4i3cgx&ss=jxkdvqi3&sl=a&tt=xij&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=1ibbj&nu=d41d8cd98f00b204e9800998ecf8427e&cl=1iu1h&ul=1izqw"'}
# cookies2=dict([l.split("=",1) for l in cookies.split(";")])
# requests.utils.add_dict_to_cookiejar(session.cookies,cookies2)
# resp2=session.get('https://www.liveauctioneers.com/item/72312039',headers=headers)
# # resp2=requests.get('https://www.liveauctioneers.com/item/72312039',headers=headers2)
# if resp2.status_code==200:
#     html=etree.HTML(resp2.text)
#     print(resp2.headers)
#     print('cookies:\n')
#     print(resp2.cookies.get_dict())
#     # print(resp2.text)
#     print(html.xpath('string(//span[@class="price___pIaPZ"]/span/span)'))
#     print(html.xpath('string(//div[@class="logged-in___qXAGK"]//span[@class="title me___g_Mmv"]/span)'))
# else:
#     print('wrong')

#important!!!!!!
# url="https://p1.liveauctioneers.com/5791/144135/72888501_1_x.jpg?auto=webp&format=pjpg&version=1560632411"
# file_name=re.search('.*/(.*?)\?.*',url)
# print(file_name.group(1))
# ttt='https://www.liveauctioneers.com/auctioneer/6629/south-florida-auction-and-estate-sale-services-inc/'
# retttt=re.search('auctioneer/(\d*?)/,',ttt)
# print
# for i in range(1,6):
#     print(i)
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# cookies ='ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-02; bidder-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYmlkZGVyIiwiaWF0IjoxNTYyMDMyNDMzLCJleHAiOjE1NjcyMTY0MzMsImlzcyI6Iml0ZW0tYXBpIiwic3ViIjoiMjgyOTgxOCJ9.6QwVwBIKPoUsApgkQP8YEnp7aG18iG3lapHCUNVg6q8; 5Xq_name=Evans%20Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; 5Xq_nuid=2829818%3A%3A%3Ab8ca267f47fe88dc529f5e65e5e098fa; 5Xq_nverify=055adb9b7ff485302e035dca15a11f75%3A%3A%3A0db0f432361a660ec0b72c0c43d87fc1; __stripe_sid=485c050c-66d2-49b5-8a68-635ff477afad; sailthru_pageviews=1; _gat=1; ki_t=1561596784612%3B1562050248611%3B1562050248611%3B7%3B93; _session_id=26563b72-ca00-41d0-97d4-d5438c2d5180; sailthru_content=d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b6048e8f3cbb938790a8bf18bf709670ce1c97e884180c8b3e40c6678af6ccae109c4a314b84df41725b3f517e98ffd41f12b64bc03c38ed1e1f0303fb4ab93b980d296e1e375f653cad6f982362e3658111660f86a4ad18c08e22e7f125847c743; lastRskxRun=1562050249940; RT="z=1&dm=www.liveauctioneers.com&si=x7ruvxy7o2r&ss=jxlgdvjv&sl=2&tt=49i&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=2y0&ul=k81"'
# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# post_data={
#     'password':'Redback1020',
#     'username':'1413476657@qq.com'
# }
# login_url='https://item-api-prod.liveauctioneers.com/auth/spalogin?c=20170802'

# session=requests.Session()
# response=session.post(login_url,data=post_data,headers=headers)

# jar= requests.cookies.RequestsCookieJar()
# for cookie in cookies.split(";"):
#     key,value=cookie.split("=",1)
#     jar.set(key,value)
# session.cookies=jar

# response=session.get('https://www.liveauctioneers.com/item/72312039')
# response=requests.get('https://www.liveauctioneers.com/item/72936248')
# html=etree.HTML(response.text)
# a=html.xpath('//div[@class="hhh"]')
# if a:
#     print('have')
# else:
#     print('dont')
# print(session.headers)
# print(session.cookies.values())
# print(response.status_code)
# print(response.cookies)
# pattern=re.compile('"amount":(.*?),"bidderId":(.*?),"currency":"(.*?)","source":"(.*?)"')
# str_item='itemFacets.*?{"categories":.*?"l1CategoryName":(.*?),.*?"l2CategoryName":(.*?),.*?"l3CategoryName":(.*?),.*?"l4CategoryName":(.*?),.*?'
# ppp='catalog":{"byId":{.*?:{"buyersPremium".*?"isCatalogOnly":(.*?),"isTimed":(.*?),'
# content_pattern='itemFacets.*?"categories":\[(.*?)\],"creators":\[(.*?)\],"materialsTechniques":\[(.*?)\],"origins":\[(.*?)\],"stylePeriods":\[(.*?)\]'
# str_item2=',"creators":[],"materialsTechniques":[{"l1CategoryId":25834,"l1CategoryLabel":"Paper","l1CategoryName":"Paper","l1CategoryUrl":"paper"}],"origins":[{"categoryId":117,"l1CategoryId":117,"l1CategoryLabel":"American Antique","l1CategoryName":"American","l1CategoryUrl":"american","l2CategoryId":null,"l2CategoryLabel":null,"l2CategoryName":null,"l2CategoryUrl":null,"l3CategoryId":null,"l3CategoryLabel":null,"l3CategoryName":null,"l3CategoryUrl":null,"l4CategoryId":null,"l4CategoryLabel":null,"l4CategoryName":null,"l4CategoryUrl":null}],"stylePeriods":[{"l1CategoryId":290,"l1CategoryLabel":"Modern","l1CategoryName":"Modern","l1CategoryUrl":"modern"}'
# '"loaded":{"72936248":1562210369641},"loading":[]},"itemShipping":{"byId":{"72936248":{"domesticFlatShipping":null,"itemId":72936248}},"loaded":{"72936248":1562210369638},"loading":[]},"landingPage":{"metaData":{"pageLabel":"","pageMetaDescription":"","pageMetaKeywords":"","pageTitle":""}},"listingAgent":{"byId":{},"loaded":{},"loading":[]},"liveBid":{"bidderHasHighBid":false,"submitted":false,"success":false},"liveCatalogStatus":{"loaded":{},"loading":[]},"liveItemStatus":{"byId":{}},"loaded":{"loaded":{"catalog-bidding-info-144235":1562210369755},"loading":[]},"location":{"error":false,"errorMessage":null,"location":"","submitted":false,"success":false,"timestamp":null},"login":{"error":false,"errorMessage":"","submitted":false,"success":false},"lostItems":{"catalogs":[],"loaded":null,"loading":false,"page":1,"pageSize":10,"totalItems":0},"makeOffer":{"error":false,"errorMessage":null,"modalType":"BUY_NOW","offerPrice":0,"submitted":false,"success":false},"modal":{"modal":"NONE"},"moreItemsFromCatalogIndex":{},"notification":{"errorTime":0,"forceEnableBanner":false,"hasActiveSubscription":false,"hasNewNotifications":true,"loading":false,"notificationCount":0,"notifications":[],"permission":"","pushNotifications":[],"showPermissionOverlay":false},"pagination":{"pageSize":24},"passwordReset":{"error":false,"errorMessage":nul
# l,"submitted":false,"success":false},"payment":{"error":false,"errorMessage":null,"submitted":false,"success":false},"persist":{"headerSearchDropdown":{"headerDropdownVisible":false},"pagination":{"sort":{}}},"recentItem":{"byId":{"72936248":{"itemId":72936248,"timestamp":1562210369757}},"loaded":0,"loading":false},"recommendedItem":{"byId":{},"loaded":0,"loading":false},"reduxAsyncConnect":{"loaded":true},"registerForCatalog":{"catalogId":null,"error":false,"fromBiddingConsole":false,"itemId":null,"submitted":false,"success":false},"retractBid":{"bidRetracted":false,"error":false,"itemId":null,"submitted":false,"success":false},"review":{"error":false,"reviewData":[{"catID":0,"lots":[],"preventReview":false,"reviewed":false}],"submitted":false,"success":false},"route":{"currentUrl":{"pathname":"\u002Fitem\u002F72936248_georgia-o-keeffe-american-modernist-gouache-paper","search":"","hash":"","action":"POP","key":null,"query":{}},"pastUrl":{"pathname":""}},"routing":{"locationBeforeTransitions":{"pathname":"\u002Fitem\u002F72936248_georgia-o-keeffe-american-modernist-gouache-paper","search":"","hash":"","action":"POP","key":null,"query":{}}},"savedItemCount":{"byId":{},"loaded":{},"loading":[]},"savedSearch":{"loaded":0,"loading":false,"searches":[]},"savedSearchItem":{"byId":{},"ids":[],"loaded":0,"loading":false},"saveItem":{},"saveSearch":{"byParams":{},"error":false,"submitted":false,"success":false},"saveSearchCheck":{"error":false,"isSavedSearch":false,"savedSearchId":0,"success":false},"search":{"error":false,"facets":[],"isLoading":true,"itemIds":[],"sort":[],"submitted":false,"success":false,"totalFound":0},"searchExclusions":{"excludedFacets":{"auctionHouse":[]},"loaded":0,"loading":false},"searchFacets":{"error":false,"facets":{"archived":[],"upcoming":[]},"submitted":false,"success":false},"searchPromoted":{"itemIds":[]},"searchSuggestions":{"error":false,"submitted":false,"success":false,"suggestions":[]},"seller":{"byId":{"1162":{"address":"15 - 280 West Beaver Creek Road","address2":"","alias":"888-auctions","city":"Richmond Hill, ON","country":"Canada","countryCode":"ca","name":"888 Auctions","regionCode":"world","sellerId":1162,"logoId":"king","stateCode":"","stateName":"other","zip":"L4B 3Z1"},"1496":{"address":"3500 NW Boca Raton Blvd.","address2":"Suite 506","alias":"carstens-galleries","city":"Boca Raton","country":"United States","countryCode":"us","name":"Carstens Galleries","regionCode":"us","sellerId":1496,"logoId":"educla","stateCode":"FL","stateName":"Florida","zip":"33431"}},"loaded":{"1162":1562210369733,"1496":1562210369733},"loadedSellers":false,"loading":[],"loadingSellers":false},"sellerCatalogCounts":{"byId":{"1162":{"doneCount":131,"liveCount":0,"onlineCount":2,"sellerId":1162,"upcomingCount":2}},"loaded":{"1162":1562210369658},"loading":[]},"sellerDetail":{"byId":{"1162":{"description":"Located just north of Toronto, Canada, 888 Auctions has grown from a small regional auction house to Canada's largest auction house specializing in Asian art, precious gems and metals, and numismatic items. Alongside our 5,400 square foot gallery, our combination of Canadian hospitality and professionalism welcomes visitors and clients from all over the world.\r\n\r\nWith a multilingual staff providing consistent assistance for international buyers through the auction process and ensuring a seamless bidding experience, clients are offered unlimited access to watch and bid on all auctions live in real time, from anywhere in the world.\r\n\r\n888 Auctions conducts live auctions every two weeks with a sell-through rate of over 85%. Categories include watercolor paintings, modern and contemporary art, jewelry and precious gems, investment-grade precious metals and rare numismatic items, ceramics, bronzes, Asian wood-carved furniture, and other rare collectibles.\r\n\r\nWith a devoted staff of specialists and appraisers, 888 Auctions continues to provide an ever-increasing calibre of items to an ever-expanding international audience. Regardless of what you are looking for, you are sure to find it here with 888 Auctions.\r\n","sellerId":1162,"email":"support@888auctions.com","phoneNumber":"(905) 763-7201","website":"http:\u002F\u002Fwww.888auctions.com"}},"loaded":{"1162":1562210369665},"loading":[]},"sellerEndedCatalogs":{"byId":{},"loaded":{},"loading":[]},"sellerFollowerCount":{"byId":{},"loading":[],"loadingSellersFollowerCount":false},"sellerPreviewCatalogs":{"byId":{},"loaded":{},"loading":[]},"sellerRatings":{"byId":{},"loaded":{},"loading":false},"sellerRecordResults":{"byId":{},"loaded":{},"loading":[]},"sellerUpcomingCatalogs":{"byId":{},"loaded":{},"loading":[]},"sendSellerMessage":{"error":false,"submitted":false,"success":false},"setPassword":{"error":false,"errorMessage":"","submitted":false,"success":false},"shouldLogin":{"completeAccountModalOpen":false,"confirmPasswordModalOpen":false,"loginModalOpen":false,"setPasswordModalOpen":false,"signUpModalOpen":false,"startTracking":false,"trigger":""},"similarItems":{"byId":{"72936248":[72936248,73330180,72936000,73257206,73330203,73330132,72936041,73330326,72935963,72936209,73330333,73330159,72936093,72936115,73330371,73330177]},"loaded":{"72936248":1562210369707},"loading":[]},"storefront":{"items":[],"loaded":{},"loading":[],"totalItems":0},"stripe":{"stripeCustomer":{}},"topRatedSellers":{"loaded":{},"topRatedSellers":[]},
# "trustMetrics":{"trustMetrics":{}},"upcomingCatalogs":{"ids":[],"loaded":0,"loading":false},"upcomingItems":{"error":false,"errorMessage":null,"itemIds":[],"loaded":null,"submitted":false,"success":false},"updateAccount":{"error":false,"errorMessage":null,"submitted":false,"success":false},"user":{"userData":{}},"userVariantTest":{"byId":{"U8xgfBmWTkK6VLBYEKqh9g":{"userSessionId":"a1c044d4-def8-40ac-bfa5-dd18ff891548","experimentId":"U8xgfBmWTkK6VLBYEKqh9g","variantId":""},"wJoQrtHVT5uj4aU7MnPxcg":{"userSessionId":"a1c044d4-def8-40ac-bfa5-dd18ff891548","experimentId":"wJoQrtHVT5uj4aU7MnPxcg","variantId":"Show Badge"},"1MEB3ntxRiKtkXAh4E0diQ":{"userSessionId":"a1c044d4-def8-40ac-bfa5-dd18ff891548","experimentId":"1MEB3ntxRiKtkXAh4E0diQ","variantId":""},"TXkK5003TVeWgQcXY9A0DA":{"userSessionId":"a1c044d4-def8-40ac-bfa5-dd18ff891548","experimentId":"TXkK5003TVeWgQcXY9A0DA","variantId":""}},"loaded":1562210369617},"video":{"byId":{},"loaded":{},"loading":[]},"viewData":{},"waitingForApproval":{"catalogId":0},"whiteLabel":{"hostname":"www.liveauctioneers.com","isWhiteLabel":false,"logo":"https:\u002F\u002Fp1.liveauctioneers.com\u002Fdist\u002Fimages\u002Flogo.svg","sellerId":0},"windowSize":{"height":1024,"width":1024},"wonItems":{"items":[],"loaded":null,"loading":false,"page":1,"pageSize":10,"totalItems":0}};</script><script src="/dist/manifest.784fdb6d9a38a414cdb6.js" charSet="UTF-8"></script><script '
# pattern=re.compile(content_pattern)
# results=re.search(pattern,response.text)
# a=results.group(4).replace('\"','')
# cate_pattern='CategoryName:(.*?),'
# patter2=re.compile(cate_pattern)
# results2=re.findall(patter2,a)
# if a:
#     for item in results2:
#         print(item)
# else: 
#     print('wu')


#到这里！！！！

#catalogonly


# print(results[0].group(1),results[0].group(2),results[0].group(3),results[0].group(4))
# for result in results:
#     print('111')
#     print(result)
#     print(result[0].group(2))
# print(html.xpath('string(//span[@class="price___pIaPZ"]/span/span)'))

# datetime_string='Fri, Jul 05, 2019 7:00 PM GMT+8'
# datetime_format='%a, %b %d, %Y %I:%M %p GMT+8'

# time=datetime.datetime.strptime(datetime_string,'%a, %b %d, %Y %I:%M %p GMT+8')
# print(datetime.datetime.strftime(time,'%H:%M:%S'))
# print((str(datetime.date.today())))
    
#数据库测试
# sql='SELECT id FROM item_indooo WHERE date-1>=CURDATE()'
# db=pymysql.connect(host='localhost',port=3306,user='root',password='root',database='testdatabase')
# cursor=db.cursor()
# cursor.execute(sql)
# results=cursor.fetchall()
# print(results)
# for result in results:
#     print(result)
#     print(result[0])

# print((datetime.date.today()+datetime.timedelta(3)))
# print(random.randint(0,1))
# starting_date=datetime.datetime.strftime((datetime.date.today()+datetime.timedelta(3)),'%b %d')
# print(starting_date)

# time = datetime.date.today().strftime('%b')
# time2=datetime.date.today().timetuple().tm_mday
# VersionInfo =time+' '+str(time2)
# print(VersionInfo)

#时区
# closing_datetime='Sat, Jul 06, 2019 3:00 PM UTC'
# datetimestamp=datetime.datetime.strptime(closing_datetime,'%a, %b %d, %Y %I:%M %p %Z')
# print(type(datetimestamp))
# bb=datetimestamp.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
# print(bb)
# cc=datetimestamp+datetime.timedelta(hours=8)
# print(cc)

#价钱分离
# price='A3,,,00'
# price=price.replace(',','')
# result=re.match('(\D)(\d*)',price)
# print(result.group(1),result.group(2))

# response=requests.get('https://item-api-prod.liveauctioneers.com/spa/small/item/73438158/bidding?c=20170802')
# print(response.text)

# post_data={"ids":[72935969]}
# r=requests.post('https://item-api-prod.liveauctioneers.com/saved-items/count?c=20170802',json=post_data)
# r_json=json.loads(r.text)
# print(r_json.get('data').get('savedItemCounts')[0].get('savedCount'))

# print(datetime.datetime.now().strftime('%H:%M:%S'))
# r=requests.get('https://classic.liveauctioneers.com/c/art/1/?rows=120&sort=dateasc')
# res=etree.HTML(r.text)
# a=res.xpath('string(//div[@class="mt25"][last()]//div[contains(@class,"item_box")][last()]//div[@class="datetimestamp"][2])')
# print(type(a))


#时间比较
# strs='Jun 6'
# a=datetime.datetime.strptime(strs,'%b %d')
# a=datetime.datetime.strftime(a,'%Y%m%d')
# # b=datetime.datetime.now()-a
# print(int(a))
# target_day=(datetime.date.today()+datetime.timedelta(days=3)).timetuple().tm_year

# print(target_day)

# r=requests.get('https://www.liveauctioneers.com/item/73137179_charles-schulz',headers=headers,cookies=jar)
# text=r.text
# result=re.match(pattern,text)
# print(result)


# a=random.randint(0,1)
# if a:
#     print('pass')
# else:
#     print('not')


#登陆
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC


# #方法1
# chrome_options = webdriver.chrome.options.Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browser=webdriver.Chrome(options=chrome_options)
# # browser=webdriver.Chrome()
# wait=WebDriverWait(browser,15)
# enter=wait.until(EC.presence_of_element_located((By.XPATH,'//a[@class="link___ link-primary-weak___ link-default___3gIWR"]')))
# enter.click()
# name=wait.until(EC.presence_of_element_located((By.XPATH,'//input[@class="form-control form-control"]')))
# name.send_keys('1413476657@qq.com')
# password=browser.find_element_by_xpath('//input[@class="form-control recordingExclude form-control"]')
# password.send_keys('Redback1020')
# login_button=browser.find_element_by_xpath('//button[@class="button___ button-primary-red___ button-primary___ submit___1XYKo"]')
# login_button.click()
# cookies=browser.get_cookies()
# browser.delete_all_cookies()
# for cookie in cookies:
#     browser.add_cookie(cookie)
# browser.get('https://www.liveauctioneers.com')
# browser.get('https://www.liveauctioneers.com/item/73279229_massive-palatial-museum-quality-gilt-wood-19th-century')
# save_item=browser.find_element_by_xpath('//button[@class="button___ button-secondary-blue___ button-secondary___ button___A-PDg"]')
# AC(browser).move_to_element(save_item).move_by_offset(5,5).click().perform()
# ok=wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="button___ button-secondary-blue___ button-secondary___ button___A-PDg undefined"]')))
# if ok:
#     time.sleep(2)
#     browser.get('https://www.liveauctioneers.com/item/72880686_si-chen-yuan-oc-california')
# time.sleep(5)

#方法2
# browser=webdriver.Chrome()
# cookies=[{'domain': 'liveauctioneers.com', 'expiry': 1924905600, 'httpOnly': False, 'name': 'rCookie', 'path': '/', 'secure': False, 'value': '2ql56r7o7jpjl9kc49ip1rjxsrhsmm'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1563096967, 'httpOnly': False, 'name': 'RT', 'path': '/', 'secure': False, 'value': '"z=1&dm=www.liveauctioneers.com&si=3qnkj8vys7r&ss=jxsrhpfz&sl=1&tt=2hh&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=2hq&nu=d41d8cd98f00b204e9800998ecf8427e&cl=38z"'}, {'domain': 'liveauctioneers.com', 'expiry': 1924905600, 'httpOnly': False, 'name': 'lastRskxRun', 'path': '/', 'secure': False, 'value': '1562492167722'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1594028167, 'httpOnly': False, 'name': 'sailthru_content', 'path': '/', 'secure': False, 'value': '1b566f4fd0a8ac2918be66ab160c0945'}, {'domain': 'liveauctioneers.com', 'httpOnly': False, 'name': '_session_id', 'path': '/', 'secure': False, 'value': 'b130f766-5a6a-4d9b-8c36-757045efbcaf'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1720258566, 'httpOnly': False, 'name': 'ki_r', 'path': '/', 'secure': False, 'value': ''}, {'domain': 'liveauctioneers.com', 'expiry': 1596656165, 'httpOnly': False, 'name': 'cto_lwid', 'path': '/', 'secure': False, 'value': 'd95606f2-db1f-40b8-8d97-eab9ec0c4aad'}, {'domain': 'liveauctioneers.com', 'expiry': 1562492225, 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1562492175, 'httpOnly': False, 'name': 'criteo_write_test', 'path': '/', 'secure': False, 'value': 'ChUIBBINbXlHb29nbGVSdGJJZBgBIAE'}, {'domain': 'liveauctioneers.com', 'expiry': 1594028164, 'httpOnly': False, 'name': 'ajs_group_id', 'path': '/', 'secure': False, 'value': 'null'}, {'domain': 'liveauctioneers.com', 'expiry': 1594028165, 'httpOnly': False, 'name': 'ajs_anonymous_id', 'path': '/', 'secure': False, 'value': '%228c3ba052-5a56-4610-a3c8-ec783e5f0f7b%22'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1720258566, 'httpOnly': False, 'name': 'ki_t', 'path': '/', 'secure': False, 'value': '1562492166774%3B1562492166774%3B1562492166774%3B1%3B1'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1562493965, 'httpOnly': False, 'name': 'sailthru_pageviews', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'liveauctioneers.com', 'expiry': 1562578565, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.816669169.1562492165'}, {'domain': 'liveauctioneers.com', 'expiry': 1563408000, 'httpOnly': False, 'name': '_gaexp', 'path': '/', 'secure': False, 'value': 'GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1562493965, 'httpOnly': False, 'name': '__stripe_sid', 'path': '/', 'secure': False, 'value': 'b83a7156-6976-4d37-beff-c2ea10fd0fcb'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1594028165, 'httpOnly': False, 'name': '__stripe_mid', 'path': '/', 'secure': False, 'value': 'a89d549f-0351-4089-a3cb-18fd0fd0760e'}, {'domain': 'www.liveauctioneers.com', 'expiry': 1594028167, 'httpOnly': False, 'name': 'sailthru_visitor', 'path': '/', 'secure': False, 'value': '96c46f7e-f452-4b85-9458-0eafa801b328'}, {'domain': 'liveauctioneers.com', 'expiry': 1924905600, 'httpOnly': False, 'name': 'rskxRunCookie', 'path': '/', 'secure': False, 'value': '0'}, {'domain': 'liveauctioneers.com', 'expiry': 1625564165, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.562658696.1562492165'}, {'domain': 'liveauctioneers.com', 'expiry': 1594028164, 'httpOnly': False, 'name': 'ajs_user_id', 'path': '/', 'secure': False, 'value': 'null'}]

# browser.get('https://www.liveauctioneers.com/item/73279229_massive-palatial-museum-quality-gilt-wood-19th-century')
# browser.delete_all_cookies()
# for cookie in cookies:
#     browser.add_cookie(cookie)
# browser.get('https://www.liveauctioneers.com/item/73279229_massive-palatial-museum-quality-gilt-wood-19th-century')
# browser.get('https://www.liveauctioneers.com/item/72880686_si-chen-yuan-oc-california')
# original_cookies='ajs_group_id=null; _ga=GA1.2.702269890.1561596772; _gid=GA1.2.1319034618.1561596772; _gaexp=GAX1.2.wJoQrtHVT5uj4aU7MnPxcg.18095.1; __stripe_mid=1e116401-2ddb-4347-91c4-f867cf51d4ea; cto_lwid=44b2c8a5-4ba4-4456-bdc5-bc388b9fca83; ajs_anonymous_id=%22ef3a5847-2d25-431d-a51e-8778b609070c%22; sailthru_visitor=99da3d35-168f-45dc-8e6a-9ca3197bf55b; ki_r=; rskxRunCookie=0; rCookie=xfhduhawoibc2hgmdf7p9k; bidder-has-logged-in=true; pagination-page-size=120; aJS=no; JS=no; optimizelyEndUserId=oeu1561685890151r0.4308360687264412; __utmz=118153238.1561685890.1.1.utmcsr=liveauctioneers.com|utmccn=(referral)|utmcmd=referral|utmcct=/c/art/1/; la_id_y=850879376; __qca=P0-242406864-1561685890483; location=%7B%22address%22%3A%22518101%22%2C%22latlng%22%3A%22%2C+%22%2C%22time%22%3A1561686096%7D; ip_country=CN; SnapABugHistory=1#; last_logged_in_user=Evans+Hu%3A%3A%3Ac3f334e6be8a351ae340c2836e575110; _session_id=c7fdff05-ae14-4228-9c13-b89553bb8114; __utma=118153238.702269890.1561596772.1561816152.1561888265.7; __utmc=118153238; la_latest_lots=%7B%2273015924%22%3A%7B%22time%22%3A1561686022%7D%2C%2272312039%22%3A%7B%22time%22%3A1561689682%7D%2C%2267244609%22%3A%7B%22time%22%3A1561890308%7D%2C%2272312038%22%3A%7B%22time%22%3A1561686356%7D%2C%2273015930%22%3A%7B%22time%22%3A1561687122%7D%2C%2273015926%22%3A%7B%22time%22%3A1561687150%7D%2C%2273276516%22%3A%7B%22time%22%3A1561687182%7D%2C%2272615538%22%3A%7B%22time%22%3A1561689958%7D%2C%2272953723%22%3A%7B%22time%22%3A1561888881%7D%7D; ajs_user_id=2829818; join-modal-last-seen=2019-07-01; ki_t=1561596784612%3B1561947391628%3B1561956599649%3B5%3B74; sailthru_content=c4e92fc5864722e6aba746dd913de7ef51b848393e88c66ec446466832e72607d9c82afcdcc314c1c2498ff8165f1f0696e3835f25cd87903bbdf1d76ecb553f891e21feab56ebffef8826059ddb5aa6de684a15947882aa21c05cf633c6db2c2ce8cdc2cabd4e718c79adf623234335ab1a34fa0e80aac04c214ab1188727d5b7709040fac4c066145acb33007961b0e51eda53cad25dfe400a2c8aa39bd97a3517bd093ec1fbaa3abcfe1d6c41b1e677cc995b974ea26cbab2090d7a578b60c97e884180c8b3e40c6678af6ccae1091660f86a4ad18c08e22e7f125847c74348e8f3cbb938790a8bf18bf709670ce1d296e1e375f653cad6f982362e365811; lastRskxRun=1561956600876; RT="z=1&dm=www.liveauctioneers.com&si=lrdka89whi&ss=jxjrgcw5&sl=0&tt=0&bcn=https%3A%2F%2Fboomcatch-prod.liveauctioneers.com%2Fbeacon&ld=72c&ul=96q5g&hd=96qvp"'

# cookies=dict([l.split("=",1) for l in original_cookies.split(";")])
# print(cookies)

# print('a{kk}b{kk}'.format(kk=1))
# db=pymysql.connect(host='cdb-0mn1dj7l.gz.tencentcdb.com',port=10130,user='root',password='Liveauctioneers123',database='item_test_2')
# cursor=db.cursor()
# sql_need_to_be_saved='SELECT item_id FROM items_info WHERE save_action_date=date_format("{date}","%Y-%m-%d")  AND experiment_type=1;'.format(date='2019-07-09')
# cursor.execute(sql_need_to_be_saved)

# from scrapy import Selector
# headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


# result=requests.get('https://www.liveauctioneers.com/c/art/1/?page=18&pageSize=24&sort=saleStart',headers=headers)
# html=etree.HTML(result.text)
# hhh=html.xpath('string(//div[@class="card___1ZynM cards___2C_7Z"][last()]//span[@class="card-date___285QP"])')
# hhh=html.xpath('//div[@class="card___1ZynM cards___2C_7Z"][last()]//span[@class="card-date___285QP"]/text()')
# selector=Selector(text=result.text)
# time_str=selector.xpath('string(//div[@class="crd___1ZynM cards___2C_7Z"][last()]//span[@class="card-date___285QP"])').extract_first()
# print(time_str)

# judge=re.search('(\d )Days Left','y Days Left')
# if judge:
#     print(judge.group(1))
# hhh_int=187/3
# print(hhh_int)
# print(int(hhh_int))
# pile=re.compile('/item/(.*?)_.*')
# res=re.search(pile,hhh)
# print(type(hhh))
# print(res.group(1))
# print((datetime.date.today()-datetime.timedelta(days=3)).strftime('%b %d'))

# print(random.choice([3,7]))

# browser=webdriver.Chrome()
# browser.get('https://www.liveauctioneers.com')
# title_oj=browser.find_element_by_xpath('//a[@class="form-link"]/span')
# print(title_oj.text)

# print(int(re.search('(\d) bidders watching this item','9 bidders watching this item',re.I).group(1)))
