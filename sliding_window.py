"""
"Given a real-time stream of joint torques, detect when a robot is approaching its torque limit using a rolling window. Implement with O(1) updates." — tests deque-based sliding window.
"""

class RollingWindow():
    def __init__(self, torque_limit: float = 10, window_size : int = 5):
        self.torque_limit = torque_limit
        self.window_size = window_size

        # initialize queue and average. We will implement it as a list with an index pointing to head that cycles through itself.
        self.window = [0.0] * self.window_size
        self.average = 0

        # count keeps track of how many things we've added to this list. It also acts like the current idx via modulo.
        self.count : int = 0

    def idx(self):
        return self.count % self.window_size

    def update(self, torque : float) -> tuple[float, bool]:
        """
        Given a torque, updates the rolling window and returns the average and whether average is greater than or equal to self.torque_limit.
        """
        # if count <= self.window_size - 1, then we are still warmstarting.
        if self.count <= self.window_size - 1:
            # Add incoming torque to window at idx, calculate average manually, increment count
            self.window[self.idx()] = torque
            self.average = sum(self.window) / (self.count + 1)
        else:
            # get old value, replace it with new torque, then update average
            old_torque = self.window[self.idx()]
            self.window[self.idx()] = torque
            self.average += (torque / self.window_size) - (old_torque / self.window_size)
        # increment count then return average and whether threshold is exceeded
        self.count += 1
        return self.average, self.average >= self.torque_limit

torque_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0]
window = RollingWindow()
for torque in torque_list:
    print(window.update(torque))