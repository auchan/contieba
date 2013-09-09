def getGBKCode(gbkFile='baidu_tieba/GBK1.1.txt',s=''): 
    #gbkFile字典文件 共3755个汉字 
    #s为要转换的汉字，暂且为gb2312编码，即从IDLE输入的汉字编码 

    #读入字典 
    with open(gbkFile) as f: 
        gbk=f.read().split() 

        #生成A1-FE的索引编码 
        t=['A1'] 
        while True: 
            if t[-1]=='FE': 
                break 
            if (ord(t[-1][1])>=48 and ord(t[-1][1])<57) or (ord(t[-1][1])>=65 and ord(t[-1][1])<70): 
                t.append(t[-1][0]+chr(ord(t[-1][1])+1)) 
                continue 
            if ord(t[-1][1])>=57 and ord(t[-1][1])<65: 
                t.append(t[-1][0]+chr(65)) 
                continue 
            if ord(t[-1][1])>=70: 
                t.append(chr(ord(t[-1][0])+1)+chr(48)) 
                continue 
        #依次索引每个汉字 
        l=list() 
        for st in s:
            if ord(st) > ord('z'):
                i=gbk.index(st)+1 
                #小节编码从B0开始，获取汉字的小节编码 
                t1='%'+t[t.index('B0'):][i//94] 
                #汉字在节点中的索引号 
                i=i-(i//94)*94 
                t2='%'+t[i-1] 
                l.append(t1+t2) 
            else:
                # 保持 ASCILL的原格式输出
                l.append(st)
    #    #最后用空格分隔输出 
    #    return ' '.join(l) 
    # 不用空格分割
        return ''.join(l)
