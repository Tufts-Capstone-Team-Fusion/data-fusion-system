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

### File Overview

calibration_matrix.npy: If this file exists, it holds a numpy array which represents a homography. As long as it exists calibration.py and video.py will use it for calibration. You can safely delete or rename this file and then run either calibration.py or video.py to go through the calibration process and make a new calibration matrix

calibration.py: This file contains an implementation of our current manual calibration along with a placeholder fusion algorithm (using the thermal image as a cutoff for the rgb image) since it was useful for checking calibration. It searches for a file called “calibration_matrix.npy” and loads a calibration from the file. Then fuses the data from two images and shows the result. If there is no “calibration_matrix.npy” it makes the user go through the calibration process and saves the result.

checkerboard.py: This file was where most of our automatic calibration experiments took place. Currently, it tries to find a rectangle in the image and then black out everything except for that rectangle but can’t locate the checkerboard in the thermal image so it’s pretty much useless. At the bottom it does show an example of how to use findChessboardCorners() which you might find useful though

get_frames.py: contains a method extract_frames() which takes the path to an mp4 file, loads the video, splits it up into frames and then returns an array of just the frames.
This method can fail if you try to load too many frames at once

split_video: is a helper file we wrote because our method for collecting data was taking a screen recording of both thermal and rgb video streams side by side and we needed a way to separate them into individual videos. It takes a video and generates two videos, one of the left and one of right halves of the original video.

test.py: is an older version of our calibration where we had to find the matching coordinates outside of the program (we used an image editing software and wrote them down on paper then put them into the two arrays manually which was very painful) and should really only be used to learn about findHomography()

video.py: Loads two videos and calibrates using the first frames (starting with a checkerboard in the video makes it much easier) from each video stream the same way that calibration.py does. It then uses that calibration matrix to fuse the two videos together and outputs the resulting video.
