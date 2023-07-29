# VS_Files_Together

This is a script to be used alongside Vigor-S software.
- The software Vigor-S produces a .csv file for each image it processes, this can lead to a hundred files for a single experiment.
- The user needs to open manually each file, copy the relevant data and paste in another spredadsheet file before do the statistics.

How the software works:
- It reads all the .csv files inside a folder and join all the relevant information in a single .csv file.
- It outputs a formated file ready to be used in any stats software, it also add columns with transformed variables, so the user don't need to worry about it.
- It also shows a matplotlib GUI window with some basic plots of the variables averages.
    - You can edit the plots using the matplotlib tools.
    - It's configured to save the output image in 300 DPI.

- Input data

![image](https://github.com/LuizSSenko/VS_Files_Together/assets/140913035/94a6e2cb-99de-40bf-a6e1-35f5de6ee445)

- output data

![image](https://github.com/LuizSSenko/VS_Files_Together/assets/140913035/3213fdfe-8646-4065-ae5c-5c5c18306cae)

- Matplotlib with plots and tools.

![image](https://github.com/LuizSSenko/VS_Files_Together/assets/140913035/48c78066-bc6b-4a30-ac3e-50cded4fb2d1)

