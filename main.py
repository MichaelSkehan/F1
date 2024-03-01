import fastf1
import seaborn as sns
from matplotlib import pyplot as plt
import fastf1.plotting
import timple.timedelta as tmpldelta

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

session = fastf1.get_session(2024, 'Bahrain', 'FP2')
session.load()
drivers=['VER', 'HAM']

driver_laps = session.laps.pick_drivers(drivers).pick_laps(range(10,21,1)).reset_index()
print(driver_laps['LapTime'])
fig, ax = plt.subplots(figsize=(8, 8))

sns.scatterplot(data=driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Driver",
                s=80,
                linewidth=0,
                legend='auto')
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

# manually set the format to force no offset
formatter = tmpldelta.TimedeltaFormatter("%m:%s:%ms")
ax.yaxis.set_major_formatter(formatter)

# The y-axis increases from bottom to top by default
# Since we are plotting time, it makes sense to invert the axis
ax.invert_yaxis()
plt.suptitle("VER V HAM long run laptimes Bahrain FP2 2024")

# Turn on major grid lines
plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()