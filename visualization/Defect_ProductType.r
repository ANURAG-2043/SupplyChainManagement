# Set CRAN repository mirror (no need to choose interactively)
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Load required packages
install.packages("dplyr")
install.packages("ggplot2")
install.packages("plotly")
install.packages("htmlwidgets")  # Ensure htmlwidgets is installed

library(dplyr)
library(ggplot2)
library(plotly)      # Load plotly for saving interactive plots
library(htmlwidgets) # Load htmlwidgets for saving plots

# Load your dataset (replace 'your_data.csv' with your actual file path)
data <- read.csv("big_data/analysis/data.csv")

# Calculate average defect rates by product type
defect_rates_by_product <- data %>%
  group_by(Product.Type) %>%  # Ensure the column name matches your data
  summarise(Average_Defect_Rates = mean(Defect.rates, na.rm = TRUE)) %>%
  ungroup()

# Create the pie chart using ggplot2
pie_chart <- ggplot(defect_rates_by_product, aes(x = "", y = Average_Defect_Rates, fill = Product.Type)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar(theta = "y") +  # Convert to pie chart
  labs(title = "Average Defect Rates by Product Type") +
  theme_void() +  # Remove background and grid
  theme(legend.title = element_blank()) +  # Remove legend title
  geom_text(aes(label = scales::percent(Average_Defect_Rates / sum(Average_Defect_Rates))),
            position = position_stack(vjust = 0.5) # Show percentages inside the pie chart
  )

# Show the pie chart
print(pie_chart)

# Save the pie chart as an HTML file
ggplotly(pie_chart) %>%
  saveWidget("DEFECT_PRODUCT.html", selfcontained = TRUE)
