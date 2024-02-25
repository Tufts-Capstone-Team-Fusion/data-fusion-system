# data-fusion-system

## Setup

### Prerequisites

- Install [Anaconda](https://www.anaconda.com/products/individual) for package management and installation.
- Install [Git](https://git-scm.com/downloads) for cloning the repository.

### Installation Steps

1. **Clone the Repository**

   - Ensure you have login credentials to access the [Tufts-Capstone-Team-Fusion](https://github.com/Tufts-Capstone-Team-Fusion). If not, email [Dave Lillethun](dave@cs.tufts.edu).

   - Clone the `data-fusion-system` repository to your local machine:

      ```bash
      git clone https://github.com/Tufts-Capstone-Team-Fusion/data-fusion-system.git
      cd data-fusion-system
      ```

2. **Run Setup**

   This setup script will create a `conda` environment called `datafusionenv` by default.
   ```bash
   bash setup.sh
   ```
   
   

### Adding new project packages
1. **Export Packages**

   ```bash
   pip freeze > requirements.txt
   ```
   
   Make sure to track requirements.txt on VCS.