class Solution:
    def maxArea(self, height: list[int]) -> int:
        
        left = 0
        right = len(height) - 1

        curr_area = 0
        max_area = 0

        while left < right:

            if height[left] < height[right]:

                curr_area = (right - left) * min(height[left], height[right])

                max_area = max(curr_area, max_area)

                left += 1
            
            else:
                curr_area = (right - left) * min(height[left], height[right])
                
                max_area = max(curr_area, max_area)
                
                right -= 1

            
            

        return max_area


