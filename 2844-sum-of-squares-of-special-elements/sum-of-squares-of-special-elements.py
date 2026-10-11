class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        result = 0

        for i in range(len(nums)):
            if len(nums) % (i+1) == 0:
                result += nums[i] * nums[i]
        
        return result
