#
# Script responsible for install inSitu dependencies.
# This script installs the following packages:
# - devtools
# - e-sensing/inSitu
# - dplyr
# 

install.packages("devtools", repos="http://cran.r-project.org")
devtools::install_github("e-sensing/inSitu")
install.packages("dplyr", repos="http://cran.r-project.org")