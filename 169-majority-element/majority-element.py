class Solution:
    def majorityElement(self, nums: list[int]) -> int:

        hash_map ={}

        for i in nums:
            if i in hash_map:
                hash_map[i] += 1
            else:
                hash_map[i] = 1

        result = 0

        for key, count in hash_map.items():
            if count > len(nums) // 2:
                return key
        