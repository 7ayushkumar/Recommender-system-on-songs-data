
# coding: utf-8


import math

from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # m:
    # the number of recommedations to return
    # defaults to 10
    #
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            #print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            #print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            #print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        #for userX in self.usersItemRatings.keys():
        if(self.k<3):
            UserXItemRatings=self.usersItemRatings[userX]
            lst=[]
            for UserY, UserYItemRatings in self.usersItemRatings.items():
                pearsonXY=self.pearsonFn(UserXItemRatings,UserYItemRatings)
                tup=(UserY,pearsonXY)
                lst.append(tup)
 
 
            sortd=sorted(lst, key=itemgetter(1), reverse=True)
            #return sortd     #[('Angelica', 1.0), ('Veronica', 0.83), ('Chan', 0.82), ('Jordyn', 0.76), ('Hailey', 0.42), ('Sam', 0.28), ('Dan', -0.36), ('Bill', -0.9)]
            ratings=self.usersItemRatings[sortd[1][0]]
            #return ratings   #{'Blues Traveler': 3.0, 'Norah Jones': 5.0, 'Phoenix': 4.0, 'Slightly Stoopid': 2.5, 'The Strokes': 3.0}
                
            d1 = {key:ratings[key] for key in ratings if key not in UserXItemRatings}
            recommendation1=sorted(d1.items(), key=itemgetter(1), reverse=True)                    #putting recommendations in form of a tuple
            return recommendation1
        
        
###### Recommendation according to three nearest neighbours

        elif(self.k==3):
            UserXItemRatings=self.usersItemRatings[userX]
            lst=[]
            for UserY, UserYItemRatings in self.usersItemRatings.items():
                pearsonXY=self.pearsonFn(UserXItemRatings,UserYItemRatings)
                pearsonXY=round((pearsonXY+1)/2,2)
                tup=(UserY,pearsonXY)
                #tup=(pearsonXY)
                lst.append(tup)
            #return lst
                
                
            sortd=sorted(lst, key=itemgetter(1),reverse=True)

            top3=sortd[1:4]
            #return top3      #[('Angelica', 0.92), ('Jordyn', 0.88), ('Chan', 0.64)]
            p_list=[top3[1] for top3 in lst]      #getting pearson values in form of list
            
        
            #return p_list                            #[0.92, 0.12, 0.64, 0.12, -0.5, 0.88, 0.22, 1.0]        
        
        
            ##Calculating the weights
            
            
            wt=sorted(p_list, reverse=True)
            wtK = wt[1:4]
        #return sortd2                           #Veronica : [0.92, 0.88, 0.64]
        
            total_wt = wt[1]+wt[2]+wt[3]
              
            i=0
            while i < len(wtK):
                wtK[i]=(wtK[i])/total_wt
                i += 1
            #weight = [ round(elem, 2) for elem in wtK ]
            weight = [ elem for elem in wtK ]
            #return rl     #Veronica : [0.38, 0.36, 0.26]
            

            ratingsK1=self.usersItemRatings[top3[0][0]]  
            ratingsK2=self.usersItemRatings[top3[1][0]] 
            ratingsK3=self.usersItemRatings[top3[2][0]]
            

            ratings1={}
            ratings1.update((x, y*weight[0]) for x, y in ratingsK1.items())  
            ratings2={}
            ratings2.update((x, y*weight[1]) for x, y in ratingsK2.items())
            ratings3={}
            ratings3.update((x, y*weight[2]) for x, y in ratingsK3.items())
        

        sumD = {x: ratings1.get(x, 0) + ratings2.get(x, 0) + ratings3.get(x, 0) for x in set(ratings1).union(ratings2).union(ratings3)}     

        for k, v in sumD.items():
            sumD[k] = round(v, 2)
        #return sumD      #{'Deadmau5': 1.7, 'Vampire Weekend': 2.2, 'Broken Bells': 2.64, 'Blues Traveler': 2.63, 'Norah Jones': 4.29, 'Phoenix': 5.0, 'Slightly Stoopid': 2.45, 'The Strokes': 2.39}
            


        d2 = {key:sumD[key] for key in sumD if key not in UserXItemRatings}   
        recomemendation2=sorted(d2.items(), key=itemgetter(1), reverse=True)
        return recomemendation2    

