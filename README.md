# Psychophysics Experiments (Stroop & Flanker)

This project focuses on a set of **psychophysics tasks** for VLM, particularly variations of the **Stroop** and **Flanker** experiments. It provides scripts for generating stimulus images, preparing experiment parameters, running the experiments, and performing statistical analyses and visualizations on the resulting data.

## Table of Contents

1. [Overview](#overview)  
2. [Directory Structure](#directory_structure)  
3. [Getting Started](#getting_started)  
4. [Scripts and Usage](#scripts_and_usage)  
5. [Data Description](#data_description)  
6. [Visualization & Analysis](#visualization_analysis)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Overview

In **cognitive psychology**, **Stroop** and **Flanker** tasks are widely used to study **attention**, **cognitive control**, and **interference**. This repository contains Python scripts and data files that illustrate:

- **Stimulus generation** (e.g., word-color mismatch for Stroop; arrow or letter/number conflicts for Flanker)  
- **Parameter and data file generation** (defining various experimental conditions)  
- **Experiment results** from one or multiple runs  
- **Data analysis and visualization** (e.g., violin plots, summary statistics)

Even if our team use these tasks to test VLM, researchers and students can use these scripts to quickly replicate standard Stroop or Flanker tasks, modify them for specific research questions, and analyze the performance of human participants or computational models.

---

## Directory Structure

A typical layout after unzipping the repository looks like this:

```
psychophysic/
├── Code/
│   ├── Data generator/
│   │   ├── flanker_generater.py
│   │   ├── Stroop_generator.py
│   │   └── ...
│   ├── Final experiment image extraction/
│   │   ├── Origin_flanker.py
│   │   ├── Origin_stroop.py
│   │   ├── squared_flanker.py
│   │   └── ...
│   ├── Image generator/
│   │   ├── flanker_image_generator.py
│   │   ├── Stroop_image_generator.py
│   │   └── ...
│   └── Violin generator/
│       ├── Summary violin/
│       │   └── ...
│       └── Violin generator/
│           └── Graph_Summary.py
│
└── Data/
    ├── Psychophysics_run.xlsx
    └── ...
```

### 1. `Code/` Directory

- **Data generator/**:  
  Contains scripts that generate experimental parameters or condition files (e.g., lists of trials, conditions, etc.) for different variations of the Flanker and Stroop tasks.

- **Final experiment image extraction/**:  
  Scripts like `Origin_flanker.py`, `Origin_stroop.py`, and `squared_flanker.py` handle the final organization or extraction of stimuli used in the experiments (e.g., resizing or cropping images, renaming files for standardization).

- **Image generator/**:  
  Scripts (`flanker_image_generator.py`, `Stroop_image_generator.py`, etc.) used to programmatically create the stimulus images (letters, shapes, numbers, colors, or any other visual stimuli required).

- **Violin generator/**:  
  Contains analysis and plotting scripts. This includes **violin plots**, which are a powerful way to visualize data distributions, along with summary statistics or other plot types (e.g., boxplots, bar charts).  
  - `Graph_Summary.py` is an example script that can produce summary figures from the collected data.

### 2. `Data/` Directory

- **Psychophysics-run.xlsx**:  
  A consolidated Excel file containing experimental results or model outputs. It typically includes columns like:  
  - `model_name`  
  - `group` (e.g., `stroop_Congruent`, `flanker_letter_Incongruent`, etc.)  
  - `group_accuracy`  
  - `overall_accuracy`  
  - `match_type`  
  - `type`  

---

## Getting Started

1. **Clone or Download**  
   - Clone this repository or download the `psychophysic.zip` archive.

2. **Set Up Your Environment**  
   - Install Python 3.7+ (recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)).
   - Install the required packages (see [Dependencies](#dependencies)):

     ```bash
     pip install openpyxl matplotlib pandas numpy pillow
     ```
     
     Additional libraries may be required depending on the scripts you plan to run (e.g., `scipy` for statistical tests).

3. **Verify Installation**  
   - Run a small script (e.g., `python flanker_image_generator.py`) to confirm everything is installed and functioning correctly.

---

## Scripts and Usage

Below is a brief overview of some core scripts. For each specific script, please refer to the inline comments or docstrings in the code for details on parameters and usage.

1. **Data Generator**  
   - `flanker_generater.py` & `Stroop_generator.py`:  
     - Purpose: Create condition or trial definition files for Flanker or Stroop tasks.  
     - Usage (example):  
       ```bash
       cd Code/Data\ generator
       python flanker_generater.py
       ```
       This might produce an output like `flanker_conditions.csv`.

2. **Image Generator**  
   - `flanker_image_generator.py` & `Stroop_image_generator.py`:  
     - Purpose: Dynamically generate PNG/JPG images for the experiments, controlling for stimuli type, color, shape, etc.  
     - Usage (example):  
       ```bash
       cd Code/Image\ generator
       python flanker_image_generator.py
       ```
       The generated images are saved to a specified directory, which can be customized in the script.

3. **Final Experiment Image Extraction**  
   - Scripts like `Origin_flanker.py`, `Origin_stroop.py`, or `squared_flanker.py`:  
     - Purpose: Post-process or reorganize images for the experiment (e.g., cropping, rotating, renaming).  
     - Usage:  
       ```bash
       cd Code/Final\ experiment\ image\ extraction
       python Origin-flanker.py
       ```
       These scripts often rely on pre-existing images from the `Image_generator` step.

4. **Violin Generator**  
   - `Graph_Summary.py`:  
     - Purpose: Load data (often from `Psychophysics_run.xlsx` or other CSV/Excel files), perform some summary calculations, and generate violin plots or other visualizations.  
     - Usage:  
       ```bash
       cd Code/Violin\ generator/Violin\ generator
       python Graph\ Summary.py
       ```
       The script can be adapted to produce additional statistics, such as means, medians, standard deviations, or significance testing using external libraries like `scipy`.

---

## Data Description

### `Psychophysics_run.xlsx`

An example of how the data might be organized:

| model_name | group                                          | group_accuracy | overall_accuracy | match_type       | type       |
|------------|------------------------------------------------|----------------|------------------|------------------|------------|
| fuyu-8b    | stroop_Congruent                               | 0.547619       | 0.495495         | ensemble_match   | image_only |
| fuyu-8b    | stroop_Incongruent                             | 0.476190       | 0.495495         | ensemble_match   | image_only |
| fuyu-8b    | flanker_letter_Congruent                       | 0.566666       | 0.495495         | ensemble_match   | image_only |
| fuyu-8b    | flanker_number_Congruent                       | 0.411111       | 0.495495         | ensemble_match   | image_only |
| ...        | ...                                            | ...            | ...              | ...              | ...        |

- **model_name**: Can be a participant ID or a model identifier.  
- **group**: The condition (e.g., `stroop_Incongruent`, `flanker_number_Congruent`).  
- **group_accuracy**: Accuracy for that specific condition.  
- **overall_accuracy**: Overall accuracy across multiple conditions (if applicable).  
- **match_type** & **type**: Additional meta-information about the trial or condition (e.g., `ensemble_match`, `image_only`, or other labels).

---

## Visualization & Analysis

1. **Violin Plots**  
   - Scripts in the `Violin_generator` folder can produce violin plots, allowing you to see the distribution of performance (accuracy, RT) across different conditions or models.  
   - Adjust the script to color-code conditions or group them by category (e.g., `Stroop_Congruent_vs_Incongruent`).

2. **Summary Statistics**  
   - Use pandas (`pd.DataFrame`) to compute summary measures like mean, median, standard deviation, or perform basic significance tests (e.g., t-tests, ANOVA) using `scipy.stats`.  
   - Export results to `.csv` or `.xlsx` files for further analysis.

3. **Sample Visual Output**  
   - A typical workflow would load `Psychophysics_run.xlsx` into a pandas DataFrame, filter or group by condition, then generate a violin plot or boxplot to compare conditions.

---

## Contributing

Contributions to this repository are welcome! Whether you have bug fixes, new features, or suggestions for improved visualizations, feel free to open an Issue or submit a Pull Request. 

### How to Contribute

1. Fork the repository.  
2. Create a new branch for your feature or bugfix:  
   ```bash
   git checkout -b feature-new-analysis
   ```
3. Commit your changes with clear messages:  
   ```bash
   git commit -m "Add new analysis function for reaction time"
   ```
4. Push to your branch and submit a Pull Request.

Please ensure your contributions are well-documented and tested.

---

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Project Author / Maintainer**: [Maijunxian Wang / Grow AI like a child]  
- **Email**: [mjxwang@ucdavis.edu]  
- **Institution/Company**: [University of California, Davis]  
- **Website / Profile**: [(https://scholar.google.com/citations?user=LexR7uoAAAAJ&hl=en)]

If you have questions regarding experiments, data analysis, or potential collaborations, feel free to reach out.

---

**Enjoy exploring psychophysics experiments and happy analyzing!**
