import random
import json
import os
import asn1tools

# V2X事件
class RSU():
    source = None   # 事件来源
    target = None   # 事件目标
    type = ''       # 事件类型
    param = None    # 参数
    createTime = 0  # 创建时间
    processTime = 0 # 处理时间

    # 事件构造器
    def __init__(self, s, t, et, ct, p):
        self.source = s
        self.target = t
        self.type = et
        self.createTime = ct
        self.param = p
    
    # 通知目标处理事件
    def notify(self):
        if not hasattr(self.target, 'handle'):
            print('target not has treatment method')

            return
        self.target.handle(self)



if __name__ == '__main__':
    pass
    