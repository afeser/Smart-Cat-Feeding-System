# METU EEE 2020 - Capstone Project

The project is developed based on ProjectDefinition.md file. It is a smart cat feeding project that can detect, identify and feed cats intelligently using machine learning, computer vision and control. Due to COVID-19 pandemic, some parts of the project is left incomplete. Version 1 prototype is ready, but unfortunately, version 2 prototype will not be completed.

Computer vision, electronic board, user interface and mechanic designs are available and tested with prototype 1. Computer vision part is improved for identification and gives practical results. More information on the test results are included in the final report. Web interface is ready to be used and also is included.

Take a look at our [demo video](https://www.youtube.com/watch?v=P49Y6lQscVo).

[![Demonstration Video](https://github.com/afeser/Smart-Cat-Feeding-System/upload/master2/ProjectFiles/main_readme_files/demo_video_intro.png)](https://www.youtube.com/watch?v=P49Y6lQscVo)


<!---
# Converting video to compressed GIF
# Source videos are saved_1.mp4 and saved_2.mp4
ffmpeg -y -i saved_1.mp4 -vf palettegen palette_1.png
ffmpeg  -i saved_1.mp4 -i palette_1.png -filter_complex paletteuse -r 10 saved_1.gif
ffmpeg  -i saved_2.mp4 -filter:v "setpts=0.05*PTS" -q:v 2 saved_2_2.mp4
ffmpeg -y -i saved_2_2.mp4 -vf palettegen palette_2.png
ffmpeg  -i saved_2_2.mp4 -i palette_2.png -filter_complex paletteuse -r 30 saved_2.gif
-->

![SIFT Vector Detection](https://github.com/afeser/Smart-Cat-Feeding-System/upload/master2/ProjectFiles/main_readme_files/saved_1.gif?raw=true)
![Optimization Algorithm without Clustering](https://github.com/afeser/Smart-Cat-Feeding-System/upload/master2/ProjectFiles/main_readme_files/saved_2.gif)

## Installation
Simply run "setup" file as a bash script. Arguments specify whether build is for client or server.

Under "build" folder, there are files to make the system work.

Some notes :
- No compilation needed
- Run both on server and client with different arguments ("./setup client" or "./setup server")



## [All Reports](https://github.com/afeser/FinalProject/tree/Report/)
