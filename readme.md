# invoice-maker

## Description 

Implementation of a script that will:
- Read student records off of a Google Sheet (for a specified time period)
- Generate PDF invoices (based on a pre-configured template)
- Email each of the PDF invoices to the required contact

## Usage

Before running, please ensure that you've done the following:
- Configured the Google sheets ID in the [gs_contants.py](app/common/gs_constants.py) file
- Added the `credentials.json` file (which contains the API KEY necessary to access the above Google Sheet) to the [app](app) directory
- Added your mail server credentials as [environment variables](#environment-variables)

```
>>> cd app
>>> python3 app.py
```

When run, you will be prompted to enter the starting invoice # for the PDFs that get generated. This input must be an **integer >= 0**.

### Available options (b/c I'm an extra bitch):

- `-h` or `--help`
    - Prints out all these options and what they do
    - eg. ```>>> python3 app.py -h```
- `-sd` or `--start-date`
    - Represents the start date for the invoicing period (inclusive)
    - When used, must be followed by a date in the format dd/mm/yy
    - eg. ```>>> python3 app.py -sd 25/12/20```
- `-ed` or `--end-date`
    - Represents the end date for the invoicing period (inclusive)
    - When used, must be followed by a date in the format dd//mm/yy
    - Requires either the `-tp` or `-sd` option to also be set
    - eg. ```>>> python3 app.py -sd 25/12/20 -ed 11/04/21```
- `-tp` or `--time-period`
    - Represents the length of the invoicing period
    - When used, must be followed by an integer number of weeks
    - Overrides the default time period
    - eg. ```>>> python3 app.py -tp 4```
- `-ad` or `--adjustments-date`
    - Represents the date as of which an adjustment is outstanding. This is reflective of the `InvoiceDate` field in the Google Sheet
    - When used, must be followed by a date in the format dd/mm/yy
    - **Mandatory** when `-ed` is set to a date prior to the current date
    - Defaults to the current date when not used
    - eg. ```>>> python3 app.py -ed 11/04/20 -ad 10/01/21```
- `-ms` or `--mail-server`
    - Represents which server to use for mailing (ie. production or test)
    - When used, must be followed by either `p` (denoting `production`) or `t` (denoting `test`)
    - eg. ```>>> python3 app.py -ms p```
    - Defaults to `p`
- `-fo` or `--files-only`
    - When used, skips the emailing of the generated invoice PDFs
    - eg. ```>>> python3 app.py -fo```
    - Defaults to `False` when not used
- `-d` or `--debug`
    - When used, prints out log statements as the script executes
    - eg. ```>>> python3 app.py -d```
    - Defaults to `False` when not used

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

The following parameters can be configured in the [here](app/common/defaults.py):

- `DEFAULT_TIME_PERIOD`
- `OLDEST_START_DATE`
- `PDF_STORAGE_PATH`
- `INVOICE_PDF_NAME_ON_EMAIL`

### Environment Variables:

The following parameters will need to be defined as environment variables:

- `EMAIL_USER`: The email address of the sending account
- `EMAIL_PASS`: The password for the above email

**Instructions:**

1. Open `.bash_profile` in your favourite CLI-based text editor (The instructions below are for nano, because fuck vim)
```
>>> nano ~/.bash_profile
```
2. Add the following lines
```
export EMAIL_USER="<email-address-to-use-for-mailing>"
export EMAIL_PASS="<password-for-above-email>"
```
3. Save the `.bash_profile` and exit (`ctrl + X` followed by `Y`)
4. Run the following command
```
>>> source ~/.bash_profile
```