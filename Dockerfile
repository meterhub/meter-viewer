FROM python:3.11

RUN pip install -U pip && \
  pip install jupyterlab matplotlib pandas numpy scipy ipywidgets -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

EXPOSE 8888

CMD ["jupyter", "lab", "--port", "8888", "--no-browser", "--ip", "0.0.0.0", "--allow-root", "--NotebookApp.token='abcd'"]