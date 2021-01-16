# invoice-maker

## Description 

Implementation of a script that will:
- Read student records off of a Google Sheet (for a specified time period)
- Generate PDF invoices (based on a pre-configured template)
- Email each of the PDF invoices to the required contact

## Usage

```
>>> python3 app.py 
```

The default time period and Google sheets link must be configured in the `constants.py` file. The API key will need to be added as part of a `credentials.json` file in the `app` directory.

### Available options (b/c I'm an extra bitch):

- `-h` or `--help`
    - Prints out all these options and what they do
    - eg. ```>>> python3 app.py -h```
- `-sd` or `--start-date`
    - Must be followed by a date in the format dd-mm-yy
    - eg. ```>>> python3 app.py -sd 25-12-20```
- `-ed` or `--end-date`
    - Must be followed by a date in the format dd-mm-yy
    - Requires either the `-tp` or `-sd` option to also be set
    - eg. ```>>> python3 app.py -sd 25-12-20 -ed 11-04-21```
- `-tp` or `--time-period`
    - Must be followed by an integer number of weeks
    - Overrides the default time period
    - eg. ```>>> python3 app.py -tp 4```
- `-d` or `--debug`
    - Prints out log statements as the script executes
    - eg. ```>>> python3 app.py -d```

### Effect of setting command line arguments
sd | ed | tp | Result
----| ----| ----|-----
☑️ | ☑️ | ☑️ | Start and end dates provided are used as bounds; Time period is ignored
☑️ | ☑️ | ☐ | Start and end dates provided are used as bounds; Time period is ignored
☑️ | ☐ | ☑️ | End Date set to Start Date + Time period
☑️ | ☐ | ☐ | End Date set to current date
☐ | ☑️ | ☑️ | Start date set to End date - Time Period
☐ | ☑️ | ☐ | Start date set to `OLDEST_START_DATE` 
☐ | ☐ | ☑️ | Start date set to current date - Time period; End date set to current date
☐ | ☐ | ☐ | Start date set to current date - `DEFAULT_TIME_PERIOD`; End date set to current date


### Defaults:

The following parameters will need to be configured in the `constants.py` file:

- `DEFAULT_TIME_PERIOD`
- `OLDEST_START_DATE`

### Environment Variables:

The following parameters will need to be defined as environment variables:

- `SENDER_EMAIL_UN`: The email address of the sending account
- `SENDER_EMAIL_PW`: The password for the above email