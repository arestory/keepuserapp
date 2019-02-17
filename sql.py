from dsc_ds import DscDatasource

ds = DscDatasource()

ds.execute_sql('''

insert ignore INTO userinfo (id,name,os_type,birthday,update_time,city,sex,birthpet,avatar,education,university,
    star_sign,ideal_mate,hometown,height,weight,characters ,station,company,hobby,referee_id,referee_name)   VALUES (
    '125818','陈玲飞','ios','1982-10-20','2019-02-12 10:52:17','深圳','female','11','https://release.image.dscapp.dscun.com/avatar/63808029-8C57-4AAF-8D81-167BBE252760.jpg','大专','吉林大学','天秤座','有责任心有担当的','广东 深圳','156','44','善良大方，得体懂事，知性会关爱！本人大专学历，从事外贸工作，积极上进，热爱生活！错过了太阳，错过了星星，在这美好的时光，千万不能再错过一个对的你！','外贸员','广东深圳南山区','旅行，读书，','125815','肖庆') 

''')