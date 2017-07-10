# Audit Log Checker 
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Functionality ###
* Validate the audit logs from actants and traders’ servers weekly before sending them to the clearing firm. Invalid (empty) log files are recorded and removed. 

### Solution ###
* Windows server
####Drives are mounted under the dev machine. The script can check and do the work sequentially based on the directory that log files resides listed in the csv file. ####
* Linux server
####Audit logs are uploaded under the sftp server on daily basis. That is where audit logs reside. Once it passes the validation (not empty), it will be pushed to the clearing firm. ####

### Who do I talk to? ###
#### Boyang Dong ####
#### boyang.dong@budoholdings.com ####
#### (312)854-2929 (work) ####