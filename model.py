class Model:
    def __init__(self, duration=7200, time_step=5, num_attendees=1000):
        """
        :param duration: total simulation length in seconds
        :param time_step: time step in seconds
        :param num_attendees: number of people attending event
        """
        self.event_checkpoints = []
        self.attendee_set = []
        self.num_attendees = num_attendees
        self.time_step = time_step
        self.current_time = 0
        self.end_time = duration

    def update(self):
        """
        process a single time step
        :return:
        """
        pass