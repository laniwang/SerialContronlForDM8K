import allModuleDm8000
'''
初始化模块参数类 ,通道数>1的模块
模块类型
模块属性
最大最小值
通道数
'''
class module(object):

    def __init__(self, moduletype, attribute, InstanceTag='', moduleString='',minValue=-100,maxValue=12, minChannel=1, maxChannel=10):
        self.errsign=0  # Execution command result.0->failed, 1->Success.2-->Other
        self.cmdString='' # Execution command string.
        self.moduleType=moduletype  #模块在字典数据名称
##        self.moduleString=modulename  #模块在
        self.InstanceTag=InstanceTag  # 设计图中的 模块的InstanceTag
        self.atrribute=attribute #属性名
        
        self.minValue=minValue #属性最小值 
        self.maxValue=maxValue #属性最大值
        self.minChannel=minChannel #属性通道数范围 最小 例子:automixer [2,32]
        self.maxChannel=maxChannel #属性通道数范围 最大
        self.commandlist=''
        print(self.InstanceTag)

     #get   
    def get_moduletype(self):
        return self.moduleType
    def get_InstanceTag(self):
        return self.InstanceTag
    def get_atrribute(self):
        return self.atrribute
    
    def get_minValue(self):
        return self.minValue
    def get_maxValue(self):
        return self.maxValue
    def get_maxChannel(self):
        return self.maxChannel
    def get_minChannel(self):
        return self.minChannel

    #set
    def set_moduleType(self, mdl):
        self.moduletype=mdl
    def set_InstanceTag(self,  ins):
        self.InstanceTag=ins
    def set_atrribute(self, atrr ):
        self.atrribute=atrr
    
    def set_minValue(self, minv):
        self.minValue=minv
    def set_maxValue(self, maxv):
        self.maxValue=maxv
    def set_maxChannel(self,maxc):
        self.maxChannel=maxc
    def set_minChannel(self, minc):
        self.minChannel=minc
    
    '''
    命令语句合成（get, set, inc, dec, toggle, subscribe, unsubscribe)
    '''
    def getCommand(self):
        self.cmdString='get %s %s %d;' % (self.InstanceTag, self.atrribute, self.minChannel )  #minChannel做为当前测试的通道
        return self.cmdString

    def setCommand(self):
        self.cmdString='set %s %s %d %d;' % (self.InstanceTag, self.atrribute, self.minChannel, self.minValue ) #minChannel做为当前测试的通道，minValue当前配置的值
        return self.cmdString

    def IncCommand(self):
        self.cmdString='Inc %s %s %d;' % (self.InstanceTag, self.atrribute, self.minChannel )  #minChannel做为当前测试的通道
        return self.cmdString
        
    

# 测试代码 
if __name__=='__main__':
    mdl=module('Mixers', 'AutoMixer', 'Gain', 'Auto1')
    string=mdl.getCommand()
    print(string)
    string=mdl.setCommand()
    print(string)
    print(mdl.get_moduletype())
    print(mdl.__doc__)
    
        
        
