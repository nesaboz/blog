#!/bin/bash
# make sure this file has correct line endings for the system, in PyCharm go to File -> File Properties -> Line Separators
# - go to github and create a new repo with name <repo_name>
# - go to the PyCharmProject folder
# - update conda and init bash for new version of conda
#     >conda update -n base -c conda-forge conda
#     >conda init bash  # after this one needs to restart terminal
# - Restart terminal
# - make sure this script is executable: chmod +x utils/setup_new_project.sh check with ls -l (should have several x values)
# - run it as ./utils/setup_new_project.sh <repo_name> <python_version> name, for example: ./setup_new_project.sh test_repo 3.10
repo_name=$"blog"
python_ver=$"3.10"
remote_name=$"https://github.com/nesaboz/blog"

if ! [[ -n $repo_name ]] || ! [[ -n $python_ver ]]; then
  echo "you didn't enter repo name and/or python version"
  exit 0
fi


wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
sudo bash Miniconda3-py310_23.1.0-1-Linux-x86_64.sh

conda init
exec bash  # I should see (base) in front of the prompt

yes | conda create -n $repo_name python=$python_ver
conda activate $repo_name

git clone $remote_name

# # for a new repo
#mkdir $repo_name
#cd $repo_name || exit
#echo $repo_name >> README.md
#git config --global init.defaultBranch main
#git init

pip install fastai==2.7.10 jupyterlab numpy pandas matplotlib torchviz scikit-learn tensorboard torchvision torch tqdm torch-lr-finder ipyplot ipywidgets opencv-python torchmetrics
yes | conda install -c conda-forge jupyter_contrib_nbextensions graphviz python-graphviz

ipython kernel install --name $repo_name --user
jupyter kernelspec list  # should list "blog" kernel

ipython locate  # locates kernel profile file
cd /home/.ipython

vi profile_default/ipython_config.py
c.InteractiveShellApp.exec_lines = [
    'import sys; sys.path.append("/home/blog")'
]

cd /home/blog/nbs
jupyter notebook --allow-root



#conda env export > env.yml
#git add .
#git commit -m "first commit"
#git branch -M main
#git remote add origin $remote_name
#git push -u origin main
jupyter notebook --generate-config
echo "Change the default kernel by modifying and uncommenting in jupyter config file following line:  c.MultiKernelManager.default_kernel_name='newDefault' \n"
echo "Add jupyter notebook extensions 'collapsable headings' and 'table of context 2' toc2"









