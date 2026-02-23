"""
"Given a real-time stream of joint torques, detect when a robot is approaching its torque limit using a rolling window. Implement with O(1) updates." — tests deque-based sliding window.
"""

def calculate_rolling_window(torque_limit : float = 10, queue_size : int = 5) -> float:
    # initialize internal queue to be empty
    my_queue = [0.0] * queue_size 
    # current idx for queue
    idx = 0
    
    # initial current average over window
    current_average = 0

    # Get first torque
    new_torque = yield

    while True:
        # Add torque to end of queue
        my_queue.append(new_torque)

        # check if queue is over limit. If so, remove oldeset element
        if len(my_queue) > queue_size:
            # get oldest torque
            oldest_torque = my_queue[0]
            # update queue to not have torque
            my_queue = my_queue[1:]
            # update current average by adding (new_torque / queue_size - oldest_torque / queue_size)
            current_average += (new_torque / queue_size) - (oldest_torque / queue_size)
        else: # queue too small for window, just return average, no easy way to get the average in O(1)
            current_average = sum(my_queue) / len(my_queue)
        # yield current_average
        new_torque = yield current_average

torque_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0]
gen = calculate_rolling_window()
next(gen)
for torque in torque_list:
    print(gen.send(torque))