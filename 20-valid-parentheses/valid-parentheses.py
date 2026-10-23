class Solution:
    def isValid(self, s: str) -> bool:
        stack = []

        for i in range(len(s)):
            if s[i] == '(' or s[i] == '{' or s[i] == '[':
                stack.append(s[i])

            else:
                if len(stack) == 0:
                    return False
                else:
                    if ((stack[-1] == '(' and s[i] == ')') or
                    (stack[-1] == '{' and s[i] == '}') or
                    (stack[-1] == '[' and s[i] == ']')):
                    
                        stack.pop()

                    else:
                        return False
        
        return len(stack) == 0


