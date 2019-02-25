import pdb
def part(n):
    #create list of 1's
    OG = [1] * n
    partitions = []
    
    def getPartitions(partitions, OG): 
        #pdb.set_trace()
        if len(OG) != 1 and 1 in OG: 
            partitions.append(OG[:])
            index = OG.index(1)
            x = OG.pop(index - 1)
            OG[index] += x
            getPartitions(partitions, OG[:])
        partitions.append(OG[:])
        try: 
            index = OG.index(1)
            if (OG[index + 1] == 1): 
                OG.pop(index)
                OG[index] += 1
                getPartitions(partitions, OG[:])
        except: 
            pass
        
        
    pdb.set_trace()
    getPartitions(partitions, OG)
    
    
part(9)