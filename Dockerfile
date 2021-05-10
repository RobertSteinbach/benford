FROM python:3
ADD main.py /
ADD static/ /static/
ADD static/Chart.js /
ADD templates/  /templates/
RUN pip install flask
CMD [ "python3","./main.py" ]
