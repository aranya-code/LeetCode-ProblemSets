class Solution:
    def maximumSubarraySum(self, nums: list[int], k: int) -> int:

        max_sum = 0
        window_sum = 0
        freq_map = {}
        left = 0

        for right in range(len(nums)):
            window_sum += nums[right]
            freq_map[nums[right]] = freq_map.get(nums[right], 0) + 1

            if right - left + 1 > k:
                outgoing = nums[left]

                window_sum -= outgoing
                freq_map[outgoing] -= 1

                if freq_map[outgoing] == 0:
                    del freq_map[outgoing]
                
                left += 1

            if right - left + 1 == k and len(freq_map) == k:
                max_sum = max(max_sum, window_sum)
        
        return max_sum
