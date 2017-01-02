# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:30:42 2016
@author: LLH
"""

## pseudo vesion

### Positive Label Propagation
# follower ---> userid
def divide(x):
    y=x.split()
    return (y[0],y[1])

#add positive label
def add_plus(x):
    z="+"+str(x[0])+" "+str(x[1])
    return (x[0],z)

#Positive Propagation
def p_check(x):
    addlist=[]
    value=x[1].split()
    if len(value)==1:
        return addlist
    else:
        parent_label=int(value[0].split("+")[1])
        child=value[1].split(",")
        for i in child:
            if int(i)>parent_label:
                addlist.append((i,"+"+str(parent_label)))
        return addlist   

def p_update(a,b):
    label=[int(a.split()[0].split("+")[1]),int(b.split()[0].split("+")[1])]
    if len(a.split())==2:
        if min(label)!=label[0]:
            p_count.add(1)
        return "+"+str(min(label))+" "+a.split()[1]
    elif len(b.split())==2:
        if min(label)!=label[1]:
            p_count.add(1)
        return "+"+str(min(label))+" "+b.split()[1]
    else:
        return "+"+str(min(label))

### Negative Label Propagation
#reverse & negtive label
def reverse(x):
    y=x.split()
    return (y[1],y[0])

def add_minus(x):
    z="-"+str(x[0])+" "+str(x[1])
    return (x[0],z)

#Negative Propagation
def n_check(x):
    addlist=[]
    value=x[1].split()
    if len(value)==1:
        return addlist
    else:
        parent_label=int(value[0].split("-")[1])
        child=value[1].split(",")
        addlist=[]
        for i in child:
            if int(i)>parent_label:
                addlist.append((i,"-"+str(parent_label)))
        return addlist

def n_update(a,b):
    label=[int(a.split()[0].split("-")[1]),int(b.split()[0].split("-")[1])]
    if len(a.split())==2:
        if min(label)!=label[0]:
            n_count.add(1)
        return "-"+str(min(label))+" "+a.split()[1]
    elif len(b.split())==2:
        if min(label)!=label[1]:
            n_count.add(1)
        return "-"+str(min(label))+" "+b.split()[1]
    else:
        return "-"+str(min(label))

def merge_label(a,b):
    return a.split()[0]+b.split()[0]

def id_label_reverse(x):
    return (x[1],x[0])
    
def assemble(a,b):
    return a+","+b

def sum_number(x):
    if len(x[1].split(","))>1:
        return [(x[0],str(len(x[1].split(",")))+"/"+x[1])]
    else:
        return []

if __name__=='__main__':
    from pyspark import SparkContext 
    sc=SparkContext("local", "labelp-pse")
    p_list=sc.textFile("hdfs://localhost:9000/user/hadoop/input/testdata")\
    .map(divide).reduceByKey(lambda a,b:a+","+b).map(add_plus)
    p_count=sc.accumulator(0)
    while 1:
        p_list=p_list.flatMap(p_check).union(p_list).reduceByKey(p_update)
        p_list.count()
        if p_count.value==0:
            break
        p_count.value=0
    n_list=sc.textFile("hdfs://localhost:9000/user/hadoop/input/testdata")\
    .map(reverse).reduceByKey(lambda a,b:a+","+b).map(add_minus)
    n_count=sc.accumulator(0)
    while 1:
        n_list=n_list.flatMap(n_check).union(n_list).reduceByKey(n_update)
        n_list.count()
        if n_count.value==0:
            break
        n_count.value=0
    all=p_list.union(n_list).reduceByKey(merge_label).map(id_label_reverse).reduceByKey(assemble)\
    .flatMap(sum_number)
    all.coalesce(5).saveAsTextFile("hdfs://localhost:9000/user/hadoop/output")
    # RDD.coalesce(5) assembles RDD in 5 partitions, which can reduce the size of RDD and accelerate