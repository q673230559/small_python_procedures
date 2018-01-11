# -*- coding: utf-8 -*-
# __author__ = 'cuter'

"""
playlist.py
plist文件本质是xml文件，关于其具体呈现形式以及相关知识参考：https://www.jianshu.com/p/04c68bd32caa
Description: Playing with iTunes Playlists.
Author: cuter
Website: http://rundeep.top
"""


import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np
import matplotlib
# 中文楷体支持
zhfont1 = matplotlib.font_manager.FontProperties(fname='font/simkai.ttf')


def findCommonTracks(fileNames):
    """
    查找两个文档共同存在的音乐，保存到common.txt
    """
    # 两个歌单歌名列表
    trackNameSets = []
    for fileName in fileNames:
        # 创建一个set
        trackNames = set()
        # 读文件
        plist = plistlib.readPlist(fileName)
        # 获取歌单列表
        tracks = plist['Tracks']
        # 遍历歌单列表
        for trackId, track in tracks.items():
            try:
                # 添加歌名到set
                trackNames.add(track['Name'])
            except:
                # 异常忽略
                pass
        # 添加到歌曲名称列表
        trackNameSets.append(trackNames)
    # 利用set计算重复歌曲
    commonTracks = set.intersection(*trackNameSets)
    # 写入文件
    if len(commonTracks) > 0:
        f = open("common.txt", 'wb')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("发现了 %d 首重复歌曲. "
              "歌名已经写入 common.txt." % len(commonTracks))
    else:
        print("没发现重复歌曲!")

def plotStats(fileName):
    """
    绘制统计信息
    """
    # 读文件
    plist = plistlib.readPlist(fileName)
    # 获取歌单
    tracks = plist['Tracks']
    # 分数列表和时长列表
    ratings = []
    durations = []
    # 遍历歌单
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # 异常忽略
            pass

    # 检查数据有效性
    if ratings == [] or durations == []:
        print("没有发现 分数/时长 数据 ： %s." % fileName)
        return

    # 上方画图
    # 按照int32读取时长数据
    x = np.array(durations, np.int32)
    # 转换成分钟
    x = x/60000.0
    # 读取评分
    y = np.array(ratings, np.int32)
    # 整个图两行，一列 从第一行开始画
    pyplot.subplot(2, 1, 1)
    # x轴时长，用圆圈o表示
    pyplot.plot(x, y, 'o')
    #
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('时长', fontproperties=zhfont1)
    pyplot.ylabel('评分', fontproperties=zhfont1)

    # 下方画图
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('时长', fontproperties=zhfont1)
    pyplot.ylabel('数量', fontproperties=zhfont1)

    # 绘制
    pyplot.show()


def findDuplicates(fileName):
    """
    寻找重复的音乐
    """
    print('在“ %s ”文件夹中寻找重复音乐中...' % fileName)
    # 读取xml文件
    plist = plistlib.readPlist(fileName)
    # 获取音乐列表
    tracks = plist['Tracks']

    # 音乐名字字典
    trackNames = {}
    # 遍历音乐列表
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # 判断我们的列表里面是否已经有了
            if name in trackNames:
                # 如果歌曲名称和时长相同，计数加一
                # 持续时长四舍五入精确到秒
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # 加入到我们的字典trackNames 键是歌名值是元组（时长，出现次数）
                trackNames[name] = (duration, 1)
        except:
            # 异常忽略
            pass
    # 保存重复的歌曲为元组（数量，歌名）到数组dups里面
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # 打印到控制台
    if len(dups) > 0:
        print("发现 %d 首重复的. 歌曲名字 保存已到 dup.txt" % len(dups))
    else:
        print("没发现重复歌曲!")
    f = open("dups.txt", 'w')
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()


# 主函数
def main():
    # 创建解析器
    descStr = """
        解析iTunes音乐软件导出的.xml 文件。
    """
    parser = argparse.ArgumentParser(description=descStr)

    group = parser.add_mutually_exclusive_group()

    # 添加命令行参数
    group .add_argument('--common', nargs = '*', dest='plFiles', required=False)
    group .add_argument('--stats', dest='plFile', required=False)
    group .add_argument('--dup', dest='plFileD', required=False)

    # 解析参数
    args = parser.parse_args()

    if args.plFiles:
        # 寻找多个播放列表共同音乐
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # 绘图（不同音乐时长与评分的关系、时长与数量的关系）
        plotStats(args.plFile)
    elif args.plFileD:
        #  查找重复音乐
        findDuplicates(args.plFileD)
    else:
        print("没找到音乐信息")


if __name__ == '__main__':
    main()
