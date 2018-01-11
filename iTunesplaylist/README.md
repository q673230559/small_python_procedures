# 使用说明
## 环境
- 安装Anaconda3 python 3.6.3
- Anaconda2默认库已经包含所需库
- plistlib库 用于解析plist格式文件
- matplotlib库 用于绘图
- numpy库 用于存数据格式化数据
- argparse库 用于解析命令行参数

## 功能
- 查找两个歌单重复的歌曲：$python playlist.py --common data/maya.xml data/rating.xml
- 统计歌单图表 $python playlist.py --stats data/rating.xml
- 查找同一歌单重复歌曲: $python playlist.py --dup data/pl1.xml