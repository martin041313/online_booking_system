# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the static data
'''  
#这部分数据是常见城市 方便用户输入
CITY_CHOICE = (
	('安庆','安庆'),
	('阿克苏','阿克苏'),
	('阿勒泰','阿勒泰'),
	('安康','安康'),
	('北京','北京'),
	('包头','包头'),
	('北海','北海'),
	('保山','保山'),
	('百色','百色'),
	('成都','成都'),
	('重庆','重庆'),
	('长沙','长沙'),
	('长春','长春'),
	('常州','常州'),
	('长治','长治'),
	('赤峰','赤峰'),
	('常德','常德'),
	('长白山','长白山'),
	('朝阳市','朝阳市'),
	('昌都','昌都'),
	('大连','大连'),
	('迪庆(香格里拉)','迪庆(香格里拉)'),
	('大理','大理'),
	('大同','大同'),
	('丹东','丹东'),
	('敦煌','敦煌'),
	('大庆','大庆'),
	('东营','东营'),
	('达县','达县'),
	('恩施','恩施'),
	('鄂尔多斯','鄂尔多斯'),
	('福州','福州'),
	('佛山','佛山'),
	('阜阳','阜阳'),
	('广州','广州'),
	('桂林','桂林'),
	('贵阳','贵阳'),
	('赣州','赣州'),
	('格尔木','格尔木'),
	('广元','广元'),
	('杭州','杭州'),
	('哈尔滨','哈尔滨'),
	('海口','海口'),
	('呼和浩特','呼和浩特'),
	('合肥','合肥'),
	('黄岩','黄岩'),
	('海拉尔','海拉尔'),
	('黄山','黄山'),
	('邯郸','邯郸'),
	('黑河','黑河'),
	('怀化','怀化'),
	('和田','和田'),
	('汉中','汉中'),
	('哈密','哈密'),
	('济南','济南'),
	('泉州(晋江)','泉州(晋江)'),
	('九寨沟','九寨沟'),
	('景洪(西双版纳)','景洪(西双版纳)'),
	('景德镇','景德镇'),
	('济宁','济宁'),
	('佳木斯','佳木斯'),
	('锦州','锦州'),
	('嘉峪关','嘉峪关'),
	('九江','九江'),
	('井冈山','井冈山'),
	('昆明','昆明'),
	('喀什','喀什'),
	('库尔勒','库尔勒'),
	('库车','库车'),
	('克拉玛依','克拉玛依'),
	('康定','康定'),
	('丽江','丽江'),
	('兰州','兰州'),
	('拉萨','拉萨'),
	('临沂','临沂'),
	('连云港','连云港'),
	('柳州','柳州'),
	('洛阳','洛阳'),
	('泸州','泸州'),
	('临沧','临沧'),
	('林芝','林芝'),
	('荔波','荔波'),
	('龙岩(连城)','龙岩(连城)'),
	('牡丹江','牡丹江'),
	('绵阳','绵阳'),
	('满洲里','满洲里'),
	('芒市','芒市'),
	('漠河','漠河'),
	('梅县','梅县'),
	('南京','南京'),
	('宁波','宁波'),
	('南宁','南宁'),
	('南昌','南昌'),
	('南通','南通'),
	('南平（武夷山）','南平（武夷山）'),
	('南阳','南阳'),
	('南充','南充'),
	('攀枝花','攀枝花'),
	('青岛','青岛'),
	('齐齐哈尔','齐齐哈尔'),
	('衢州','衢州'),
	('秦皇岛','秦皇岛'),
	('庆阳','庆阳'),
	('上海','上海'),
	('深圳','深圳'),
	('三亚','三亚'),
	('沈阳','沈阳'),
	('石家庄','石家庄'),
	('汕头','汕头'),
	('思茅','思茅'),
	('昭通','昭通'),
	('天津','天津'),
	('太原','太原'),
	('通辽','通辽'),
	('腾冲','腾冲'),
	('铜仁','铜仁'),
	('天水','天水'),
	('塔城','塔城'),
	('武汉','武汉'),
	('温州','温州'),
	('无锡','无锡'),
	('乌鲁木齐','乌鲁木齐'),
	('威海','威海'),
	('潍坊','潍坊'),
	('万州','万州'),
	('乌兰浩特','乌兰浩特'),
	('乌海','乌海'),
	('梧州','梧州'),
	('西安','西安'),
	('厦门','厦门'),
	('西宁','西宁'),
	('徐州','徐州'),
	('襄樊(襄阳)','襄樊(襄阳)'),
	('西昌','西昌'),
	('锡林浩特','锡林浩特'),
	('烟台','烟台'),
	('银川','银川'),
	('义乌','义乌'),
	('宜昌','宜昌'),
	('延吉','延吉'),
	('榆林','榆林'),
	('运城','运城'),
	('盐城','盐城'),
	('宜宾','宜宾'),
	('延安','延安'),
	('伊宁','伊宁'),
	('伊春','伊春'),
	('永州','永州'),
	('郑州','郑州'),
	('珠海','珠海'),
	('张家界','张家界'),
	('湛江','湛江'),
	('舟山(普陀山)','舟山(普陀山)'),
	('中卫','中卫'),
	)
COMPANY_CHOICES = (
		('0','unlimit'),
		('1','CHINA SOUTHERN'    ),
		('2','AIR CHINA'    ),
		('3','CHINA EASTERN'    ),
		('4','SHANGHAI AIRLINES'    ),
		
	)