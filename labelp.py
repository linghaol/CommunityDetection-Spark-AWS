# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:30:42 2016
@author: LLH
"""

# fully distributed version (for AWS EMR)

## separate follower and user
def divide(x):
    y=x.split(',')
    return (y[0],y[1])
    
# Positive Label Propagation
## add positive label: 
def add_plus(x):
    z="+"+str(x[0])+" "+str(x[1])
    return (x[0],z)

## positive propagation
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

## update positive label of each user
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

# Negative Label Propagation
## reverse & add negtive label
def reverse(x):
    y=x.split(',')
    return (y[1],y[0])
def add_minus(x):
    z="-"+str(x[0])+" "+str(x[1])
    return (x[0],z)

## negative propagation
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

## update negative label of each user
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

## put positive and negative label of each user together, eg. '(id,+1-2 followers)'
def merge_label(a,b):
    return a.split()[0]+b.split()[0]

## change the positive of id and label for community member collection later, eg ('+1-2,id')
def id_label_reverse(x):
    return (x[1],x[0])

## community member collection by label
def assemble(a,b):
    return a+","+b

## calculate the size of each community (the number of members)
def sum_number(x):
    if len(x[1].split(","))>1:
        return [(x[0],str(len(x[1].split(",")))+"/"+x[1])]
    else:
        return []

if __name__=='__main__':
    from pyspark import SparkContext
    # initialize
    sc=SparkContext("yarn", "labelp")
    # reduceByKey() uses ',' to collect all followers of a user
    p_list=sc.textFile("s3://spark-llh/inputfile/edges.csv")\
    .coalesce(100).map(divide).reduceByKey(lambda a,b:a+","+b).map(add_plus)
    # initialize accumulator
    p_count=sc.accumulator(0)
    while 1:
        p_list=p_list.coalesce(100).flatMap(p_check).union(p_list).reduceByKey(p_update)
        p_list.count()  # an action to trigger transformations and accumulator 
        if p_count.value==0:
            break
        p_count.value=0
    n_list=sc.textFile("s3://spark-llh/inputfile/edges.csv")\
    .coalesce(100).map(reverse).reduceByKey(lambda a,b:a+","+b).map(add_minus)
    n_count=sc.accumulator(0)
    while 1:
        n_list=n_list.coalesce(100).flatMap(n_check).union(n_list).reduceByKey(n_update)
        n_list.count()
        if n_count.value==0:
            break
        n_count.value=0
    all=p_list.union(n_list).coalesce(100).reduceByKey(merge_label).map(id_label_reverse).reduceByKey(assemble)\
    .flatMap(sum_number)
    # Attention!! Output folder should NOT exist before generating, which means that 'spark-llh' bucket shouldn't have a folder called 'output' previously 
    all.coalesce(50).saveAsTextFile("s3://spark-llh/output")
