This application requires Frappe & ERPnext to be installed as this application is made to modify and some functionalities.If HR use needs to be restored ,please run the following command
Note : All the followig commands should be executed in /frappe-bench/ Directory

  - bench switch-to-branch version-13-beta frappe erpnext --upgrade
  - bench start
  Open Another Terminal simultaneously and Navigate to /frappe-bench/:
  - bench update
  - bench migrate
  
  
  (If everything goes well you can close this terminal)
  Restore the Database Backup of HR.Link of Documentaiton of Backup and Restoration : https://docs.google.com/document/d/1uHltlPyxnZTcYNOp2zwM_YSabbuwcUVJiGGzSK3fLng/edit
  You can get Backup files here - https://drive.google.com/drive/folders/1o-dtDrft8hytGfh5tA4mF062ZqCEChvo?usp=sharing
  
  Now,also install s3_backup app with ERPnext by following command(As DB contain s3-backup data):
  - bench get-app s3_backup https://github.com/ccfiel/s3_backup.git
  -bench --site install-app s3_backup

subject to changeGet the customizations done as per the changes needed for STS's HR
	
  bench get-app hr_customizations https://github.com/shwetangdalvisd/erpnext_hr_customizations
  To install the new app
    bench --site [site-name] install-app hr_customizations	
    bench start

And now u are ready to use the ERP SoftwareIf running in browser show maintenance page ,please run the following command.
	
  bench --site site-name set-maintenance-mode off
  PS:This app was designed to get the following functionalities sorted
 
  1.Auto cancellation of leaves at month end.
  
  2.Allowing future attendance .
  
  3.Leave allocation on Granting and at the start of the month.
  
  4.Changing the leave allocation procedure to eliminate rounding and accept fractional values.
  
  5.Restricting the back dated leave applications upto 2 days.
  
  6.Restricting the user to approve / reject the leave applications applied.
  
  7.Custom Report which could be searched as "Report Monthly Attendance sheet STS"
