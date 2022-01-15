#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

int main(int argc, char* argv[]) {
    int so;
    char s[100];
    struct sockaddr_in ad;

    socklen_t ad_length = sizeof(ad);
    struct hostent *hep;

    // create socket
    int serv = socket(AF_INET, SOCK_STREAM, 0);

    // init address
    hep = gethostbyname(argv[1]);
    memset(&ad, 0, sizeof(ad));
    ad.sin_family = AF_INET;
    ad.sin_addr = *(struct in_addr*)hep->h_addr_list[0];
    ad.sin_port = htons(12345);

    // connect to server
    connect(serv, (struct sockaddr*)&ad, ad_length);
    
    memset(&s, 0, 100);
    FILE* file;
    file = fopen("send_file.txt", "r");
    if (file == NULL) {
    	printf("The file is null");
    } else {
    	printf("Read file successfully");
    }
    
    char buffer[1024] = {0};
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
    	int i = send(serv, buffer, sizeof(buffer), 0);
    	if (i == -1) {
    		printf("Send data fail");
    	}
    	memset(&buffer, 0, sizeof(buffer));
    }
    
    close(serv);
    return 0;
}

