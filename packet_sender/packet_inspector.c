#include <stdio.h>
#include <pcap.h>
#include <time.h>
#include <linux/ip.h>
#include <linux/if_ether.h>
#include <linux/tcp.h>

char *pcap_lookupdev(char *errbuf);
//pcap_t *pcap_open_live(char *device, int snaplen, int promisc, int to_ms, char *errbuf);

// int prase_packet(const u_char *packet, int caplen){
//     u_int16_t e_type;
//     u_int32_t offset;
//     int payload_len;
//     const u_char *tcp_payload;

//     //ethernet header
//     struct ethhdr *eth = NULL;
//     eth = (struct ethhdr *)packet;
//     e_type = ntohs(eth->h_proto);
//     offset = sizeof(struct ethhdr);
//     show_ethhdr(eth);

//     //vlan 802.1q
//     while (e_type == ETH_P_8021Q){
//         e_type = (packet[offset + 2] << 8) + packet[offset + 3];
//         offset += 4;
//     }
//     if(e_type != ETH_P_IP){
//         return -1;
//     }
    
// }


void get_packet(u_char *user, const struct pcap_pkthdr *pkthdr, const u_char *packet){
    static int count = 0;
    printf("\n-------------------------\n");
    printf("\t\tpacket %d\n", count);
    printf("\n-------------------------\n");
    printf("Packet id: %d\n", count);
    printf("Packet length: %d\n", pkthdr->len);
    printf("Number of bytes : %d\n", pkthdr->caplen);
    printf("Received time : %s\n", ctime((const time_t *) &pkthdr->ts.tv_sec));
    pcap_dump(user, pkthdr, packet);
    count++;
}


int main(int argc, char const *argv[])
{
    char errbuf[PCAP_ERRBUF_SIZE];
    // 获取可用网口
    char *dev;
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL){
        fprintf(stderr, "Can not find default device: %s\n", errbuf);
        return(2);
    }
    printf("Device: %s\n", dev);

    //打开进行监听的网口
    pcap_t *handle;
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL){
        fprintf(stderr, "Can not open device %s: %s\n", dev, errbuf);
        return(2);
    }
    printf("Device: %s has been opened\n", dev);

    //设置过滤条件

    //1. 获取当前网口掩码
    bpf_u_int32 mask;
    bpf_u_int32 net;
    if(pcap_lookupnet(dev, &net, &mask, errbuf) == -1){
        fprintf(stderr, "Get net and mask failed: %s\n",errbuf);
        return(2);
    }
    //2. 编译过滤条件
    char filter[] = "port 22";
    struct bpf_program fp;
    if(pcap_compile(handle, &fp, filter, 0, net) == -1){
        fprintf(stderr, "Can not parse filter %s: %s\n", filter, pcap_geterr(handle));
        return(2);
    }
    //3. 设置过滤条件
    if(pcap_setfilter(handle, &fp) == -1){
        fprintf(stderr, "Can not set filter %s: %s\n", filter, pcap_geterr(handle));
        return(2);
    }

    //抓包
    //1. pcap_next，一次一个包
    // const u_char *packet;
    // struct pcap_pkthdr header;
    // packet = pcap_next(handle, &header);
    // printf("jacked a packet with length of [%d]\n", header.len);
    
    //2. pcap_loop, 使用回调函数重复抓包
    
    const u_char *packet;
    struct pcap_pkthdr header;
    u_char *user;
    // pcap_loop(handle, -1, get_packet, user);

    //存储流量
    pcap_dumper_t *dumpfile;
    dumpfile = pcap_dump_open(handle, "./save.pcap");
    if (dumpfile == NULL){
        fprintf(stderr, "Can not open output file");
        return(2);
    }
    pcap_loop(handle, 100, get_packet, (u_char *) dumpfile);
    
    
    pcap_close(handle);
    return 0;
}
