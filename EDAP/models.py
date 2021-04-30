import mongoengine
import numpy as np
from scipy.optimize import curve_fit as curve_fit
import scipy.integrate as spi
# Create your models here.

class City(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    size = mongoengine.StringField(max_length=32)


class Leijitwomonth(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Leiji(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Rumors(mongoengine.Document):
    data = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Yiqingv2(mongoengine.Document):
    dataList = mongoengine.DictField()
    timestamp = mongoengine.IntField()

class Leijiworld(mongoengine.Document):
    timestamp = mongoengine.IntField()
    leijidata = mongoengine.DictField()
    countrydata = mongoengine.DictField()

class Provincehistory(mongoengine.Document):
    timestamp = mongoengine.IntField()
    place = mongoengine.StringField()
    dataList = mongoengine.DictField()

class Realtimenews(mongoengine.Document):
    timestamp = mongoengine.IntField()
    data = mongoengine.DictField()

country_name_map = {
    '钻石公主号邮轮': 'Diamond Princess Cruise Ship',
    '安哥拉': 'Angola',
    '阿富汗': 'Afghanistan',
    '阿尔巴尼亚': 'Albania',
    '阿尔及利亚': 'Algeria',
    '安道尔共和国': 'Andorra',
    '安圭拉岛': 'Anguilla',
    '安提瓜和巴布达': 'Antigua and Barbuda',
    '阿根廷': 'Argentina',
    '亚美尼亚': 'Armenia',
    '阿森松': 'Ascension',
    '澳大利亚': 'Australia',
    '奥地利': 'Austria',
    '阿塞拜疆': 'Azerbaijan',
    '巴哈马': 'Bahamas',
    '巴林': 'Bahrain',
    '孟加拉': 'Bangladesh',
    '巴巴多斯': 'Barbados',
    '白俄罗斯': 'Belarus',
    '比利时': 'Belgium',
    '伯利兹': 'Belize',
    '贝宁': 'Benin',
    '百慕大群岛': 'Bermuda Is',
    '玻利维亚': 'Bolivia',
    '博茨瓦纳': 'Botswana',
    '巴西': 'Brazil',
    '文莱': 'Brunei',
    '保加利亚': 'Bulgaria',
    '布基纳法索': 'Burkina Faso',
    '缅甸': 'Burma',
    '布隆迪': 'Burundi',
    '喀麦隆': 'Cameroon',
    '加拿大': 'Canada',
    '开曼群岛': 'Cayman Is',
    '中非共和国': 'Central African Republic',
    '乍得': 'Chad',
    '智利': 'Chile',
    '中国': 'China',
    '哥伦比亚': 'Colombia',
    '刚果': 'Congo',
    '库克群岛': 'Cook Is',
    '哥斯达黎加': 'Costa Rica',
    '古巴': 'Cuba',
    '塞浦路斯': 'Cyprus',
    '捷克': 'Czech Republic',
    '丹麦': 'Denmark',
    '吉布提': 'Djibouti',
    '多米尼加共和国': 'Dominica Rep',
    '厄瓜多尔': 'Ecuador',
    '埃及': 'Egypt',
    '萨尔瓦多': 'El Salvador',
    '爱沙尼亚': 'Estonia',
    '埃塞俄比亚': 'Ethiopia',
    '斐济': 'Fiji',
    '芬兰': 'Finland',
    '法国': 'France',
    '法属圭亚那': 'French Guiana',
    '法属玻利尼西亚': 'French Polynesia',
    '加蓬': 'Gabon',
    '冈比亚': 'Gambia',
    '格鲁吉亚': 'Georgia',
    '德国': 'Germany',
    '加纳': 'Ghana',
    '直布罗陀': 'Gibraltar',
    '希腊': 'Greece',
    '格林纳达': 'Grenada',
    '关岛': 'Guam',
    '危地马拉': 'Guatemala',
    '几内亚': 'Guinea',
    '圭亚那': 'Guyana',
    '海地': 'Haiti',
    '洪都拉斯': 'Honduras',
    '香港': 'Hongkong',
    '匈牙利': 'Hungary',
    '冰岛': 'Iceland',
    '印度': 'India',
    '印度尼西亚': 'Indonesia',
    '伊朗': 'Iran',
    '伊拉克': 'Iraq',
    '爱尔兰': 'Ireland',
    '以色列': 'Israel',
    '意大利': 'Italy',
    '科特迪瓦': 'Ivory Coast',
    '牙买加': 'Jamaica',
    '日本': 'Japan',
    '约旦': 'Jordan',
    '柬埔寨': 'Kampuchea (Cambodia )',
    '哈萨克斯坦': 'Kazakhstan',
    '肯尼亚': 'Kenya',
    '韩国': 'Korea',
    '科威特': 'Kuwait',
    '吉尔吉斯斯坦': 'Kyrgyzstan',
    '老挝': 'Laos',
    '拉脱维亚': 'Latvia',
    '黎巴嫩': 'Lebanon',
    '莱索托': 'Lesotho',
    '利比里亚': 'Liberia',
    '利比亚': 'Libya',
    '列支敦士登': 'Liechtenstein',
    '立陶宛': 'Lithuania',
    '卢森堡': 'Luxembourg',
    '澳门': 'Macao',
    '马达加斯加': 'Madagascar',
    '马拉维': 'Malawi',
    '马来西亚': 'Malaysia',
    '马尔代夫': 'Maldives',
    '马里': 'Mali',
    '马耳他': 'Malta',
    '马里亚那群岛': 'Mariana Is',
    '马提尼克': 'Martinique',
    '毛里求斯': 'Mauritius',
    '墨西哥': 'Mexico',
    '摩尔多瓦': 'Moldova',
    '摩纳哥': 'Monaco',
    '蒙古': 'Mongolia',
    '蒙特塞拉特岛': 'Montserrat Is',
    '摩洛哥': 'Morocco',
    '莫桑比克': 'Mozambique',
    '纳米比亚': 'Namibia',
    '瑙鲁': 'Nauru',
    '尼泊尔': 'Nepal',
    '荷属安的列斯': 'Netheriands Antilles',
    '荷兰': 'Netherlands',
    '新西兰': 'New Zealand',
    '尼加拉瓜': 'Nicaragua',
    '尼日尔': 'Niger',
    '尼日利亚': 'Nigeria',
    '朝鲜': 'North Korea',
    '挪威': 'Norway',
    '阿曼': 'Oman',
    '巴基斯坦': 'Pakistan',
    '巴拿马': 'Panama',
    '巴布亚新几内亚': 'Papua New Guinea',
    '巴拉圭': 'Paraguay',
    '秘鲁': 'Peru',
    '菲律宾': 'Philippines',
    '波兰': 'Poland',
    '葡萄牙': 'Portugal',
    '波多黎各': 'Puerto Rico',
    '卡塔尔': 'Qatar',
    '留尼旺': 'Reunion',
    '罗马尼亚': 'Romania',
    '俄罗斯': 'Russia',
    '圣卢西亚': 'St.Lucia',
    '圣文森特岛': 'Saint Vincent',
    '东萨摩亚(美)': 'Samoa Eastern',
    '西萨摩亚': 'Samoa Western',
    '圣马力诺': 'San Marino',
    '圣多美和普林西比': 'Sao Tome and Principe',
    '沙特阿拉伯': 'Saudi Arabia',
    '塞内加尔': 'Senegal',
    '塞舌尔': 'Seychelles',
    '塞拉利昂': 'Sierra Leone',
    '新加坡': 'Singapore',
    '斯洛伐克': 'Slovakia',
    '斯洛文尼亚': 'Slovenia',
    '所罗门群岛': 'Solomon Is',
    '索马里': 'Somali',
    '南非': 'South Africa',
    '西班牙': 'Spain',
    '斯里兰卡': 'SriLanka',
    '圣文森特': 'St.Vincent',
    '苏丹': 'Sudan',
    '苏里南': 'Suriname',
    '斯威士兰': 'Swaziland',
    '瑞典': 'Sweden',
    '瑞士': 'Switzerland',
    '叙利亚': 'Syria',
    '台湾省': 'Taiwan',
    '塔吉克斯坦': 'Tajikstan',
    '坦桑尼亚': 'Tanzania',
    '泰国': 'Thailand',
    '多哥': 'Togo',
    '汤加': 'Tonga',
    '特立尼达和多巴哥': 'Trinidad and Tobago',
    '突尼斯': 'Tunisia',
    '土耳其': 'Turkey',
    '土库曼斯坦': 'Turkmenistan',
    '乌干达': 'Uganda',
    '乌克兰': 'Ukraine',
    '阿拉伯联合酋长国': 'United Arab Emirates',
    '阿联酋': 'United Arab Emirates',
    '英国': 'United Kingdom',
    '美国': 'United States',
    '乌拉圭': 'Uruguay',
    '乌兹别克斯坦': 'Uzbekistan',
    '委内瑞拉': 'Venezuela',
    '越南': 'Vietnam',
    '也门': 'Yemen',
    '南斯拉夫': 'Yugoslavia',
    '津巴布韦': 'Zimbabwe',
    '扎伊尔': 'Zaire',
    '赞比亚': 'Zambia',
    '克罗地亚': 'Croatia',
    '北马其顿': 'North Macedonia',
    '安道尔': 'Andorra',
    '多米尼加': 'Dominican Republic',
    '塞尔维亚': 'Republic of Serbia',
    '刚果（金）': 'Dem.Rep.Congo',
    '巴勒斯坦': 'Palestine',
    '波黑': 'Bosnia and Herzegovina',
    '梵蒂冈': 'Status Civitatis Vaticanae',
    '不丹': 'Kingdom of Bhutan',
    '至尊公主邮轮': 'Grand Princess',
    '大不列颠及北爱尔兰联合王国': 'United Kingdom of Great Britain and Ireland',
    '英国（含北爱尔兰）': 'United Kingdom',
    '北爱尔兰': 'Northern Ireland',
    '根西岛': 'Guernsey',
    '法罗群岛': 'Faroe',
    '圣马丁岛': 'Sint Maarten',
    '圣巴泰勒米': 'Saint Barthelemy',
    '法属波利尼西亚': 'French Polynesia',
    '留尼汪': 'Reunion Island',
    '泽西岛': 'Bailiwick of Jersey',
    '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines',
    '毛里塔尼亚': 'The Islamic Republic of Mauritania',
    '赤道几内亚': 'The Republic of Equatorial Guinea',
    '卢旺达': 'Republic of Rwanda',
    '马恩岛': 'Isle of Man',
    '黑山': 'Montenegro',
    '佛得角': 'Cape Verde',
    '刚果（布）':'Congo Brazzaville'
}

continent_name_map = {
    '亚洲': 'Asia',
    '欧洲': 'Europe',
    '北美洲': 'North America',
    '南美洲': 'South America',
    '非洲': 'Africa',
    '大洋洲': 'Oceania',
    '南极洲': 'Antarctica',
    '其他': 'Others'
}

# 预测类
class Predict:
    def logistic(daydata,prdictday):
        # 数据录入——请在这里修改或补充每日病例数，数据太多时用"\"表示换行
        每日病例数 = daydata#[115, 142, 198, 235, 343, 436, 596, 727, 873, 1087, 1330, \
                 #1470, 2091, 2792, 3409, 4043, 4756, 5655, 6280, 7448, 8591]

        天数 = len(每日病例数)  # 自动计算上面输入的数据所对应的天数
        xdata = [i + 1 for i in range(天数)]  # 横坐标数据，以第几天表示
        ydata = 每日病例数  # 纵坐标数据，表示每天对应的病例数

        # S型曲线函数公式定义
        def func(x, k, a, b):
            return k / (1 + (k / b - 1) * np.exp(-a * x))

        # 非线性最小二乘法拟合
        popt, pcov = curve_fit(func, xdata, ydata, method='dogbox', \
                               bounds=([1000., 0.01, 10.], [10000000., 1.0, 1000.]))
        k = popt[0]
        a = popt[1]
        b = popt[2]

        # 计算拟合数据后的数据
        延长天数 = prdictday  # 需要预测的天数
        x = np.linspace(0, len(xdata) + 延长天数)  # 横坐标取值
        y = func(x, *popt)  # 纵坐标计算值
        li = []
        for i in range(len(x)):
          li.append(str(x[i])+','+str(y[i]))
        return li

    def seir(people):
        # N: 区域内总人口                      #
        # S: 易感者                           #
        # E: 潜伏者                           #
        # I: 感染者                           #
        # R: 康复者                           #
        # r: 每天接触的人数                    #
        # r2: 潜伏者每天接触的人数              #
        # beta1: 感染者传染给易感者的概率, I——>S #
        # beta2: 潜伏者感染易感者的概率, E——>S   #
        # sigma: 潜伏者转化为感染者的概率, E——>I #
        # gama: 康复概率, I——>R                #
        # T: 传播时间                          #
        N = people#100000  # 湖北省为6000 0000
        E_0 = 0
        I_0 = 1
        R_0 = 0
        S_0 = N - E_0 - I_0 - R_0
        beta1 = 0.78735  # 真实数据拟合得出
        beta2 = 0.15747
        # r2 * beta2 = 2
        sigma = 0.1  # 1/14, 潜伏期的倒数
        gamma = 0.1  # 1/7, 感染期的倒数
        r = 1  # 政府干预措施决定
        T = 150

        # ode求解
        INI = [S_0, E_0, I_0, R_0]

        def SEIR(inivalue, _):
            X = inivalue
            Y = np.zeros(4)
            # S数量
            Y[0] = - (r * beta1 * X[0] * X[2]) / N - (r * beta2 * X[0] * X[1]) / N
            # E数量
            Y[1] = (r * beta1 * X[0] * X[2]) / N + (r * beta2 * X[0] * X[1]) / N - sigma * X[1]
            # I数量
            Y[2] = sigma * X[1] - gamma * X[2]
            # R数量
            Y[3] = gamma * X[2]
            return Y

        T_range = np.arange(0, T + 1)
        Res = spi.odeint(SEIR, INI, T_range)
        S_t = Res[:, 0]
        E_t = Res[:, 1]
        I_t = Res[:, 2]
        R_t = Res[:, 3]
        return {'S_t':S_t,'E_t':E_t,'I_t':I_t,'R_t':R_t}
