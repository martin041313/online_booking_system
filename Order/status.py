'''
@version: v2.0
@note: All status of an order
'''
ORDER_UNPAID = 0   		# after user creates order 
ORDER_PAID = 1	   		# after user pays order
ORDER_SHIPPING = 2    		# after seller sends product 
ORDER_ARRIVE = 3   		# after the product arrives
ORDER_COMPLETED = 4		# after the user confirms the receiption
ORDER_REFUND_PENDING = 5	# after someone posts cancel request 
ORDER_CLOSED = 6		# after the order closes abnormally
ORDER_COMMENTED = 7     # after the order is commented
