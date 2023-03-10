import argparse
import cache_checker
import cloc_proxy

def main(args):
    print(args.include_ext)
    # print(args.include_dir)
    # Initialize the database connection
    # cache_checker.init("test.db")

    # Call the functions from the cache_checker module
    # cache_checker.caches_by_dir_n_commit(args.dir, args.commit)
    # cache_checker.checks_if_cache_exits(args.dir, args.commit)

    # cache_checker.close()
    # cloc_proxy.count_loc()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My script description')
    
    parser.add_argument(
        '--exclude-ext', 
        nargs='+', 
        metavar='<ext1> [,<ext2>[...]]', 
        help='Do not count files having the given file name extensions.')
    
    parser.add_argument(
        '--exclude-dir', 
        nargs='+', 
        metavar='<D1>[,D2[...]]', 
        help='Exclude the given comma separated directories  D1, D2, D3, et cetera, from being scanned. For example --exclude-dir=.cache,test  will skip  all files and subdirectories that have /.cache/ or /test/ as their parent directory. Directories named .bzr, .cvs, .hg, .git, .svn, and .snapshot are always excluded. This option only works with individual directory names so including file path separators is not  allowed. Use --fullpath and --not-match-d=<regex> to supply a regex matching multiple subdirectories.')

    parser.add_argument(
        '--no-match-d', 
        nargs='+', 
        metavar='<regex>', 
        help='Count all files except those in directories matching the Perl regex. Only the trailing  directory name is compared, for example, when counting in /usr/local/lib, only \'lib\' is compared to the regex. Add --fullpath to compare parent directories to the regex. Do not include file path separators at the beginning or end of the regex.')
    
    parser.add_argument(
        '--no-match-f', 
        nargs='+', 
        metavar='<regex>', 
        help='Count all files except those whose basenames match the Perl regex.  Add --fullpath to include parent directories in the regex instead of just the basename.')

    parser.add_argument(
        '--include-ext', 
        nargs='+', 
        metavar='<ext1> [,<ext2>[...]]', 
        help='Count only languages having the given comma separated file extensions. Use --show-ext to see the recognized extensions.')
    
    parser.add_argument(
        '--include-dir', 
        nargs='+', 
        metavar='<D1>[,D2,]', 
        help='Include the given comma separated directories D1, D2, D3, et cetera')
    
    parser.add_argument(
        '--match-d', 
        nargs='+', 
        metavar='<regex>', 
        help='Only count files in directories matching the Perl regex.  For example  --match-d=\'/(src|include)/\'  only counts files in directories containing  /src/ or /include/.  Unlike --not-match-d,  --match-f, and --not-match-f, --match-d always compares the fully qualified path against the regex.')
    
    parser.add_argument(
        '--match-f', 
        nargs='+', 
        metavar='<regex>', 
        help='Count all files except those whose basenames match the Perl regex.  Add --fullpath to include parent directories in the regex instead of just  the basename.')


    args = parser.parse_args()
    main(args)
