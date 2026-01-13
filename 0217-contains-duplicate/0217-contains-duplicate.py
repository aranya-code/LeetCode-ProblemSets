class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        status = set()

        for i in nums:
            if i in status:
                return True
            status.add(i)
        return False