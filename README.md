# Markdown to Dayone

This tool helps you to convert your Markdown files into JSON format that can be imported into [DayOne app](https://dayoneapp.com/).
Currentlly tested with Obsidian markdown files. Raise an issues if other markdown support is needed.

## How to use?

Using this tool requires familiarity with the Terminal app and Python virtualenvs. Currently, this works only for MacOS.

1. Clone the repo

    ```bash
    # Clones the repo
    $ git clone https://github.com/romitjain/markdown-to-dayone.git
    ```

2. Run the script

    ```bash
    $ cd markdown-to-dayone
    # Make virtualenv
    $ python3 -m venv ./.venv
    $ source .venv/bin/activate
    $ python3 main.py --source <location of the markdown folder>
    ```

3. Add all photos under `photos` folder

    3.1. Once the above steps are completed, create a new folder named as `photos` and add all the photos that will be required in the import in this folder. It should not have any nested structure or image names should not have any spaces.

    3.2. Zip the export and the photos

    ```bash
    # Create a zip file
    $ zip -r day_one_import.zip day_one_import.json photos/
    ```

4. Import the zip file in DayOne Journal. Refer [here](https://dayoneapp.com/guides/settings/importing-data-to-day-one/) and import the `JSON Zip File` type import. Once the dialog box appears, choose the zip file that was generated in the above step.

### Customizations

One can also customize where the output is written and wheather to run in debug mode.

```bash
usage: main.py [-h] --source SOURCE [--dest DEST] [--debug DEBUG]

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE  Location of the file or folder which you want to convert. If you pass the folder location, all files present will be converted
  --dest DEST      Location of the folder where you want to dump the converted notes in JSON format. Defaults to the current working directory.
  --debug DEBUG    Weather to run in debug mode (y/n). Defaults to `n`
```
