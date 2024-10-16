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

# Create the scatter plot
fig <- plot_ly(
    data = data,
    x = ~Price,
    y = ~`Revenue.generated`,  # Use backticks for names with spaces
    color = ~`Product.Type`,
    text = ~paste(
        'Number of products sold:', `Number.of.products.sold`, '<br>',
        'Availability:', Availability, '<br>',
        'Customer demographics:', `Customer.demographics`
    ),
    hoverinfo = "text",
    type = 'scatter',
    mode = 'markers'
) %>%
  add_lines(
    fit = "linear",  # Adding a linear trendline
    mode = "lines",
    line = list(color = 'black', width = 2),
    name = "Trendline"
  ) %>%
  layout(
    title = "Scatter Plot of Price vs. Revenue Generated",
    xaxis = list(title = "Price"),
    yaxis = list(title = "Revenue Generated")
  )

# Show the figure
fig

# Save the figure as an HTML file
saveWidget(fig, "PRICE_REVENUE.html")
