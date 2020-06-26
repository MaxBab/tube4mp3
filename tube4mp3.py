#!/bin/env python

import argparse
import youtube_dl


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download YouTube video and convert into mp3')
    parser.add_argument('--url', help='Specify the YouTube video url')
    parser.add_argument('--start-time',
                        help='Start time of the clip in hh:mm:ss form')
    parser.add_argument('--end-time',
                        help='End time of the clip in hh:mm:ss form')
    parser.add_argument('--clip-list',
                        help='External file with list of dicts of the clips '
                        'and relevant arguments. '
                        'Ex: url=<url>, start_time=0:1:22, end_time=0:3:40')
    parser.add_argument('--verbose', action='store_true',
                        help='Print download messages to stdout')
    return parser.parse_args()

def ydl_opts(opts, verbose=False):
    """Build download options for youtube_dl"""
    ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
    if not verbose:
        ydl_opts.update({'quiet': 'true'})
    postprocessor_args = []
    if opts.get('start_time'):
        postprocessor_args.extend(['-ss', opts.get('start_time')])
    if opts.get('end_time'):
        postprocessor_args.extend(['-t', opts.get('end_time')])
    if postprocessor_args:
        ydl_opts.update({'postprocessor_args': postprocessor_args})
    return ydl_opts

def parse_manual_input(args):
    manual_input = 'url={}'.format(args.url)
    if args.start_time:
        manual_input += ', start_time={}'.format(args.start_time)
    if args.end_time:
        manual_input += ', end_time={}'.format(args.end_time)
    return [manual_input]

def read_ext_file(file):
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    return lines

def prepare_download_opts(clips):
    clip_list = []
    for clip in clips:
        clip_params = clip.split(', ')
        param_dict = {}
        for clip_param in clip_params:
            param = clip_param.split('=', 1)
            param_dict.update({param[0]: param[1]})
        clip_list.append(param_dict)
    return clip_list

def progress(count, total, status=''):
    # https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
        
    
def main():
    args = parse_args()
    if args.url:
        arguments = parse_manual_input(args)
    elif args.clip_list:
        arguments = read_ext_file(args.clip_list)
    clip_args = prepare_download_opts(arguments)
    clip_args_list = []
    for opt in clip_args:
        clip_args_list.append(ydl_opts(opt, verbose=args.verbose))
    download_failures = []
    for index, (url, clip_opts) in enumerate(zip(clip_args, clip_args_list)):
        if not args.verbose:
            progress(index, len(clip_args), status='In progress - {}'
                     .format(url.get('url')))
        try:
            ydl = youtube_dl.YoutubeDL(clip_opts)
            ydl.download([url.get('url')])
        except youtube_dl.DownloadError:
            download_failures.append(url.get('url'))
        except OSError:
            download_failures.append(url.get('url'))
    if download_failures:
        print('Some of the clips faced download issues.\n'
              'The clips are: {}'.format(download_failures))

if __name__ == '__main__':
    main()
