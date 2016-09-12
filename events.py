

import os

te_inp = os.getenv("TRIGGER_EVENT_IP")

# Set static trigger for demo. This would be the user IP at the branch.
# te_inp="172.16.91.77/24" (PC bad guy)
# Server to ping simulated 172.16.118.120 in branch


def trigger_event():
    e_trigger = te_inp
    return e_trigger
