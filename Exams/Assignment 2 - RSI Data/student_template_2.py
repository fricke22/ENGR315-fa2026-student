"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
#makes the siginifigence level 0.05, which we can use to answer the null hypthesis
a = 0.05
#locate and read teh CSV file containing the RSI data 
folder = Path(__file__).resolve().parent
data = pd.read_csv(folder / "data" / "drop-jump" / "all_participant_data_rsi.csv")

#Task 1 T-Test
#grab both measurment from the shared trials
pair = data.dropna(subset=["force_plate_rsi", "accelerometer_rsi"])
# this seperates the two measumrents into individual variables 
fp = pair["force_plate_rsi"]
acc = pair["accelerometer_rsi"]

#this is the differecnces between the two expermental values 
difference = fp - acc
#this performes a t-stat and the p value 
t_stat, p_val = stats.ttest_rel(fp, acc)
#displays the data from the trials 
print(f"Number of paried trails is {len(pair)}")
print(f"Force plate mean = {fp.mean()}")
print(f"Accelerometer mean = {acc.mean()}")
print(f"Mean paired diff is{difference.mean()}")
print(f"t-val is{t_stat}")
print(f"p_value is {p_val}")
#this either rejcets or accepts the null hypothesis
if p_val < a:
    print("Reject H,, to large of a difference in mean ")
else:
    print("Fail to reject H")
#task 2
# we only need the accel for this test 
accel = data["accelerometer_rsi"].dropna()
#mu is the esitmaed me and sigma is the esitmated stand diviation 
mu, sigma = stats.norm.fit(accel)
#number of bins for chi test
numbin = 10
# fits the normal distrubation in 10 equal probabilty regions 
prob = np.linspace(0,1, numbin + 1)
#each bin ideally should 9.7 enteries for the bun 
binedge = stats.norm.ppf(prob, loc=mu, scale=sigma)
#this is the observed frequiences 
observe, _ = np.histogram(accel, bins=binedge)

# these are the expected about in each of the 10 bins 
expected = np.full(numbin, len(accel) / numbin)
#perfoms a chi square goodness of fit test 
#ddof  reduces the degrees of freedom by 2, because we already use the mean and standdev from teh sample data
chi_stat, chi_p = stats.chisquare(f_obs=observe, f_exp=expected,ddof=2)
# display the fitted normal distrubbation and the chi square test 
print("\nTASK 2: Accelerometer normal goodness-of-fit test")
print(f"Fitted mean = {mu}")
print(f"Fitted standard deviation = {sigma}")
print(f"Observed counts = {observe}")
print(f"Expected count per bin = {expected[0]}")
print(f"Chi-square statistic = {chi_stat}")
print(f"Degrees of freedom = {numbin - 1 - 2}")
print(f"p-value = {chi_p}")

#we create the hisogram here 
plt.figure(figsize=(8,5))
plt.hist(accel,bins=12,density=True,color="white", edgecolor="black", label="Task 2")
#400 evenly spaced boxes across 3 standard devations 
x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 400)
plt.plot(x, stats.norm.pdf(x, loc=mu, scale=sigma),color="red",linewidth=2,label="fittednorm")

plt.title("Accelerometer RSI across all participants")
plt.xlabel("accelerometer RSI")
plt.ylabel("Probability density")
plt.legend()
#this can adjust the spacing so nothing overlaps 
plt.tight_layout()
#we can determine the fit from the normal distributiom 
if chi_p < a:
    print("Reject H, normal distrubution is a bad fit")
else:
    print("Fail to rejcet H")
#Task 3
# this only picks trials with F
partf = data.loc[data["trial"].str.startswith("F_trial")].copy()
#Defines a function with a confidence interval 
def mean_ci(label, values):
    #remove the missing measurments
    values = values.dropna()
    #finds the sample mean 
    mean = values.mean()
    # calculates the interval using the tudents t disptrubtionm
    low,upp = stats.t.interval(confidence=1-a,df=len(values) - 1,loc=mean, scale=stats.sem(values))
    print(f"{label}: mean = {mean:.5f}, 95% CI = [{low:.5f}, {upp:.5f}]")
# takes the froce plate measurments from the f trials 
f_fp = partf["force_plate_rsi"]
# tajkes the accelerometer measuments from the 5 trials 
f_acc = partf["accelerometer_rsi"]
#95% confidence interval for the force plate
mean_ci("Force plate", f_fp)
#95% confidence interval for the accelerometer
mean_ci("Accelerometer", f_acc)
#postivie indicates a higher force plate, while negative indicates a higher accelermeter 
mean_ci("Force plate minus accelerometer", f_fp - f_acc)
# show the plot 
plt.show()