import pandas as pd
import matplotlib.pyplot as plt

# Create DataFrames for each dataset
population_data = {
    'Year': [1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Population (K)': [806, 806, 1174, 1370, 1578, 1630, 1669, 1718, 1789, 1872, 1976, 2032, 2089, 2150, 2234, 2332, 2430, 2526, 2598, 2657, 2776, 2841, 2930, 3022, 3121, 3225, 3338, 3422, 3493, 3575, 3653, 3738, 3836, 3922, 3978, 4064, 4119, 4200, 4266, 4331, 4407, 4470, 4560, 4822, 5059, 5196, 5328, 5472, 5612, 5757, 5900, 6041, 6209, 6369, 6508, 6631, 6748, 6869, 6991, 7116, 7244, 7337, 7552, 7695, 7837, 7984, 8134, 8297, 8463, 8628, 8798, 8967, 9140, 9291, 9449, 9656, 9842]
}

losses_data = {
    'Start Year': [1947, 1956, 1967, 1967, 1973, 1978, 1982, 1985, 1987, 1996, 2000, 2006, 2008, 2012, 2014, 2021, 2023],
    'All Losses': [2000, 300, 40, 56, 50, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, 10, 1500]
}

df_population = pd.DataFrame(population_data)
df_losses = pd.DataFrame(losses_data)

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Population
ax1.plot(df_population['Year'], df_population['Population (K)'], color='blue', label='Population (K)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Population (K)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for losses
ax2 = ax1.twinx()
ax2.plot(df_losses['Start Year'], df_losses['All Losses'], color='red', label='All Losses', linestyle='--')
ax2.set_ylabel('All Losses', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add titles and legends
fig.suptitle('Population Growth and Losses Over the Years')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show plot
plt.show()
