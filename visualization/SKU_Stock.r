# Load required packages
options(repos = c(CRAN = "https://cran.rstudio.com/"))
install.packages("dplyr")
install.packages("plotly")
install.packages("htmlwidgets")  # Ensure htmlwidgets is installed

library(dplyr)
library(plotly)
library(htmlwidgets)  # Load htmlwidgets library

# Load your dataset (replace 'your_data.csv' with your actual file path)
data <- read.csv("big_data/analysis/data.csv")

# Check the column names
print(colnames(data))

# Group data by Product Type and SKU, using backticks if necessary
grouped_stock_data <- data %>%
  group_by(`Product.Type`, SKU) %>%
  summarise(`Stock.levels` = sum(`Stock.levels`, na.rm = TRUE)) %>%
  ungroup()

# Create the line chart
stock_chart <- plot_ly(
    data = grouped_stock_data,
    x = ~SKU,
    y = ~`Stock.levels`,
    color = ~`Product.Type`,
    type = 'scatter',
    mode = 'lines+markers'
) %>%
  layout(
    title = 'Stock Levels by SKU Under Each Product Type',
    xaxis = list(title = 'SKU'),
    yaxis = list(title = 'Stock Levels'),
    template = 'plotly_white'
  )

# Save the line chart as an HTML file
saveWidget(stock_chart, "SKU_STOCK.html")

# Show the line chart in the Viewer (optional, for RStudio users)
stock_chart
