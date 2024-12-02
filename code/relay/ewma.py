class EWMA:
    def __init__(self, initial_length=10, alpha=0.2, increase=0.15, decrease=0.15):
        self.current_length = initial_length  # initial focus length (e.g., 10 minutes)
        self.alpha = alpha  # smoothing factor for EWMA
        self.previous_length = initial_length  # starting point for EWMA
        self.increase = increase  # increase factor for focus length
        self.decrease = decrease # decrease factor for focus length

        self.predicted = []
        self.actual = []

    def adjust(self, completed_session_length):
        """
        Adjust the focus length based on the completed session length
        """

        if completed_session_length >= self.current_length or completed_session_length in self.actual:
            adjustment = 1 + self.increase
        else:
            adjustment = 1 - self.decrease

        self.actual.append(completed_session_length)
        
        # Apply EWMA with adjustment
        self.current_length = (self.alpha * (completed_session_length) + (1 - self.alpha) * self.previous_length) * (adjustment)
        # self.current_length = ro,nd(self.current_length, )
        self.current_length = self.current_length // 1

        # Update the previous length for the next session
        self.previous_length = self.current_length
        self.predicted.append(self.current_length)

        return self.current_length

    def export(self):
        """
        Export the actual and predicted focus lengths
        """
        return self.actual, self.predicted

    def focus_score(self):
        """
        Calculate the focus score based on the actual and predicted focus lengths
        """
        return sum(self.actual) / sum(self.predicted)

if __name__ == '__main__':
    focus = EWMA()

    # User completes a 15-minute session
    next_suggestion = focus.adjust(15)
    print(f"Next suggested focus length: {next_suggestion} minutes")

    # User completes a 5-minute session
    next_suggestion = focus.adjust(15)
    print(f"Next suggested focus length: {next_suggestion} minutes")

    next_suggestion = focus.adjust(15)
    next_suggestion = focus.adjust(10)

    print(focus.actual)
    print(focus.predicted)

