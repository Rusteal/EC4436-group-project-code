import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read ONS CSV
df = pd.read_csv(
    "unemployment_relevant.csv",
    header=None,
    names=["date", "unemployment"],
    encoding="utf-8-sig"
)

# Convert dates and values
# Automatically excludes annual, quarterly and metadata rows
df["date"] = pd.to_datetime(
    df["date"], format="%Y %b", errors="coerce"
)

df["unemployment"] = pd.to_numeric(
    df["unemployment"], errors="coerce"
)

df = df.dropna().sort_values("date")

# Plot
fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(
    df["date"],
    df["unemployment"],
    color="#426F8C",
    linewidth=2.5,
    label="ONS unemployment rate"
)

ax.set_title("UK unemployment rate", fontsize=14)
ax.set_ylabel("Per cent")
ax.set_ylim(2, 6)

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax.grid(axis="y", alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)

fig.text(0.1, 0.01, "Source: ONS, MGSX", fontsize=9)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig("unemployment.png", dpi=300, bbox_inches="tight")
plt.show()