import plistlib
import pprint

import click
import pcapy

BPLIST_MAGIC = b'bplist'


@click.command()
@click.argument('pcap', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('out', type=click.File('wt'))
def main(pcap, out):
    pcap = pcapy.open_offline(pcap)
    while True:
        packet = pcap.next()[1]
        if BPLIST_MAGIC in packet:
            try:
                plist = plistlib.loads(packet[packet.find(BPLIST_MAGIC):])
                out.write('---\n')
                out.write(pprint.pformat(plist))
                out.write('\n---\n')
            except plistlib.InvalidFileException:
                pass


if __name__ == '__main__':
    main()
