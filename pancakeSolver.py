import heapq
import random

def reverse(li): ## a list reversing function since the built-in one does it in-place
    n = len(li) - 1
    newli = []
    while (n >= 0):
        newli = newli + [li[n]]
        n = n - 1
    return newli

def goal_check(n): ## creates the "correct" pancake stack -- used to see if solution is found
    return reverse(range(1, n+1))

def randomStack(n): ## initializes a randomized stack of size n
    li = range(1, n+1)
    random.shuffle(li)
    return li

class pancakeStack:

    def __init__(self, st=[]):
        self.stack = st

    def toList(self):
        return self.stack

    def flip(self, pos): ## flips the stack of pancakes at the specified position
                         ## stack = [1, 2, 3, 4]
                         ## stack.flip(1) = [4, 3, 2, 1]
                         ## indexing begins at 1. max cardinality of flip pos == len(stack)-1
                         ## i.e. stack.flip(3) = [1, 2, 4, 3]
                         ## and stack.flip(4) = [1, 2, 3, 4] = stack.flip(5) etc.
        if (pos == 1):
            return reverse(self.stack) # returns new list because this is used to create new stacks
        else:
            return self.stack[:pos-1] + reverse(self.stack[pos-1:])
        
    def stacklen(self):
        return len(self.stack)

    def heuristic(self): ## "Gap" heuristic test as defined in the word document
        score = 0
        lilen = len(self.stack)
        if (self.stack[0] != lilen): score = score + 1
        i = 0
        while (i < lilen-1):
            x = self.stack[i]
            plus1 = x + 1
            minus1 = x - 1
            if ((self.stack[i+1] != plus1) & (self.stack[i+1] != minus1)): ## if a pancake's neighbor is not an adjacent pancake, the heuristic score increases
                                                                           ## i.e. we're further from the goal line
                score = score + 1
            i = i + 1
        return score

    def goalAssert(self, goal): # check to see if a stack is in the "goal" state
        if (self.stack == goal): return True
        else: return False

class pancakeSolver:

    def Astar(self, stack):
        stacklen = stack.stacklen()
        goal = goal_check(stacklen) # create "correct" stack to check against
        
        if (stack.goalAssert(goal)): return [] ## if the pancakes are already in order do nothing
        
        pq = [] ## priority queue used to store unexplored nodes
    
        for x in range(1, stacklen): # at each possible flip position
            newstack = pancakeStack(stack.flip(x)) # create a new stack
            if (newstack.goalAssert(goal)): return [x]
            else:
                heapq.heappush(pq, (1+newstack.heuristic(), newstack, [x]))
                # if it's not the solution, push the candidate onto the priority queue
                # the cost is the backward cost of the flip (1) + the forward cost (heuristic)
    
        while len(pq) > 0: ## now, try the candidates in the queue by increasing cost
            curr = heapq.heappop(pq) ## get the least expensive node
            currstack = curr[1] ## the current list
            flips = curr[2] ## the flips made to produce the current list based on the initial (our solution)
            lastflip = flips[len(flips)-1]

            for x in range(1, stacklen):
                if (x != lastflip): # we don't want to backtrack and make the flip we just made
                    newstack = pancakeStack(currstack.flip(x))
                    if (newstack.goalAssert(goal)): return flips + [x]
                    else:
                        heapq.heappush(pq, (1+len(flips)+newstack.heuristic(), newstack, flips + [x]))
                        # the cost is the backward cost of the flips (1 + #flips) + the forward cost (heuristic)
                        
    #####################

    def userList(self, n):  ## takes custom input from the user to set up the stack of pancakes
        if (n < 2): return "Number too small!"
        li = []
        numbers = range(1, n+1)
        print "Welcome to the pancake flipper. Select the order of pancakes, starting from the bottom (5 is biggest)."
        
        while (1):
            num1 = input("Bottom Pancake. Enter a number 1-" + str(n))
            if num1 in numbers:
                li = li + [num1]
                break
            else:
                print "Number not in range (1-" + str(n) + "). Try again."
                
        i = 1
        while (i < n - 1):
            num = input("Next Pancake. Enter a number 1-" + str(n) + " (no repeats)")
            if num in numbers:
                if (num not in li):
                    li = li + [num]
                    i = i + 1
                else:
                    print str(num) + " has already been entered. Try again."
            else:
                print "Number not in range (1-" + str(n) + "). Try again."
                
        while (1):
            numlast = input("Last Pancake. Enter a number 1-" + str(n) + " (no repeats)")
            if numlast in numbers:
                if (numlast not in li):
                    li = li + [numlast]
                    return li
                else:
                    print str(lastnum) + " has already been entered. Try again."
            else:
                print "Number not in range (1-" + str(n) + "). Try again."
                
    ########################

    def flip(self, li, pos): ## used to print out the A* solution without creating a bunch of pancakeStacks
        if (pos == 1):
            return reverse(li)
        else:
            return li[:pos-1] + reverse(li[pos-1:])

    def Graphic_Astar(self, n): ## gives a graphical look at the Astar algorithm and how the solution is applied to order the pancakes
        stack = pancakeStack(self.userList(n))
        newli = stack.toList()
        sol = self.Astar(stack) ## result of Astar is just a list of flips
        i = 0
        n = len(sol)
        if (n == 0): print "Pancakes already in order!" ## if no flips, the pancakes were already ordered
        else:
            print "Starting configuration:      " + str(newli)
            while (i < n):
                newli = self.flip(newli, sol[i]) ## use initial position and flips to produce an ordered stack
                print "Flip at location " + str(sol[i]) + " yields:   " + str(newli)
                i = i + 1
            print "Done!"

    def Graphic_Astar_Auto(self, stack): # the above is for manual input. this is for automated input
        newli = stack.toList()
        sol = self.Astar(stack)
        i = 0
        n = len(sol)
        if (n == 0): print "Pancakes already in order!" 
        else:
            print "Starting configuration:      " + str(newli)
            while (i < n):
                newli = self.flip(newli, sol[i])
                print "Flip at location " + str(sol[i]) + " yields:   " + str(newli)
                i = i + 1
            print "Total: " + str(n) + " flips at locations (in order): " + str(sol)
            print "Done!"
            
    ########################


def main():
    print "Select Mode: "
    print "(1) Automatic (2) Manual"
    selection = input("Press 1 or 2 then Enter: ")
    choices = [1, 2]
    solver = pancakeSolver()
    while (selection not in choices):
        print "Bad input!"
        selection = input("Press 1 or 2 then Enter: ")
    if (selection == 1):
        n = random.randint(3, 20)
        print "Random stack size = " + str(n)
        stack = pancakeStack(randomStack(n))
        solver.Graphic_Astar_Auto(stack)
    else:
        print "Choose stack size (>2): "
        num = input("Input number then press Enter: ")
        while (num < 3):
            print "Bad input!"
            num = input("Input number then press Enter: ")
        print "Choose stack manually (1)? Or initialize random stack with chosen size (2)?"
        sel = input("Press 1 or 2 then Enter: ")
        while (sel not in choices):
            print "Bad input!"
            sel = input("Press 1 or 2 then Enter: ")
        if (sel == 1):
            solver.Graphic_Astar(num)
        else:
            stack = pancakeStack(randomStack(num))
            solver.Graphic_Astar_Auto(stack)

if __name__ == "__main__":
    main()
    


    
