# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        current = head
        index = 0
        while current:
            index += 1
            current = current.next

        target_index = index - n
        if target_index == 0:
            return head.next
        current = head
        prev = None
        current_index = 0
        while current:
            if current_index == target_index:
                prev.next = current.next
                break
            prev = current
            current = current.next
            current_index += 1

        return head




        