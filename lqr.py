"""
"Implement a simple 1D discrete-time LQR rollout. Given A, B, Q, R matrices, simulate a trajectory and compute the cost." — tests numerical reasoning and matrix ops in code.
"""
# We treat all vectors as column vectors, but since we assume this id 1D, A, B, Q, R, state and action are all scalars and transpose does nothing.
# Dynamics: x_{t+1} = A*x_t + B*u_t
# Cost: of trajectory \tau = [x_1,...,x_T]: \sum_{t=1}^{T} x_{t}^T * Q * x_{t} + u_t * R * u_t

class LQR():
    def __init__(self, A, B, Q, R):
        self.A = A
        self.B = B
        self.Q = Q
        self.R = R

    def compute_trajectory_cost(self, state_list : list[float], action_list : list[float]):
        """
        We assume state_list is length T+1, and action_list is length T.
        """
        total_cost = 0
        for (x_t, u_t) in zip(state_list[:-1], action_list, strict=True):
            total_cost += (x_t**2)*self.Q + (u_t **2) * self.R
        # terminal state cost
        total_cost += (state_list[-1]**2)*self.Q

        return(total_cost)
    def simulate_trajectory(self, x_0: float, action_list: list[float]):
        # make a list to hold state trajectories, put in starting state
        state_list = [x_0]
        # go through each action and add new state using most recent state tau[-1]
        for action in action_list:
            next_state = self.A * state_list[-1] + self.B * action
            state_list.append(next_state)
        return(state_list, action_list)
    
lqr = LQR(1,1,1,1)
action_list = [2.0, 3.0]
start_state = 0.0
state_list, action_list = lqr.simulate_trajectory(start_state, action_list)
lqr.compute_trajectory_cost(state_list, action_list)
