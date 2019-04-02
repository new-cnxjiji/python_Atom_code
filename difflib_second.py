import re, difflib
from collections import Counter
from string import digits
#将文档读取到一个列表当中，用于下一步的处理
def get_content(path):
    #打开文件
    with open(path, 'r', encoding = 'gb18030', errors = 'ignore') as f:
        #将文件中的内容全部按行读取
        content_temp = f.readlines()
        #创建一个新的列表，用于存储处理过的字符串
        content = []
        #这个循环用于去除掉字符串中的符号
        for line in content_temp:
            #去掉字符串中的数字
            remove_digits = str.maketrans('', '', digits)
            line = line.translate(remove_digits)
            #去掉字符串末尾的换行符
            line = line.strip("\n")
            #去掉字符串中间的各种标点符号
            line = re.sub('[，/：/、/。/）/（/《/》]', '', line)
            #将处理好的字符串添加到实现创建好的列表末尾
            content.append(line)
    #返回处理好的字符串列表
    return content


#比较两个字符串的相似度，完全相似返回值为1，相似度越小，值越接近0
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
'''
#将关键词存为字典的键值
#def insert_dimension(content_insert, key_insert, dict_temp = {}):
#    content = content_insert[0]
#    key = key_insert[0]
#    dict[key] = content
#    return dict
'''
#将两个列表拼接成字典
def montage(key_insert, content_insert):
    #拼接字典，以关键词为键，原文为值
    dict_temp = dict(zip(key_insert, content_insert))
    #返回拼接好的字典
    return dict_temp

#使用|将关键词分隔开，方便正则表达式匹配
def string_split(keys):
    #对每一个关键词串进行替换，将其中的空格换成|
    for i in range(0, len(keys)):
        keys[i] = keys[i].replace(' ', '|')
    #返回处理好的列表
    return keys




#将文件路径引入,原文档
#content = get_content("difflib_text.txt")
#将关键词文件路径引入，键值
#key = get_content("difflib_text_key.txt")
#对关键词键进行预处理
#key = string_split(key)
#print(key)

'''
#length = len(key)
'''

#print(length)
#print(content)
#dict = montage(key, content)
#print(dict)


"""
str = "辉哥在通话状态时，用识别码照照片，还上传了媒体内容和文件。"
keys = key[0]
temp = re.findall(keys, str)
print(temp)
"""
#主函数
def main(path):
    #将模型原文按条导入列表
    content = get_content("difflib_text.txt")
    #将关键词导入列表
    key = get_content("difflib_text_key.txt")
    #对关键词列表进行处理，将空格替换成|，方便正则表达式的使用
    key = string_split(key)
    #将两个列表拼接成字典
    dict = montage(key, content)
    #将要进行匹配的新文件写入列表
    newfile = get_content(path)
    #创建一个空列表，用于储存相似度匹配的得分
    goals = []
    #创建一个空列表，用于储存新文件中进行了匹配的条目
    target = []
    #从第一组关键词进行匹配
    for i in range(0, len(key)):
        #将一组关键词在新文件中，借助正则表达式逐条匹配
        for line in newfile:
            #无论该条目中是否有这组关键词，返回正则表达式的结果
            goal = re.findall(key[i], line)
            #包含该组关键词则在goals列表末尾添加上匹配的相似度得分
            if len(goal):
                #计算两个匹配条目的相似度得分
                goals.append(string_similar(content[i], line))
                #将进行匹配的条目存入实现创建好的列表中
                target[i] = line
                #该组关键词得到了匹配，跳出循环，进行下一组关键词的匹配
                break
            else :
                target[i] = None
    #最终返回得分的列表和得到匹配的对象列表
    return goals, target
#计算相似度得分的平均值
def averagenum(num):
    #初始化
    nsum = 0
    #得分加总
    for i in range(len(num)):
        nsum += num[i]
    #返回平均值
    return nsum / len(num)
