import os
import argparse
import socket
import random
import time
from urllib.parse import urlparse
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send
from scapy.all import sniff, wrpcap, rdpcap


def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except:
        return None


def parse_url(url_arg):
    if not url_arg.startswith('http://') and not url_arg.startswith('https://'):
        url_arg = 'http://' + url_arg

    parsed = urlparse(url_arg)
    hostname = parsed.hostname
    path = parsed.path if parsed.path else '/'
    scheme = parsed.scheme or 'http'
    return hostname, path, scheme


def send_http_request(hostname, path, custom_request=None):
    dest_ip = resolve_hostname(hostname)
    if not dest_ip:
        return None

    port = 80
    client_sport = random.randint(1025, 65500)

    if custom_request:
        http_request_str = custom_request
    else:
        http_request_str = f'GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n'

    syn = IP(dst=dest_ip) / TCP(sport=client_sport, dport=port, flags='S')
    syn_ack = sr1(syn, timeout=5, verbose=False)

    if not syn_ack or not syn_ack.haslayer(TCP):
        return None

    client_seq = syn_ack[TCP].ack
    client_ack = syn_ack[TCP].seq + 1

    ack = IP(dst=dest_ip) / TCP(
        sport=client_sport,
        dport=port,
        seq=client_seq,
        ack=client_ack,
        flags='A'
    )
    send(ack, verbose=False)

    time.sleep(0.1)

    req = IP(dst=dest_ip) / TCP(
        sport=client_sport,
        dport=port,
        seq=client_seq,
        ack=client_ack,
        flags='PA'
    ) / http_request_str

    send(req, verbose=False)

    return dest_ip, port, client_sport


# === ИСПРАВЛЕННАЯ ЧАСТЬ ===
def capture_traffic(hostname, timeout=30, output_file=None):
    packets = sniff(
        iface="\\Device\\NPF_Loopback",
        filter="tcp",
        timeout=timeout
    )

    if not output_file:
        output_file = "gruyere.pcap"

    wrpcap(output_file, packets)
    print(f"[+] Захвачено пакетов: {len(packets)}")
    print(f"[+] Трафик сохранён в {output_file}")

    return packets


# =========================


def analyze_packets(packets):
    if not packets:
        return

    http_data = []
    for pkt in packets:
        if pkt.haslayer('Raw'):
            data = pkt['Raw'].load.decode('utf-8', errors='ignore')
            if 'HTTP' in data or 'GET' in data or 'POST' in data:
                http_data.append(data)

    print(f"Найдено HTTP-сообщений: {len(http_data)}")

    for i, data in enumerate(http_data[:3], 1):
        print(f"\nHTTP-сообщение {i}:\n")
        print(data[:300])


def analyze_saved_traffic(pcap_file):
    packets = rdpcap(pcap_file)
    analyze_packets(packets)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send')
    parser.add_argument('--capture')
    parser.add_argument('--analyze')
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--output')
    parser.add_argument('--request')

    args = parser.parse_args()

    if args.send:
        hostname, path, _ = parse_url(args.send)
        send_http_request(hostname, path, args.request)

    if args.capture:
        packets = capture_traffic(args.capture, args.timeout, args.output)
        analyze_packets(packets)

    if args.analyze:
        analyze_saved_traffic(args.analyze)


if __name__ == '__main__':
    main()
