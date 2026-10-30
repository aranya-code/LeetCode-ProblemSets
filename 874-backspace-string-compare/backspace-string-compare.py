class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        
        stack1 = []
        for i in s:
            if i == '#':
                if stack1:
                    stack1.pop()
            else:
                stack1.append(i)


        stack2 = []
        for j in t:
            if j == '#':
                if stack2:
                    stack2.pop()
            else:
                stack2.append(j)


        return stack1 == stack2
            
            