# E-book to images script

This script converts an e-book to images. It is useful for exporting e-books which does not allow exporting to images.

## Usage

Install python 3.11 or higher.
Install dependencies: `pip install -r requirements.txt`
Run the script: `python main.py` or `python3 main.py`
First, enter the page of your e-book. The images will be saved in the `images` folder.
Then, follow the gui instructions to export the images.

### Notes

This script only run on x86_64 systems. It will not run on arm or other architectures due to [pynput](https://pypi.org/project/pynput/) library limitations.
