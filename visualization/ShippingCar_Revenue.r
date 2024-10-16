# Set CRAN repository mirror
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Load required packages
install.packages("dplyr")
install.packages("plotly")
install.packages("htmlwidgets")  # Ensure htmlwidgets is installed

library(dplyr)
library(plotly)
library(htmlwidgets)  # Load htmlwidgets library

# Load your dataset (replace 'your_data.csv' with your actual file path)
data <- read.csv("big_data/analysis/data.csv")

# View the first few rows of the dataset to confirm it's loaded correctly
head(data)

# Calculate total revenue by shipping carrier
total_revenue <- data %>%
  group_by(`Shipping.carriers`) %>%
  summarise(`Revenue.generated` = sum(`Revenue.generated`, na.rm = TRUE)) %>%
  ungroup()

# Create the bar chart
fig <- plot_ly(
    data = total_revenue,
    x = ~`Shipping.carriers`,
    y = ~`Revenue.generated`,
    type = 'bar',
    marker = list(color = 'lightblue')
) %>%
  add_text(text = ~`Revenue.generated`, textposition = 'auto') %>%
  layout(
    title = 'Total Revenue by Shipping Carrier',
    xaxis = list(title = 'Shipping Carrier'),
    yaxis = list(title = 'Revenue Generated'),
    template = 'plotly_white'
  )

# Show the figure
fig

# Save the figure as an HTML file
saveWidget(fig, "REVENUE_SHIPPING_CARRIER.html")
