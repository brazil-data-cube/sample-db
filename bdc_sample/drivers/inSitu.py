import os
from bdc_sample.core.driver import CSV


class InSitu(CSV):
    """
    Driver for InSitu Sample for data loading to `sampledb`

    This class is an abstraction of repository
    https://github.com/e-sensing/inSitu.git

    **Make sure** you have `R` in PATH. You can download `R`
    in https://cran.r-project.org/
    """

    def __init__(self, entries, storager, **kwargs):
        mappings = {"class_name": "label"}

        super(InSitu, self).__init__(entries, mappings, storager, **kwargs)

    def load_data_sets(self):
        """
        Load data sets in memory using database format.
        Calls `R` script to generate CSV sample data set. After that,
        process the `CSV` files to the storager handler
        """

        # Read data sets (.rda) from R to CSV
        InSitu.generate_data_sets(self.entries)

        return super().load_data_sets()

    @classmethod
    def generate_data_sets(cls, entries):
        """
        Generates sample from inSitu package in R. It will generate `.csv` files
        inside the provided in this object creation.

        Make sure you have R installed on PATH.
        This function tries to install inSitu dependencies with the
        following commands:

        ```R
        install.packages("devtools")
        devtools::install_github("e-sensing/inSitu")
        install.packages("dplyr")
        ```

        After that, execute R functions to load `.rda` files and export to CSV
        """
        import subprocess
        from pathlib import Path

        scripts_dir = Path(__file__).parent / 'r-scripts/'

        export_csv_script = scripts_dir / 'export-inSitu-samples-csv.R'
        install_dependencies_script = scripts_dir / 'install-inSitu.R'

        if not os.path.exists(entries):
            os.mkdir(entries)

        # Install dependencies
        subprocess.call('R --silent -f {}'.format(
            install_dependencies_script), shell=True)

        rcommands = 'R --silent -f {} --args {}'.format(
            export_csv_script, entries)
        # Execute script to generate Sample CSV data
        subprocess.call(rcommands, shell=True)
