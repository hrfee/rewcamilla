### rewCamilla

Convert [Room EQ Wizard](https://www.roomeqwizard.com/) EQ .txt files into filters and a pipeline for [CamillaDSP](https://github.com/HEnquist/camilladsp). Currently only works with Peaking filters.

```
usage: rewcamilla.py [-h] [-g] input

Convert REW Generic EQ files to filters and a pipeline for CamillaDSP.

positional arguments:
  input       Generic EQ .txt file from REW.

options:
  -h, --help  show this help message and exit
  -g, --gain  add gain reduction filter equal to maximum peak gain.
  ```
