class Solution:
    def findMaxConsecutiveOnes(self, nums: list[int]) -> int:
        
        max_count = 0
        count = 0

        for num in nums:
            if num == 1:
                count += num
            else:
                count = 0
            
            max_count = max(count, max_count)
        return max_count

