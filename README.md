# Project: 또박이

This is the document for **또박이** audio processing model using **Kaldi** and it's Korean recipe **Zeroth**   

You can find more information in [https://kaldi-asr.org](https://kaldi-asr.org, "Kaldi link") and [https://github.com/goodatlas/zeroth](https://github.com/goodatlas/zeroth, "Zeroth link")   

This document contains how to build Korean GOP(Goodness of Pronounciation) calculating engine using Kaldi and Zeroth   

## 1. Installation

### Requirements
----

* LTS version Linux (I tested in 18.04 on Ubuntu)
* RAM more than 64GB
* Enough storage more than 150GB
* NVIDIA GPU

### Install Prerequisites for Kaldi
----

These are the lists we should install   
Just copy them in terminal   

```
sudo apt-get update;
sudo apt-get install -y autoconf;
sudo apt-get install -y automake;
sudo apt-get install -y bzip2;
sudo apt-get install -y ffmpeg;
sudo apt-get install -y gawk;
sudo apt-get install -y g++;
sudo apt-get install -y git;
sudo apt-get install -y gstreamer1.0-plugins-good;
sudo apt-get install -y gstreamer1.0-tools;
sudo apt-get install -y gstreamer1.0-pulseaudio;
sudo apt-get install -y gstreamer1.0-plugins-bad;
sudo apt-get install -y gstreamer1.0-plugins-base;
sudo apt-get install -y gstreamer1.0-plugins-ugly;
sudo apt-get install -y libatlas3-base;
sudo apt-get install -y libgstreamer1.0-dev;
sudo apt-get install -y libtool-bin;
sudo apt-get install -y make;
sudo apt-get install -y python2.7;
sudo apt-get install -y python3;
sudo apt-get install -y python-pip;
sudo apt-get install -y python-yaml;
sudo apt-get install -y python-simplejson;
sudo apt-get install -y python-gi;
sudo apt-get install -y subversion;
sudo apt-get install -y wget;
sudo apt-get install -y build-essential;
sudo apt-get install -y python-dev;
sudo apt-get install -y sox;
sudo apt-get install -y flac;
sudo apt-get install -y zlib1g-dev;
sudo apt-get clean autoclean;
sudo apt-get autoremove -y;
pip install ws4py==0.3.2
pip install tornado==4.5.3

```

Because we need gpu for efficient learning, we should also install cuda library   

```
sudo apt install gcc-7 g++-7

sudo ln -s /usr/bin/gcc-7 /usr/local/cuda/bin/gcc
sudo ln -s /usr/bin/g++-7 /usr/local/cuda/bin/g++

```

### Download source from Kaldi repository
----

I installed Kaldi version 5.5.636 (2020-02-08)   

```
git clone https://github.com/kaldi-asr/kaldi.git
```

### Build Kaldi Tools
----

Build tools in tools directory which is in a kaldi directory   

```
cd tools
./extras/check_dependencies.sh
```

Read the result and install them   
Run again and check the result is 'all OK'   

**Note**   
If mkl is not installing properly, then run this script   

```
wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
sudo sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'
sudo apt-get update
sudo apt-get install -f --allow-downgrades --allow-remove-essential --allow-change-held-packages -y intel-mkl-64bit-2019.1-053
```

Compile the directory using **make**   

**Note**   
You can make faster compile using more processors.   
_You can find out number of cpu by `grep -c processor /proc/cpuinfo`._   


```
make -j "num_of_cpu"
```

Install port audio for audio IO.   
```
./install_portaudio.sh
```

Install morfessor for Korean morpheme.   
```
./extras/install_morfessor.sh
```

### Build Kaldi Source
----

Move to src directory and install kaldi sources   
It will take long time based on your environment   

```
cd ../src
./configure --shared
make depend -j "num_of_cpu"
make -j "num_of_cpu"
```

### Download source from Zeroth
----

Download Zeroth from Git   
Please install Zeroth right next to Kaldi   

```
git clone https://github.com/goodatlas/zeroth
```

### Edit Locale Settings
----

```
sudo locale-gen ko_KR.UTF-8
```

In `/etc/default/locale`, change right values to 'ko_KR.UTF-8' except LANG   
In your home directory, add `export LC_ALL=”ko_KR.UTF-8”` in `.bashrc`   

### Install Prerequisites for Zeroth
----

```
sudo apt-get update;
sudo apt-get install -y zlib1g-dev make automake autoconf libtool;
sudo apt-get install -y flac;
sudo apt-get install -y subversion;
sudo apt-get install -y libatlas3-base;
sudo apt-get install -y build-essential;
sudo apt-get install -y python;
sudo apt-get install -y python-pip python-dev;
sudo python -m pip install awscli;
sudo apt-get install -y unzip;
sudo apt-get install -y flac;
sudo apt-get install -y sox;
sudo apt-get install -y libsox-fmt-all;
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py";
sudo python get-pip.py;
sudo python3 get-pip.py;
sudo apt-get install -y gawk;
sudo apt-get install parallel
sudo add-apt-repository ppa:openjdk-r/ppa 
sudo apt-get update
sudo apt-get install g++ openjdk-7-jdk python-dev python3-dev
sudo python3 -m pip install JPype1-py3
sudo python3 -m pip install konlpy
sudo apt-get install curl
sudo -s
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

### Edit Path
----

Remove symbolic links and remake it   
```
cd s5

rm steps utils
ln -s "Kaldi path"/egs/wsj/s5/steps steps
ln -s "Kaldi path"/egs/wsj/s5/utils utils

```

Change KALDI_ROOT in `path.sh` to kaldi path   

### Edit Settings
----

Change 'num_jobs_initial' and 'num_jobs_final' to "number_of_gpu" in `local/chain/multi_condition/run_tdnn_1n.sh`   
You can easily find out the number of gpu by `lspci | grep -i VGA`

Change 'nCPU' in `run_openslr.sh`
Comment out 'exit' in `run_openslr.sh`

** Optional **   

You can use kspon data if you download data from [http://www.aihub.or.kr](http://www.aihub.or.kr, AI HUB)   
Put 5 Kspon Speech files in kspon directory   
You can check files in [https://github.com/goodatlas/zeroth/pull/13/files](https://github.com/goodatlas/zeroth/pull/13/files, Kspon Updated)   
Don't forget to change permission of files   

## 2. Learning

Run `sudo nvidia-smi --compute-mode=3`   
```
nohup ./run_openslr.sh
[ctrl] z
bg
disown
jobs
tail -f nohup.out
```

Check if the learning is done properly   
If not, you can start at the point by changing stage in `run_openslr.sh`   
Learning may take more than a day   
