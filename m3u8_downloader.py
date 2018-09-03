"""M3U8 Downloader

Download the ts files according to the given m3u8 file.
"""
import argparse
import os

import ffmpy
import m3u8


class M3U8Downloader:
    """M3U8 Downloader Class"""

    def __init__(self, uri, timeout=None, headers=None,
                 ffmpeg_path=r'C:\Program Files (x86)\ffmpeg-4.0.2\bin\ffmpeg.exe', ffmpeg_loglevel='quiet'):
        """Initialize a M3U8 Downloader.

        Args:
            uri (:obj:`str`): The URI of the m3u8 file.
            timeout (:obj:`int`, optional): The timeout used when loading
                from uri. Defaults to ``None``.
            headers (:obj:`list` of :obj:`str`, optional): The headers used
                when loading from uri. Defaults to ``None``.
            ffmpeg_path (:obj:`str`, optional): The path to ffmpeg executable.
                Defaults to ``ffmpeg``.
            ffmpeg_loglevel (:obj:`str`, optional): The logging level of
                ffmpeg. Defaults to ``quiet``.
        """
        if not headers:
            headers = {}

        self.uri = uri
        self.ffmpeg_path = ffmpeg_path
        self.ffmpeg_loglevel = ffmpeg_loglevel
        self.m3u8 = m3u8.load(uri=uri, timeout=timeout, headers=headers)

    def download(self, output='output.ts'):
        """Start downloading and merging with the given m3u8 file.

        Args:
            output (:obj:`str`): The path to output. Defaults to ``output.ts``
        """
        if self.m3u8.is_variant:

            print('There are multiple m3u8 files listed in this file.')
            print('Select one to download.')
            print()

            for index, playlist in enumerate(self.m3u8.playlists):
                self._print_stream_info(playlist, index)

            try:
                fetch_index = int(input('Index> '))

                downloader = M3U8Downloader(
                    self.m3u8.playlists[fetch_index].absolute_uri,
                    ffmpeg_path=self.ffmpeg_path,
                    ffmpeg_loglevel=self.ffmpeg_loglevel,
                )
                downloader.download(output)
            except (ValueError, IndexError):
                print('Invalid index.')

        else:
            dirname = os.path.dirname(output)
            if dirname:
                os.makedirs(os.path.dirname(output), exist_ok=True)

            ffmpeg_cmd = ffmpy.FFmpeg(
                self.ffmpeg_path,
                '-y',
                # '-y -loglevel {}'.format(self.ffmpeg_loglevel),
                inputs={self.uri: None},
                outputs={output: '-c copy'},
            )
            print('Start downloading and merging with ffmpeg...')
            print(ffmpeg_cmd.cmd)

            ffmpeg_cmd.run()

    @staticmethod
    def _print_stream_info(playlist, index=0):
        print('INDEX: ' + str(index))

        stream_info = playlist.stream_info
        if stream_info.bandwidth:
            print('Bandwidth: {}'.format(stream_info.bandwidth))
        if stream_info.average_bandwidth:
            print('Average bandwidth: {}'.format(stream_info.average_bandwidth))
        if stream_info.program_id:
            print('Program ID: {}'.format(stream_info.program_id))
        if stream_info.resolution:
            print('Resolution: {}'.format(stream_info.resolution))
        if stream_info.codecs:
            print('Codecs: {}'.format(stream_info.codecs))
        print()


def main():
    """Parse the arguments to start the download.

    Parse the arguments to construct the M3U8Downloader object, then start
    downloading with the given m3u8 file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='URI of the m3u8 file')
    parser.add_argument('-t', '--timeout', type=int, default=None,
                        help='timeout used when loading from uri (default %(default)s)')
    parser.add_argument('--ffmpeg-path', default='ffmpeg',
                        help='path to ffmpeg executable (default %(default)s)')
    parser.add_argument('--ffmpeg-loglevel', default='quiet',
                        help='logging level of ffmpeg (default %(default)s)')
    parser.add_argument('-o', '--output', default='output.ts',
                        help='path to output (default %(default)s)')
    parser.add_argument('-y', '--overwrite', action='store_true',
                        help='overwrite output files without asking')
    args = parser.parse_args()

    if not args.overwrite and os.path.isfile(args.output):
        print('ERROR: File "{}" already exists.'.format(args.output))
        return

    downloader = M3U8Downloader(
        uri=args.uri,
        timeout=args.timeout,
        ffmpeg_path=args.ffmpeg_path,
        ffmpeg_loglevel=args.ffmpeg_loglevel,
    )
    downloader.download(output=args.output)

if __name__ == '__main__':
    main()
