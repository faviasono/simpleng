from datetime import datetime
import pandas as pd


class HistoryRetrieval:
    def __init__(self, user_id):
        self.user_id = user_id

    def load_history(self):
        # TODO: make connection BQ

        return pd.DataFrame([dict(input_text="hello there", output_text="Hi darling", timestamp_add=datetime.now())])
