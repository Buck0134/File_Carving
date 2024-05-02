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

Before you begin, ensure you have Python 3 and Sleuth Kit installed on your system. This application has been tested on UNIX/Linux and macOS systems. You will also need to clone the repository on your local machine. 

    git clone https://github.com/Buck0134/File_Carving.git

## Start the Application using created script

1. **For Linux Based Machine**
    Grant execute permissions to the starting script
    ```sh
    chmod +x start_application.sh
    ```

    Start the Application by running the script
    ```
    ./start_application.sh
    ```
2. **For Windows Based Machine**
    Double click on ```start_application.bat``` to start the application


## Start the Application using Manual Setup

You can use the following commands to manually install dependencies and start up the application

### Installation

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
- Stackoverflow.com for downloading files: https://stackoverflow.com/questions/3749231/download-file-using-javascript-jquery
- w3schools.com for appending children to an HTML element: https://www.w3schools.com/js/js_htmldom_nodes.asp
- stackoverflow.com for removing rows in a table: https://stackoverflow.com/questions/7271490/delete-all-rows-in-an-html-table
- stackoverflow.com for dynamically creating checkboxes: https://stackoverflow.com/questions/866239/creating-the-checkbox-dynamically-using-javascript
- stackoverflow.com for checking whether checkboxes are checked: https://stackoverflow.com/questions/23175006/how-to-check-multiple-checkboxes-with-javascript
- geeksforgeeks.org for for converting string to integers in Javascript: https://www.geeksforgeeks.org/convert-a-string-to-an-integer-in-javascript/
- w3schools.com for for alerting a message to users: https://www.w3schools.com/jsref/met_win_alert.asp 
- shecodes.io for for updating button's name: https://www.shecodes.io/athena/24803-how-to-change-button-label-with-javascript
- stackoverflow for setting onclick function for dynamically created buttons: https://stackoverflow.com/questions/14034737/creating-a-button-dynamically-with-arguments-for-onclick
- w3schools.com for setting onclick function for dynamically created buttons: https://www.w3schools.com/jsref/event_onclick.asp
- geeksforgeeks for URL params seperators: https://www.geeksforgeeks.org/how-to-get-url-parameters-using-javascript/
- w3schools.com for setting an element's attributes dynamically: https://www.w3schools.com/jsref/met_element_setattribute.asp
- w3schools.com for creating collapsed buttons: https://www.w3schools.com/bootstrap5/bootstrap_collapse.php
- builtin.com for waiting sometime during execution: https://builtin.com/software-engineering-perspectives/javascript-sleep</br>
CSS related:
- w3schools.com for wrapping text based on whitespances: https://www.w3schools.com/cssref/pr_text_white-space.php
- https://www.shecodes.io/athena/1837-how-to-put-2-images-on-one-line-with-css
- getbootstrap.com for putting 2 elements in one line: https://getbootstrap.com/docs/5.3/getting-started/introduction/
- getbootstrap.com for utilizing columns to create a side bar in Bootstrap: https://getbootstrap.com/docs/5.3/layout/columns/
- getbootstrap.com for formatting the table through Bootstrap: https://getbootstrap.com/docs/4.0/content/tables/
- stackoverflow.com for right aligning the div elements: https://stackoverflow.com/questions/7693224/how-do-i-right-align-div-elements





