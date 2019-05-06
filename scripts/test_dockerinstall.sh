#!/bin/bash
docker build -t oracle7 .
docker run -itv /home/travis:/home/travis --name oracle7 /bin/bash
