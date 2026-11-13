MUD SYSTEM  (Python + XAMPP MySQL)
==================================

ස්ථාපනය / INSTALL (එක් වරක් / once)
1. Python install කරන්න (python.org) - "Add Python to PATH" tick කරන්න.
2. XAMPP Control Panel එකේ  Apache සහ MySQL  "Start" කරන්න.
3. Browser එකේ  http://localhost/phpmyadmin  විවෘත කර
   "New" -> Database name:  mud_system  -> Create   (utf8mb4_general_ci)
4. මේ folder එකේ Command Prompt විවෘත කර:
       pip install -r requirements.txt
5. ධාවනය / RUN:
       python app.py
6. Browser: http://127.0.0.1:5000

භාවිතය / HOW TO USE
1. Imports page  -> IMPORT_LIST.xlsx upload.  (වැරදි balance auto සකස් වේ, දින නිවැරදි වේ)
2. Mapping page  -> ERP family -> MUD item -> import description පරීක්ෂා කරන්න.
3. New MUD       -> header පුරවා QuickReport.xlsx upload.
4. Preview       -> FIFO allocation බලන්න. අවශ්‍ය නම් Qty වෙනස් කරන්න / entry එකක් මුලින් තෝරන්න /
                    පේළියක් එකතු කරන්න (උදා: T/B Tags 770720 -> "Tea Bags Tags").
5. CONFIRM       -> import balance අඩු වේ.  "Download MUD (Excel)".
6. වැරදුණොත්      -> "Undo / cancel MUD" -> balance ආපසු ලැබේ.

NOTES
- XAMPP MySQL password තිබේ නම් app.py හි DB_URL වෙනස් කරන්න:
  mysql+pymysql://root:PASSWORD@localhost:3306/mud_system
- Balance = opening balance - ledger deductions. කිසිවිටක අතින් ටයිප් නොකරයි.
- Shortage තිබේ නම් CONFIRM අවහිර වේ (balance මදි).
