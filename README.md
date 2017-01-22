# Lab 1 setup

We use Anaconda + Python 3.5 for this lab. This is a short guide on installing software on DICE machines. For other OS, refer to [Anaconda page](https://www.continuum.io/downloads)

### Download Anaconda
Open a terminal on the DICE machine and then type the following command:
```
wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
```
This will download the installation file.

Start the installation by entering:

```
bash Anaconda3-4.2.0-Linux-x86_64.sh
```

### Set up a virtual environment and install packages
Clone the lab github repository:
```
git clone https://github.com/INFR11133/lab1.git
cd lab1
```

Create and install packages by entering the command:
```
conda create --name lab1
source activate lab1
conda install seaborn pandas jupyter matplotlib  
```

Start the notebook by entering the command:
```
jupyter notebook
```
