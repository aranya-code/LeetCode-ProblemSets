class Solution:

    from collections import deque

    def timeRequiredToBuy(self, tickets: list[int], k: int) -> int:

        queue = deque(enumerate(tickets))
        time = 0

        while queue:
            person, remaining = queue.popleft()

            remaining -= 1
            time += 1

            if remaining > 0:
                queue.append((person, remaining))

            elif person == k:                
                return time

        return time
