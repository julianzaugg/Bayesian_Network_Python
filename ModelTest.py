'''
Created on Feb 13, 2012

@author: julianzaugg
'''
try:
    from BNet import BNet
except ImportError, e:
    print e
    from BNet import BNet
from CPT import CPT
from GDT import GDT
from NoisyOR import NoisyOR

file_name = "D6_training_data.txt"

class ModelTest(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.train_values = []
        self.load_data()
        bn = BNet();
    #    sequence features node(s)
        nterm = CPT("NTERM", []);
    #    structural disorder nodes
        coils_c = CPT("COILS_C", []);
        hotloops_c = CPT("HOTLOOPS_C", []);
        disorder = CPT("DISORDER", ["COILS_C", "HOTLOOPS_C"]);
        
    #    PTM nodes
        y_phosphorylation = CPT("Y_PHOSPHORYLATION", []);
        st_phosphorylation = CPT("ST_PHOSPHORYLATION", []);
        ypwm = GDT("Y_PWM",  [ "Y_PHOSPHORYLATION" ]);
        stpwm = GDT("ST_PWM",  ["ST_PHOSPHORYLATION"]);
        glycosylation = CPT("GLYCOSYLATION", []);
        acetylation = CPT("ACETYLATION", []);
        ptm = NoisyOR("PTM",  ["Y_PHOSPHORYLATION", "ST_PHOSPHORYLATION",
            "GLYCOSYLATION", "ACETYLATION" ]);
        
        # domainarchitecture nodes
        cadherin = CPT("CADHERIN", []);
        igc = CPT("IGC", []);
        znfc2 = CPT("ZNFC2", []);
        ig_like = CPT("IG_LIKE", []);
        sp = CPT("SP", []);
        cc = CPT("CC", []);
        ig = CPT("IG", []);
        tm = CPT("TM", []);
        rrm = CPT("RRM", []);
#        glob = CPT("GLOB",  [ "IGC", "IG_LIKE","IG"]);
        domain = NoisyOR("DOMAIN",  ["CADHERIN", "ZNFC2",
            "SP", "CC", "TM", "RRM", "IGC", "IG_LIKE", "IG"]);
        
        #define the stability nodes
        Sstability = CPT("STABLE",  ["NTERM", "DOMAIN", "PTM", "DISORDER"]);
        
        #add nodes to the network
        #sequence features
        bn.add(nterm);
        disorder
        bn.add(coils_c);
        bn.add(hotloops_c);
        bn.add(disorder);
#        #PTMs
        bn.add(y_phosphorylation);
        bn.add(ypwm);
        bn.add(st_phosphorylation);
        bn.add(stpwm);
        bn.add(glycosylation);
        bn.add(acetylation);
        bn.add(ptm);
        #domain and architecture
        bn.add(cadherin);
        bn.add(igc);
        bn.add(znfc2);
        bn.add(ig_like);
        bn.add(sp);
        bn.add(cc);
        bn.add(ig);
        bn.add(tm);
        bn.add(rrm);
#        bn.add(glob);
        bn.add(domain);
        #stability
        bn.add(Sstability);
#        for i in self.train_values:
#            print i
        bn.train(["Y_PHOSPHORYLATION", "Y_PWM", "ST_PHOSPHORYLATION",
                            "ST_PWM", "GLYCOSYLATION", "ACETYLATION","CADHERIN",
                            "IGC", "ZNFC2", "IG_LIKE","SP","CC", "IG", "TM", "RRM",
                            "NTERM", "COILS_C", "HOTLOOPS_C",
                            "STABLE"], self.train_values, ["PTM", "DOMAIN",
                                                           "DISORDER"], 7)
#        bn.train(["Y_PHOSPHORYLATION", "Y_PWM", "ST_PHOSPHORYLATION", "ST_PWM",
#                 "GLYCOSYLATION", "ACETYLATION"], self.train_values, ["PTM"], 7)

        print nterm
        print coils_c
        print hotloops_c
        print disorder
        print y_phosphorylation
        print ypwm
        print st_phosphorylation
        print stpwm
        print glycosylation
        print acetylation
        print ptm
        print cadherin
        print igc
        print znfc2
        print ig_like
        print sp
        print cc
        print ig
        print tm
        print rrm
        print domain
        print Sstability
        
    def load_data(self):
        fd = open(file_name, 'r')
        temp = []
        for line in fd.readlines():
            temp.append(line.split())
        temp.pop(0)
        index_pos = [0,1,2,3,5,4,6,7,8,9,10,11,12,13,14,15,20,21, -1]
        for l in temp:
            temp2 = []
            for i in index_pos:
                temp2.append(self.convert(l[i]))
            self.train_values.append(temp2)
    
    def load_dataPTM(self):
        fd = open(file_name, 'r')
        temp = []
        for line in fd.readlines():
            temp.append(line.split())
        temp.pop(0)
        index_pos = []

    def convert(self, thing):
        if thing == "S" or thing == "true":
            return True
        elif thing == "U" or thing == "false":
            return False
        else:
            return float(thing)
if __name__ == '__main__':
    ModelTest()
    
    