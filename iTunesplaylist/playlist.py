# -*- coding: utf-8 -*-
# __author__ = 'cuter'

"""
playlist.py

Description: Playing with iTunes Playlists.
Author: Mahesh Venkitachalam
Website: electronut.in
"""


import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np


def findCommonTracks(fileNames):
    """
    Find common tracks in given playlist files, and save them
    to common.txt.
    """
    # 音轨名称
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(fileName)
        # get the tracks
        tracks = plist['Tracks']
        # iterate through tracks
        for trackId, track in tracks.items():
            try:
                # add name to set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks) > 0:
        f = open("common.txt", 'wb')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    """
    Plot some statistics by readin track information from playlist.
    """
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks
    tracks = plist['Tracks']
    # create lists of ratings and duration
    ratings = []
    durations = []
    # iterate through tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass

    # ensure valid data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return

    # cross plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
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
            # is there an entry already?
            if name in trackNames:
                # if name and duration matches, increment count
                # duration rounded to nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add entry - duration and count
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass
    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save dups to file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
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
