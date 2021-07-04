

def Similarity(interest,product):
    splittedInterest=interest.split(" ")
    splittedProduct=product.split(" ")
    rVector=splittedInterest+(splittedProduct)
    l1=[]
    l2=[]
    for word in rVector:
        if word in splittedInterest:l1.append(1)
        else:l1.append(0)
        if word in splittedProduct:l2.append(1)
        else:l2.append(0)
    c=0
    for i in range(len(rVector)):
        c+=l1[i]*l2[i]
    cosine=c / float((sum(l1)*sum(l2))**0.5)
   
    return cosine