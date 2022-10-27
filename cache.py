import sys
def printusage(): 
    print("Usage: python3 cache.py [-hv] -s <s> -E <E> -b <b> -t <tracefile>")
    print("-h: Optional help flag that prints usage info")
    print("-v: Optional verbose flag that displays trace info")
    print("-s <s>: Number of set index bits (S = 2 s is the number of sets")
    print("-E <E>: Associativity (number of lines per set)")
    print("-b <b>: Number of block bits (B = 2 b is the block size)")
    print("-t <tracefile>: Name of the valgrind trace to replay\n")
    return

def cachesim(scmnd): 
    verbose = False 
    hits = 0
    misses = 0 
    evictions = 0
    s=scmnd 
    s.pop(0)

    if (len(s) < 8 or len(s) > 9): 
        print("Length error")
        print(s)
        return printusage() 
    elif (s[0] == "-hv" or s[0] == "-h"): 
        return printusage()
    elif (s[0] == "-v"): 
        verbose = True 
        s.pop(0)

    #Get set index bits
    if (s[0] == "-s"): 
        try:
            set_index_bits = int(s[1])
            if (set_index_bits <= 0): 
                return printusage()
        except ValueError: 
            print("Value error set")
            return printusage()
    else: 
        print("set error")
        return printusage()

    #Get number of lines per set
    if (s[2]=="-E"): 
        try: 
            E = int(s[3])
            if (E <= 0): 
                return printusage()
        except ValueError: 
            print("E error except")
            return printusage()
    else: 
        print("Elineerror")
        return printusage()

    #Get block bits
    if (s[4]=="-b"): 
        try: 
            b = int(s[5])
            if (b <= 0): 
                return printusage()
        except ValueError: 
            print("block valueerror")
            return printusage()
    else: 
        print("blockbiterror")
        return printusage()

    #tracefile
    if (s[6]!="-t" or s[7]==None): 
        print("traceerror")
        return printusage()
    elif (s[6]=="-t" and s[7]!=None): 
        tracefile = s[7]
    
    #Try opening, if file not valid then print usage information. 
    try: 
        t = open(tracefile, "r")
    except:
        return printusage()
    
    # Create cache here 
    if (set_index_bits > 0 and E > 0 and b > 0): 
        cache=createcache(set_index_bits,E,b)
    else: 
        return printusage()
    #For each line in the tracefile
    for line in t: 
        l = line
        l= l.split()
        instruction=l[0]

        #Ignore I instruction
        if (instruction == 'I'): 
            continue
        #split the memory address access and the number of bits accessed 
        #convert the address into binary from hexadecimal
        #uses zfill to fill the leading bits with 0's to reach 64 bits
        else: 
            a = l[1].split(",")
            address = a[0]
            bytes_accessed=a[1]
            address = bin(int(address,16))[2:]
            address = address.zfill(64)

            # Now we have a 64 bit address
            # take b block bits from least significant
            # take s set bits from middle
            # Remaining take as tag
    
    
    return

#Create class cache holds list of sets[id, E, b]
# Sets class holds list of lines 
class Cache: 
    def __init__(self, s,E,b): 
        self.sets=[Set(0,E,b)]*(2**s)
        self.number_of_sets=2**s
        self.number_of_blocks=2**b
class Set: 
    def __init__(self, id=None,E=None,b=None): 
        self.setid=id
        self.lines=[Line(0,2**b)]*E
        
class Line: 
    def __init__(self, tag=None, numblocks=None): 
        self.tag = tag
        self.valid = 0
        self.numblocks=numblocks
        self.block=[None]* numblocks 

def createcache(s,E,b): 
    setbits= s 
    lines_per_set=E
    blockbits=b
    cache = Cache(setbits, lines_per_set,blockbits)
    return cache

cachesim(sys.argv)
#print(createcache(2,2,4))


