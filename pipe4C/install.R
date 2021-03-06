# Install packages
install.packages(c('optparse', 'caTools', 'config', 'isotone', 'devtools'))

# Install Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
      install.packages("BiocManager")

# Install Bioconductor packages
BiocManager::install("ShortRead")
BiocManager::install("GenomicRanges")
BiocManager::install("GenomicAlignments")
BiocManager::install("BSgenome")
BiocManager::install('BSgenome.Hsapiens.UCSC.hg19')

# Load peakC
library("devtools")
install_github("deWitLab/peakC")
