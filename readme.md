# invoice-maker

## Description 

Implementation of a script that will:
- Read student records off of a Google Sheet (for a specified time period)
- Generate PDF invoices (based on a pre-configured template)
- Email each of the PDF invoices to the required contact

## Usage

```
>>> cd clone https://github.com/theshevon/invoice-maker
>>> cd app
>>> python3 app.py 
```

The default time period and Google sheets link must be configured in the `constants.py` file. The API key will need to be added as part of a `credentials.json` file in the `app` directory.

### Available options (b/c I'm an extra bitch):

- `-h` or `--help`
    - Prints out all these options and what they do
    - eg. ```>>> python3 app.py -h```
- `-sd` or `--start-date`
    - When used, must be followed by a date in the format dd-mm-yy
    - eg. ```>>> python3 app.py -sd 25-12-20```
- `-ed` or `--end-date`
    - When used, must be followed by a date in the format dd-mm-yy
    - Requires either the `-tp` or `-sd` option to also be set
    - eg. ```>>> python3 app.py -sd 25-12-20 -ed 11-04-21```
- `-tp` or `--time-period`
    - When used, must be followed by an integer number of weeks
    - Overrides the default time period
    - eg. ```>>> python3 app.py -tp 4```
- `-ms` or `--mail-server`
    - When used, must be followed by either `p` (denoting `production`) or `t` (denoting `test`)
    - eg. ```>>> python3 app.pt -ms p```
    - Defaults to `p`
- `-d` or `--debug`
    - Prints out log statements as the script executes
    - eg. ```>>> python3 app.py -d```
    - Defaults to `False`

### Effect of setting command line arguments

-sd | -ed | -tp | Result
----| ----| ----|-----
☑️ | ☑️ | ☑️ | Start and end dates provided are used as bounds; Time period is ignored
☑️ | ☑️ | ☐ | Start and end dates provided are used as bounds; Time period is ignored
☑️ | ☐ | ☑️ | End Date set to (Start Date + Time period)
☑️ | ☐ | ☐ | End Date set to current date
☐ | ☑️ | ☑️ | Start date set to (End date - Time Period)
☐ | ☑️ | ☐ | Start date set to `OLDEST_START_DATE` 
☐ | ☐ | ☑️ | Start date set to (current date - Time period); End date set to current date
☐ | ☐ | ☐ | Start date set to (current date - `DEFAULT_TIME_PERIOD`); End date set to current date

**Important**: When the `-ms` flag is set to `t`, the script will log the email information to a local debugging server. This will need to be run prior to running the script, and can be done so by executing the following command:
```
>>> python3 -m smtpd -c DebuggingServer -n localhost:1025
```  
### Defaults:

The following parameters can be configured in the `constants.py` file:

- `DEFAULT_TIME_PERIOD`
- `OLDEST_START_DATE`
- `PDF_STORAGE_PATH`

### Environment Variables:

The following parameters will need to be defined as environment variables:

- `EMAIL_USER`: The email address of the sending account
- `EMAIL_PASS`: The password for the above email