class EWMA:
    def __init__(self, initial_length=10, alpha=0.4, increase=0.15, decrease=0.05):
        self.current_length = initial_length  # initial focus length (e.g., 10 minutes)
        self.alpha = alpha  # smoothing factor for EWMA
        self.previous_length = initial_length  # starting point for EWMA
        self.increase = increase  # increase factor for focus length
        self.decrease = decrease # decrease factor for focus length

        self.history = [10]
        self.actual = [10]


    def adjust(self, completed_session_length):
        # Determine if the session length should be increased or decreased
        if completed_session_length >= self.current_length or completed_session_length not in self.actual:
            # adjustment = self.current_length * (1 + self.increase)  # Increase by 10% if they stayed focused
            adjustment = 1 + self.increase
        else:
            # adjustment = self.current_length * (1 - self.decrease)  # Decrease by 5 minutes if they didn't stay focused
            adjustment = 1 - self.decrease

        self.actual.append(completed_session_length)
        
        # Apply EWMA with adjustment
        self.current_length = (self.alpha * (completed_session_length) + (1 - self.alpha) * self.previous_length) * (adjustment)
        # print(f"Previous length: {self.previous_length}, Current length: {self.current_length}")


        # Update the previous length for the next session
        self.previous_length = self.current_length
        self.history.append(self.current_length)

        return self.current_length

if __name__ == '__main__':
    focus = EWMA()

    # User completes a 15-minute session
    next_suggestion = focus.adjust(15)
    print(f"Next suggested focus length: {next_suggestion} minutes")

    # User completes a 5-minute session
    next_suggestion = focus.adjust(15)
    print(f"Next suggested focus length: {next_suggestion} minutes")

    next_suggestion = focus.adjust(15)
    next_suggestion = focus.adjust(15)

    print(focus.actual)
    print(focus.history)

