# 草尼馬 Line Bot

[![codebeat badge](https://codebeat.co/badges/8606dde5-df3a-4bae-beb5-0c8b46f48ac3)](https://codebeat.co/projects/github-com-tonyyang924-mudhorse-line-bot-master)

### LINEID： @sgc9537d

<img src="./mudhorse.jpg" width="256" height="256" />
<img src="./mudhorse_qrcode.png" width="256" height="256" />

## 指令

### androidweekly
爬androidweekly.net當週前5筆新文章。

### 591
爬591租屋網的物件，每次回更新時間最新的前五筆。

<span style="color:red; font-weight: bold;">目前只支援雙北</span>

### 格式
```
591 位置=[新北市,台北市,...,三重區,蘆洲區,大安區] 類型=[整層住家,獨立套房,分租套房,雅房,車位,其他] 租金=[最低價格,最高價格] 坪數=[最低坪數,最高坪數]
```

## 範例

```
591 位置=新北市 類型=整層住家 坪數=20,30

591 位置=三重區 租金=10000,23000 類型=整層住家

591 位置=蘆洲區 類型=獨立套房 租金=5000,15000
```
![](./screenshot/1.png)

## 功能

已實現：

* 選擇區域
* 選擇類型
* 選擇坪數
* 租金範圍

## Contributing

* Fork this project
* Create feature branch: `git checkout -b my-feature-branch`
* Commit your change
* Push to the branch: `git push origin my-feature-branch`
* Submit a pull request

## Author

* **Tony Yang** - initial & develop basic feature - [tonyyang924](https://github.com/tonyyang924)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details