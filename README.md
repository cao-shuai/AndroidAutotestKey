# AndroidAutotestKey
功能：
  根据excel配置 ，自动生成遥控器脚本按键
使用方法：
  1.python autokeytool.p 或者 python autokeytool.py --sheet X  说明： X为对应xls中SheetX
  2. SheetX为对应的按键map，获取map方法可以利用excel 中Sheet2 中的第二列的方式获取
  3. 生成的autokeyfile.sh 丢到板卡里执行即可
说明：
  1. key.xls sheet1为要调用填的按键值顺序，第三列的等待时长random为0-10S随机值。
  2. 按键名字需要和sheet2或者sheetX进行大小写匹配。
