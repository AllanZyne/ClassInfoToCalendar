项目为上学时用日历来记录课表

## 环境要求

Python 3

安装依赖

```
pip install xldr
```

## 执行详解
1、配置 classInfo Excel 表格

classTime：第几节。这个参数要配合 conf_classTime.json 文件

2、配置 conf_classTime.json

```js
{
  "calendarName" : "课程表",       // 日历名
  "firstWeekDate" : "20200217",   // 第一周星期一的日期
  "totalWeek": "20",              // 总周数
  "classTime": [
    {   // classTime = 1
        "name":"第 1、2 节",
        "startTime":"0750",
        "endTime":"0925"
    },
    {   // classTime = 2
        "name":"第 3、4、5 节",
        "startTime":"0945",
        "endTime":"1210"
    },
    {   // classTime = 3
        "name":"第 6、7 节",
        "startTime":"1400",
        "endTime":"1530"
    },
    {   // classTime = 4
        "name":"第 8、9、10 节",
        "startTime":"1555",
        "endTime":"1820"
    },
    {   // classTime = 5
        "name":"第 11、12、13 节",
        "startTime":"1930",
        "endTime":"2155"
    }
  ]
}
```

3、运行 excelReader.py 脚本

完成后生成一个 conf_classInfo.json 配置文件

4、运行 main.py 脚本

完成后在工作目录下会生成一个 class.ics 文件

5、打开 class.ics 文件