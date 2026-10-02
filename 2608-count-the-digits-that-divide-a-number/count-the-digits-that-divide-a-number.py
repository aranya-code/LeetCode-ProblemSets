class Solution:
    def countDigits(self, num: int) -> int:
        result = 0

        for digit in str(num):
            digit = int(digit)

            if num % digit == 0:
                result += 1
        return result

        