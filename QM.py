class QM:
  def __init__(self):
    self.__v = int(input('Enter the number of variables: '))
    temp =str(input('Enter min-terms separated by spaces :'))
    self.__mt=temp.split(' ')
    for i in range(len(self.__mt)):
      self.__mt[i]=int(self.__mt[i])
    self.__mt.sort()
    self.__dnt = ''
    for i in range(self.__v):
      self.__dnt+='x'
    self.__answer = ''
    
  def solve(self):
    self.__create_tables()
    self.__tobin()
    self.__ones()
    self.__PItables()
    self.__PIselect()
    self.__EPItable()
    self.__EPIselect()
    self.__expression()

  def __create_tables(self):
    self.__tables=[]
    for i in range(self.__v+1):
      self.__tables.append([])
      for j in range((self.__v)+1-i):
        self.__tables[i].append([])

#converting minterms into binary form and removing invalid entries
  def __tobin(self):
    for i in range(len(self.__mt)):
      self.__mt[i] = bin(self.__mt[i])
      self.__mt[i] = self.__mt[i].replace('0b','')
      while (len(self.__mt[i])<self.__v):
        self.__mt[i] = '0'+self.__mt[i]
    i=0
    while (i<len(self.__mt)-1):
      if(self.__mt[i]==self.__mt[i+1]):
        self.__mt.pop(i)
        i-=1
      i+=1
    i=0
    while (i<len(self.__mt)):
      if (len(self.__mt[i])>self.__v):
        self.__mt.pop(i)
        i-=1
      i+=1

#grouping terms having same no of 1's
  def __ones(self):
    for i in range(len(self.__mt)):
      temp = str(self.__mt[i])
      min_no = int(temp,2)
      min_no = 'm'+str(min_no)
      nos=temp.count('1')
      self.__tables[0][nos].append([min_no,self.__mt[i],0])
      self.__mt[i]=[min_no,self.__mt[i]] 
  
  def __PItables(self):
    for i in range(len(self.__tables)-1):
      for j in range(len(self.__tables[i])-1):
        for k in range(len(self.__tables[i][j])):
          for l in range(len(self.__tables[i][j+1])):
            ret,mark = self.__comp(self.__tables[i][j][k][1],self.__tables[i][j+1][l][1],self.__tables[i][j][k][0],self.__tables[i][j+1][l][0])
            if(self.__tables[i][j][k][2]!=1):
              self.__tables[i][j][k][2]=mark
            if(self.__tables[i][j+1][l][2]!=1):
              self.__tables[i][j+1][l][2]=mark
            if(mark==1):
              self.__tables[i+1][j].append(ret) 

  def __comp(self,a,b,c,d):
    ind = str(c)+','+str(d)
    temp = ind.split(',')
    i=0
    while (i<len(temp)-1):
      if(temp[i]==temp[i+1]):
        temp.pop(i)
        i-=1
      i+=1
    ind = temp[0]
    for i in range(1,len(temp)):
      ind= ind+','+temp[i]
    temp = []
    diff = 0
    term = ''
    for i in range(len(a)):
      if(a[i]!=b[i]):
        diff+=1
    if (diff!=1):
      temp=[ind,self.__dnt,0]
      return temp,0
    else:
      for i in range(len(a)):
        if(a[i]!=b[i]):
          term+='-'
        else:
          term+=a[i]
      temp=[ind,term,0]
      return temp,1
      
  def __PIselect(self):
    self.__PI=[]
    for i in range(len(self.__tables)):
      for j in range(len(self.__tables[i])):
        for k in range(len(self.__tables[i][j])):
          if((self.__tables[i][j][k][2]!=1)and(self.__tables[i][j][k][1]!=self.__dnt)):
            temp=self.__tables[i][j][k]
            self.__PI.append([temp[0],temp[1]])
    i=0
    while (i<len(self.__PI)-1):
      if(self.__PI[i][1]==self.__PI[i+1][1]):
        self.__PI.pop(i)
        i-=1
      i+=1   
        
  def __EPItable(self):
    self.__EPItable=[]
    temp=[]
    for i in range(len(self.__mt)):
      temp.append(self.__mt[i][0])
    temp.insert(0,[])
    self.__EPItable.insert(0,temp)
    for i in range(len(self.__PI)):
      temp = self.__PI[i]
      temp.append(0)
      self.__EPItable.insert(i+1,[temp])
      for j in range(len(self.__mt)):
        self.__EPItable[i+1].append(0)
    for i in range(1,len(self.__EPItable)):
      for j in range(1,len(self.__EPItable[0])):
        temp = self.__EPItable[i][0][0].split(',')
        t=0
        for k in range(len(temp)):
          if(self.__EPItable[0][j]==temp[k]):
            t+=1
            break
        if (t!=0):
          self.__EPItable[i][j]=1
    
  def __EPIselect(self):
    for i in range(1,len(self.__EPItable)):
      for j in range(1,len(self.__EPItable[0])):
        total=0
        first=0
        for k in range(1,len(self.__EPItable)):
          total+=self.__EPItable[k][j]
        if(total==i):
          for l in range(1,len(self.__EPItable)):
            if(self.__EPItable[l][j]==1):
              first=l
              break
        last=len(self.__EPItable)-1
        done=0
        while(last>=first):
          if((self.__EPItable[last][j]==1)and(self.__EPItable[last][0][2]==1)):
            done+=1
            break
          last-=1
        if(done==0 and first!=0):
          self.__EPItable[first][0][2]=1
    self.__EPI=[]
    for i in range(1,len(self.__EPItable)):
      if(self.__EPItable[i][0][2]==1):
        temp=[self.__EPItable[i][0][0],self.__EPItable[i][0][1]]
        self.__EPI.append(temp)

  def printTables(self):
    print('Prime Implicant selection tables')
    for i in range(len(self.__tables)):
      print('================')
      print('Table ',i+1)
      print('================')
      for j in range(len(self.__tables[i])):
        for k in range(len(self.__tables[i][j])):
          temp=self.__tables[i][j][k]
          if(temp[1]!=self.__dnt):
            print(temp)
        print('-------------------')
    print()
    print('Essential Prime Implicant selection table')
    for i in range(len(self.__EPItable)):
      print(self.__EPItable[i])
    
  def printImplicants(self):
    print('Prime Implicants')
    for i in range(len(self.__PI)):
      print(self.__PI[i][0],'     ',self.__PI[i][1])
    print()
    print('Essential Prime Implicants')
    for i in range(len(self.__EPI)):
      print(self.__EPI[i][0],'     ',self.__EPI[i][1])

  def solution(self):
    print()
    print('_______________________')
    print('Minimal Expression: ',self.__answer)
    print('_______________________') 

  def __expression(self):
    letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    self.__vars=[]
    for i in range(self.__v):
      self.__vars.append(letters[i])
    temp = []
    for i in range(len(self.__EPI)):
      temp.append(self.__EPI[i][1])
    for i in range(len(temp)):
      exp=''
      ind=0
      for j in self.__vars:
        if(temp[i][ind]=='1'):
          exp+=j
        elif(temp[i][ind]=='0'):
          exp+=j
          exp+='\''
        ind+=1
      temp[i]=exp
    for i in range(len(temp)):
      self.__answer+=temp[i]
      if(i<(len(temp)-1)):
        self.__answer+='+'
    self.__answer.replace('+',' + ')
    self.solution()