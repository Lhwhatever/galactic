This is an application I created in September 2016 (which is nearly 2 years ago, as of the time I published this to GitHub) which creates a visualisation of all the stars within 12 light years of the sun.

# How to run
Code is in `plot.py`. Requires Python 3, and `matplotlib`, `pandas` and `numpy`.

Run `python plot.py`.

# Details
Note: All Excel files here were created using Excel 2017.

## Colours
Star colours are determined from a lookup table (`Colors.csv`). I've forgotten where the original source of the lookup table is from (some forum), but nevertheless, my most sincere gratitude to the author. The original text form can be found on `starcolors.txt`.

## Stars
A list of stars and associated information were extracted from Wikipedia circa Sept 2016. Currently only features stars within 12 LY of the sun. The information can be found in `Stars.csv`. An Excel backup can be found in `Stars.bak.xlsx`.

## Spectral Colours
I attempted to use temperatures instead to represent star colours, but I don't think I succeeded then. The data can be found inside `Temperature.xlsx`, `colors.py` and `Colors.ipynb`.

## Output Sample
Sample output can be found in `neighbourhood.png` and `BG.png`.

## Unused/Deprecated Files
The current only deprecated file is `Test.ipynb`. I used it to help come up with the formatting and the code for the various CSV and PY files.
