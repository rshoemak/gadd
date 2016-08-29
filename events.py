

import os

te_inp = os.getenv("TRIGGER_EVENT_IP")

# Set static trigger for demo. This would be the user IP at the branch.
# te_inp="10.100.1.10"


def trigger_event():
    e_trigger = te_inp
    return e_trigger
