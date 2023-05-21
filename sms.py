# import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from twilio.rest import Client

# Twilio setup
account_sid = 'AC6e1bc09375053b77f46f8296c3e5b8cc'
auth_token = '24cd62937a25842f8571759a94c4bbe4'
client = Client(account_sid, auth_token)

# Your phone number and the recipient's phone number
from_phone_number = '+12545893281'
to_phone_number = '+966564775975'

# specify the file
file_path = "merged_fixed.csv"

# read the csv file
df = pd.read_csv(file_path)

# check if 'LocalTimeStamp' and 'T1_y' are in the dataframe columns
if "LocalTimestamp" not in df.columns or "T1_y" not in df.columns:
    print("Error: 'LocalTimestamp' or 'T1_y' not found in the dataframe")
else:
    # apply moving average to smooth the data
    df["T1_y_smooth"] = df["T1_y"].rolling(window=10).mean()

    # define the plot
    fig, ax = plt.subplots()

    # define the red box
    red_box = patches.Rectangle((0, 0), 1, 1, color="red")

    # flag to track whether the box should be displayed
    box_on = [False]

    # function to update the plot for each frame
    def update(frame):
        # add the data up to the current frame
        ax.clear()
        ax.plot(df["LocalTimestamp"][:frame], df["T1_y_smooth"][:frame])

        # add grid to the plot
        ax.grid(True)

        # if the latest value is above 38.5, toggle the box
        if df["T1_y"].iloc[frame] > 38.5:
            box_on[0] = not box_on[0]

            # Send an SMS alert
            message = client.messages.create(
                body='Alert: Value exceeded 38.5 at timestamp ' + str(df["Local
