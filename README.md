# AI-Vibrancy-Index

This program creates some preliminary new [AI vibrancy indices](https://aiindex.stanford.edu/vibrancy/) for potential use in the 2022 AI Index.

How to run the program:
1. Clone the git repo
2. Manually downloaded 2021 raw data below (as xlsx, with all sheets)  and put in data\raw:
   1. Publications Data [here](https://docs.google.com/spreadsheets/d/1OPNdnrNYNVhQirJJdZl60n0ejme0D8l-L6C9Ccuv_RY/edit#gid=975288704)
   2. Investment amount and number of companies data [here](https://docs.google.com/spreadsheets/d/188Yb-azRYtszLSMaaDjvKrUFCpQRJeN4M3ZohBeFzUc/edit#gid=214452203)
   3. 2020 Global Vibrancy Rankings [here](https://docs.google.com/spreadsheets/d/1obZ7lM2NIukzFnZYrehLc6eiwvyk3OzofgDPSSZphAw/edit#gid=1315097645)
3. Manually downloaded 2022 raw data below and put in data\raw:
   1. It is in the private google rive [here](https://drive.google.com/drive/folders/16KoFscHY4YWlWpXKfzyNU-AZz2K-3irT)
4. Run vibrancy.py
5. Push new version to Github (especially reports\vibrancy_data_main.csv)
6. Refresh the [Google sheet](https://docs.google.com/spreadsheets/d/1zUEqCg1r_QNexU_7YmVO5xzreunEeuvGniLUQF83dDQ/edit#gid=980468888) for this project, which loads reports\vibrancy_data_main.csv
7. Results will then automatically be exported to the [Google Doc](https://docs.google.com/document/d/1YHbOObWgznxNOM8fmctvzB5pbb5nAm-YhASUbEsRdUg/edit#)