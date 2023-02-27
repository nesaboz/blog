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
repo_name=$1
python_ver=$2

if ! [[ -n $repo_name ]] || ! [[ -n $python_ver ]]; then
  echo "you didn't enter repo name and/or python version"
  exit 0
fi

yes | conda create -n $repo_name python=$python_ver
conda activate $repo_name


mkdir $repo_name
cd $repo_name || exit
echo $repo_name >> README.md
git config --global init.defaultBranch main
git init

pip install -U numpy pandas matplotlib torchviz scikit-learn tensorboard torchvision torch tqdm torch-lr-finder ipyplot ipywidgets opencv-python torchmetrics
yes | conda install -c conda-forge jupyter_contrib_nbextensions graphviz python-graphviz

ipython kernel install --name $repo_name --user
conda env export > env.yml
git add .
git commit -m "first commit"
git branch -M main
remote_name=git@github.com:nesaboz/$repo_name.git
git remote add origin $remote_name
git push -u origin main
jupyter notebook --generate-config
echo "Change the default kernel by modifying and uncommenting in jupyter config file following line:  c.MultiKernelManager.default_kernel_name='newDefault' \n"
echo "Add jupyter notebook extensions 'collapsable headings' and 'table of context 2' toc2"

