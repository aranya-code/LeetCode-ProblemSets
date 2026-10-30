class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack1 = []

        for i in s:
            if stack1 and stack1[-1] == i:
                stack1.pop()
            else:
                stack1.append(i)

        return "".join(stack1)

        