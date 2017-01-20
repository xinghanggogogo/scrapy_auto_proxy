### scrapy_auto_proxy

### 基于scrapy自动爬取代理并设置代理
#### 请根据自己的需要,将/demo/middlewares/middlewares.py中calss ProxyMiddleware的两种代理方法开启或关闭.(注意只能选择一种代理的方法,并且当你选择从import中导入代理的方法时需要你拥有自己的代理服务器,并且在设置在/settings.py中)

### 介于互联网上的代理网站提供的免费代理可用比例不大,使用代理时每次会先检测代理的可用性,若不可用,则将之移除代理队列

### 请使用脚本维护爬取的代理的数据库,例如在crontab中根据自己的爬取频率到项目目录执行"scrapy crawl 360_proxy;scrapy crawl xici_proxy"

### 爬取的代理可以选择存储在项目根目录下的json文件中,也可以选择存储在数据库中,请根据需要在/demo/pipelines/db.py;/demo/middlewares/middlewares.py中更改配置

### 代理选择规则为最简单的random规则

### 附带了几个最简单的例子
#### 爬取'http://wufazhuce.com/' 'one' 每日图片信息
#### 爬取'http://ename.dict.cn/' 英文名信息
#### 爬取国内主流直播平台的直播信息,包括斗鱼 全民 战旗 火猫, 虎牙 b站
#### 爬取中英文亚马逊书城的图书信息

