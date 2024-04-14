# File Carving Application

## Overview

The File Carving Application is designed to streamline and automate the file carving process, featuring a user-friendly interface that facilitates quick and efficient viewing and carving of disk image files. This application is ideal for digital forensics investigators and enthusiasts looking to recover deleted or inaccessible files from disk images with ease.

## Features

- **Upload Disk Image**: Easily upload disk images for analysis.
- **View Partition Table**: Inspect the partition table to identify different segments.
- **Select and Carve Partitions**: Choose specific or multiple partitions for carving, either individually or combined.
- **List Files**: Dynamically list all files, including deleted files, within the disk image.
- **Display File Tree Structure**: View the hierarchical structure of files and folders.
- **Select and Carve Files**: Extract specific or multiple files, supporting both individual and combined carving.
- **Get File Hash**: Calculate and retrieve the hash of carved files for integrity verification.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python 3 installed on your system. This application has been tested on UNIX/Linux and macOS systems.

### Installation

1. **Clone the repository**

    Begin by cloning the repository to your local machine:

    ```sh
    git clone https://github.com/Buck0134/File_Carving.git
    ```

2. **Set up a virtual environment**

    Navigate to the cloned repository and create a virtual environment:

    ```sh
    cd File_Carving
    python3 -m venv myenv
    ```

3. **Activate the virtual environment**

    Activate the virtual environment to isolate your package dependencies:

    ```sh
    source myenv/bin/activate
    ```

4. **Install dependencies**

    Install the required Python packages using pip:

    ```sh
    pip3 install -r requirements.txt
    ```

### Usage

To start the application, run the following command from the root directory of the project:

```sh
python3 server/app.py
```

## References:
- https://www.w3schools.com/js/js_htmldom_nodes.asp
- https://stackoverflow.com/questions/7271490/delete-all-rows-in-an-html-table
- https://stackoverflow.com/questions/866239/creating-the-checkbox-dynamically-using-javascript
- https://stackoverflow.com/questions/23175006/how-to-check-multiple-checkboxes-with-javascript
- https://www.geeksforgeeks.org/convert-a-string-to-an-integer-in-javascript/
- https://www.w3schools.com/jsref/met_win_alert.asp 
- https://www.shecodes.io/athena/24803-how-to-change-button-label-with-javascript
- https://stackoverflow.com/questions/14034737/creating-a-button-dynamically-with-arguments-for-onclick
- https://www.w3schools.com/jsref/event_onclick.asp
- https://www.geeksforgeeks.org/how-to-get-url-parameters-using-javascript/</br>
CSS related:
- https://www.w3schools.com/cssref/pr_text_white-space.php
- https://www.shecodes.io/athena/1837-how-to-put-2-images-on-one-line-with-css
- https://getbootstrap.com/docs/5.3/getting-started/introduction/
- https://getbootstrap.com/docs/5.3/layout/columns/
- https://getbootstrap.com/docs/4.0/content/tables/




