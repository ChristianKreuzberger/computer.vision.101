# How to Train Our Future Overlords

![](lakeside-hackfest-18.png)

This is a task-based approach to getting an overview over the current (computer vision) machine learning landscape! Check out the branches of the repository, the explanations, links, and tasks in the [computer.vision.ipynb](computer.vision.ipynb). 

# Setup

Once Python 3.6 is installed, `pip3 install -r requirements.txt` should set up the rest for the notebook. 

# Start


Run `jupyter notebook` from the source directory. 

~~~
$ cd computer.vision.101
$ jupyter notebook
~~~

# Start with Docker

Work in Progress

ToDo:

* Start with a volume to persist changes within the notebook and other files
* Automatically switch to the user that supplied the source files

* Run Jupyter Notebook: 
 ``docker run -p 8888:8888 -it christiankreuzberger/computer.vision.101:1.0 jupyter notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root``

* Run api server
 ``docker run -p 5000:5000 -it christiankreuzberger/computer.vision.101:1.0 python api_server.py --host=0.0.0.0``


# Building the Docker image
If you plan to make any changes to the docker image, you can build it using
```bash

docker build --rm -t christiankreuzberger/computer.vision.101:1.0 .
```

# License 

MIT
