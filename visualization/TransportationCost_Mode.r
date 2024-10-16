# Set CRAN repository mirror
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Load required packages
install.packages("dplyr")
install.packages("plotly")  # Install plotly for interactive plots
install.packages("htmlwidgets")  # Ensure htmlwidgets is installed

library(dplyr)
library(plotly)  # Load plotly library
library(htmlwidgets)  # Load htmlwidgets library

# Load your dataset (replace 'your_data.csv' with your actual file path)
data <- read.csv("big_data/analysis/data.csv")

# Group by Transportation modes and sum Costs
grouped_transportation_data <- data %>%
  group_by(Transportation.modes) %>%
  summarise(Total_Costs = sum(Costs, na.rm = TRUE)) %>%
  ungroup()

# Create the pie chart using plotly directly
interactive_pie_chart <- plot_ly(
  data = grouped_transportation_data,
  labels = ~Transportation.modes,
  values = ~Total_Costs,
  type = 'pie',
  textinfo = 'label+percent',
  insidetextorientation = ' radial'
) %>%
  layout(
    title = "Cost Distribution by Transportation Mode",
    showlegend = TRUE
  )

# Save the interactive pie chart as an HTML file
saveWidget(interactive_pie_chart, "TRANSPORTATION_MODE.html")

# Display the interactive pie chart in the Viewer (optional, for RStudio users)
interactive_pie_chart
