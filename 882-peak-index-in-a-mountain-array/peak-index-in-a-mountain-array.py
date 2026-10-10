class Solution:
    def peakIndexInMountainArray(self, arr: list[int]) -> int:

        left = 1
        right = len(arr) - 2

        while left < right:

            mid = left + (right - left) // 2

            if arr[mid-1] < arr[mid] and arr[mid] > arr[mid+1]:
                return mid

            elif arr[mid-1] < arr[mid]:
                left = mid + 1

            else:
                right = mid

        return left