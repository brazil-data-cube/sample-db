#
# Script responsible for install inSitu dependencies.
# This script installs the following packages:
# - devtools
# - e-sensing/inSitu
# - dplyr
#

# Function to check whether package is installed
is.installed <- function(mypkg){
    is.element(mypkg, installed.packages()[,1])
}

if (!is.installed("devtools")) {
    install.packages("devtools", repos="http://cran.r-project.org")
}

devtools::install_github("e-sensing/inSitu")

if (!is.installed("dplyr")) {
    install.packages("dplyr", repos="http://cran.r-project.org")
}