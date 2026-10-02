#282A
'''a=0
for i in range(int(input())):
    o=input()
    if o.count('++')!=0:
        a+=1
    elif o.count('--')!=0:
        a-=1
print(a)'''

#50A
'''a=input()
y=list(map(int,a.split()))
print(y[0]*y[1]//2)'''

#263A
'''a=[]
for i in range(5):
    y=list(input().split())
    a.append(y)
for j in range(5):
    if '1' in a[j]:
        g=j
for k in range(5):
    if '1' in a[g][k]:
        m=k
print(abs(int(g)-2)+abs(int(m)-2))'''

#236Aa=input()
'''n=0
an=[]
for i in a:
    if i not in an:
        if a.count(i)==1:
            n+=1
        elif a.count(i)>1:
            an.append(i)
            n+=1
print('CHAT WITH HER!' if n%2==0 else 'IGNORE HIM!')'''

#281A
'''a=input()
b=a.capitalize()
print (b[0]+a[:0]+a[1:])'''

#2256A
'''for i in range(int(input())):
    l=list(map(int,input().split()))
    t=max(l)-min(l)
    m=l.index(max(l))
    l[m]=sum(l)-max(l)
    n=max(l)-min(l)
    print(t if t<n else n)'''

#791A
'''l=list(map(int,input().split()))
b=0
while l[0]<=l[1]:
    l[0]*=3
    l[1]*=2
    b+=1
print(b)'''

#617A
'''n=int(input())
b=0
while n>0:
    if n>=5:
        n-=5
        b+=1
    else:
        n-=n
        b+=1
print(b)'''

#266A
'''a=0
b=int(input())
l=list(input())
n,m=0,1
for i in range(b-1):
    if l[n]==l[m]:
        a+=1
    n+=1
    m+=1
print(a)'''

#546A
'''l=list(map(int,input().split()))
t=(l[2]*(l[2]+1))*l[0]/2
print(int(t-l[1]) if t>=l[1] else 0)'''

#59A
'''l=input()
b,c=0,0
for i in l:
    if i.isupper():
        b+=1
    else:
        c+=1
if b>c:
    print(l.upper())
else:
    print(l.lower())'''

#977A
'''l=list(map(int,input().split()))
for i in range(l[1]):
    if l[0]%10==0:
        l[0]/=10
    else:
        l[0]-=1
print(int(l[0]))'''

'''#110
a=list(input())
l=a.count('4')+a.count('7')
if l==4 or l==7 or l==47 or l==
    if len(a)==1:
        print('NO')
    else:
        print('YES')
else:
    print('NO')'''