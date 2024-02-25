# data-fusion-system

## Setup

### Prerequisites

- Install [Anaconda](https://www.anaconda.com/products/individual) for package management and installation.
- Install [Git](https://git-scm.com/downloads) for cloning the repository.

### Installation Steps

1. **Clone the Repository**

   - Ensure you have login credentials to access the [Tufts-Capstone-Team-Fusion](https://github.com/Tufts-Capstone-Team-Fusion). For help, email [Dave Lillethun](dave@cs.tufts.edu).

   - Clone the `data-fusion-system` repository to your local machine:

      ```bash
      git clone https://github.com/Tufts-Capstone-Team-Fusion/data-fusion-system.git
      cd data-fusion-system
      ```

2. **Setup Environment**

   To set up your environment after cloning the repository, follow these steps:

   - Create a new Conda environment using the command:
     ```bash
     conda create --name datafusionenv python=3.11 -y
     ```
   - Activate the newly created environment (you will need to reactive when reopening this project, but some IDEs like PyCharm  allow you to [automatically activate environments](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)):
     ```bash
     conda activate datafusionenv
     ```
   - Install the necessary packages from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```
     **Note: After installing, if there are any updates made to `requirements.txt` from VCS you will need to repeat this step.**

### Adding new project packages
1. **Export Packages**
   When installing a package that doesn't exist already in `requirements.txt`, ensure your conda environment is active with `conda activate datafusionenv` and use `pip install [package-name]`.
   Then, export the changes to allow others to work with your code seamlessly when you push it to VCS:

   ```bash
   pip freeze > requirements.txt
   ```
   
   Make sure to track requirements.txt on VCS so you get other people's updates to `requirements.txt`.