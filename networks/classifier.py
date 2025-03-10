from .layers import *
from .node import *

# 'LR_classifier' and 'HV_classifier'

class HV_FC(GPUModule):
    def __init__(self,input_dim=2048+512):
        super(HV_FC,self).__init__()
        self.linear=nn.Linear(input_dim,2)
        nn.init.constant_(self.linear.weight,1e-4) #avoiding imbalanced prediction at the very start
        nn.init.constant_(self.linear.bias, 0)
        
    def forward(self,node):
        """
        @params:
            node.type=.tree.Node
        @return:
            Size([1,2])
        """
        return self.linear(self.move_tensor_to_gpu(node.feat[0].unsqueeze(0)))
    
    
    
class LR_FC(GPUModule):
    def __init__(self,input_dim=2*(2048+512)):
        super(LR_FC,self).__init__()
        self.linear=nn.Linear(input_dim,1)
    def forward(self,node):
        """
        @params:
            node.type=.tree.Node
        @return:
            Size([1,2])
        """
        chs=[self.move_tensor_to_gpu(ch.feat[0].unsqueeze(0)) for ch in node.children]
        return torch.cat([self.linear(torch.cat(chs,dim=-1)),
                         self.linear(torch.cat(chs[::-1],dim=-1))],
                         dim=-1)
    
class LR_FC_Fusion(GPUModule):
    def __init__(self,input_dim=2*(2048+512)):
        super(LR_FC_Fusion,self).__init__()
        self.linear=nn.Linear(input_dim,1)
    def forward(self,node):
        """
        @params:
            node.type=.tree.Node
        @return:
            Size([1,2])
        """
        return torch.cat([self.linear(torch.cat(
            [self.move_tensor_to_gpu(node.feat[0].unsqueeze(0)),
             self.move_tensor_to_gpu(node.children[0].feat[0].unsqueeze(0))],dim=-1)),
                         self.linear(torch.cat(
                             [self.move_tensor_to_gpu(node.feat[0].unsqueeze(0)),
                              self.move_tensor_to_gpu(node.children[1].feat[0].unsqueeze(0))],dim=-1))],
                         dim=-1)
