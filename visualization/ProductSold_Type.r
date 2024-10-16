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
data <- read.csv('big_data/analysis/data.csv')

# Group data by Product Type and sum the number of products sold
product_sales_data <- data %>%
  group_by(`Product.Type`) %>%
  summarise(`Number.of.products.sold` = sum(`Number.of.products.sold`, na.rm = TRUE)) %>%
  ungroup()

# Create the pie chart
pie_chart <- plot_ly(
    data = product_sales_data,
    labels = ~`Product.Type`,
    values = ~`Number.of.products.sold`,
    type = 'pie',
    textinfo = 'percent+label',
    hole = 0.5,  # Creates a donut chart
    marker = list(colors = RColorBrewer::brewer.pal(n = 8, name = "Pastel1")),  # Use a pastel color palette
    hoverinfo = 'label+value+percent'  # Show details on hover
) %>%
  layout(
    title = 'Sales Distribution by Product Type',
    showlegend = TRUE
  )

# Show the pie chart
pie_chart

# Save the pie chart as an HTML file
saveWidget(pie_chart, "SALE_TYPE.html")
