import ngram_score as ns  # 适应度计算
import random
import math

pm = 0.4
minFitness = 0

fitness = ns.ngram_score('english_quadgrams.txt')
cipher = input('输入密文（输入为空则运行样例数据）：')
cipher = cipher.split(' ')
cipher = ''.join(cipher)
cipher=cipher.upper()
if cipher == '':
    # 原文为the international collegiate programming contest is an annual competitive programming competition among the universities of the world，密文中已将空格去掉
    cipher = 'OFPNWOPZWRONSWRLQSLLPINROPHZSIZRBBNWIQSWOPKONKRWRWWYRLQSBHPONONUPHZSIZRBBNWIQSBHPONONSWRBSWIOFPYWNUPZKNONPKSGOFPDSZLE'

    #hello world
    #out the hats


def calFitness(key):  # 计算适应度
    plain = cipher
    plain = list(plain)
    for i in range(len(plain)):
        if ord(plain[i]) >= ord('A') and ord(plain[i]) <= ord('Z'):
            plain[i] = key[ord(plain[i])-ord('A')]
    plain = ''.join(plain)
    return fitness.score(plain)


class Individual(object):
    def __init__(self, key=None):
        self.key = []  # key是个体的编码，即是一个字符集到字符集的一一对应映射
        self.fitness = 0  # 个体适应度

        if key == None:
            self.key = [chr(ch+ord('A')) for ch in range(0, 26)]
            random.shuffle(self.key)
        else:
            self.key = key

        self.fitness = calFitness(self.key)

    def __eq__(self, other):
        return (self.key == other.key)

    def __hash__(self):
        return hash(''.join(self.key))


def countSame(k1, k2):  # 计算相似度
    cnt = 0
    for i in range(26):
        if k1[i] == k2[i]:
            cnt = cnt+1

    return cnt


def concentration(group):  # 计算浓度概率
    pd = [0]
    for i in range(1, len(group)):
        pd.append(countSame(group[i-1].key, group[i].key))

    return [x/26 for x in pd]


def mutation(id):  # 变异
    global minFitness
    tmp = id.key.copy()
    f1 = calFitness(id.key)

    kids = []
    for i in range(26):
        for j in range(i):
            tmp[i], tmp[j] = tmp[j], tmp[i]

            r = random.uniform(0, 1)
            f2 = calFitness(tmp)
            if f2 > f1:  # 优势变异直接加入
                kids.append(tmp.copy())
            elif r <= pm and f2 > minFitness:  # 劣势变异以较小概率加入
                kids.append(tmp.copy())

            tmp[i], tmp[j] = tmp[j], tmp[i]

    return kids


def IGA():
    print('密文为： '+cipher)
    print("初始化...")

    global minFitness
    alpha = 0.7  # 亲和系数
    N = 200  # 免疫记忆库容量
    M = 100000  # 初始抗体数量，大量初始随机抗体可以避免找不到全局最优解
    group = []
    for _ in range(M):
        group.append(Individual())  # 初始化抗体，其有M个随机抗体

    cnt = 0  # 连续最大适应度没有变化的代数
    last = 0  # 上一代中的最大适应度
    T = 0

    print("破解中...（大约需要3~10分钟）")
    while cnt < 5 or T < 10:  # 迭代
        T = T+1
        print('')

        print('更新免疫记忆库...')
        group = list(set(group))
        group.sort(key=lambda id: id.fitness)
        group.reverse()
        global minFitness

        if len(group) > N:  # 更新免疫记忆库
            group = group[0:N]

        minFitness = group[-1].fitness

        if group[0].fitness != last:
            last = group[0].fitness
            cnt = 1
        else:
            cnt = cnt+1

        print('当前最大适应度：', group[0].fitness)
        print('计算浓度概率与适应度概率...')
        pd = concentration(group)
        pf = [(len(group)-i)/len(group) for i in range(len(group))]
        new = []
        for i in range(len(group)):
            if random.uniform(0, 1) <= alpha*pf[i]+(1-alpha)*pd[i]:
                kids = mutation(group[i])
                new = new + kids
        
        new = [Individual(id) for id in new]
        print('诞生的抗体数量:', len(new))
        group = group + new

    print('迭代次数：', T-cnt)
    group.sort(key=lambda id: id.fitness)
    group.reverse()
    print('解密密钥：', group[0].key)
    print('最大适应度：', group[0].fitness)

    plain = cipher
    plain = list(plain)
    for i in range(len(plain)):
        if ord(plain[i]) >= ord('A') and ord(plain[i]) <= ord('Z'):
            plain[i] = group[0].key[ord(plain[i])-ord('A')]
    plain = ''.join(plain)

    print('明文：', plain.lower())


IGA()
input('按下回车键结束程序')