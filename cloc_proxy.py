import subprocess
import json

def count_loc(config):
    argsstr = ''

    # run cloc command
    if(config.exclude_dir != None):
        dirs = config.exclude_dir
        opt = dirs.join(' ')

        argsstr += f'--exclude-dir={opt}'

    if(config.exclude_ext != None):
        dirs = config.exclude_ext
        opt = dirs.join(' ')

        argsstr += f'--exclude-ext={opt}'

    if(config.no_match_dir != None):
        argsstr += f'--not-match-d={config.no_match_dir}'                

    if(config.no_match_f != None):
        argsstr += f'--no-match-f={config.no_match_f}'


    if(config.include_dir != None):
        dirs = config.include_dir
        regex_opt = dirs.join('|')

        argsstr += f'--match-d=/({regex_opt})/'

    if(config.include_ext != None):
        dirs = config.include_ext
        opt = dirs.join(' ')
        
        argsstr += f'--include-ext={opt}'

    if(config.match_dir != None):
        argsstr += f'--match-d={config.match_dir}'

    if(config.match_f != None):
        argsstr += f'--match-f={config.match_f}'


    cmd = 'cloc ./ {argstr} --json'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # get output and error messages
    stdout, stderr = process.communicate()
    
    count_result = json.loads(stdout.decode())

    # print results
    print(stdout.decode())
    # print(stderr.decode())