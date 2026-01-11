# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        list1 = l1
        list2 = l2
        carry = 0
        dummyList =ListNode()
        dummyHead = dummyList

        while list1 or list2 or carry:
            result = carry
            if list1:
                result += list1.val
                list1 = list1.next
            if list2:
                result += list2.val
                list2 = list2.next
            
            dummyList.next = ListNode(int(result % 10))
            dummyList = dummyList.next
            carry = int(result // 10)
        
        return dummyHead.next
